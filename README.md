# Deployment Infrastructure

This repository contains deployment scripts and utilities for the Interview Platform, including:

- **Local Deployment**: Scripts for local testing and development
- **Remote Deployment**: Scripts for deploying to Google Cloud Platform
- **Cleanup Utilities**: Tools for cleaning up deployed resources
- **Deployment Orchestration**: Python scripts for managing deployments

## Features

- **Local Testing**: Test deployments locally before pushing to production
- **Cloud Deployment**: Automated deployment to Google Cloud Run
- **Resource Management**: Create, manage, and clean up cloud resources
- **Infrastructure as Code**: Terraform configurations for consistent deployments

## Prerequisites

- Google Cloud CLI (`gcloud`) installed and authenticated
- Python 3.12+
- Poetry for dependency management
- Access to existing Terraform infrastructure (managed separately)

## Quick Start

### Local Testing
```bash
poetry run python local.py --create_session
```

### Remote Deployment
```bash
poetry run python remote.py --create
```

### Cleanup
```bash
poetry run python cleanup.py --resource_id=your-resource-id
```

## Project Structure

```
deployment/
├── local.py          # Local deployment and testing scripts
├── remote.py         # Remote cloud deployment scripts
├── cleanup.py        # Resource cleanup utilities
└── README.md         # This file
```

## Integration

This deployment infrastructure is designed to work with:
- **interview-agents**: ADK agent system
- **ingest-google-interview**: Data ingestion service
- **python-runner-service**: Algorithm debugging service
- **firebase-dashboard**: Frontend application
- **terraform**: Infrastructure management (separate submodule)

## License

Part of the Interview Platform suite.
