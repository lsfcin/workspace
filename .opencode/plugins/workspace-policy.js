// Workspace policy plugin for opencode.
// Mirrors the workspace's .claude/settings.json PreToolUse/PostToolUse hooks so
// opencode enforces the SAME workspace behavioral policies as Claude Code:
//   - context-gate.py     : force CONTEXT.md chain read before Read/Edit/Write/Grep
//   - bash-context-gate.py: same chain gate for Bash commands touching files
//   - heredoc-gate.py     : warn-only — a cat >/tee heredoc meets no Edit|Write gate
//   - pre-edit.py         : first-line comment, line-count limits, CONTEXT.md line-2
//   - facade-scan.py      : list facade exports before writing a new Code/ file
//   - facade-gate.py      : block Code/ module edits until the module facade is read
//   - issues-gate.py      : ISSUES.md FIXED flips require a regression spec
//   - spec-read-gate.py   : spec-locked module edits require its SPEC.md read first
//   - pre-read.py         : block source reads when a current interface file exists
//   - post-edit.sh        : regenerate interfaces, terms check, context_synchronizer
//   - facade-tracker      : record facade reads for facade-gate session state
//   - context-tracker.py  : record CONTEXT.md/interface reads for context-gate + pre-read
//   - precompact-wipe.sh  : wipe seen-markers on experimental.session.compacting
//
// The existing core/hooks/* scripts remain the single source of truth. This plugin
// only TRANSLATES opencode's tool.execute.before/after events into the
// stdin-JSON + CLAUDE_TOOL_NAME/CLAUDE_TOOL_INPUT env schema the scripts already
// expect, and maps Claude exit-2 to opencode throw. Design lifted from
// core/hooks/copilot/copilot-pre-tool.py / copilot-post-tool.py (prior art for a non-Claude
// agent — copilot-pre-tool.py's `gate()` ordering is the reference this plugin
// mirrors: context-gate before pre-read/pre-edit, issues-gate after
// facade-gate). Translation helpers live in ../wp-helpers.js (kept out of
// plugins/ so opencode does not auto-load them as a plugin).
//
// Every payload carries a session-stable id (`opencode<host-pid>`, the Copilot
// pattern) and every spawn asks core/run for the interpreter — the platform seam —
// never the bare word python3. Full event->script mapping, stdin-vs-env schema,
// and the warning-surfacing limitation are documented in ../CONTEXT.md.

import { spawnSync } from "node:child_process"
import {
  HOOKS, TOOL_MAP, SESSION_ID, WORKSPACE,
  python, buildPayloads, buildGrepPayload, run, warn,
} from "../index.js"

function blockMsg(r, fallback) {
  return `${r.stdout || ""}${r.stderr || ""}`.trim() || fallback
}

