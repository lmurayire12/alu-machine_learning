#!/usr/bin/env python3
"""Script that provides stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # 1. Total logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # 2. Method stats
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")

    # 3. Status check
    status_check_count = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_check_count} status check")

