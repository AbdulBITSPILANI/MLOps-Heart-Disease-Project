# GitHub Actions CI/CD Workflow

This directory contains the CI/CD pipeline configuration for the MLOps project.

## Workflow File

- `ci_cd.yml`: Complete CI/CD pipeline with linting, testing, training, and Docker build

## Workflow Overview

The pipeline runs on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger (workflow_dispatch)

## Pipeline Stages

### 1. Lint Job
- **Purpose**: Code quality checks
- **Steps**:
  - Checkout code
  - Setup Python 3.9
  - Install Black and Flake8
  - Run Black (code formatting check)
  - Run Flake8 (linting)

### 2. Test Job
- **Purpose**: Unit testing and coverage
- **Steps**:
  - Checkout code
  - Setup Python 3.9
  - Install dependencies
  - Run pytest with coverage
  - Upload coverage reports to Codecov

### 3. Train Job
- **Purpose**: Model training validation
- **Dependencies**: Requires lint and test jobs to pass
- **Steps**:
  - Checkout code
  - Setup Python 3.9
  - Install dependencies
  - Download dataset
  - Train models
  - Validate model artifacts
  - Upload model artifacts

### 4. Docker Build Job
- **Purpose**: Container build and validation
- **Dependencies**: Requires train job to complete
- **Steps**:
  - Checkout code
  - Setup Docker Buildx
  - Download model artifacts
  - Build Docker image
  - Test Docker container (health check)

### 5. Summary Job
- **Purpose**: Pipeline status summary
- **Runs**: Always (even if other jobs fail)

## Artifacts

### Model Artifacts
- Uploaded from train job
- Includes: `models/` directory and `mlruns/` directory
- Retention: 7 days
- Used by: Docker build job

## Viewing Workflow Runs

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select a workflow run
4. View individual job logs
5. Download artifacts if needed

## Local Testing

Test workflow components locally:

### Linting
```bash
black --check src/ tests/
flake8 src/ tests/ --max-line-length=120
```

### Testing
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Training
```bash
python src/data/download_data.py
python src/models/train.py
```

### Docker Build
```bash
docker build -t heart-disease-api .
docker run -d -p 8000:8000 --name test-api heart-disease-api
sleep 10
curl http://localhost:8000/health
docker stop test-api && docker rm test-api
```

## Customization

### Add New Jobs
Edit `.github/workflows/ci_cd.yml`:

```yaml
new-job:
  name: New Job Name
  runs-on: ubuntu-latest
  needs: [test]
  steps:
    - uses: actions/checkout@v3
    # ... your steps
```

### Change Python Version
Update the `python-version` in setup-python actions:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'  # Change here
```

### Add Deployment Step
Add deployment job after Docker build:
```yaml
deploy:
  name: Deploy to Kubernetes
  runs-on: ubuntu-latest
  needs: [docker-build]
  steps:
    - uses: actions/checkout@v3
    # ... deployment steps
```

## Environment Variables

Set secrets in GitHub repository settings:
- Go to Settings → Secrets and variables → Actions
- Add repository secrets as needed

Example secrets:
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password
- `KUBECONFIG`: Kubernetes config (base64 encoded)

## Troubleshooting

### Workflow fails on linting
- Run Black locally: `black src/ tests/`
- Fix Flake8 issues: `flake8 src/ tests/`

### Tests fail in CI but pass locally
- Check Python version matches
- Verify all dependencies are in requirements.txt
- Check for environment-specific issues

### Docker build fails
- Verify Dockerfile syntax
- Check if model artifacts are available
- Test Docker build locally

### Artifacts not available
- Check artifact upload step completed
- Verify artifact retention settings
- Check download step in dependent job

## Best Practices

1. **Fail Fast**: Lint and test early in pipeline
2. **Parallel Jobs**: Run independent jobs in parallel
3. **Artifact Management**: Upload and download artifacts efficiently
4. **Caching**: Use GitHub Actions cache for dependencies
5. **Secrets**: Never commit secrets, use GitHub Secrets
6. **Status Badges**: Add workflow status badge to README

## Status Badge

Add to README.md:
```markdown
![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/CD%20Pipeline/badge.svg)
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

