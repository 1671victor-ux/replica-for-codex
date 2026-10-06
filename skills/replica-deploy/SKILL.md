---
name: replica-deploy
description: >-
  Ships an app clone live on the user's own domain: a preflight gate (tests
  green, parity must-haves done, rebrand sweep clean, listing linted, legal
  pages up), production database and env vars, the host, DNS records for the
  domain and for email, Stripe live mode, OAuth redirects, monitoring, and
  mobile builds to TestFlight and Play. Use when the user says "deploy it",
  "ship it", "put it live", "connect my domain", "go to production",
  "publish the app", or after $replica-launch.
---

# replica-deploy

Reads everything in `replica/`. Writes `replica/deploy.md` (the checklist in
`preflight.md` in this folder, filled in).

## The rules

- **Nothing goes live without the user's go.** Show the preflight results and
  ask.
- **The user buys and signs in.** Codex never buys a domain, enters a card,
  types a password or pastes a live key. Codex writes the exact DNS records,
  env var names and commands; the user does the account steps.
- **Not until it is rebranded.** The sweep must be clean. No exceptions.

## Step 1: preflight

Run every check and paste the results into `deploy.md`:

```bash
npx playwright test                                                  # replica-test
python3 ~/.codex/skills/replica-diff/parity.py replica/features.csv
python3 ~/.codex/skills/replica-brand/sweep.py . --config replica/brand.json
python3 ~/.codex/skills/replica-launch/listing.py replica/launch/listing.json
npm run build                                                        # production build passes
```

If Codex uses a custom skills directory, resolve each bundled script from the
loaded skill folder instead of assuming the default `~/.codex/skills` path.

Plus by hand: no open S1 or S2 bugs, privacy policy and terms pages live
(listing every processor), cookie banner if you use non-essential cookies in
the EU or UK, account deletion works, the favicon, titles and OG image are
yours.

Any failure stops the deploy. Say which and why.

For Expo/React Native add these hard gates for every required platform:

- the mobile environment doctor passes;
- the production-like native build installs and launches;
- all core Maestro flows pass on the named simulator/emulator;
- the current screenshot/diff set has no missing platform/device/state pair;
- permissions, deep links, offline recovery, background/resume, account
  deletion, privacy disclosures and branded system surfaces were verified;
- version/build numbers, bundle/package IDs, signing owner and EAS project are
  the intended production targets.

## Step 2: production services

- A **separate production project** for the database (never the dev one),
  backups on, migrations run by the deploy, not by hand.
- Env vars set in the host for production, matching `.env.example`. Live
  keys only here.
- **Stripe**: switch to live mode, recreate products and prices, add the
  production webhook endpoint and its signing secret, test one real
  purchase and refund it.
- **OAuth**: add the production domain to every provider's redirect URIs and
  authorised origins. Google scopes that need verification must be approved,
  or only test users can sign in.
- **Email**: the sending domain verified with the provider.

## Step 3: host and domain

Default: Vercel for Next.js (Netlify, Cloudflare Pages, Fly or Render
otherwise). Connect the repo so `main` deploys and pull requests get preview
URLs.

The domain, after the user buys it at any registrar:

| record | name | value |
| --- | --- | --- |
| A | @ | the host's apex IP (Vercel: shown in the domain settings) |
| CNAME | www | the host's target (Vercel: `cname.vercel-dns.com`) |
| TXT | @ or a subdomain | the host's verification value, if asked |

Email DNS from the email provider: SPF (TXT), DKIM (CNAME or TXT), and a
DMARC record starting at `v=DMARC1; p=none; rua=mailto:you@yourdomain` then
tightened to `quarantine` once reports are clean. Without these, your
confirmation emails go to spam.

Pick one canonical host (apex or www) and redirect the other. HTTPS is
automatic on the hosts above; check it.

## Step 4: watch it

Error tracking (Sentry or the host's), uptime checks on the home page and the
core flow's API, logs kept, analytics (a privacy-friendly one avoids the
cookie banner), and an alert to the user's email or phone. Then do the core
flow on the live site yourself, and ask the user to do it on their phone.

## Step 5: mobile, if there is an app

Expo: use explicit production profiles with `eas build --platform ios` and
`eas build --platform android`, then submit the exact successful build to
TestFlight and Play internal testing. Do not use ambiguous "latest" artifacts.
Native: archive in Xcode, upload to App Store Connect; Gradle bundle to Play
Console. The user owns the developer accounts ($99 a year for Apple, $25 once
for Google). Beta first, then review with the listing from replica-launch.
Run a real-device smoke pass from each beta channel before requesting store
review; simulator/emulator results alone do not verify signing, push,
associated domains, purchases, camera, notifications or release distribution.
Submitting builds, changing DNS, enabling live Stripe, and deploying production
are external mutations: show the exact target and preflight result, then obtain
the user's explicit approval immediately before each action.

## Output

`replica/deploy.md` with every check and its result, the live URL, the DNS
records set, and what to watch in the first week. The clone is now an app
with your name on it.

Source attribution: [references/origin.md](references/origin.md).
