---
name: unfinished-work
description: >-
  Finds a change that was made in one part of the code that should also be
  made somewhere else. Use when the user asks for an unfinished-work review,
  a consistency pass, missed updates, or /unfinished-work.
disable-model-invocation: true
icon: git-branch
color: yellow
---

# Unfinished work

Find a change that was made in one part of the code that should also be made somewhere else. Report those gaps. Do not edit the repo unless the user asks.

## Scope

If the prompt includes `Mode: current file`, read the listed files from disk and do not use git. Treat each file's current behavior as the source of truth. Search the repo for other sites that encode the same fact and still disagree with this file. A gap counts only when another site should match this file and does not. Skip the numbered list below and skip reading a diff. Use the file contents wherever this skill says to read the diff.

Otherwise:

1. If the user names files, a PR, or a commit, review that.
2. If they ask for uncommitted, local, or dirty changes, review `git diff` plus staged changes.
3. Otherwise review branch changes against the merge-base with the default base branch, including committed, staged, and unstaged changes.

## How to look

Read the diff and name each distinct change: a field added or removed, a symbol renamed, a condition changed, a new branch, a new argument, a new error, a new config key, or any other behavior change.

For each change, find the other places that encode the same fact. Search the repo. Read sibling functions, other implementations of the same interface, callers, and registries. A gap counts only when another site still has the old behavior and the change in the diff should have been applied there too.

Check:

- The same type, DTO, schema, query, or client updated in one layer and not the next
- A new case handled in one switch, map, or registry and missing from the others
- Duplicated logic updated in one copy only
- Call sites still using the old signature, old value, or old assumption
- Tests, fixtures, and migrations that still describe the old behavior
- UI that states or assumes something that is no longer true

Skip new feature ideas, style nits, and coding-standards violations. Skip a site that correctly keeps the old behavior; if a near miss looks intentional, say why.

## Report

Lead with the scope you reviewed. Pair each finding with the site that changed and the site that did not. Then a table, highest severity first. If there are no gaps, say no unfinished work was found and omit the table.

| Severity | Change | Missing location | What still needs the same change |
| --- | --- | --- | --- |
| Must fix | Added `status` on `Order` (`order.ts:14`) | `api/order.proto:18` | Proto message still has no `status` field |

**Must fix** means the missed site will be wrong. **Suggestion** means it is a likely twin and the diff does not prove it must change. Location is `file:line`.
