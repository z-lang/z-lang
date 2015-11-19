
PYTHON = python3
ZLANG = ${PYTHON} main.py
TEMPLATES = src/haskellTemplate.py

.PHONY: all test template clean

all: template

test: template
	@${PYTHON} -m unittest discover -s src -v -p *Test.py

template: ${TEMPLATES}

src/%Template.py: template/%.template
	@echo -n 'template = """' > "$@"
	@cat "$^" >> "$@"
	@echo '"""' >> "$@"

clean:

