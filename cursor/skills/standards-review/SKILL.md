---
name: standards-review
description: >-
  Reviews a diff against personal coding standards: assertions through
  logErrorAndSendMSTeamsMessage, mock-free unit tests for pure functions,
  integration tests only when a repo pattern already exists, logInfo and
  logError on every branch with no PII or PHI, bugs.md notes, checked return
  values, and complexity limits. Use when the user asks for a standards
  review or /standards-review.
disable-model-invocation: true
icon: bug
color: orange
---

# Standards review

Review the requested change against the standards below. Report findings. Do not edit the repo unless the user asks for fixes.

## Scope

If the prompt includes `Mode: current file`, read the listed files from disk and do not use git. Apply the checklist to the whole file. Skip the check that compares diff size to the size of the problem. Still flag unjustified complexity in the file. Unrelated bugs are bugs outside the reviewed files. Skip the numbered list below.

Otherwise:

1. If the user names files, a PR, or a commit, review that.
2. If they ask for uncommitted, local, or dirty changes, review `git diff` plus staged changes.
3. Otherwise review branch changes against the merge-base with the default base branch, including committed, staged, and unstaged changes.

Read enough surrounding code to judge each check. A diff line alone is not enough for a missing assertion, log, or test.

## Checklist

### Assertions

Impossible states should log an error and send a message to the on-call team (or the repo's equivalent), then return, throw, or respond with the right error. Flag a bare `throw`, silent return, or comment where that assertion belongs.

### Pure functions and unit tests

IO-free logic should be a pure function with unit tests that need no mocks. Flag new logic that is testable without IO but has no unit tests, and flag unit tests that mock.

### Integration tests

If the repo already has an integration-test pattern, IO functions in the diff need tests in that pattern, with no mocks except one or two in a rare case. If the repo has no integration-test pattern, do not request new integration tests.

### Logging

Every branch logs with `logInfo` or `logError` (or the repo's equivalents) and says which branch was taken. Flag a branch with no log. Flag any log that could contain PII or PHI.

### Unrelated bugs

If you notice a bug outside the change, run `uuidgen`, and write it up in `bugs_<uuid>.md`.

### Return values

Every non-void call's result is checked. Errors are handled. Values that must hold are asserted. Either path logs the result. Flag an ignored return value.

### Complexity

Flag a diff that is far larger than the problem (hundreds of lines for a change that could be about a hundred). Flag a workaround piled on a bad earlier decision; the fix is a `foundation_fix_required<uuid>.md` in the repo root. Flag extra complexity with no benefit. If the more complex design is justified, `complexity_justification<uuid>.md` must explain it.

## Report

Lead with the scope you reviewed. Then a table, highest severity first. Omit the table when there are no findings and say the standards review found no issues.

| Severity | Standard | Location | Finding |
| --- | --- | --- | --- |
| Must fix | Assertions | `path/file.ts:42` | What is wrong and what the standard requires |

Severity is **Must fix** or **Suggestion**. Location is `file:line`. After the table, list standards that passed in one line each, then any **Unrelated bugs**.
