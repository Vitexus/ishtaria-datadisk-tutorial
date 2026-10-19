# Local development of the tutorial datadisk
#
#   make test      validate the datadisk
#   make stage     stage for local testing
#   make server    start local server with this datadisk
#   make stop      stop that server
#   make logs      follow its log
#   make clean     remove build/ and stop server

SHELL := /bin/bash
DEV_DB ?= ishtaria_tutorial_dev
SEED ?= 12345
SERVER_DIR := ../ishtaria-server
PGM := ../ishtaria-worldgen/examples/planet-seed12345-256.pgm
BUILD := $(CURDIR)/build
STAGE := $(BUILD)/datadisks
DB_URL := postgresql:///$(DEV_DB)?host=/var/run/postgresql

.PHONY: test stage server start stop logs clean

test:
	python3 ../ishtaria-protocol/tests/validate_datadisk.py .

stage:
	rm -rf $(STAGE)/tutorial
	mkdir -p $(STAGE)/tutorial
	cp -a datadisk.yaml places npcs dialogues quests i18n music media $(STAGE)/tutorial/
	@echo "staged tutorial datadisk"

$(BUILD)/server.toml:
	mkdir -p $(BUILD)
	sed -e 's|^listen = .*|listen = "127.0.0.1:7400"|' -e 's|^server_name = .*|server_name = "localhost"|' \
	    -e 's|^database_url = .*|database_url = "$(DB_URL)"|' $(SERVER_DIR)/etc/server.toml > $@

server: stage stop start

start: $(BUILD)/server.toml
	psql -lqt postgres | cut -d'|' -f1 | grep -qw $(DEV_DB) || createdb $(DEV_DB)
	cd $(SERVER_DIR) && cargo build --locked
	@first=""; \
	if [ "$$(psql -tA $(DEV_DB) -c "select to_regclass('worlds') is not null and exists(select 1 from worlds)" 2>/dev/null)" != "t" ]; then \
	  first="--import $(abspath $(PGM)) --seed $(SEED) --datadisk tutorial"; echo "creating the world in $(DEV_DB)"; fi; \
	cd $(SERVER_DIR) && ISHTARIA_DATADISK_DIR=$(STAGE) DATABASE_URL='$(DB_URL)' \
	  nohup ./target/debug/ishtaria-server $(BUILD)/server.toml $$first > $(BUILD)/server.log 2>&1 & echo $$! > $(BUILD)/server.pid
	@for i in $$(seq 1 40); do curl -sf http://127.0.0.1:7400/health >/dev/null && { echo "server up: http://127.0.0.1:7400"; exit 0; }; sleep 0.5; done; \
	  echo "server did not come up, see $(BUILD)/server.log"; tail -20 $(BUILD)/server.log; exit 1

stop:
	@pkill -f '[i]shtaria-server $(BUILD)/server.toml' || true
	@rm -f $(BUILD)/server.pid
	@sleep 1

logs:
	tail -f $(BUILD)/server.log

clean: stop
	rm -rf $(BUILD)
