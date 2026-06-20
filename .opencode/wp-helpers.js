// Helpers for the workspace-policy opencode plugin.
// Lives OUTSIDE .opencode/plugins/ so opencode does not auto-load it as a
// plugin (opencode scans only .opencode/plugins/*). Imported by
// .opencode/plugins/workspace-policy.js.
//
// These are the translation layer between opencode's tool.execute.before
// /after events and the stdin-JSON + CLAUDE_TOOL_NAME/CLAUDE_TOOL_INPUT env
// schema that the existing .hooks/* scripts already expect (see
// .claude/settings.json and .hooks/copilot-pre-tool.py for the prior art).

import { spawnSync } from "node:child_process"
import { resolve } from "node:path"

export const WORKSPACE = "/mnt/workspace"
export const HOOKS = `${WORKSPACE}/.hooks`

// opencode tool names -> Claude canonical env value + matcher group.
//   read             -> Read  (pre-read.sh, facade-tracker)
//   edit, apply_patch-> Edit  (pre-edit + facade-scan + facade-gate, post-edit.sh)
//   write            -> Write (same scripts; pre-edit.py Write branch + facade-scan)
export const TOOL_MAP = {
  read:        { canonical: "Read",  group: "read" },
  edit:        { canonical: "Edit",  group: "edit" },
  write:       { canonical: "Write", group: "edit" },
  apply_patch: { canonical: "Edit",  group: "edit" }, // edit-permission; paths in patchText
}

// Reusable key lists — same as copilot-pre-tool.py (camelCase + snake_case).
const PATH_KEYS = ["filePath", "file_path", "path", "file", "filepath", "targetPath", "target_path"]
const CONTENT_KEYS = ["content", "text", "newCode", "new_code"]
const OLD_KEYS = ["oldString", "old_string", "oldText", "old_text"]
const NEW_KEYS = ["newString", "new_string", "newText", "new_text"]

// apply_patch markers embedded in patchText (per opencode docs).
const APPLY_PATCH_RE = /^\*\*\*\s+(?:Add File|Update File|Move to|Delete File):\s+(.+)$/gm

function firstString(obj, keys) {
  if (!obj || typeof obj !== "object") return ""
  for (const k of keys) if (typeof obj[k] === "string" && obj[k]) return obj[k]
  return ""
}

// Resolve a possibly-relative path against the workspace root.
function normalizePath(raw) {
  if (!raw || typeof raw !== "string" || !raw.trim()) return ""
  return resolve(WORKSPACE, raw)
}

// Build the Claude-shape payload(s) from opencode's args. For apply_patch
// there is no filePath; paths are embedded in patchText markers — extract them
// and return one payload per path (caller iterates).
export function buildPayloads(args, toolName) {
  if (toolName === "apply_patch") {
    const patchText = args.patchText || ""
    const paths = [...patchText.matchAll(APPLY_PATCH_RE)].map(m => normalizePath(m[1].trim()))
    return paths.filter(Boolean).map(p => ({
      file_path: p, content: "", old_string: "", new_string: "",
    }))
  }
  const fp = normalizePath(firstString(args, PATH_KEYS))
  if (!fp) return []
  return [{
    file_path: fp,
    content:    firstString(args, CONTENT_KEYS),
    old_string: firstString(args, OLD_KEYS),
    new_string: firstString(args, NEW_KEYS),
  }]
}

// python3 <script>  OR  bash <script>. Hooks read JSON from stdin (pre) or
// CLAUDE_TOOL_INPUT env (post) — never as a CLI arg — so argv is just the
// interpreter + script path.
function argvFor(script) {
  return script.endsWith(".sh") ? ["bash", script] : ["python3", script]
}

// Spawn a hook script with the Claude Code stdin-JSON + env schema.
// `stdin:true`  -> pre-hook: feed JSON on stdin.
// `stdin:false` -> post-hook: feed JSON via CLAUDE_TOOL_INPUT env var.
// Always sets CLAUDE_TOOL_NAME = canonical ("Edit"/"Write"/"Read").
export function run(script, payload, canonical, { stdin } = {}) {
  const env = { ...process.env, CLAUDE_TOOL_NAME: canonical }
  const json = JSON.stringify(payload)
  if (stdin) {
    return spawnSync(argvFor(script)[0], argvFor(script).slice(1), {
      input: json, env, cwd: WORKSPACE, encoding: "utf8",
    })
  }
  env.CLAUDE_TOOL_INPUT = json
  return spawnSync(argvFor(script)[0], argvFor(script).slice(1), {
    env, cwd: WORKSPACE, encoding: "utf8",
  })
}

// Non-blocking warning surfacing. opencode has no inline-tool-warning API on
// `tool.execute.before`, so pre-hook warnings go to two channels: a server log
// entry + a TUI toast. The LLM does NOT see these; only the user does. Blocking
// messages use throw (separate code path) which the LLM DOES see.
export async function warn(client, msg) {
  const text = (msg || "").trim()
  if (!text) return
  try {
    await client.app.log({ body: { service: "workspace-policy", level: "warn", message: text } })
  } catch {}
  try {
    await client.tui.showToast({ body: { message: text, variant: "warning", title: "workspace-policy" } })
  } catch {}
}
