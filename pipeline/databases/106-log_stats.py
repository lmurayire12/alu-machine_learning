#!/usr/bin/env python3
"""Script that provides stats about Nginx logs stored in MongoDB, with IP stats"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    # Total logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Method stats
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({'method': method})
        print(f"\tmethod {method}: {count}")

    # Status check
    status_check_count = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_check_count} status check")

    # Top 10 IPs
    print("IPs:")
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

