default: help

NAME=imgsrv
VERSION=0.1
RELEASE=0
PWD=$(shell bash -c "pwd -P")
RPMDIST=$(shell rpm --eval '%dist')
RPMTOP=$(PWD)/rpmbuild
SPEC=$(NAME).spec
TARBALL=$(NAME)-$(VERSION)-$(RELEASE).tar.gz
SRPM=$(RPMTOP)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE).src.rpm
# for dev phony
DIST=$(shell bash -c "uname -r")
# Unit tests
TEST_SOURCE=tests
TEST_OUTPUT=$(RPMTOP)/TESTS
TEST_UNIT_FILE=unit-tests.xml
#Sphinx doc
DOC_BUILDDIR=doc/build

help:
	@echo
	@echo "Usage: make <target> where <target> is one of"
	@echo
	@echo "clean       clean temp files from local workspace"
	@echo "codecheck   run code checkers pep8 and pylint"
	@echo "test        run unit tests locally"
	@echo "all         clean test doc rpm"
	@echo

all: clean codecheck 

clean:
	$(RM) $(NAME)*.tar.gz $(SPEC)
	$(RM) -r rpmbuild build doc/build imgsrv.egg-info
	@find -name '*.py[co]' -delete
	make clean -C doc/
	@echo
	
codecheck: 
	@echo "------Starting PEP8 code analysis------"
	find imgsrv/ tests/ -name "*.py" |xargs pep8 --verbose --statistics --count --show-pep8 --exclude=.eggs
	@echo "------Starting Pylint code analysis------"
	find imgsrv/ tests/ -name "*.py" |xargs pylint --rcfile=.pylintrc
	@echo
