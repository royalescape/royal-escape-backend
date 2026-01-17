from bson import ObjectId
from datetime import datetime


def serialize_mongo(doc: dict | None) -> dict | None:
    if not doc:
        return None

    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, list):
            serialized[key] = [
                serialize_mongo(v) if isinstance(v, dict) else v for v in value
            ]
        else:
            serialized[key] = value

    return serialized


def serialize_mongo_list(docs: list[dict]) -> list[dict]:
    return [serialize_mongo(doc) for doc in docs]
