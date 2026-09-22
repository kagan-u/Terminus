.PHONY: help sim anim tui build benchmark config hash banner ultra list test testjs install clean

help:
	@echo ""
	@echo "  TERMINUS - available commands"
	@echo "  " + "=============================="
	@echo "  make sim        run interactive simulator"
	@echo "  make build      live build simulation"
	@echo "  make tui        interactive terminal UI"
	@echo "  make anim       terminal animation"
	@echo "  make benchmark  run performance benchmarks"
	@echo "  make config     compare all versions"
	@echo "  make ultra      list ultra versions"
	@echo "  make hash       verify Terminus.zip integrity"
	@echo "  make banner     print ascii banner"
	@echo "  make chart      generate matplotlib charts"
	@echo "  make video      generate video"
	@echo "  make test       run python tests"
	@echo "  make testjs     run javascript tests"
	@echo "  make install    install python package"
	@echo "  make clean      remove generated files"
	@echo ""

sim:
	python3 terminus_sim.py

build:
	python3 terminus_build.py

tui:
	python3 terminus_tui.py

anim:
	python3 terminus_anim.py

benchmark:
	python3 terminus_benchmark.py

config:
	python3 terminus_config.py

ultra:
	python3 terminus_ultra.py --list

hash:
	python3 terminus_hash.py

banner:
	python3 terminus_banner.py

chart:
	python3 terminus_graph.py

video:
	python3 terminus_video.py

test:
	python3 -m pytest tests/ -v

testjs:
	node tests/test.js

install:
	pip install -e .

clean:
	rm -rf __pycache__ tests/__pycache__ src/__pycache__ src/*/__pycache__
	rm -rf terminus_charts terminus_frames terminus_interactive
	rm -rf *.egg-info dist build
