# Architecture: {{your app}} (a rebuild of {{app}}'s core features)

## Stack

| layer | choice | why |
| --- | --- | --- |
| web | | |
| mobile runtime | Expo + React Native + TypeScript | |
| navigation | Expo Router | |
| database | | |
| auth | | |
| payments | | |
| email | | |
| jobs | | |
| hosting | | |

## Mobile contract

| item | choice |
| --- | --- |
| platforms | {{iOS / Android / both}} |
| reference devices | {{device + OS per platform}} |
| app scheme | {{...}} |
| iOS bundle ID | {{...}} |
| Android package | {{...}} |
| development runtime | {{Expo development build}} |
| EAS profiles | development, preview, e2e, production |
| E2E | Maestro flows {{F-IDs}} |
| offline policy | {{...}} |
| push/deep-link routing | {{...}} |

## Schema

Tables: {{n}}. Access rules: {{RLS | data-layer checks}}.

```sql
-- or see replica/schema.sql
```

## API

| method path | does | who | input | output | flow |
| --- | --- | --- | --- | --- | --- |

Webhooks in: {{...}}  Webhooks out: {{...}}
Jobs: {{name, schedule, what it does}}

## The parts that bite

- time zones:
- idempotency:
- races:
- secure native sessions:
- offline conflicts:
- push token rotation:
- app/API version compatibility:

## Build order

1. Vertical slice: {{screens, tables, routes}}
2. Must-haves:
3. Should-haves:
4. Fixes from replica-entrepreneur:

Each mobile milestone names its iOS and Android acceptance device, Maestro
flows, and screenshot states.
