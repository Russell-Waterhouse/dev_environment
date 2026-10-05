---
name: review-all
description: >-
  Runs Bugbot, Security Review, unfinished-work, and standards-review as four
  parallel subagents and writes one combined report to review_<uuid>.md. Use
  when the user asks for /review-all or a full parallel review.
disable-model-invocation: true
---

# Review all

Before launching, run `uuidgen` once and keep that value for this run. The report file is `review_<uuid>.md`. Do not invent the UUID, and do not reuse `review.md`.

Launch four subagents in one message. They run in parallel, each with a fresh context. Do not read their skill files. Do not compute a diff before launching. Do not edit the repo except to write the combined report to `review_<uuid>.md`.

## Scope

The repository path is the active workspace or repository root.

Pass the same diff mode to every subagent:

- Default: `branch changes` (committed, staged, and unstaged changes against the merge-base with the default base branch).
- User asked for uncommitted, local, dirty, or not-yet-committed changes: `uncommitted changes`.
- User named files, a commit, or a PR: say that in the unfinished-work and standards-review prompts. Bugbot and Security Review still receive `Diff: branch changes` or `uncommitted changes` unless a checkout is required below.

Include `Base Branch` on the Bugbot and Security Review prompts only when the review must compare against a specific branch other than the repository's default base branch.

If the user names a PR or branch to review, check that branch out before launching. If checkout is blocked by local changes, stop and ask before stashing. Launch only after that branch is checked out.

## Launch

In a single message, call the Task tool four times. Set `run_in_background` to false unless the user asked for a background run, or Multitask Mode requires background runs. If they run in the background, wait until all four finish, then write the report.

1. `subagent_type`: `bugbot`. `description`: `Bugbot`. Prompt:

```text
Full Repository Path: <absolute repository path>
Diff: <branch changes|uncommitted changes>
Base Branch: <only when needed>
Custom Instructions: <only when the user gave review instructions>
```

2. `subagent_type`: `security-review`. `description`: `Security Review`. Same prompt shape. `Diff` is only `branch changes` or `uncommitted changes`.

3. `subagent_type`: `unfinished-work`. `description`: `Unfinished work`. If that type is unavailable, use `generalPurpose` with the same prompt:

```text
Read and follow /home/russ/.cursor/skills/unfinished-work/SKILL.md.
Full Repository Path: <absolute repository path>
Diff: <branch changes|uncommitted changes>
Scope: <files, commit, or PR only when the user named one>
Return only the report that skill specifies. Do not edit the repo.
```

4. `subagent_type`: `standards-review`. `description`: `Standards review`. Same fallback. Prompt:

```text
Read and follow /home/russ/.cursor/skills/standards-review/SKILL.md.
Full Repository Path: <absolute repository path>
Diff: <branch changes|uncommitted changes>
Scope: <files, commit, or PR only when the user named one>
Return only the report that skill specifies. Do not edit the repo.
```

If Bugbot reports that it could not compute the diff, retry that one subagent once with `Diff: natural language`, no `Base Branch`, and a `Change Description` of one block per changed file (`<path> (added|modified|deleted|renamed)` plus bullets). If Bugbot or Security Review fails for another reason, retry that one once with the same prompt. Then stop retrying.

## Report

Write one report to `review_<uuid>.md` in the repository root, using the UUID from the start of this run. Do not print the report to regular output. Use these four headings, and put each subagent's report under its heading unchanged:

- Bugbot
- Security Review
- Unfinished work
- Standards review

If one fails, put the short error under that heading and still include the others. Do not merge findings across reviews. Do not fix findings unless the user asks. After writing the file, tell the user the report path, including the UUID.
