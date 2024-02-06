HATCH=hatch
PROJECT_NAME=$(shell ${HATCH} project metadata|jq -r '.name')

all: test

cli test cov help:
	${HATCH} run $@ ${EXTRA}

# XXX always run formatter first to wrap long lines
# https://github.com/pypa/hatch/discussions/1205#discussioncomment-8087562
fmt:
	${HATCH} fmt -f
	${HATCH} fmt
	
mypy:
	${HATCH} run types:check

build:
	${HATCH} build

deploy: mypy build reinstall

reinstall:
	-pipx uninstall "${PROJECT_NAME}"
	pipx install dist/*$$(${HATCH} version)*.whl

try:
	${HATCH} run cli -d \
		-b starship \
		-g https://github.com/starship/starship \
		-a starship-x86_64-unknown-linux-musl.tar.gz

try2:		
	${HATCH} run cli -d \
		-b direnv \
		-g https://github.com/direnv/direnv \
		-a direnv.linux-amd64
