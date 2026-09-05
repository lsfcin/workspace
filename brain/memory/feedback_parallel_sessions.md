---
name: feedback-parallel-sessions
description: How to work safely when multiple Claude/opencode sessions edit /mnt/workspace at once
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b984cbbb-d1a1-4ff4-a01a-76dd62abd2f0
  modified: 2026-08-14T14:26:13.375Z
---

Lucas runs several sessions on `/mnt/workspace` in parallel. The tree is a shared mutable surface, so sessions collide —
this is a recurring source of confusion and breakage.

**Why:** one session's uncommitted edits are invisible to another; shared files (`core/hooks/pre-commit`, `.gitignore`,
`CONTEXT.md`, `core/flows/craft/craft.md`, `.claude/agents/craft-*`) get co-edited. Real incident 2026-07-18: a `git mv`
of a skill left a dangling mirror symlink another session's opencode choked on at startup (broke websearch).

**How to apply:**
- **Partition by subtree.** One session owns `core/`, another `code/`, another `brain/`. Never two sessions in `.hooks/`
  or `.gitignore` at once.
- **Before refactoring a file, check `git status`** — if it's already `M` (dirty from another session), it's contended;
  don't rewrite it, coordinate or defer.
- **Stage explicitly, never `git add -A`.** List your own files so you don't sweep a parallel session's work into your
  commit.
- **A parallel writer can be a bot, not a session, and it writes while you work.** Incident
  2026-08-17: `git add -A` before a rename commit staged a fresh `brain/INBOX.md` capture the
  aiwbot Telegram frontend had appended minutes earlier. Caught by reading the staged diff, not by
  `git status` at session start — the file was clean when the session began. **`brain/INBOX.md` is
  append-at-any-moment; treat it as never yours to stage unless the INBOX is the work.**
- **Staging explicitly is not enough — `git commit` commits the whole index, not what you just
  added.** Incident 2026-08-13: `git add ROADMAP.md ISSUES.md` followed by `git commit` swept in
  nine files (`brain/GOALS.md`, `brain/TODO.md`, `branches/ecovila/*`, `core/*`) that were already
  staged in the index when the session *started*. Nothing was lost, but another session's WIP
  landed under an unrelated commit message, and the fix (soft-reset + recommit) needs a force-push
  to a branch the other machine may hold — so it could not be cleanly undone. **Check `git status`
  for a pre-dirty index at session start, and prefer `git commit -- <paths>` when it is not clean.**
- **A REFUSED commit leaves its index staged, and the next commit absorbs it.** Incident
  2026-09-05: a commit was blocked by the pre-commit gate (a parallel session's untracked goal file
  broke a root check). The fix was a separate one-file commit — but everything staged for the
  refused attempt was still in the index, so that "chore(brain): track hair.md" commit silently
  carried a generator change and a new test. Nothing was lost and nothing was another session's, but
  the message names a third of its own content, and the checkout was shared so amending it would
  have meant a force-push under someone else's HEAD. **After any refused commit, `git status`
  before the next one** — or `git commit -- <paths>`, which is the same defence as the bullet above.
- **HEAD is shared state too — check the branch immediately before committing, not at session
  start.** Incident 2026-08-14: the session began on `feature/wos-typeset`, a parallel session
  switched the shared checkout to `feature/brain-attention` mid-flight, and the commit landed on
  *their* branch and was auto-pushed there by `core/hooks/post-commit`. It was caught only because
  that hook prints the branch it pushed. Recovery is non-destructive and worth remembering:
  `git merge-base --is-ancestor <your-branch> <sha>` to confirm a fast-forward, then
  `git branch -f <your-branch> <sha>` and push **your** branch — never reset or force-push theirs,
  and never `git checkout` your branch back, which just yanks HEAD out from under them.
- **Commit often** to checkpoint — each session should start from a known point.
- **A Write rejected with "file has been modified since read" is a collision signal, not a harness
  quirk.** Incident 2026-07-29: it fired on `brain/TODO.md` while a parallel `/roundup` was draining
  the INBOX. Re-reading only the first lines satisfied the tool but the subsequent full-file Write
  reverted 5 of that session's lines. On that error: re-read the *whole* file, or `git diff` /
  `git show` the concurrent commit, then merge — never re-Write from the pre-error snapshot.
  Corollary: the other session may also have *committed* mid-session, so `git log --oneline -5`
  is worth a look before assuming your base is what you branched from.
- Ties into [[feedback-provider-agnostic-naming]] and the [[project-verify-roadmap]] enforcement work.
