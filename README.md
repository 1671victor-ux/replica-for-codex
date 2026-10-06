# Replica for Codex

Eleven coordinated Codex skills for a clean-room mobile app replication
pipeline: the Replica methodology, Codex-native research and device work,
React Native/Expo, iOS Simulator and Android Emulator verification, visual
diffs, reproducible E2E tests, differentiation, store preparation and deploy.

Adapted from [Replica Skill](https://github.com/Jakeschincariol/replica-skill)
by Jake Schincariol under the MIT license. This repository preserves the
methodology and helper scripts while replacing Claude-specific invocation,
paths, browser assumptions, and authorization behavior with Codex-native
equivalents.

## Install all 11 skills with one Codex prompt

Paste this as one message in Codex:

```text
$skill-installer

Install all 11 Codex-ready skills from https://github.com/1671victor-ux/replica-for-codex using these repository paths: skills/replica-recon, skills/replica-architect, skills/replica-design, skills/replica-build, skills/replica-backend, skills/replica-test, skills/replica-diff, skills/replica-entrepreneur, skills/replica-brand, skills/replica-launch, skills/replica-deploy. Install them into the default user skills directory. They are already adapted from Claude to Codex and implement the Replica methodology as a React Native/Expo mobile pipeline with iOS and Android run, screenshot, diff, fix, Maestro E2E, App Store and deploy gates. Preserve the shared replica/ artifact workflow, MIT attribution, clean-room methodology, $replica-* invocation syntax, Codex paths, and authorization boundaries. After installation, verify that all 11 skills are present and run the bundled skill validator on every installed directory. If validation finds a confirmed Claude-only term, .claude path, slash-command invocation, unavailable tool, or automatic external write, adapt only that incompatible portion before reporting success. Report the installed paths and validation results. Do not publish, deploy, or modify external services.
```

The repository is already Codex-adapted. The compatibility pass in the prompt
is deliberately retained so future upstream syncs cannot silently reintroduce
Claude-only assumptions.

Installed skills become available on the next Codex turn.

## Tutorial

The complete Russian walkthrough is in [TUTORIAL.md](TUTORIAL.md). It follows
one mobile project from scope and recon through Expo builds, iOS/Android
screenshots, diff/fix, Maestro E2E, branding, store preparation, and deploy.

## Mobile-first pipeline

```text
RECON -> ARCHITECT -> DESIGN -> BUILD -> BACKEND
-> RUN ON IOS + ANDROID -> SCREENSHOT -> DIFF -> FIX -> E2E TEST
-> ENTREPRENEUR -> BRAND -> APP STORE -> DEPLOY
```

Invoke the first stage with `$replica-recon`. Each stage reads and updates the
shared `replica/` directory in the user's project. The FIX arrow loops through
`$replica-build`, `$replica-diff`, and `$replica-test` until required
platform/device/state pairs and core flows pass.

For mobile projects the skills standardize:

- Expo development builds with React Native and TypeScript;
- an explicit `replica/mobile.md` platform/device/deep-link contract;
- paired iOS Simulator and Android Emulator screenshots;
- structural diff artifacts organized by platform, device, screen and state;
- Maestro E2E flows, with optional `agent-device` evidence collection;
- TestFlight and Play internal-testing gates before store review.

## Codex adaptations

- `$replica-*` invocation instead of Claude slash commands.
- `~/.codex/skills` paths and custom-install fallback guidance.
- `web.run` for public research and connected browser/computer-use tools for
  user-authorized interactive work.
- No secrets requested in chat and no automatic production or external writes.
- Conditional commits rather than mandatory repository mutations.
- Native iOS/Android build, capture, diff, fix and Maestro E2E gates.
- `agents/openai.yaml` metadata for all eleven skills.
- Per-skill source attribution and MIT license retention.

## Included helpers

The six upstream helpers remain, plus two Codex mobile helpers. All Python
helpers use only the standard library:

- `contrast.py` — WCAG token contrast checks.
- `imgdiff.py` — structural or pixel PNG comparison.
- `parity.py` — weighted feature parity scoring.
- `reviews.py` — evidence-backed feedback theme ranking.
- `sweep.py` — original-brand residue detection.
- `listing.py` — App Store and Google Play metadata linting.
- `mobile_doctor.py` — read-only Expo, simulator/emulator and tool readiness.
- `mobile_capture.py` — deterministic iOS/Android screenshot capture.

## Requirements

- Codex with Agent Skills support.
- Python 3.8 or newer for bundled helpers.
- Internet access during installation from GitHub.

Mobile execution additionally needs the platform SDKs (Xcode Simulator on
macOS and/or Android SDK/emulator), the project's Expo dependencies, and
Maestro for the default device E2E path. `agent-device` is optional.

No Python packages are required by the Replica helpers.

## Mobile toolchain references

The pipeline follows the current official guidance for
[Expo development builds](https://docs.expo.dev/develop/development-builds/introduction/),
[Expo E2E with Maestro](https://docs.expo.dev/eas/workflows/examples/e2e-tests/),
[Expo agent-device](https://docs.expo.dev/agents/agent-device/),
[React Native testing](https://reactnative.dev/docs/testing-overview),
[Apple Simulator capture](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference),
and [Android adb screencap](https://developer.android.com/tools/adb).

## Safety boundary

Replica for Codex rebuilds functionality and UX patterns in a clean room. It
does not copy source code, private APIs, proprietary assets, trademarks,
licensed content, or another product's user network. Research is limited to
public sources and the user's own authorized account.
