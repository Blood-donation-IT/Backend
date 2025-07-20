
ROOT_DIR := $(shell git rev-parse --show-toplevel)
PROTO_DIR := $(ROOT_DIR)/api-specs/user
OUTPUT_DIR := $(ROOT_DIR)/services/user-profile/src/protos
PROTO_FILE := $(PROTO_DIR)/user-profile.proto

proto:
	@mkdir -p $(OUTPUT_DIR)
	@echo "Generating gRPC files from $(PROTO_FILE)..."
	python -m grpc_tools.protoc \
		-I=$(ROOT_DIR)/api-specs \
		--python_out=$(OUTPUT_DIR) \
		--grpc_python_out=$(OUTPUT_DIR) \
		--mypy_out=$(OUTPUT_DIR) \
		$(PROTO_FILE)
	@echo "Done. Files generated in $(OUTPUT_DIR)."

clean:
	@echo "Cleaning up generated files..."
	find $(OUTPUT_DIR) -type f -name "*.py" ! -name "__init__.py" -delete
	@echo "Done."

rebuild: clean proto