.PHONY: clean

clean:
	rm -rf html

html:
	mkdir html
	python -c "from src.catalog_utils import dump_html_output; dump_html_output('html')"
