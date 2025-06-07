docker-build:
	docker build \
		-f Dockerfile.dev \
		--progress=plain \
		.
.PHONY: docker-build
