.PHONY: lint format

lint:
	./gradlew spotlessCheck
	./scripts/swiftformat iosApp/iosApp --lint --config .swiftformat
	./scripts/swiftlint lint --config .swiftlint.yml

format:
	./gradlew spotlessApply
	./scripts/swiftformat iosApp/iosApp --config .swiftformat
	./scripts/swiftlint --fix --config .swiftlint.yml
	$(MAKE) lint
