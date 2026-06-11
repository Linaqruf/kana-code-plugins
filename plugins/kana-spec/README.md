# kana-spec

Write grounded specifications for anything — a project, a feature, a design
system, an API — with one command:

```
/kana-spec                                # spec the whole project
/kana-spec a comments feature             # component-scale spec
/kana-spec overhaul the design system     # audit-first, migration checklist
/kana-spec document this codebase         # capture reality as a spec
```

The output is built for **compound engineering**: `SPEC.md` is what future
agent sessions read, `SPEC/` files are what they look up, `CLAUDE.md` points
at both, and `prompt.md` restarts the loop — each session checks off phases
and feeds discoveries back into the spec.

## How it works

One pipeline for every subject and mode (Plan / Document / Overhaul):

```
SCOUT → FRAME → INTERVIEW → SCOPE CHECK → ENRICH → DRAFT → DRAFT CHECK → DELIVER
```

- **spec-scout** (agent) maps the codebase first — every claim cites
  `file:line` or is reported as unknown; large repos get parallel scouts.
  The map pre-fills the interview, so you only answer what code can't.
- **The interview** runs on phase goals, not scripts: intent → boundary
  (multi-select MVP picking, ruthless scoping) → shape (architecture options
  shown as side-by-side diagrams, recommended-first with honest tradeoffs)
  → risks. It disagrees with you once, plainly, when the evidence warrants —
  then defers.
- **spec-critic** (agent) reviews twice from a fresh context: a Scope Check
  *before* drafting (wrong premises die at their cheapest point) and a Draft
  Check after — enforcing a literal quality rubric and a cold-start test:
  "could a session with zero context start work from this spec alone?"
- The spec ships with a **Decision Log** (what was decided, why, what was
  rejected) and an **Assumptions & Evidence ledger** (every load-bearing
  premise marked VERIFIED with evidence or UNVERIFIED with what it gates) —
  so future sessions can re-verify instead of trusting.

Want more rigor? Say "be paranoid": dual scouts with reconciled findings and
critique-to-fixed-point.

## Install

```bash
/plugin marketplace add Linaqruf/kana-code-plugins
/plugin install kana-spec@kana-code-plugins
```

> Upgrading from `project-spec` (≤4.x)? Uninstall it first — this plugin
> replaces it under a new name, and v5 has no compatibility layer (your
> existing SPEC.md files still work: discovery is by globbing, not naming).

## Outputs

| Artifact | When | What |
|----------|------|------|
| `SPEC.md` | project-scale | Complete spec: requirements, architecture, system maps, phases |
| `SPEC/<slug>.md` | component-scale | Feature/design/migration spec |
| `SPEC/*.md` supplements | with your consent | Lookup references (schemas, endpoints, SDK patterns) |
| `CLAUDE.md` | project-scale | Agent pointer file (never duplicates the spec) |
| `prompt.md` | specs with phases | Compound-engineering session bootstrapper |

## Philosophy

- The spec is not the product — better future sessions are.
- Claims need citations; unknowns are written as unknown.
- Quality bars must be checkable, or they're vibes.
- An independent reviewer that onboards itself beats self-review every time.

## License

MIT
