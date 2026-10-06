# Replica for Codex: пошаговый туториал

Этот туториал проводит один мобильный проект через весь конвейер:

```text
RECON → ARCHITECT → DESIGN → BUILD → BACKEND
→ RUN ON iOS + ANDROID → SCREENSHOT → DIFF → FIX → E2E TEST
→ ENTREPRENEUR → BRAND → APP STORE → DEPLOY
```

В примере мы создаём собственный habit-tracker `PulseHabit`, изучая публично
доступное приложение той же категории. Название условное: на этапе BRAND оно
будет проверено и при необходимости заменено.

Главный принцип: Replica воспроизводит задачу, пользовательский поток и
полезные UX-паттерны, но не копирует исходный код, закрытые API, тексты,
название, логотип, изображения, платные шрифты или пользовательскую базу
исходного приложения.

## 1. Что понадобится

Минимум:

- Codex с установленными 11 навыками Replica;
- отдельный Git-репозиторий будущего приложения;
- Node.js и Python 3.8+;
- Android Studio с эмулятором для Android;
- macOS и Xcode с Simulator для локального iOS-тестирования;
- Maestro для мобильных E2E-тестов;
- доступ только к публичным материалам и собственному аккаунту в исследуемом
  приложении.

Expo `agent-device` необязателен. Если он установлен, Codex сможет собирать
дополнительные логи, снимки и видео, но воспроизводимые Maestro-файлы всё равно
остаются источником истины.

Для публикации позже понадобятся собственные аккаунты Apple Developer и
Google Play Console. Они не нужны для первых этапов.

Официальные инструкции:

