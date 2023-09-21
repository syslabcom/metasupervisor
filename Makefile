include Makefile.config

.PHONY: all
all: etc/supervisord.conf links

bin:
	mkdir -p bin

etc:
	mkdir -p etc

var/log:
	mkdir -p var/log

var/run:
	mkdir -p var/run

.venv/bin/pip3:
	@echo "Creating a virtualenv using $$(which python${PYTHON_VERSION})"
	$$(which python${PYTHON_VERSION}) -m venv .venv

.venv/bin/supervisord: .venv/bin/pip3 requirements.txt var/log var/run
	./.venv/bin/pip3 install -IUr requirements.txt

etc/supervisord.conf: etc .venv/bin/pip3 scripts/generate_supervisord_conf.py
	./.venv/bin/python ./scripts/generate_supervisord_conf.py ${SUPERVISORD_PORT} ${SUPERVISORD_PASSWORD}

bin/supervisord: bin var/log var/run .venv/bin/supervisord

.PHONY: links
links: .venv/bin/supervisord bin
	@if [ ! -L bin/supervisord ]; then ln -s ../.venv/bin/supervisord bin/supervisord; fi
	@if [ ! -L bin/supervisorctl ]; then ln -s ../.venv/bin/supervisorctl bin/supervisorctl; fi
