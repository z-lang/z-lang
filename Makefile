
PYTHON = python3
ZLANG = PYTHONPATH="gen"; ${PYTHON} src/main.py
TEMPLATES = gen/haskellTemplate.py

.PHONY: all verbose test template clean

all: template
	@${ZLANG} -c demo.zl

verbose: template
	@${ZLANG} -tsc demo.zl

test: template
	@PYTHONPATH="src:gen"; \
	${PYTHON} -m unittest discover -s test -v -p *Test.py

template: gen ${TEMPLATES}

gen/%Template.py: template/%.template
	@echo -n 'template = """' >> "$@"
	@cat "$^" >> "$@"
	@echo '"""' >> "$@"

gen:
	mkdir gen

clean:
	@rm -rf gen

