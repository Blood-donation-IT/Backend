SHELL := /bin/bash
ROOT_DIR := $(shell git rev-parse --show-toplevel 2>/dev/null || echo .)

proto:
	@echo "Running protobuf generator..."
	@cd "$(ROOT_DIR)" && py -3 scripts/contracts/services/authorization/generate_proto.py $(MYPY)
