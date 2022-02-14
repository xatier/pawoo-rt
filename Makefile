.PHONY: all build push

name = pawoo-rt:latest
image = xatier/$(name)
registry = ghcr.io/xatier

all: build push

build:
	podman build --squash --no-cache -t $(image) .

run:
	podman run --rm -it \
		--name pawoo-rt \
		--env TOKEN=1234 \
		-p 127.0.0.1:5566:5566 \
		$(image)

push:
	podman images $(image)
	podman tag $(shell podman images $(image) -q) $(registry)/$(name)
	podman push $(registry)/$(name)
