docker-build:
	docker build \
		-f Dockerfile.dev \
		--progress plain \
		--no-cache \
		.
.PHONY: docker-build
