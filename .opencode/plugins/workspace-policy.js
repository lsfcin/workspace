// Workspace policy plugin for opencode.
// Mirrors /mnt/workspace/.claude/settings.json PreToolUse/PostToolUse hooks so
// opencode enforces the SAME workspace behavioral policies as Claude Code:
//   - context-gate.py     : force CONTEXT.md chain read before Read/Edit/Write
//   - bash-context-gate.py: same chain gate for Bash commands touching files
//   - pre-edit.py         : first-line comment, line-count limits, CONTEXT.md line-2
//   - facade-scan.py      : list facade exports before writing a new Code/ file
//   - facade-gate.py      : block Code/ module edits until the module facade is read
//   - known-bugs-gate.py  : KNOWN-BUGS.md FIXED flips require a regression spec
//   - spec-read-gate.py   : spec-locked module edits require its SPEC.md read first
//   - pre-read.sh         : block source reads when a current interface file exists
//   - post-edit.sh        : regenerate interfaces, terms check, context_synchronizer
//   - facade-tracker      : record facade reads for facade-gate session state
//   - context-tracker.py  : record CONTEXT.md/interface reads for context-gate + pre-read
//
// The existing .hooks/* scripts remain the single source of truth. This plugin
// only TRANSLATES opencode's tool.execute.before/after events into the
// stdin-JSON + CLAUDE_TOOL_NAME/CLAUDE_TOOL_INPUT env schema the scripts already
// expect, and maps Claude exit-2 to opencode throw. Design lifted from
// .hooks/copilot-pre-tool.py / copilot-post-tool.py (prior art for a non-Claude
// agent — copilot-pre-tool.py's `gate()` ordering is the reference this plugin
// mirrors: context-gate before pre-read/pre-edit, known-bugs-gate after
// facade-gate). Translation helpers live in ../wp-helpers.js (kept out of
// plugins/ so opencode does not auto-load them as a plugin).
//
// Full event->script mapping, stdin-vs-env schema, and the warning-surfacing
// limitation are documented in ../CONTEXT.md.

import { HOOKS, TOOL_MAP, buildPayloads, run, warn } from "../index.js"

function blockMsg(r, fallback) {
  return `${r.stdout || ""}${r.stderr || ""}`.trim() || fallback
}

