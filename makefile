LOGS = "logs/logs.html"

.DEFAULT: help
help:
	@echo "make prepare-files"
	@echo "	prepare the necessary files to work"

all: prepare-files prepare-files install-pyrequirements clean-pyc
	@echo "CanaryBot has been prepared and configured."

prepare-files:
	@echo "You are preparing all the necessary requirements to"
	@echo "work with CanaryBot in your system."
	echo "<ul>" > ${LOGS}
	echo "</ul>" >> ${LOGS}
	@echo "Content of ${LOGS}"
	cat ${LOGS}

install-pyrequirements:
	@echo "Installing all Python requirements from requirements.txt"
	pip install -r requirements.txt

clean-pyc:
	@echo "Deleting all Python compiled bytecode files (.pyc and .pyo)"
	find . -name "*.pyc" -exec rm --force {} +
	find . -name "*.pyo" -exec rm --force {} +
