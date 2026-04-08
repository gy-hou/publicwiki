.PHONY: serve build clean install lint new-post deploy help check-venv

VENV ?= .venv
PYTHON ?= python3
VENV_PYTHON := $(VENV)/bin/python
VENV_MKDOCS := $(VENV)/bin/mkdocs
PORT ?= 8000

# 默认目标
help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 创建虚拟环境并安装依赖
	@if [ ! -x "$(VENV_PYTHON)" ]; then \
		$(PYTHON) -m venv $(VENV); \
	fi
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt
	$(VENV_PYTHON) -m pip install mkdocs==1.6.1

check-venv:
	@if [ ! -x "$(VENV_MKDOCS)" ]; then \
		echo "未找到 $(VENV_MKDOCS)，请先执行 make install"; \
		exit 1; \
	fi

serve: check-venv ## 本地预览（热重载，自动避让端口冲突）
	@PORT=$(PORT); \
	while lsof -nP -iTCP:$$PORT -sTCP:LISTEN >/dev/null 2>&1; do \
		PORT=$$((PORT + 1)); \
	done; \
	echo "Starting MkDocs at http://127.0.0.1:$$PORT/openresource-wiki/"; \
	$(VENV_MKDOCS) serve -a 127.0.0.1:$$PORT --open

build: check-venv ## 构建静态站点
	$(VENV_MKDOCS) build --strict

clean: ## 清理构建产物
	rm -rf site/

lint: check-venv ## 检查内容健康度
	$(VENV_PYTHON) scripts/lint_content.py --docs-dir docs/

new-post: ## 创建新博客文章 (usage: make new-post TITLE="文章标题")
	@if [ -z "$(TITLE)" ]; then echo "Usage: make new-post TITLE=\"文章标题\""; exit 1; fi
	@DATE=$$(date +%Y-%m-%d); \
	SLUG=$$(echo "$(TITLE)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-'); \
	FILE="docs/blog/posts/$${DATE}-$${SLUG}.md"; \
	echo "---" > $$FILE; \
	echo "date: $${DATE}" >> $$FILE; \
	echo "authors:" >> $$FILE; \
	echo "  - gy-hou" >> $$FILE; \
	echo "categories:" >> $$FILE; \
	echo "  - 待分类" >> $$FILE; \
	echo "tags:" >> $$FILE; \
	echo "  - 待填写" >> $$FILE; \
	echo "---" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "# $(TITLE)" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "<!-- more -->" >> $$FILE; \
	echo "" >> $$FILE; \
	echo "正文内容..." >> $$FILE; \
	echo "Created: $$FILE"

deploy: check-venv ## 手动部署（通常用 CI 自动部署）
	$(VENV_MKDOCS) gh-deploy --force