- [Expo development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [Expo E2E с Maestro](https://docs.expo.dev/eas/workflows/examples/e2e-tests/)
- [Expo agent-device](https://docs.expo.dev/agents/agent-device/)
- [React Native testing](https://reactnative.dev/docs/testing-overview)
- [Android Debug Bridge](https://developer.android.com/tools/adb)

## 2. Установка навыков

Отправьте в Codex одним сообщением:

```text
$skill-installer

Install all 11 Codex-ready skills from https://github.com/1671victor-ux/replica-for-codex using these repository paths: skills/replica-recon, skills/replica-architect, skills/replica-design, skills/replica-build, skills/replica-backend, skills/replica-test, skills/replica-diff, skills/replica-entrepreneur, skills/replica-brand, skills/replica-launch, skills/replica-deploy. Install them into the default user skills directory. Preserve the Replica methodology, React Native/Expo mobile pipeline, iOS and Android run/screenshot/diff/fix/Maestro E2E loop, shared replica/ artifacts, MIT attribution, $replica-* invocation syntax, Codex paths, and authorization boundaries. Validate all 11 installed skills and report their paths. Do not publish, deploy, or modify external services.
```

Используйте навыки в следующем новом сообщении или новом чате после установки.

## 3. Подготовьте рабочий проект

Откройте в Codex отдельную папку будущего приложения. В ней будут жить код и
служебная директория `replica/`.

Рекомендуемая исходная структура:

```text
pulsehabit/
├── .git/
├── AGENTS.md              необязательно: правила вашего репозитория
└── README.md
```

Не создавайте Expo-проект заранее, если у вас нет предпочтений по стеку.
`$replica-architect` сначала зафиксирует архитектуру. Если проект уже
существует, прямо скажите Codex сохранить выбранный стек и соглашения.

Полезно заранее определить:

| решение | пример |
| --- | --- |
| исследуемое приложение | ссылка на App Store / Google Play / сайт |
| продуктовый срез | привычки, ежедневный check-in, серии и напоминания |
| аудитория | люди, которым нужен простой офлайн-first трекер |
| платформы | iOS и Android |
| эталон iOS | iPhone 15, выбранная версия iOS |
| эталон Android | Pixel 8, выбранный API level |

Не начинайте со scope «скопировать всё приложение». Один законченный основной
поток полезнее двадцати недостроенных экранов.

## 4. Этап RECON

Цель: получить доказательную карту продукта до написания кода.

Отправьте:

```text
$replica-recon

Изучи приложение <ССЫЛКА> как clean-room reference для моего собственного мобильного продукта. Используй только публичные источники и мой собственный авторизованный аккаунт. Scope первой версии: создание привычки, ежедневный check-in, серия выполнений, напоминание и базовая статистика. Целевые платформы: iOS и Android. Предложи точные эталонные устройства и версии ОС, но зафиксируй их только после моего подтверждения. Создай полный набор артефактов replica/ и отдельно перечисли всё, чего нельзя уверенно установить по источникам.
```

Если требуется войти в ваш аккаунт, выполняйте секретный ввод только в
официальном интерфейсе. Не передавайте пароль, 2FA-код или токен в чат.

После этапа должны появиться:

```text
replica/
├── recon.md
├── features.csv
├── mobile.md
└── screens/
    ├── ios/<device>/S01/<state>.png
    └── android/<device>/S01/<state>.png
```

Проверьте перед продолжением:

- у каждого экрана есть стабильный ID `S01`, `S02` и так далее;
- у каждого потока есть ID `F01`, `F02`;
- состояния `empty`, `loading`, `filled`, `error` и `permission-denied` не
  смешаны в одну строку;
- различия iOS и Android записаны отдельно;
- догадки помечены как догадки и снабжены пробелом в доказательствах;
- чужие скриншоты лежат только в `replica/screens/` и не попадут в продукт.

Если карта слишком широкая, остановитесь и попросите:

```text
Сократи scope до одного вертикального потока F01, который можно закончить и проверить на iOS и Android. Остальное оставь в features.csv как should/could.
```

## 5. Этап ARCHITECT

Цель: превратить recon-карту в реализуемый Expo-проект.

```text
$replica-architect

Спроектируй мобильную архитектуру по текущим replica/recon.md, replica/features.csv и replica/mobile.md. По умолчанию используй Expo, React Native, TypeScript и Expo Router. Нужны development, preview, e2e и production profiles, iOS Simulator build и Android APK для E2E. Спроектируй offline-first check-in, безопасную сессию, deep links и push reminders. Сначала дай тонкий вертикальный slice F01, затем must-have функции. Не создавай внешние сервисы и не используй live credentials.
```

Ожидаемые результаты:

```text
replica/architecture.md
replica/schema.sql          или первая migration
```

Проверьте, что архитектура фиксирует:

- `scheme`, iOS bundle ID и Android package;
- минимальные версии ОС;
- development/preview/e2e/production profiles;
- формат локального кеша и разрешение конфликтов;
- безопасное хранение refresh token;
- ротацию push token;
- Maestro flow IDs и снимки, необходимые для каждого milestone;
- API и таблицы, привязанные к конкретным потокам `Fxx`.

Архитектура не должна копировать предполагаемый внутренний стек исходного
приложения. Она должна реализовать наблюдаемое поведение простыми средствами.

## 6. Этап DESIGN

Цель: получить самостоятельную дизайн-систему, которая сохраняет понятную
структуру продукта без копирования его фирменного образа.

```text
$replica-design

Создай дизайн-систему для React Native по recon-карте и разрешённым reference screenshots. Сохрани информационную иерархию и знакомые UX-паттерны, но не копируй логотип, тексты, иллюстрации, платные шрифты или фирменный цвет. Подготовь typed tokens.ts, спецификации компонентов, accessibility/testID contract и development-only component gallery. Проверь iOS и Android отдельно и доведи contrast report до нуля AA-ошибок.
```

Результат обычно выглядит так:

```text
replica/design/
├── tokens.json
├── tokens.ts
└── components.md
```

Запустите проверку контраста:

```bash
python3 ~/.codex/skills/replica-design/contrast.py replica/design/tokens.json
```

Переходите дальше только при `0 failing AA`.

## 7. Этап BUILD: первый вертикальный slice

Цель: построить работающий F01 с временным data layer, а не коллекцию
несвязанных экранов.

```text
$replica-build

Реализуй первый вертикальный slice F01 по replica/architecture.md. Создай Expo/React Native приложение, app shell, Expo Router routes, design primitives и детерминированные seed data. Пока используй fake data layer с теми же интерфейсами, которые ожидает будущий backend. Для каждого экрана реализуй все зафиксированные состояния, доступные имена, testID, keyboard avoidance и safe areas. Обновляй replica/features.csv и replica/build-log.md. Не переходи к should/could, пока F01 не работает целиком.
```

Хороший вертикальный slice для примера:

```text
F01 Создание и ежедневное выполнение привычки
S01 onboarding → S02 список → S03 новая привычка → S04 карточка → S05 check-in
```

После сборки проверьте:

- основной поток проходит на seed data;
- экранный код не зависит от fake backend напрямую;
- интерактивные элементы имеют стабильные `testID`;
- в компонентах нет случайных hex/pixel-значений вместо tokens;
- `features.csv` содержит честные `yes`, `partial` или `no`;
- незавершённые состояния явно записаны в `build-log.md`.

## 8. Этап BACKEND

Цель: заменить временный data layer настоящими данными и безопасной
авторизацией.

```text
$replica-backend

Реализуй backend из replica/architecture.md для F01 и текущих must-have функций. Создай migrations, RLS/access rules, seed script, auth и offline-safe idempotent mutations. Для native auth используй поддерживаемый мобильный flow и OS-backed secure storage; ничего чувствительного не помещай в AsyncStorage или bundle. Подготовь .env.example без значений. Используй только официальные API и test mode. После реализации верни управление replica-build для подключения реального data layer и native verification.
```

Пользователь самостоятельно создаёт аккаунты внешних сервисов и вводит ключи
в локальное окружение. Codex может подготовить `.env.example`, но не должен
просить секреты в чате или включать их в Git.

Обязательная ручная проверка: второй тестовый пользователь не должен видеть
данные первого.

## 9. Подключите backend и запустите native loop

Вернитесь к build:

```text
$replica-build

Замени fake data layer реальной реализацией из replica-backend. Затем выполни native device loop для F01 на обоих устройствах из replica/mobile.md: build/run, детерминированное состояние, screenshot, diff, fix и повторный smoke flow. Не считай web preview доказательством работоспособности iOS или Android.
```

Сначала проверьте окружение:

```bash
python3 ~/.codex/skills/replica-test/mobile_doctor.py . --require both
```

Диагност завершится с ошибкой, если отсутствует обязательный runtime,
Expo-конфигурация или Node/Npx. Это корректный stop-gate, а не сбой навыка.
Строгая E2E-проверка позднее добавит флаг `--e2e` и потребует `.maestro/` и
Maestro CLI.

Когда менялись native dependencies или app config, пересоберите development
build:

```bash
npx expo run:ios
npx expo run:android
```

Если native build уже актуален, обычно достаточно запустить bundler и открыть
существующий development build:

```bash
npx expo start
```

## 10. SCREENSHOT и DIFF

Подготовьте исходное и клоновое приложение в одинаковом состоянии. Должны
совпадать платформа, модель устройства, ОС, ориентация, данные и открытый экран.

Захват клона:

```bash
python3 ~/.codex/skills/replica-diff/mobile_capture.py ios replica/clone-screens/ios/iphone-15/S05/filled.png
python3 ~/.codex/skills/replica-diff/mobile_capture.py android replica/clone-screens/android/pixel-8/S05/filled.png
```

Если запущено несколько устройств, передайте точный идентификатор:

```bash
python3 ~/.codex/skills/replica-diff/mobile_capture.py ios replica/clone-screens/ios/iphone-15/S05/filled.png --device <SIMULATOR_UDID>
python3 ~/.codex/skills/replica-diff/mobile_capture.py android replica/clone-screens/android/pixel-8/S05/filled.png --device <ADB_SERIAL>
```

Сравните одинаковые пары:

```bash
mkdir -p replica/diffs/ios/iphone-15/S05
mkdir -p replica/diffs/android/pixel-8/S05
python3 ~/.codex/skills/replica-diff/imgdiff.py replica/screens/ios/iphone-15/S05/filled.png replica/clone-screens/ios/iphone-15/S05/filled.png --out replica/diffs/ios/iphone-15/S05/filled.png --json > replica/diffs/ios/iphone-15/S05/filled.json
python3 ~/.codex/skills/replica-diff/imgdiff.py replica/screens/android/pixel-8/S05/filled.png replica/clone-screens/android/pixel-8/S05/filled.png --out replica/diffs/android/pixel-8/S05/filled.png --json > replica/diffs/android/pixel-8/S05/filled.json
```

Затем запустите сам навык:

```text
$replica-diff

Проверь feature parity и все обязательные пары platform/device/screen/state. Отчитайся отдельно по iOS и Android, перечисли отсутствующие пары и худшие key screens. Игнорируй различия фирменного цвета, но анализируй структуру, иерархию, safe areas, keyboard behavior, gestures и system back. Если gate красный, сформируй конкретный FIX backlog в порядке влияния на F01.
```

Feature score:

```bash
python3 ~/.codex/skills/replica-diff/parity.py replica/features.csv
```

Правильный результат этапа — не «похожая картинка», а ответ на три вопроса:

1. Выполняет ли клон ту же пользовательскую задачу?
2. Узнаваема ли информационная иерархия без копирования бренда?
3. Есть ли отдельные доказательства для iOS и Android?

## 11. FIX loop

Если diff сообщает `return to build`, не переходите к E2E:

```text
$replica-build

Исправь только красные пункты из replica/parity.md, начиная с must-have и худшего key screen. Не меняй бренд ради повышения layout score. После каждого исправленного состояния повторно запусти обе платформы, пересними ту же пару и снова вызови replica-diff. Остановись, когда gate станет ready for E2E или когда появится конкретный внешний blocker.
```

Цикл выглядит так:

```text
BUILD → RUN iOS/Android → CAPTURE → DIFF
  ↑                                  │
  └──────────── FIX backlog ─────────┘
```

Не закрывайте Android-дефект успешным снимком iOS и наоборот.

## 12. E2E TEST

Цель: закрепить критические пользовательские потоки как воспроизводимые тесты.

```text
$replica-test

Создай и запусти Maestro E2E для всех must-have flows на обоих устройствах из replica/mobile.md. Минимум: launch/reset, auth, F01, validation error, offline/retry, deep-link cold start и sign out. Сохрани evidence по platform/flow, а воспроизведённые дефекты запиши в replica/bugs.md. Для каждого S1/S2 сначала создай падающий regression test, затем исправь и повтори suite на обеих платформах.
```

Минимальный Maestro flow находится в
`~/.codex/skills/replica-test/maestro.example.yml`. Рабочие тесты проекта
кладутся в `.maestro/`, например:

```text
.maestro/
├── F01-create-and-check-in.yml
├── F02-offline-retry.yml
└── F03-deep-link.yml
```

Локальный запуск:

```bash
python3 ~/.codex/skills/replica-test/mobile_doctor.py . --require both --e2e
maestro test .maestro
```

Доказательства сохраняются отдельно:

```text
replica/test-results/mobile/
├── ios/F01/
└── android/F01/
```

Условие перехода дальше: нет открытых S1/S2, а обязательные тесты зелёные на
обеих заявленных платформах. Если исправление изменило layout, повторите DIFF.

## 13. ENTREPRENEUR

Теперь продукт должен стать лучше исходного, а не только функционально близким.

```text
$replica-entrepreneur

Исследуй реальные публичные отзывы о reference app и категории. Не выдумывай отзывы, рейтинги или цитаты; каждая цитата должна быть дословной и иметь ссылку. Сохраняй platform и app_version. Выдели повторяющиеся проблемы, недостающие функции и незакрытые аудитории. Составь 5–8 evidence-backed улучшений и добавь их в features.csv как функции, которых нет у оригинала.
```

После сбора данных:

```bash
python3 ~/.codex/skills/replica-entrepreneur/reviews.py replica/reviews.csv --out replica/feedback.md
```

Не называйте три комментария трендом. Слабые темы должны оставаться помеченными
как `thin`. Выбранные улучшения проходят тот же BUILD → DIFF → E2E loop.

## 14. BRAND

```text
$replica-brand

Создай самостоятельный бренд на основе replica/fixes.md. Подготовь кандидаты названия, фактический список trademark/domain/store/handle checks, новую палитру, voice guide и briefs для iOS icon, Android adaptive icon, splash и notification icon. Затем замени исходный бренд в app config, bundle/package identity, deep links, permission strings и интерфейсе. Запусти sweep до чистого результата и пересобери обе native-платформы.
```

Проверка остатков:

```bash
python3 ~/.codex/skills/replica-brand/sweep.py . --config replica/brand.json
```

`exit 1` означает, что запускать продукт рано. Исправьте совпадения и проверьте
глазами launcher icon, splash, permission dialogs, share sheet и уведомления.

Автоматическая проверка названия не заменяет юридическую экспертизу товарного
знака.

## 15. APP STORE

Этот этап выполняет `$replica-launch`:

```text
$replica-launch

Подготовь landing, pricing и отдельные store packs для iOS и Android на основе подтверждённого positioning angle и нового бренда. Не используй отзывы reference app как testimonials. Создай listing.json, screenshot plan, captions, privacy/data-safety evidence, review notes, demo-account instructions, deep-link test case и release notes. Проверь актуальные требования App Store Connect и Play Console перед экспортом и запиши дату проверки.
```

Проверка listing:

```bash
python3 ~/.codex/skills/replica-launch/listing.py replica/launch/listing.json
```

Структура результата:

```text
replica/launch/
├── landing.md
├── pricing.md
├── listing.json
├── launch-plan.md
└── store/
    ├── ios/
    └── android/
```

Store screenshots создаются из брендированной production-like сборки. На них
не должно быть simulator chrome, debug menu, seed labels или чужих assets.

## 16. DEPLOY

Сначала только preflight:

```text
$replica-deploy

Выполни полный preflight, но ничего не публикуй. Проверь parity, bugs, Maestro на iOS/Android, screenshot matrix, brand sweep, store listing, production builds, privacy, account deletion, bundle/package IDs, signing owner и EAS project. Покажи отдельный результат каждого gate и точные внешние действия, для которых потребуется моё подтверждение.
```

Любая ошибка останавливает deploy. Когда всё зелёное, Codex отдельно запросит
разрешение непосредственно перед внешним изменением: production deploy,
настройкой DNS, включением Stripe live, отправкой в TestFlight/Play или store
review.

Для Expo используются явные платформы и профили:

```bash
eas build --platform ios --profile production
eas build --platform android --profile production
```

В TestFlight и Play Internal Testing отправляется конкретная успешная сборка,
а не неоднозначный «последний build». До review нужен smoke test на реальных
устройствах из обоих beta-каналов.

## 17. Как продолжить работу в новом чате

Все этапы обмениваются данными через `replica/`. Поэтому не нужно пересказывать
всю историю. Используйте:

```text
Продолжи Replica for Codex pipeline по артефактам в replica/. Сначала определи последний завершённый gate и незакрытые must-have/S1/S2. Не повторяй завершённые этапы. Предложи следующий $replica-* skill и начни работу, если для неё не требуется новое внешнее разрешение.
```

Для быстрой проверки состояния:

```text
Прочитай replica/recon.md, architecture.md, features.csv, mobile.md, build-log.md, parity.md и bugs.md. Дай status по iOS и Android: последний зелёный gate, отсутствующие evidence pairs, открытые S1/S2 и следующий конкретный шаг. Ничего не изменяй.
```

## 18. Итоговая структура артефактов

```text
replica/
├── recon.md
├── features.csv
├── mobile.md
├── architecture.md
├── schema.sql
├── backend.md
├── build-log.md
├── test-plan.md
├── bugs.md
├── parity.md
├── reviews.csv
├── feedback.md
├── fixes.md
├── brand.md
├── brand.json
├── deploy.md
├── design/
├── screens/
│   ├── ios/<device>/<screen>/<state>.png
│   └── android/<device>/<screen>/<state>.png
├── clone-screens/
│   ├── ios/<device>/<screen>/<state>.png
│   └── android/<device>/<screen>/<state>.png
├── diffs/
│   ├── ios/<device>/<screen>/<state>.{png,json}
│   └── android/<device>/<screen>/<state>.{png,json}
├── test-results/mobile/
│   ├── ios/<flow>/
│   └── android/<flow>/
└── launch/
    └── store/{ios,android}/
```

## 19. Definition of done

Приложение можно считать release candidate, когда:

- все must-have в `features.csv` имеют `yes`;
- обязательные пары iOS/Android screenshot-state существуют;
- layout/behavior diff прошёл согласованные thresholds;
- все core Maestro flows зелёные на обеих платформах;
- нет открытых S1/S2;
- второй пользователь не видит данные первого;
- offline retry не создаёт дубликаты;
- deep links, permissions, background/resume и account deletion проверены;
- rebrand sweep чист;
- store listing lint проходит;
- privacy/data-safety ответы соответствуют реальному поведению сборки;
- TestFlight и Play Internal Testing прошли real-device smoke test;
- пользователь явно подтвердил каждое production/store действие.

До выполнения этих условий слово «готово» означает только завершение текущего
этапа, а не готовность продукта к публикации.

## 20. Частые ошибки

**Codex сразу пишет много экранов.** Верните работу к одному F01 и thin
vertical slice.

**Есть только web preview.** Это не мобильная проверка. Запустите native
development build на заявленных платформах.

**iOS прошёл, Android не запускали.** Android остаётся `unverified`; общий gate
красный.

**Diff сравнивает разные данные или устройства.** Повторите снимки с одинаковым
platform/device/orientation/state contract.

**Layout score повышают копированием цвета и assets.** Остановитесь. Diff
проверяет структуру; бренд обязан быть самостоятельным.

**E2E flaky.** Уберите таймерные ожидания, используйте устойчивые accessibility
labels/testID, детерминированные seed data и независимый reset состояния.

**Секрет попал в чат или Git.** Считайте его скомпрометированным, отзовите у
провайдера и создайте новый. Значения хранятся только в разрешённом secret/env
хранилище.

**Codex собирается отправить build без подтверждения.** Остановите выполнение.
Создание артефакта и внешняя публикация — разные разрешения.
