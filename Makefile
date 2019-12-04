CWD := $(shell pwd)
.PHONY: cohbuilds-test-container
cohbuilds-test-container:
	docker build -f test.Dockerfile -t cohbuilds-test .

.PHONY: cohbuilds-test
test: cohbuilds-test-container
	docker run -v ${CWD}/CohBuildsApi:/cohbuilds -it cohbuilds-test

.PHONY: clean
clean:
	docker rmi -f cohbuilds-test
