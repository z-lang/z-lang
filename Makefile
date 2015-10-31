
PYTHON = python3
ZLANG = ${PYTHON} src/main.py
TEMPLATES = src/haskellTemplate.py

.PHONY: all verbose test template clean

all: template
	@${ZLANG} -c demo.zl

verbose: template
	@${ZLANG} -tsc demo.zl

test: template
	@${PYTHON} -m unittest discover -s src -v -p *Test.py

template: ${TEMPLATES}

src/%Template.py: template/%.template
	@echo -n 'template = """' >> "$@"
	@cat "$^" >> "$@"
	@echo '"""' >> "$@"

clean:

