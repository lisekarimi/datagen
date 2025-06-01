# GitLab CI Local Testing Commands
# 
# Prerequisites:
#   1. Install WSL2 with Ubuntu:
#      - PowerShell (Admin): wsl --install
#      - Restart computer
#      - Open Ubuntu app, create user
#   
#   2. Enable Docker Desktop WSL Integration:
#      - Docker Desktop → Settings → Resources → WSL Integration
#      - Enable "Ubuntu" ✅
#      - Apply & Restart
#   
#   3. Install gitlab-ci-local in WSL Ubuntu:
#      - sudo wget -O /etc/apt/sources.list.d/gitlab-ci-local.sources https://gitlab-ci-local-ppa.firecow.dk/gitlab-ci-local.sources
#      - sudo apt-get update && sudo apt-get install gitlab-ci-local make
#      - sudo usermod -aG docker $USER && newgrp docker
#
#   4. Navigate to project in WSL:
#      - cd /mnt/c/path/to/your/project
#

# Usage:
#  1. Open WSL Ubuntu App 
#  2. Navigate to your project directory 
#     cd /mnt/c/path/to/your/project 
# 		cd /mnt/c/Users/synch/Dropbox/pro/projects/portfolio/datagen
#  3. Run make commands to test GitLab CI jobs locally
#     Example: make -f gitlabci.mk <target>


# All required environment variables are defined in the .env file
include .env
export

# =====================================
# 🛠️ All jobs
# =====================================

test-list-all:		## List all jobs
	gitlab-ci-local --list


# =====================================
# 🔄 Continuous Integration
# =====================================

test-lint:		## Test linting job only
	gitlab-ci-local --file ci/lint.yml

test-security:		## Test security scan job only
	gitlab-ci-local --file ci/scan.yml

test-unit:		## Test unit tests job only
	gitlab-ci-local --file ci/test.yml


# =====================================
# 🚀 Deployment Testing
# =====================================

test-deploy:		## Test deployment pipeline locally
	export $$(grep -v '^#' .env | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$$//' | xargs) > /dev/null 2>&1 && gitlab-ci-local --file ci/deploy.yml deploy_to_huggingface --variable GIT_USERNAME=$$GIT_USERNAME --variable GIT_USER_EMAIL=$$GIT_USER_EMAIL --variable HF_USERNAME=$$HF_USERNAME --variable HF_TOKEN=$$HF_TOKEN


# =====================================
# 🛠️ Utilities
# =====================================

check-docker:		## Check Docker integration works
	docker --version && docker ps


# =====================================
# 📚 Documentation & Help
# =====================================

help: ## Show this help message
	@echo Available commands:
	@echo.
	@python3 -c "import re; lines=open('gitlabci.mk', encoding='utf-8').readlines(); targets=[re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$',l) for l in lines]; [print(f'  make {m.group(1):<20} {m.group(2)}') for m in targets if m]"


# =======================
# 🎯 PHONY Targets
# =======================

.PHONY: $(shell python3 -c "import re; print(' '.join(re.findall(r'^([a-zA-Z_-]+):\s*.*?##', open('gitlabci.mk', encoding='utf-8').read(), re.MULTILINE)))")