---
name: review-ux
description: >-
  Reviews UI against personal UX standards: instant feedback beside the
  action, complete success or error feedback, consistent UI and wording,
  blocked invalid actions with explanations, obvious consequences before
  irreversible actions, one obvious next step, obvious navigation, common
  practices, and basic accessibility. Use when the user asks for a UX review
  or /review-ux.
disable-model-invocation: true
icon: eye
color: blue
---

# UX review

Review the requested change against the standards below. Write the report to a file. Do not edit the repo except to write that file. Do not fix findings unless the user asks.

Before reviewing, run `uuidgen` once and keep that value for this run. The report file is `ux_review_<uuid>.md` in the repository root. If the scope is a file that is not inside a git repo, write it in that file's directory. Do not invent the UUID, and do not reuse `ux_review.md`.

## Scope

If the prompt includes `Mode: current file`, read the listed files from disk and do not use git. Apply the standards to the whole file.

Otherwise:

1. If the user names files, a PR, or a commit, review that.
2. If they ask for uncommitted, local, or dirty changes, review `git diff` plus staged changes.
3. Otherwise review branch changes against the merge-base with the default base branch, including committed, staged, and unstaged changes.

Read enough surrounding UI to judge each standard: the control, its handler, the feedback rendered next to it, the view, and the navigation that reaches it. A diff line alone is not enough.

If the scope has no user-facing UI, write that in the report file and stop.

## Standards

### 1. Every Action the User Takes Should Have Instant Feedback Instantly Close to Where They Took the Action.

After a user clicks a submit button, the button should be greyed out, not
clickable, and a loading spinner should appear beside or below or above the
submit button.

### 2. Every Action the User Takes Should Have Complete Feedback As Soon As Possible Close to Where They Took the Action.

After the user action finishes, either something shows the success, or an error
message that says what went wrong and what to do next is displayed beside or below
or above the submit button that was clicked.

### 3. The UI Should Be Consistent At All Times.

If one part of your UI says you have three items in a list, and the list only
has two items, that's impermissible.

Two items that refer to the same thing or concept must use the same word to refer to it.

Two buttons that do similar things should look and behave similarly everywhere.

### 4. Invalid Actions Should Be Blocked Before Being Taken.

The "Submit" Button should be greyed out and shouldn't be clickable until the
data being submitted is valid. Invalid actions should explain why they are
invalid. If the data in a form is invalid, a detailed error message explaining
what is invalid and why is shown, and the error message disappears the frame
after the error is corrected.

### 5. The Consequences Of An Action Must Be Obvious Before The Action is Taken.

If an action cannot be trivially undone (destructive actions, writing immutable
data, confirming payment, etc.) the consequences must be made obvious BEFORE
the action is taken.

### 6. Every View Should Have One Obvious Next Step

The user should know immediately when looking at a view what the next step
is that they want to take.

### 7. The Next Navigation Should Always Be Obvious

If the user wants to get to view 3 from view 1, it should be obvious to the
user that clicking the navigation for view 2 gets them closer to view 3, and on
view 2 it should be obvious that clicking the navigation for view 3 gets them
to their destination.

### 8. Follows Common Practices Where Prudent

Happy path should have some green. Errors are red. An Icon for a hamburger menu
should open a hamburger menu.

### 9. Basic Accessibility Is Followed

Colour isn't the only signal, text and icons are used in conjunction. Text is
always legible against the background.

## Applying the standards

The submit-button examples apply to every user action, not only forms. Judge what the markup, styles, and handlers show. Flag a violation. Skip a standard the change does not touch. If contrast or placement cannot be judged from the code, say that in the finding instead of guessing.

Use these short titles in the report: Instant feedback, Complete feedback, Consistency, Block invalid actions, Obvious consequences, One obvious next step, Obvious navigation, Common practices, Basic accessibility.

## Report

Write the report to `ux_review_<uuid>.md`, using the UUID from the start of this run. Do not print the report to regular output. Lead with the scope you reviewed. Then a table, highest severity first. Omit the table when there are no findings and say the UX review found no issues.

| Severity | Standard | Location | Finding |
| --- | --- | --- | --- |
| Must fix | Instant feedback | `path/file.tsx:42` | What is wrong and what the standard requires |

Severity is **Must fix** or **Suggestion**. Location is `file:line`. After the table, list standards that passed in one line each. After writing the file, tell the user the report path, including the UUID.
