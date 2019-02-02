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
	@echo "	install the Python requirements from requirements.txt."
	@echo "\nmake clean-pyc"
	@echo "	clean all Python compiled bytecode files."
	@echo "\nmake pywikibot"
	@echo "	CanaryBot is prepared to run on PAWS so it is unnecessary to configure Pywikibot since you configure it in PAWS correctly. But if you want to run CanaryBot outside PAWS (in your local computer) you need to execute this make instruction."

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
	@echo "\nCreating a CSV for the duplicated descriptions"
	echo "id,desc" >> duplicatedFullStopsDesc.csv

install-pyrequirements:
	@echo "\nInstalling all Python requirements from requirements.txt."
	pip install -r requirements.txt

clean-pyc:
	@echo "\nDeleting all Python compiled bytecode files (.pyc and .pyo)."
	find . -name "*.pyc" -exec rm --force {} +
	find . -name "*.pyo" -exec rm --force {} +

pywikibot:
	@echo "\nClonning Pywikibot from its official repository..."
	git clone --recursive https://gerrit.wikimedia.org/r/pywikibot/core.git
	@echo "\nGenerating necessary files when the scripts are going to be out of PAWS"
	python core/generate_user_files.py
	@echo "\nLogging..."
	python core/pwb.py login
	@echo "\nPywikibot has been configured!"
