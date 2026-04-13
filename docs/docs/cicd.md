# ⚙️ CI Setup Guide

## GitLab CI/CD Configuration

Here's a clean, corrected version of your section with proper formatting and clarity:

### Prerequisites

Before running the CI/CD pipeline, add the following secrets to your **GitLab project settings** under **Settings → CI/CD → Variables**:

- `HF_TOKEN`
- `HF_USERNAME`
- `GIT_USERNAME`
- `GIT_USER_EMAIL`

### CI/CD Pipeline

Our GitLab CI pipeline automatically runs on pushes and merge requests to ensure code quality and security:

- **Code Quality:** Ruff linting and formatting checks
- **Testing:** Unit tests with pytest
- **Security:** Gitleaks secret detection
- **Continuous Delivery**: Manual deployment to Hugging Face Spaces via web trigger for production releases

The full pipeline (quality checks + deployment) can be triggered manually through GitLab's web interface for complete end-to-end delivery.

### Local Testing

Use `gitlab-ci-local` to test GitLab CI pipelines locally before pushing. See `gitlabci.mk` for installation and usage instructions.

## CI/CD Worklow

![DataGen Workflow](https://github.com/lisekarimi/datagen/blob/main/assets/cicd.png?raw=true)
