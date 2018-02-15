all: help

help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make build            - build all images"
	@echo "   1. make pull             - pull all images"
	@echo "   1. make clean            - remove all images"
	@echo ""

build:
	@docker build --tag=keymint/keymint_tools keymint_tools/

pull:
	@docker pull keymint/keymint_tools

clean:
	@docker rmi -f keymint/keymint_tools
