
all: update_from

init:
	pylint --generate > .pylintrc
	sed -i 's/output-format=text/output-format=colorized/g' .pylintrc
	#output-format=text

requi:
	pip3 freeze requirements.txt



auto_formater:
	pre-commit run --all-files -c .pre-commit-config.yaml
