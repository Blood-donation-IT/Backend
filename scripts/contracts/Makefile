ROOT_DIR := $(shell git rev-parse --show-toplevel)
PROTO_SRC := $(ROOT_DIR)/api-specs
PROTO_OUT := $(ROOT_DIR)/contracts/src/contracts

proto:
	mkdir -p $(PROTO_OUT)/user
	touch $(PROTO_OUT)/__init__.py
	touch $(PROTO_OUT)/user/__init__.py
	python -m grpc_tools.protoc \
		-I=$(PROTO_SRC) \
		--python_out=$(PROTO_OUT) \
		--grpc_python_out=$(PROTO_OUT) \
		$(PROTO_SRC)/user/*.proto