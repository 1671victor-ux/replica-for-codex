---
name: replica-test
description: >-
  Tests every flow of an app clone on its real target: Playwright for web and
  Maestro plus iOS simulators and Android emulators for Expo/React Native.
  Generates happy paths and edge cases, captures evidence, fixes regressions,
  and reports bugs in a fixed format. Use when the
  user says "test my clone", "find bugs", "QA this", "click through
  everything", "write e2e tests", "does it work", or after $replica-build or
  $replica-backend.
---

# replica-test

Reads the flows in `replica/recon.md` and the platform contract in
`replica/mobile.md` when present. Writes `replica/test-plan.md`,
`replica/bugs.md`, and end-to-end tests in the project (`e2e/` for web,
`.maestro/` for mobile). Templates in this folder include `test-plan.md`,
`bug-report.md`, `e2e.example.spec.ts`, and `maestro.example.yml`.

Run the bundled, read-only environment check before mobile testing:

```bash
python3 ~/.codex/skills/replica-test/mobile_doctor.py . --require both
```

## The rule

**Test your clone, not the original.** Never load test, fuzz, script or
hammer the original app's servers. Using the original by hand, as a normal
user, to see how it behaves is fine.

## Step 1: the plan

For every flow F01, F02... in the recon map, write:

- **Happy path**: the steps, and what the user should see at the end.
- **Edge cases** that apply. Go down this list for every flow:
  empty input, very long input, emoji and accents, two tabs at once,
  double click on submit, back button mid-flow, refresh mid-flow, slow
  network, offline, expired session, second user's data (must be invisible),
  time zones and daylight saving, mobile width, keyboard only, screen reader
  labels; on mobile also app background/resume, process restart, airplane
  mode/reconnect, permission denied then enabled in Settings, keyboard open,
  deep-link cold start, notification entry, small/large font, safe areas,
  and the Android system back gesture.
- **Negative cases**: wrong password, card declined (Stripe test card
  `4000 0000 0000 0002`), permission denied, deleted record.

Number every case: F01-H1, F01-E3, F01-N2.

## Step 2: automate the target runtime

Choose by runtime. Do not count a web preview as mobile E2E.

### Web

Playwright, one spec per flow, against the local dev server with seed data.
Use roles and labels for selectors (`getByRole('button', { name: 'Book' })`),
never CSS classes. See `e2e.example.spec.ts`.

```bash
npm i -D @playwright/test && npx playwright install chromium
npx playwright test
```

Add to every spec: fail on console errors, fail on any 5xx response, and an
axe accessibility scan (`@axe-core/playwright`) on each screen.

### Expo / React Native

Reuse the project's mobile E2E framework if it already has one. Otherwise use
Maestro because the same declarative flows can exercise iOS and Android and
Expo's EAS workflows support it. Copy `maestro.example.yml` to one flow per
recon flow, replace placeholders, and use stable accessibility text or test
IDs. Run locally:

```bash
maestro test .maestro
```

The minimum automated set on both required platforms is: app launch or reset,
authentication, the core paid/user-value flow, one validation error, one
offline/retry case, a deep link, and sign out. Component tests with Jest and
React Native Testing Library provide fast feedback but do not replace device
E2E.

When `agent-device` is installed, Codex may use it to inspect the live app,
collect logs/screenshots/video, or run supported Maestro YAML. Keep the
Maestro files as the reproducible source of truth; record any exploratory
agent-device session separately instead of treating it as an invisible test.

## Step 3: click through the rest

What cannot be automated (emails arriving, OAuth with real providers,
payments end to end, visual glitches) gets a manual pass. For a web app, use a
connected browser/computer-use tool to drive the local clone and screenshot
each step when available. Otherwise give the user the checklist and wait for
answers.

For an Expo or native mobile app, run the same cases on both required
platforms and write evidence under
`replica/test-results/mobile/{ios|android}/{flow}/`. Evidence includes build
identifier, device and OS, command, pass/fail, screenshot on failure, and the
relevant device/app log. If only one platform is available, report the other
as unverified rather than passed.

## Step 4: report bugs

Every bug goes in `replica/bugs.md` in the `bug-report.md` format: an ID, a
severity, exact steps, expected, actual, evidence. Severity:

| | means |
| --- | --- |
| S1 | data loss, security hole, payments wrong, core flow blocked |
| S2 | a feature broken, no workaround |
| S3 | broken with a workaround, or visibly wrong |
| S4 | cosmetic |

Only report what you reproduced. "Might be an issue" goes in a separate
"to check" list.

## Step 5: fix loop

Fix S1 and S2 first. For every fix: write the failing test first, fix, watch
it pass, keep the test. Re-run the whole suite after each batch. Update
`bugs.md` with the commit that fixed each one when commits are part of the
requested workflow; otherwise record the changed files and test name.

For a visual mobile failure, return to `$replica-build`, capture the same
platform/device/state again, run `$replica-diff`, then rerun the failed
Maestro flow on both platforms. Do not close a platform-specific bug from a
passing test on the other platform.

## Output

`test-plan.md`, web and/or mobile specs, `bugs.md`, device evidence, and a
summary broken down by platform: cases run, passed, failed, bugs by severity,
fixed so far. Ship nothing with an open S1. If a fix changes layout, return to
`$replica-diff`; otherwise continue to `$replica-entrepreneur`.

Source attribution: [references/origin.md](references/origin.md).
