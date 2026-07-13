.PHONY: lint format install-hooks python-lint python-typecheck python-test generate-openapi

lint:
	./gradlew spotlessCheck
	./scripts/swiftformat iosApp/iosApp --lint --config .swiftformat
	./scripts/swiftlint lint --config .swiftlint.yml
	$(MAKE) python-lint

format:
	./gradlew spotlessApply
	./scripts/swiftformat iosApp/iosApp --config .swiftformat
	./scripts/swiftlint --fix --config .swiftlint.yml
	uv --directory backend run ruff format .
	$(MAKE) lint

install-hooks:
	git config core.hooksPath .githooks

python-lint:
	uv --directory backend run ruff format --check .
	uv --directory backend run ruff check .

python-typecheck:
	uv --directory backend run ty check

python-test:
	uv --directory backend run pytest

generate-openapi:
	uv --directory backend run python scripts/generate_openapi.py --output openapi.json
