---
name: feedback-background-bash-reliability
description: "Backgrounded Bash tool calls (run_in_background) can die silently across a ScheduleWakeup boundary, with no completion notification and no error in the redirected log."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 74826d96-6100-4c92-bff4-41d661d99a77
  modified: 2026-07-21T05:19:31.306Z
---

Don't trust a long multi-step `&&`-chained background Bash command to survive a `ScheduleWakeup` pause, especially when the user later interrupts before the wakeup prompt fires. Observed in [[project_spacemantics]]:
two lanes were launched with `run_in_background: true`, each `> logfile 2>&1`, doing `cmdA && cmdB`. One lane died between `cmdA` finishing and `cmdB` starting — no error written to the log despite `2>&1`, no task-notification ever arrived, and `ps` showed nothing alive. The other lane died before producing any output at all (0-byte log after 15+ minutes). Re-running the *same* commands directly in the foreground completed cleanly with no errors — the work itself was fine; only the background/wakeup combination lost it.

**Why:** unconfirmed, but the process's lifetime appears tied to something that doesn't survive a `ScheduleWakeup`-driven pause-and-resume cycle, at least when the user also sends a message in between.

**How to apply:** for a multi-step background sweep the user is waiting on (not a fire-and-forget task), prefer either (a) running it in the foreground if it fits a single tool-call timeout, or (b) running each step as its own independent background call (not chained with `&&`) so one dying doesn't silently take the rest with it, and check on it actively rather than trusting a long `ScheduleWakeup` + notification to be the only signal. If a background lane's log goes quiet, check `ps` for the actual process before assuming it's still working — a quiet log can mean "dead," not "slow."

**Second finding (2026-07-21, [[project_aiwbot]] Phase B live smoke):** a `Bash` call with `run_in_background: true` appears to run in a network-isolated sandbox — starting the aiwbot Telegram poller (`python -m frontend.bot`) that way failed every outbound HTTPS call to `api.telegram.org` with `httpcore.ConnectTimeout`, while the identical command run as a foreground call (or detached with a trailing `&`/`disown` from a foreground call) connected fine. The tool reported the background task as "failed" and `TaskStop` on its id immediately returned "No task found" — but a `telegram.error.Conflict:
terminated by other getUpdates request` kept recurring against every subsequent foreground-launched instance for 20+ seconds after, meaning the "failed" background process was still alive and still holding a long-poll somewhere invisible to this shell's `pgrep`/`ps` — not actually killed, just unreachable/unaccounted for. Only the target service's own token could be revoked to force it off.
**How to apply:** never launch a long-running network service (a poller, a daemon) via `run_in_background: true` — start it detached from a foreground call instead (`nohup cmd > log 2>&1 & disown`). If a background attempt at one already failed, assume its process may still be alive and uncontactable rather than gone; don't just retry in the foreground and expect a clean slate — check for symptoms of the orphan (e.g. a `Conflict` from Telegram, a port already bound) before concluding the retry itself is broken.
