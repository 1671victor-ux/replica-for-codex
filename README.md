# Replica for Codex

Eleven coordinated Codex skills for clean-room product research and app
development. The workflow maps what a product does, plans and builds an
original implementation, tests it, finds evidence-backed opportunities to
improve it, gives it a distinct brand, and prepares launch and deployment.

Adapted from [Replica Skill](https://github.com/Jakeschincariol/replica-skill)
by Jake Schincariol under the MIT license. This repository preserves the
methodology and helper scripts while replacing Claude-specific invocation,
paths, browser assumptions, and authorization behavior with Codex-native
equivalents.

## Install all 11 skills with one Codex prompt

Paste this as one message in Codex:

```text
$skill-installer

Install all 11 Codex-ready skills from https://github.com/1671victor-ux/replica-for-codex using these repository paths: skills/replica-recon, skills/replica-architect, skills/replica-design, skills/replica-build, skills/replica-backend, skills/replica-test, skills/replica-diff, skills/replica-entrepreneur, skills/replica-brand, skills/replica-launch, skills/replica-deploy. Install them into the default user skills directory. They are already adapted from Claude to Codex; preserve the shared replica/ artifact workflow, MIT attribution, clean-room methodology, $replica-* invocation syntax, Codex paths, and authorization boundaries. After installation, verify that all 11 skills are present. If validation finds a confirmed Claude-only term, .claude path, slash-command invocation, unavailable tool, or automatic external write, adapt only that incompatible portion before reporting success. Report the installed paths and validation results. Do not publish, deploy, or modify external services.
```

The repository is already Codex-adapted. The compatibility pass in the prompt
is deliberately retained so future upstream syncs cannot silently reintroduce
Claude-only assumptions.

Installed skills become available on the next Codex turn.

## Pipeline

```text
replica-recon -> replica-architect -> replica-design -> replica-build
-> replica-backend -> replica-test -> replica-diff -> replica-entrepreneur
-> replica-brand -> replica-launch -> replica-deploy
```

Invoke the first stage with `$replica-recon`. Each stage reads and updates the
shared `replica/` directory in the user's project.

## Codex adaptations

- `$replica-*` invocation instead of Claude slash commands.
- `~/.codex/skills` paths and custom-install fallback guidance.
- `web.run` for public research and connected browser/computer-use tools for
  user-authorized interactive work.
- No secrets requested in chat and no automatic production or external writes.
- Conditional commits rather than mandatory repository mutations.
- Web plus iOS/Android simulator or emulator testing guidance.
- `agents/openai.yaml` metadata for all eleven skills.
- Per-skill source attribution and MIT license retention.

## Included helpers

The six upstream helpers remain standard-library Python scripts:

- `contrast.py` — WCAG token contrast checks.
- `imgdiff.py` — structural or pixel PNG comparison.
- `parity.py` — weighted feature parity scoring.
- `reviews.py` — evidence-backed feedback theme ranking.
- `sweep.py` — original-brand residue detection.
- `listing.py` — App Store and Google Play metadata linting.

## Requirements

- Codex with Agent Skills support.
- Python 3.8 or newer for bundled helpers.
- Internet access during installation from GitHub.

No Python packages are required by the Replica helpers.

## Safety boundary

Replica for Codex rebuilds functionality and UX patterns in a clean room. It
does not copy source code, private APIs, proprietary assets, trademarks,
licensed content, or another product's user network. Research is limited to
public sources and the user's own authorized account.
