---
name: review-file
description: >-
  Runs Bugbot, Security Review, unfinished-work, and standards-review as four
  parallel subagents on a file as it currently exists, and writes one combined
  report to review_<uuid>.md. Use when the user asks for /review-file or a full
  review of a file rather than a git diff or branch.
disable-model-invocation: true
---

# Review file

Same four reviews as /review-all, applied to a file's current contents. Before launching, run `uuidgen` once and keep that value for this run. The report file is `review_<uuid>.md`. Do not invent the UUID, and do not reuse `review.md`. Do not compute a git diff. Do not require a branch. Do not check a branch out. Do not read the file before launching. Do not read the reviewers' skill files. Do not edit the repo except to write the combined report to `review_<uuid>.md`.

## Scope

The files are the paths the user named or attached. If they named none, use the file open in the editor. If they named a directory, or no file can be resolved, stop and ask which file to review.

The repository path is the git root that contains those files. If a file is not inside a git repo, use that file's directory as the repository path.

## Launch

In a single message, call the Task tool four times. Set `run_in_background` to false unless the user asked for a background run, or Multitask Mode requires background runs. If they run in the background, wait until all four finish, then write the report.

Pass the same file list to every subagent. Use absolute paths.

1. `subagent_type`: `bugbot`. `description`: `Bugbot`. Use `Diff: natural language` on the first launch. Do not try `branch changes` first. Prompt:

```text
Full Repository Path: <absolute repository path>
Diff: natural language
Change Description:
<repo-relative path> (modified):
- Review this file as it currently exists on disk. Read the whole file. There is no branch and no diff.
Custom Instructions: Review the current contents of the named files. Do not look for a git diff or a branch.
```

Repeat the Change Description block once per file.

2. `subagent_type`: `security-review-file`. `description`: `Security Review`. Do not use `security-review`; that subagent stops when the git diff is empty. If `security-review-file` is unavailable, use `generalPurpose` with the same prompt:

```text
Read and follow /home/russ/.cursor/skills/review-security-file/criteria.md.
Full Repository Path: <absolute repository path>
Files: <absolute paths>
Return only the report that file specifies. Do not edit the repo.
```

3. `subagent_type`: `unfinished-work`. `description`: `Unfinished work`. If that type is unavailable, use `generalPurpose` with the same prompt:

```text
Read and follow /home/russ/.cursor/skills/unfinished-work/SKILL.md.
Full Repository Path: <absolute repository path>
Mode: current file
Files: <absolute paths>
Return only the report that skill specifies. Do not edit the repo.
```

4. `subagent_type`: `standards-review`. `description`: `Standards review`. Same fallback. Prompt:

```text
Read and follow /home/russ/.cursor/skills/standards-review/SKILL.md.
Full Repository Path: <absolute repository path>
Mode: current file
Files: <absolute paths>
Return only the report that skill specifies. Do not edit the repo.
```

If Bugbot or Security Review fails, retry that one once with the same prompt. Then stop retrying.

## Report

Write one report to `review_<uuid>.md` in the repository root (or the file's directory when there is no git root), using the UUID from the start of this run. Do not print the report to regular output. Use these four headings, and put each subagent's report under its heading unchanged:

- Bugbot
- Security Review
- Unfinished work
- Standards review

If one fails, put the short error under that heading and still include the others. Do not merge findings across reviews. Do not fix findings unless the user asks. After writing the file, tell the user the report path, including the UUID.
