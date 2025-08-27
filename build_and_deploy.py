#!/usr/bin/env python3
"""
Build and deployment script for the interview agents.

This script:
1. Installs the interview-agents package
2. Copies it locally to avoid path issues
3. Runs the deployment
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    if isinstance(cmd, str):
        cmd = cmd.split()
    
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    
    return result

def main():
    """Main build and deploy function."""
    # Get the current directory (deployment)
    deployment_dir = Path(__file__).parent
    project_root = deployment_dir.parent
    interview_agents_dir = project_root / "interview-agents"
    local_copy_dir = deployment_dir / "interview-agents-local"
    
    print("🚀 Starting build and deployment process...")
    
    # Step 1: Install interview-agents package
    print("\n📦 Step 1: Installing interview-agents package...")
    try:
        run_command(["poetry", "install"], cwd=interview_agents_dir)
        print("✅ Successfully installed interview-agents dependencies")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install interview-agents: {e}")
        return 1
    
    # Step 2: Copy interview_agents package directly into deployment directory
    print("\n📁 Step 2: Copying interview_agents package into deployment directory...")
    try:
        source_package_dir = interview_agents_dir / "interview_agents"
        target_package_dir = deployment_dir / "interview_agents"
        
        # Remove existing copy if it exists
        if target_package_dir.exists():
            shutil.rmtree(target_package_dir)
        
        # Copy the interview_agents package directly
        def ignore_patterns(dir, files):
            return ['__pycache__', '*.pyc']
        
        shutil.copytree(source_package_dir, target_package_dir, ignore=ignore_patterns)
        print("✅ Successfully copied interview_agents package into deployment directory")
    except Exception as e:
        print(f"❌ Failed to copy interview_agents package: {e}")
        return 1
    
    # Step 3: Update the deployment configuration
    print("\n🔧 Step 3: Updating deployment configuration...")
    try:
        # Update remote.py to remove extra_packages (since package is now local)
        remote_py_path = deployment_dir / "remote.py"
        with open(remote_py_path, 'r') as f:
            content = f.read()
        
        # Remove the extra_packages line entirely
        lines = content.split('\n')
        updated_lines = []
        for line in lines:
            if 'extra_packages=' not in line:
                updated_lines.append(line)
        
        with open(remote_py_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        # Update remote.py import to use local package
        with open(remote_py_path, 'r') as f:
            content = f.read()
        
        # Replace the import path
        content = content.replace(
            'sys.path.insert(0, os.path.join(os.path.dirname(__file__), \'interview-agents-local\'))',
            '# Local package import'
        )
        
        with open(remote_py_path, 'w') as f:
            f.write(content)
        
        # Update pyproject.toml to remove the external dependency
        pyproject_path = deployment_dir / "pyproject.toml"
        with open(pyproject_path, 'r') as f:
            pyproject_content = f.read()
        
        # Remove the interview-agents dependency line
        lines = pyproject_content.split('\n')
        updated_lines = []
        for line in lines:
            if not line.strip().startswith('interview-agents = {path = "../interview-agents"'):
                updated_lines.append(line)
        
        with open(pyproject_path, 'w') as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ Successfully updated deployment configuration")
    except Exception as e:
        print(f"❌ Failed to update deployment configuration: {e}")
        return 1
    
    # Step 4: Regenerate lock file and install deployment dependencies
    print("\n📦 Step 4: Regenerating lock file and installing dependencies...")
    try:
        # First regenerate the lock file
        run_command(["poetry", "lock"], cwd=deployment_dir)
        print("✅ Successfully regenerated lock file")
        
        # Then install dependencies
        run_command(["poetry", "install"], cwd=deployment_dir)
        print("✅ Successfully installed deployment dependencies")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install deployment dependencies: {e}")
        return 1
    
    # Step 5: Run the deployment
    print("\n🚀 Step 5: Running deployment...")
    try:
        run_command(["poetry", "run", "python", "remote.py", "--create"], cwd=deployment_dir)
        print("✅ Deployment completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return 1
    
    print("\n🎉 Build and deployment process completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
