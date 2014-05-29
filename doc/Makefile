test: rapid1000.pdf
	open -a preview rapid1000.pdf

rapid1000.html: rapid1000.haml list.txt rapidmag.rb reports.html parser.html rapid1000messages.html rapid1000reports.html
	env STATIC_DIR=../thoustatics ruby rapidmag.rb rapid1000.haml list.txt > rapid1000.html
	env STATIC_DIR=../static ruby rapidmag.rb rapid1000.haml list.txt > ../thoutemplates/rapid1000.html

../thoustatics/stylesheets/rapid1000.css: ../thoustatics/stylesheets/rapid1000.scss
	sass --update ../thoustatics/stylesheets/rapid1000.scss

rapid1000.pdf: rapid1000.html ../thoustatics/stylesheets/rapid1000.css
	prince -o rapid1000.pdf rapid1000.html

rapid1000messages.html: ../thoureport/messages/rapid1000messages.py
	cd .. && pydoc -w thoureport/messages/rapid1000messages.py && mv rapid1000messages.html doc/

rapid1000reports.html: ../thoureport/reports/rapid1000reports.py
	cd .. && pydoc -w thoureport/reports/rapid1000reports.py && mv rapid1000reports.html doc/

reports.html: ../thoureport/reports/reports.py
	cd .. && pydoc -w thoureport/reports/reports.py && mv reports.html doc/

parser.html: ../thoureport/messages/parser.py
	cd .. && pydoc -w thoureport/messages/parser.py && mv parser.html doc/

clean:
	rm -f rapid1000.pdf rapid1000.html ../thoustatics/stylesheets/rapid1000.css
