def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    The average score is computed from the topics field,
    and returned with the key 'averageScore' for each student.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        { "$sort": { "averageScore": -1 } }
    ]
    return list(mongo_collection.aggregate(pipeline))

