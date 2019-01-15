LOGS = "logs/logs.html"
JS = "logs/js"
CSVTOHTMLTABLE = "csv_to_html_table.js"

.DEFAULT: help
help:
	@echo "Available commands:"
	@echo "\nmake all"
	@echo "	prepare the necessary files, install the Python requirements and clean all Python compiled bytecode files."
	@echo "\nmake prepare-files"
	@echo "	prepare the necessary files to work."
	@echo "\nmake install-pyrequirements"
	@echo " install the Python requirements from requirements.txt."
	@echo "\nmake clean-pyc"
	@echo "	clean all Python compiled bytecode files."

all: prepare-files prepare-files prepare-duplicatedcsv install-pyrequirements clean-pyc
	@echo "\nCanaryBot has been prepared and configured."

prepare-files:
	@echo "You are preparing all the necessary requirements to"
	@echo "work with CanaryBot in your system."
	echo "<ul>" > ${LOGS}
	echo "</ul>" >> ${LOGS}
	@echo "\nContent of ${LOGS}"
	cat ${LOGS}
	@echo "\nCreating the ${JS} folder"
	mkdir ${JS}
	@echo "\nDownloading CSV to HTML Table in the correct locationt (${CSVTOHTMLTABLE})."
	curl -o ${JS}/${CSVTOHTMLTABLE} https://raw.githubusercontent.com/derekeder/csv-to-html-table/master/js/csv_to_html_table.js

prepare-duplicatedcsv:
	@echo "\nWritting a CSV with the header 'id' and 'duplicated'"
	echo "id, sentence" >> duplicatedFullStopsDesc.csv

install-pyrequirements:
	@echo "\nInstalling all Python requirements from requirements.txt."
	pip install -r requirements.txt

clean-pyc:
	@echo "\nDeleting all Python compiled bytecode files (.pyc and .pyo)."
	find . -name "*.pyc" -exec rm --force {} +
	find . -name "*.pyo" -exec rm --force {} +
