# Mobile contract: {{app}}

## Targets

| platform | required | reference device | OS | orientation |
| --- | --- | --- | --- | --- |
| iOS | yes/no | {{iPhone model}} | {{version}} | portrait |
| Android | yes/no | {{Pixel/device class}} | {{API/version}} | portrait |

## Identity and routing

- App scheme: `{{scheme}}`
- iOS bundle ID: `{{com.company.app}}`
- Android package: `{{com.company.app}}`
- Universal/app-link hosts: {{hosts or unknown}}
- Deep links to verify: {{URL -> screen}}

## Native surfaces

- Permissions and denial behavior: {{...}}
- Notification entry points: {{...}}
- System sheets / share / pickers: {{...}}
- Keyboard and safe-area rules: {{...}}
- Background/resume behavior: {{...}}
- Offline/reconnect behavior: {{...}}
- Platform differences: {{...}}

## Evidence paths

```text
replica/screens/{ios|android}/{device}/{screen}/{state}.png
replica/clone-screens/{ios|android}/{device}/{screen}/{state}.png
replica/diffs/{ios|android}/{device}/{screen}/{state}.{png,json}
replica/test-results/mobile/{ios|android}/{flow}/
```

Unknowns must cite the missing evidence; do not silently invent behavior.
