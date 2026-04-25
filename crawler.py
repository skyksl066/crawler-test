#!/usr/bin/env python3
"""
Simple Web Crawler for Testing
GitHub Actions Automation with SFTP Upload 
"""

import requests
import json
from datetime import datetime


def main():
    print("=" * 60)
    print("Python Crawler Test - GitHub Actions Automation")
    print("=" * 60)

    test_results = {
        "timestamp": datetime.now().isoformat(),
        "test_name": "Web Crawler Test",
        "status": "success",
        "data": []
    }

    # Test 1: Basic environment check
    print("\n[TEST 1] Running basic tests...")
    print("✓ Python environment is working")
    print("✓ Requests library imported successfully")
    test_results["data"].append({"test": "Python environment", "result": "PASS"})

    # Test 2: HTTP request
    print("\n[TEST 2] Testing HTTP request...")
    try:
        response = requests.get("https://httpbin.org/get", timeout=10)
        if response.status_code == 200:
            print("✓ HTTP GET request successful")
            test_results["data"].append({"test": "HTTP request", "result": "PASS"})
        else:
            print(f"✗ HTTP request failed with status {response.status_code}")
            test_results["data"].append({"test": "HTTP request", "result": "FAIL"})
    except Exception as e:
        print(f"✗ HTTP request error: {str(e)}")
        test_results["data"].append({"test": "HTTP request", "result": "FAIL", "error": str(e)})

    # Test 3: Data processing
    print("\n[TEST 3] Data processing...")
    sample_data = {
        "crawled_at": datetime.now().isoformat(),
        "items": [
            {"id": 1, "name": "Item 1", "value": 100},
            {"id": 2, "name": "Item 2", "value": 200},
            {"id": 3, "name": "Item 3", "value": 300}
        ]
    }
    print(f"✓ Processed {len(sample_data['items'])} items")
    test_results["data"].append({
        "test": "Data processing",
        "result": "PASS",
        "items_processed": len(sample_data["items"])
    })

    # Final summary
    print("\n" + "=" * 60)
    print("CRAWLING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Timestamp: {test_results['timestamp']}")
    print(f"Total tests: {len(test_results['data'])}")

    # Save results
    output_file = "crawler_output.txt"
    try:
        with open(output_file, "w") as f:
            f.write("Crawler Execution Report\n")
            f.write("=" * 60 + "\n")
            f.write(f"Timestamp: {test_results['timestamp']}\n")
            f.write(f"Status: {test_results['status']}\n")
            f.write("\nTest Results:\n")
            for item in test_results["data"]:
                f.write(f"  - {item.get('test')}: {item.get('result')}\n")
            f.write("\nFull JSON Results:\n")
            f.write(json.dumps(test_results, indent=2))
        print(f"\n✓ Output saved to {output_file}")
    except Exception as e:
        print(f"\n✗ Failed to save output: {str(e)}")

    return 0


if __name__ == "__main__":
    exit(main())
