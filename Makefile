PROJECT = sns_to_pubsub
VIRTUAL_ENV = py_venv

install: virtual
build: virtual clean_package build_package_temp copy_python remove_unused zip

virtual:
	if ! [ -d $(VIRTUAL_ENV) ]; then \
	  virtualenv $(VIRTUAL_ENV) -p python3.7; \
	  source ./$(VIRTUAL_ENV)/bin/activate; \
	  pip3 install -r ./$(PROJECT)/requirements.txt; \
	fi

clean_package:
	rm -rf ./package/*

build_package_temp:
	mkdir -p ./package/tmp/lib;
	cp -rf ./$(PROJECT)/. ./package/tmp/;

copy_python:
	if [ -d $(VIRTUAL_ENV)/lib ]; then \
	  cp -rf $(VIRTUAL_ENV)/lib/python3.7/site-packages/. ./package/tmp/; \
	fi

	if [ -d $(VIRTUAL_ENV)/lib64 ]; then \
	  cp -rf $(VIRTUAL_ENV)/lib64/python3.7/site-packages/. ./package/tmp/; \
	fi

remove_unused:
	rm -rf ./package/tmp/wheel*;
	rm -rf ./package/tmp/easy-install*;
	rm -rf ./package/tmp/setuptools*

zip:
	cd ./package/tmp && zip -r ../$(PROJECT).zip .

run:
	docker build -t lambda-image .
	docker run --rm -it -v ${PWD}/package:/src/package lambda-image  make build
