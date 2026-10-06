# Deploy checklist: {{your app}}

Date: {{YYYY-MM-DD}}  Commit: {{sha}}  Go from user: {{yes / not yet}}

## Preflight (all must pass)

- [ ] e2e suite green: {{n passed / n}}
- [ ] no open S1 or S2 bugs
- [ ] parity: all must-haves done ({{n/n}}), feature score {{n}}
- [ ] rebrand sweep clean (`sweep.py` exit 0)
- [ ] store listing passes (`listing.py` exit 0), if shipping to stores
- [ ] production build passes
- [ ] iOS production-like build installs and core Maestro flows pass
- [ ] Android production-like build installs and core Maestro flows pass
- [ ] mobile screenshot/diff matrix complete for required devices and states
- [ ] deep links, permissions, offline recovery and background/resume verified
- [ ] bundle/package IDs, version/build numbers, signing owner and EAS project verified
- [ ] privacy policy and terms live, every processor listed
- [ ] account deletion works
- [ ] favicon, titles, OG image, emails, app icon are yours

## Production

- [ ] separate production database, backups on, migrations in the deploy
- [ ] env vars set (names match .env.example)
- [ ] Stripe live: products, prices, webhook endpoint + secret, one real purchase refunded
- [ ] OAuth redirect URIs and origins include the production domain
- [ ] Google OAuth verification approved (if using sensitive scopes)
- [ ] email sending domain verified

## Domain

- [ ] A @ -> {{value}}
- [ ] CNAME www -> {{value}}
- [ ] SPF, DKIM, DMARC set
- [ ] canonical host chosen, the other redirects
- [ ] HTTPS valid

## Watch

- [ ] error tracking
- [ ] uptime checks
- [ ] analytics
- [ ] core flow done on the live site, desktop and phone

## Mobile distribution

- [ ] exact iOS build sent to TestFlight; real-device beta smoke passed
- [ ] exact Android build sent to Play internal testing; real-device beta smoke passed
- [ ] App Store privacy labels and Google Play Data safety match the build
- [ ] store screenshots/listings are final branded production artifacts
- [ ] explicit user approval recorded before each submit or review action
