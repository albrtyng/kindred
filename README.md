# Kindred

This is a Kotlin Multiplatform project targeting Android, iOS.

* [/iosApp](./iosApp/iosApp) contains an iOS application. Even if you’re sharing your UI with Compose Multiplatform,
  you need this entry point for your iOS app. This is also where you should add SwiftUI code for your project.

* [/shared](./shared/src) is for code that will be shared across your Compose Multiplatform applications.
  It contains several subfolders:
  - [commonMain](./shared/src/commonMain/kotlin) is for code that’s common for all targets.
  - Other folders are for Kotlin code that will be compiled for only the platform indicated in the folder name.
    For example, if you want to use Apple’s CoreCrypto for the iOS part of your Kotlin app,
    the [iosMain](./shared/src/iosMain/kotlin) folder would be the right place for such calls.
    Similarly, if you want to edit the Desktop (JVM) specific part, the [jvmMain](./shared/src/jvmMain/kotlin)
    folder is the appropriate location.

### Running the apps

Use the run configurations provided by the run widget in your IDE's toolbar. You can also use these commands and options:

- Android app: `./gradlew :androidApp:assembleDebug`
- iOS app: open the [/iosApp](./iosApp) directory in Xcode and run it from there.

### Running tests

Use the run button in your IDE's editor gutter, or run tests using Gradle tasks:

- Android tests: `./gradlew :shared:testAndroidHostTest`
- iOS tests: `./gradlew :shared:iosSimulatorArm64Test`
- Backend tests: `make python-test`

### Backend API

The [`backend`](./backend) directory contains the Python 3.13 FastAPI service. It uses `uv` to
manage locked dependencies, `pytest` for unit and integration tests, Ruff for formatting and
linting, and Ty for type checking.

- Start the API: `uv --directory backend run uvicorn kindred_api.main:app --reload`
- Run backend formatting and lint checks: `make python-lint`
- Run backend type checks: `make python-typecheck`
- Generate the OpenAPI artifact: `make generate-openapi`

### Branch naming

Feature branches must follow `<type>/KIN-<number>-<description>`, where `type` is one of `feat`,
`fix`, `ci`, `chore`, `docs`, `refactor`, or `test`. For example:
`feat/KIN-15-scaffold-fastapi-backend`.

### Code quality

Formatting and linting commands require macOS with `curl`, `shasum`, and `unzip`; these are included with macOS.
SwiftLint requires a full Xcode installation, not only the Command Line Tools.
The wrapper automatically uses `/Applications/Xcode.app` when `DEVELOPER_DIR` is not set.
Xcode is also required to build or run the iOS app.

- Check all formatting and Swift lint rules: `make lint`
- Apply formatting and SwiftLint fixes, then recheck: `make format`
- Enable the pre-commit lint hook once per checkout after cloning or switching branches: `make install-hooks`
- Check Kotlin formatting only: `./gradlew spotlessCheck`
- Apply Kotlin formatting only: `./gradlew spotlessApply`

The Swift wrappers download pinned official macOS releases of SwiftFormat and SwiftLint on first use.
Downloads are SHA-256 checksum-verified and cached in `$HOME/Library/Caches/kindred-tools` by default.
Set `KINDRED_TOOLS_DIR` to choose another cache location; CI should cache that directory between jobs.

---

Learn more about [Kotlin Multiplatform](https://www.jetbrains.com/help/kotlin-multiplatform-dev/get-started.html)…
