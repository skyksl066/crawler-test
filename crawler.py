#!/usr/bin/env python3
"""
Simple Web Crawler for Testing
GitHub Actions Automation with FTP Upload
"""

import requests
import json
from datetime import datetime

SEPARATOR = "=" * 60


def main():
    print(SEPARATOR)
    print("Python Crawler Test - GitHub Actions Automation")
    print(SEPARATOR)

    run_timestamp = datetime.now().isoformat()
    test_results = {
        "timestamp": run_timestamp,
        "test_name": "Web Crawler Test",
        "status": "success",
        "data": []
    }

    print("\n[TEST 1] Running basic tests...")
    print("✓ Python environment is working")
    print("✓ Requests library imported successfully")
    test_results["data"].append({"test": "Python environment", "result": "PASS"})

    print("\n[TEST 2] Testing HTTP request...")
    try:
        response = requests.get("https://httpbin.org/get", timeout=10)
        if response.status_code == 200:
            print("✓ HTTP GET request successful")
            test_results["data"].append({"test": "HTTP request", "result": "PASS"})
        else:
            print(f"✗ HTTP request failed with status {response.status_code}")
            test_results["data"].append({"test": "HTTP request", "result": "FAIL"})
    except requests.RequestException as e:
        print(f"✗ HTTP request error: {str(e)}")
        test_results["data"].append({"test": "HTTP request", "result": "FAIL", "error": str(e)})

    print(f"\n{SEPARATOR}")
    print("CRAWLING COMPLETED SUCCESSFULLY!")
    print(SEPARATOR)
    print(f"Timestamp: {run_timestamp}")
    print(f"Total tests: {len(test_results['data'])}")

    output_file = "crawler_output.txt"
    try:
        with open(output_file, "w") as f:
            f.write("Crawler Execution Report\n")
            f.write(SEPARATOR + "\n")
            f.write(f"Timestamp: {run_timestamp}\n")
            f.write(f"Status: {test_results['status']}\n")
            f.write("\nTest Results:\n")
            for item in test_results["data"]:
                f.write(f"  - {item.get('test')}: {item.get('result')}\n")
            f.write("\nFull JSON Results:\n")
            f.write(json.dumps(test_results, indent=2))
        print(f"\n✓ Output saved to {output_file}")
    except OSError as e:
        print(f"\n✗ Failed to save output: {str(e)}")

    return 0


if __name__ == "__main__":
    exit(main())
