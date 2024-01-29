.PHONY: build

test:
	@pants test ::

lint:
	@pants lint ::

fmt:
	@pants fmt ::

build:
	@pants package ::

check:
	@pants check ::

clean:
	@rm -rf dist/ .pids/ .pants.d/