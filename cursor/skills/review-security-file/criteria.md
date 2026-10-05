# Security review of a file

Perform a security review of the current contents of the files named in the prompt. Read those files from disk. Do not use git diff. Do not require a branch. Do not edit the repo.

## Scope

- Review the named files as they currently exist.
- Do not report vulnerabilities in other files unless code in a named file makes them newly exploitable.
- Report only concrete, validated security issues with realistic exploitability.
- Use readonly tools to inspect surrounding code before making claims.
- Consider common application security vulnerabilities, insecure configuration, infrastructure security, unsafe code patterns or parameters, and security-related TODOs in the named files that were not completed.

## Prioritize

- Authorization, privilege escalation, and cross-tenant or cross-user access.
- Credential, secret, token, or sensitive data exposure.
- Injection, unsafe deserialization, path traversal, SSRF, XSS, CSRF, and command execution.
- Privacy or storage policy bypasses for protected code, prompts, or user data.
- Feature gate or control-plane bypasses with security impact.
- Agent/tool trust boundaries: hidden prompts or command blocks, auto-approved tools, MCP capabilities, delimiter handling, command execution identity, tool timeouts, and fail-open behavior.
- Filesystem and workspace boundaries: path normalization and containment, symlink-sensitive writes, unsafe project/root switching, archive extraction, cache/plugin paths, and agent/tool-controlled filesystem inputs.
- Config/template injection: wiring source code, file contents, paths, prompts, completions, search results, stack traces, or serialized code-bearing payloads into config objects or templates.
- API/RPC privilege annotations for procedures in the named files, especially actions involving admin, permission, policy, secret, token, credential, rollout, deploy, delete, backfill, suspend, block, override, or other sensitive control-plane behavior.
- Platform-sensitive patterns: unauthenticated route markers, unvalidated identity accessors, auth context mutation, TLS validation bypasses, sensitive debug logging, and CSP or unsafe HTML/script exceptions.

## Triage

- Trace data origin through the call chain before reporting. Ask whether an attacker can realistically control the input and what constraints apply.
- Check implicit sanitization and validation such as URL parsing, database existence checks, auth/permission checks, type coercion, enum validation, schema validation, framework middleware, React/SolidJS escaping, and ORM parameterization.
- Verify functions, variables, type definitions, initialization, validation logic, and authorization patterns with tools before claiming they are missing.
- Report security-related TODOs or comments only when they represent a real missing control on a path in a named file and you can trace a concrete attacker-controlled path to meaningful impact.
- Only report medium, high, or critical issues. Discard low-severity hygiene, speculative defense-in-depth comments, and findings without a demonstrated security consequence.

## Privacy and data-handling checks

- Credentials must not be logged or stored plaintext.
- PII/PHI must not be logged or stored plaintext.

## Resource-exhaustion triage

- Report only when there is unauthenticated or low-cost amplification, cross-tenant or cross-user storage/response growth, attacker-controlled fanout, expensive processing per byte, quota/rate-limit bypass with shared impact, or persistence in a hot global index or frequently read shared path.

## False positives to avoid

- Missing auth when framework-level middleware exists.
- SQL injection in parameterized ORM calls such as Prisma or TypeORM.
- XSS in ordinary JSX expressions; focus on explicit raw-HTML insertion sinks and framework escape hatches.

## Report

Lead with the files you reviewed. For each finding include severity, location as `file:line` in a named file, impact, attack path, evidence, and remediation. The evidence should support exploitability. Only medium, high, or critical.

Then a table, highest severity first. Omit the table when there are no findings and say no security issues were found.

| Severity | Location | Finding |
| --- | --- | --- |
| High | `path/file.ts:42` | One sentence impact |