export const WorkspacePolicy = async ({ client }) => {
  // The `opencode-plugin` switch (core/SPECS.md § AD-14). Asked through
  // feature_law.py's --enabled arm, which exists so a second harness reaches the same
  // registry without a second implementation of it. Off = register no hooks at all,
  // which is the honest observable: opencode runs with none of the canonical gates.
  // The interpreter comes from core/run --python (the platform seam): the bare word
  // `python3` is the spelling that silently disables the whole plugin on a Windows
  // clone — the Store alias prints an advert, exits 9009, and the probe reads as "off".
  const py = python()
  if (!py) return {}
  const on = spawnSync(py, [`${HOOKS}/feature_law.py`, "--enabled", "opencode-plugin"], {
    encoding: "utf8",
  })
  if (on.status !== 0) return {}
  return {
    "tool.execute.before": async (input, output) => {
      // Bash — CONTEXT.md chain gate on any workspace file the command touches,
      // plus the warn-only heredoc gate (cat > / tee writes meet no Edit|Write gate).
      // Not in TOOL_MAP (bash isn't file-path-based): handled separately.
      if (input.tool === "bash") {
        const command = (output.args && (output.args.command || output.args.cmd)) || ""
        if (!command) return
        const payload = { command, session_id: SESSION_ID }
        const r = run(`${HOOKS}/read/bash-context-gate.py`, payload, "Bash", { stdin: true })
        if (r.status === 2) throw new Error(blockMsg(r, "CONTEXT GATE (Bash)"))
        if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        const h = run(`${HOOKS}/checks/heredoc-gate.py`, payload, "Bash", { stdin: true })
        if (h.stdout && h.stdout.trim()) await warn(client, h.stdout)
        return
      }

      // Grep — context-gate only (Claude parity: the Grep matcher sits on the chain
      // gate, never on pre-read.py). Its target is a `path`, not a `file_path`.
      if (input.tool === "grep") {
        const p = buildGrepPayload(output.args || {})
        if (!p) return
        const g = run(`${HOOKS}/read/context-gate.py`, p, "Grep", { stdin: true })
        if (g.status === 2) throw new Error(blockMsg(g, "CONTEXT GATE"))
        if (g.stdout && g.stdout.trim()) await warn(client, g.stdout)
        return
      }

      const m = TOOL_MAP[input.tool]
      if (!m) return
      const payloads = buildPayloads(output.args || {}, input.tool)
      if (payloads.length === 0) return

      if (m.group === "read") {
        for (const p of payloads) {
          // 1. context-gate.py — force CONTEXT.md chain read before the file itself.
          const g = run(`${HOOKS}/read/context-gate.py`, p, "Read", { stdin: true })
          if (g.status === 2) throw new Error(blockMsg(g, "CONTEXT GATE"))
          if (g.stdout && g.stdout.trim()) await warn(client, g.stdout)
          // 2. pre-read.py — interface-first source gate.
          const r = run(`${HOOKS}/read/pre-read.py`, p, "Read", { stdin: true })
          if (r.status === 2) throw new Error(blockMsg(r, "READ INTERFACE FIRST"))
          if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        }
        return
      }

      // edit/write/apply_patch — Edit|Write matcher, pre-hooks in order.
      for (const p of payloads) {
        // 1. context-gate.py — force CONTEXT.md chain read before editing.
        const g = run(`${HOOKS}/read/context-gate.py`, p, m.canonical, { stdin: true })
        if (g.status === 2) throw new Error(blockMsg(g, "CONTEXT GATE"))
        if (g.stdout && g.stdout.trim()) await warn(client, g.stdout)
        // 2. pre-edit.py — size + first-line + CONTEXT.md line-2.
        //    Skipped for apply_patch: no content/old/new fields in patchText.
        if (input.tool !== "apply_patch") {
          const r = run(`${HOOKS}/checks/pre-edit.py`, p, m.canonical, { stdin: true })
          if (r.status === 2) throw new Error(blockMsg(r, "pre-edit blocked"))
          if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        }
        // 3. facade-scan.py — Write only; inform about existing facade exports.
        //    Never blocks (exit 0 only); guarded anyway.
        if (m.canonical === "Write") {
          const r = run(`${HOOKS}/facade/facade-scan.py`, p, "Write", { stdin: true })
          if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
          if (r.status === 2) throw new Error(blockMsg(r, "facade-scan blocked"))
        }
        // 4. facade-gate.py — block Code/ edits until facade read this session.
        const r = run(`${HOOKS}/facade/facade-gate.py`, p, m.canonical, { stdin: true })
        if (r.status === 2) throw new Error(blockMsg(r, "READ FACADE FIRST"))
        if (r.stdout && r.stdout.trim()) await warn(client, r.stdout)
        // 5. issues-gate.py — ISSUES.md FIXED flips need a regression spec.
        const k = run(`${HOOKS}/checks/issues-gate.py`, p, m.canonical, { stdin: true })
        if (k.status === 2) throw new Error(blockMsg(k, "ISSUES GATE"))
        if (k.stdout && k.stdout.trim()) await warn(client, k.stdout)
        // 6. spec-read-gate.py — spec-locked module edits need its SPEC.md read first.
        const s = run(`${HOOKS}/read/spec-read-gate.py`, p, m.canonical, { stdin: true })
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
          const r = run(`${HOOKS}/facade/facade-tracker.py`, p, "Read", { stdin: false })
          if (r.stdout && r.stdout.trim()) msgs.push(r.stdout.trim())
          const c = run(`${HOOKS}/read/context-tracker.py`, p, "Read", { stdin: false })
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

    // PreCompact equivalent — wipe this session's CONTEXT.md seen-markers so the
    // chain is re-read after compaction (injected context may be summarized away).
    // Same script Claude Code runs; it reads the session id from stdin JSON and
    // consults feature_law itself, so an off switch stays in one registry.
    "experimental.session.compacting": async () => {
      spawnSync("bash", [`${HOOKS}/session/precompact-wipe.sh`], {
        input: JSON.stringify({ session_id: SESSION_ID }),
        cwd: WORKSPACE, encoding: "utf8",
      })
    },
  }
}