export const WorkspacePolicy = async ({ client }) => {
  return {
    "tool.execute.before": async (input, output) => {
      // Bash — CONTEXT.md chain gate on any workspace file the command touches.
      // Not in TOOL_MAP (bash isn't file-path-based): handled separately.
      if (input.tool === "bash") {
        const command = (output.args && (output.args.command || output.args.cmd)) || ""
        if (!command) return
        const r = run(`${HOOKS}/bash-context-gate.py`, { command }, "Bash", { stdin: true })
        if (r.status === 2) throw new Error(blockMsg(r, "CONTEXT GATE (Bash)"))
        if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        return
      }

      const m = TOOL_MAP[input.tool]
      if (!m) return
      const payloads = buildPayloads(output.args || {}, input.tool)
      if (payloads.length === 0) return

      if (m.group === "read") {
        for (const p of payloads) {
          // 1. context-gate.py — force CONTEXT.md chain read before the file itself.
          const g = run(`${HOOKS}/context-gate.py`, p, "Read", { stdin: true })
          if (g.status === 2) throw new Error(blockMsg(g, "CONTEXT GATE"))
          if (g.stdout && g.stdout.trim()) await warn(client, g.stdout)
          // 2. pre-read.sh — interface-first source gate.
          const r = run(`${HOOKS}/pre-read.sh`, p, "Read", { stdin: true })
          if (r.status === 2) throw new Error(blockMsg(r, "READ INTERFACE FIRST"))
          if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        }
        return
      }

      // edit/write/apply_patch — Edit|Write matcher, pre-hooks in order.
      for (const p of payloads) {
        // 1. context-gate.py — force CONTEXT.md chain read before editing.
        const g = run(`${HOOKS}/context-gate.py`, p, m.canonical, { stdin: true })
        if (g.status === 2) throw new Error(blockMsg(g, "CONTEXT GATE"))
        if (g.stdout && g.stdout.trim()) await warn(client, g.stdout)
        // 2. pre-edit.py — size + first-line + CONTEXT.md line-2.
        //    Skipped for apply_patch: no content/old/new fields in patchText.
        if (input.tool !== "apply_patch") {
          const r = run(`${HOOKS}/pre-edit.py`, p, m.canonical, { stdin: true })
          if (r.status === 2) throw new Error(blockMsg(r, "pre-edit blocked"))
          if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        }
        // 3. facade-scan.py — Write only; inform about existing facade exports.
        //    Never blocks (exit 0 only); guarded anyway.
        if (m.canonical === "Write") {
          const r = run(`${HOOKS}/facade-scan.py`, p, "Write", { stdin: true })
          if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
          if (r.status === 2) throw new Error(blockMsg(r, "facade-scan blocked"))
        }
        // 4. facade-gate.py — block Code/ edits until facade read this session.
        const r = run(`${HOOKS}/facade-gate.py`, p, m.canonical, { stdin: true })
        if (r.status === 2) throw new Error(blockMsg(r, "READ FACADE FIRST"))
        if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        // 5. known-bugs-gate.py — KNOWN-BUGS.md FIXED flips need a regression spec.
        const k = run(`${HOOKS}/known-bugs-gate.py`, p, m.canonical, { stdin: true })
        if (k.status === 2) throw new Error(blockMsg(k, "KNOWN-BUGS GATE"))
        if (k.stdout && k.stdout.trim()) await warn(client, k.stdout)
        // 6. spec-read-gate.py — spec-locked module edits need its SPEC.md read first.
        const s = run(`${HOOKS}/spec-read-gate.py`, p, m.canonical, { stdin: true })
        if (s.status === 2) throw new Error(blockMsg(s, "SPEC GATE"))
        if (s.stdout && s.stdout.trim()) await warn(client, s.stdout)
      }
    },

    "tool.execute.after": async (input, output) => {
      const m = TOOL_MAP[input.tool]
      if (!m) return
      // `after` carries args on `input.args` (per @opencode-ai/plugin types).
      const payloads = buildPayloads(input.args || output.args || {}, input.tool)
      if (payloads.length === 0) return

      const msgs = []
      if (m.group === "read") {
        for (const p of payloads) {
          const r = run(`${HOOKS}/facade-tracker.py`, p, "Read", { stdin: false })
          if (r.stdout && r.stdout.trim()) msgs.push(r.stdout.trim())
          const c = run(`${HOOKS}/context-tracker.py`, p, "Read", { stdin: false })
          if (c.stdout && c.stdout.trim()) msgs.push(c.stdout.trim())
        }
      } else {
        for (const p of payloads) {
          const r = run(`${HOOKS}/post-edit.sh`, p, m.canonical, { stdin: false })
          if (r.stdout && r.stdout.trim()) msgs.push(r.stdout.trim())
          if (r.stderr && r.stderr.trim()) msgs.push(r.stderr.trim())
        }
      }

      const text = msgs.join("\n\n").trim()
      if (!text) return
      // Append post-hook output (✓ .pyi regenerated, 💬 FIRST-LINE MISSING, …)
      // to the tool result so the LLM sees it — output.output is opencode's
      // only inline channel for after-hooks.
      if (typeof output.output === "string") {
        output.output = `${output.output}\n\n--- workspace-policy ---\n${text}`
      } else {
        output.output = `\n--- workspace-policy ---\n${text}`
      }
      try {
        await client.app.log({ body: { service: "workspace-policy", level: "info", message: text } })
      } catch {}
    },
  }
}
