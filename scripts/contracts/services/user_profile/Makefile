SHELL := /bin/bash
ROOT_DIR := $(shell git rev-parse --show-toplevel 2>/dev/null || echo .)

proto:
	@echo "🚀 Running protobuf generator..."
	@python $(ROOT_DIR)/scripts/contracts/services/user_profile/generate_proto.py $(MYPY)