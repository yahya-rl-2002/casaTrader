#!/usr/bin/env python3
"""
Test runner script for the Fear & Greed Index project
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🧪 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Main test runner"""
    print("🚀 Fear & Greed Index - Test Suite")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Test commands
    test_commands = [
        ("python -m pytest tests/unit/ -m unit -v", "Unit Tests"),
        ("python -m pytest tests/integration/ -m integration -v", "Integration Tests"),
        ("python -m pytest tests/ -v --tb=short", "All Tests"),
        ("python -m pytest tests/ --cov=app --cov-report=html --cov-report=term", "Coverage Report"),
    ]
    
    results = []
    
    for command, description in test_commands:
        success = run_command(command, description)
        results.append((description, success))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {description}")
    
    # Overall result
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n🎉 All tests passed successfully!")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())







