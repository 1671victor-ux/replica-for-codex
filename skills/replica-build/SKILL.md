---
name: replica-build
description: >-
  Rebuilds an app screen by screen from the recon map: app shell first, then
  the core flow as a vertical slice, then every screen with all its states,
  ticking off the feature matrix as it goes. Writes every line fresh, never
  the original's code, assets or copy. Use when the user says "build the
  clone", "build screen S07", "start building", "rebuild this screen",
  "implement the booking page", or after $replica-design.
---

# replica-build

Reads `replica/recon.md`, `replica/architecture.md`, `replica/design/`.
Updates `replica/features.csv` (the `clone` column) and keeps
`replica/build-log.md`.

For a mobile project also read `replica/mobile.md`. Treat Expo/React Native as
the product runtime, not as a web preview: build and inspect native iOS and
Android surfaces throughout the work.

## The rules

- **Clean room.** Every line of code is written here, from the recon map and
  the specs. Never paste the original's HTML, CSS, JavaScript, SVGs or
  images, never load anything from its domain or CDN, never "view source and
  adapt".
- **Your words.** Write every label, button, empty state and email fresh.
  Matching what a button does is parity. Matching its sentence is copying.
- **Tokens only.** No raw hex or pixel values in components. If a value is
  missing, add it to the tokens.

## Step 1: the shell

Routing for every screen in the inventory (stub pages are fine), the layout
(nav, header, sidebar), tokens wired in, the primitives from replica-design,
and seed data so screens have something real to show. If commits are part of
the requested workflow, commit this shell as its own change; otherwise record
completion in `replica/build-log.md`.

## Step 2: the vertical slice

The core loop from the recon map, end to end, before anything else. For a
booking app: create an event type, open the public page, book a slot, see it
on the dashboard. Ugly is fine. Working is the point. If replica-backend has
not run yet, use the seed data and a fake data layer with the same function
signatures, so swapping in the real one changes no screen code.

## Step 3: screen by screen

Work in the order of `architecture.md`. For each screen:

1. Read its row in the recon map: purpose, components, states, which flows
   pass through it.
2. Look at the reference screenshot for layout and hierarchy. Not for pixels.
3. Build it with the primitives. Real data from the data layer.
4. **Every state**: empty, loading (skeletons, not spinners, if the original
   does), filled, error, no permission, long content (a 60 character name),
   mobile width.
5. Basics, every time: semantic HTML and keyboard support on web; accessible
   names, roles, font scaling, touch targets, keyboard avoidance and stable
   `testID` values on React Native.
6. Set the matching rows in `features.csv` to `yes` or `partial` (with a note).
7. Screenshot it in the same platform/device/state as the reference. Mobile
   output uses `replica/clone-screens/{ios|android}/{device}/S07/{state}.png`.
8. If the user requested commits or the repository instructions require them,
   make one commit per screen: `build: S07 booking page`. Otherwise keep the
   same screen-sized change boundary and record it in the build log.

## Definition of done, per screen

- [ ] every state from the recon map, plus empty, error and loading
- [ ] web: works at 390px and 1440px; mobile: required iOS and Android devices
- [ ] web keyboard flow or mobile screen-reader/touch/keyboard behavior works
- [ ] no console errors
- [ ] no hard-coded copy borrowed from the original
- [ ] features.csv updated
- [ ] screenshot saved for diff

## Native device loop

For every mobile screen and every core-flow change:

1. Run the project's checks, then build or start its Expo development build.
2. Launch the exact iOS simulator and Android emulator named in
   `replica/mobile.md` (`npx expo run:ios` / `npx expo run:android` when a
   native rebuild is needed; otherwise `npx expo start` and open the existing
   development build).
3. Seed a deterministic account and navigate to the recorded state. Prefer
   stable deep links and test IDs over coordinate taps.
4. Capture both platform screenshots at the contract paths and run
   `$replica-diff`.
5. Fix material layout or behavior gaps, recapture, and repeat until the
   screen meets the parity verdict. Then run its Maestro smoke flow.

If a required simulator, SDK, or device-control tool is unavailable, report
the exact missing prerequisite and leave that platform unverified. A web
render is not proof that a native screen works.

## Step 4: the build log

`replica/build-log.md`, one line per screen: ID, date, done or partial, what
is missing, what was harder than expected. When a feature is bigger than it
looked, say so in the log and in the chat. Do not quietly ship half of it.

## When you are stuck on how something works

Go back to the original as a user: read its help article, watch its public
walkthrough, use the user's own account. Do not dig into its code or network
calls. Then build your own version of the behaviour.

## Output

Screens built, the feature matrix updated, screenshots saved, and a summary:
screens done of total, must-haves done of total, what is next. Then
`$replica-backend` if the data layer is still fake, else `$replica-test`.

Source attribution: [references/origin.md](references/origin.md).
