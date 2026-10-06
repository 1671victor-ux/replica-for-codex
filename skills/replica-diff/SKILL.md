---
name: replica-diff
description: >-
  Compares an app clone against the original: a feature parity score from the
  feature matrix (weighted by must, should, could) with the missing list in
  build order, plus a screenshot layout diff that ignores colour so a rebrand
  does not count against you. Captures from iOS Simulator and Android devices
  and compares every platform/device/state pair. Use when the
  user says "how close is my clone", "compare it to the original", "what's
  missing", "parity check", "diff the screens", "is it ready", or after
  $replica-build captures the native screens.
---

# replica-diff

Three tools in this folder, all standard-library Python, no Python installs:

```bash
python3 ~/.codex/skills/replica-diff/parity.py replica/features.csv
python3 ~/.codex/skills/replica-diff/imgdiff.py replica/screens/S07.png replica/clone-screens/S07.png --out diff-S07.png
python3 ~/.codex/skills/replica-diff/imgdiff.py a.png b.png --json > replica/diffs/S07.json
python3 ~/.codex/skills/replica-diff/parity.py replica/features.csv --visual replica/diffs/*.json --markdown > replica/parity.md
python3 ~/.codex/skills/replica-diff/mobile_capture.py ios replica/clone-screens/ios/iphone-15/S07/filled.png
python3 ~/.codex/skills/replica-diff/mobile_capture.py android replica/clone-screens/android/pixel-8/S07/filled.png
```

## What parity means here

**Parity means it does the same job, not that it looks the same.** The
feature score is the number that matters: can a user do everything they could
do in the original. The layout score checks structure (is the information in
the same places, in the same hierarchy), because that is what makes a switcher
feel at home. It deliberately ignores colour, because replica-brand changes
every colour on purpose. Do not chase pixel parity with the original. Its
exact look is its trade dress, and it changes before launch.

## Step 1: feature parity

Make sure `replica/features.csv` is current: every row's `clone` column is
`yes`, `partial` (with a note), `no`, or `skip` (with a reason). Then:

```bash
python3 ~/.codex/skills/replica-diff/parity.py replica/features.csv
```

It weights must 3, should 2, could 1, counts partial as half, leaves out
`skip` rows and rows you added that the original does not have, and prints:
the score, must-haves done of total, each area weakest first, and the missing
list in build order. Must-haves not done means not shippable, and it says so.

## Step 2: layout diff

For each key screen, take two screenshots in the **same platform, device,
orientation and state** (same data shape, same tab open, logged in the same
way). Web defaults are 1440x900 desktop and 390x844 mobile. Native captures
use the exact simulator/emulator profiles from `replica/mobile.md`. The
original's come from public pages or the user's own account, saved in
`replica/screens/{platform}/{device}/{screen}/{state}.png`; the clone's go in
the identical tree under `replica/clone-screens/`.

`mobile_capture.py` wraps the official device commands without shell
redirection: `xcrun simctl io ... screenshot` for iOS and `adb exec-out
screencap -p` for Android. It refuses to overwrite unless `--force` is set.
Select a specific simulator UDID or Android serial when more than one is
running.

```bash
python3 ~/.codex/skills/replica-diff/imgdiff.py replica/screens/S07.png replica/clone-screens/S07.png --out replica/diffs/S07.png
```

Layout mode (default) turns both into edge maps, cuts them into a grid, and
compares where things are, scoring only cells with something in them. It
reports the score (matches 90+, close 75+, partly 50+, different), the
regions that differ (in the original's pixel coordinates, biggest first), and
a height difference if the clone's page is much longer or shorter. Retina and
non-retina screenshots compare fine: both are scaled to the same width.

`--mode pixel` is exact comparison. Use it for your own regressions (clone
today against clone last week), not against the original.

Generate one JSON result per pair beneath
`replica/diffs/{platform}/{device}/{screen}/{state}.json`. Never average iOS
and Android into one opaque number: report each platform, the worst key-screen
score, and missing pairs. A missing required capture is a failed gate, not a
zero that can be averaged away.

## Step 3: behaviour diff

Walk each flow in both apps and compare what the scores cannot see: clicks to
finish the core flow, what happens on errors, what is remembered between
visits, what emails arrive. Fewer clicks than the original is a win. Write
each difference as: flow, original does, clone does, fix or keep.

On mobile include gestures and system back, keyboard movement, permissions,
system sheets, deep-link cold/warm start, background/resume, offline recovery,
notifications, safe areas and screen-reader order. Tag every difference
`ios`, `android`, or `both`.

## Step 4: the report

`replica/parity.md`: overall score, feature score, layout score per screen,
missing features in build order, behaviour differences, and a verdict:

- **return to build**: any must-have missing, required capture absent, or a key
  screen below the agreed layout threshold
- **ready for E2E**: all must-haves done, feature score 80+, every required
  capture present, and key screens meet the threshold
- **release candidate** is not awarded here; it requires `$replica-test`, the
  differentiation work, rebrand and deploy preflight

Give honest numbers. A clone at 62% is at 62%.

## Output

`replica/parity.md`, the diff images/JSON grouped by platform, and the top five
things to build next. If a must-have or key screen fails, return to
`$replica-build`, recapture, diff again, and rerun `$replica-test`. Continue to
`$replica-entrepreneur` only when the gate is green.

Source attribution: [references/origin.md](references/origin.md).
