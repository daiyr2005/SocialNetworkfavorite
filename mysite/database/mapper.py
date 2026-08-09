def favorite_document_to_response(document: dict):

    return {
        "id": str(document["_id"]),
        "user_id": document["user_id"],
        "created_date": document["created_date"]
    }

def favorite_items_document_to_response(document: dict):
    return {
        "id": str(document["_id"]),
        "favorite": document["favorite"],
        "favorite_name": document["favorite_name"],
        "content": document["content"],
        "created_date": document["created_date"],
        "updated_date": document["updated_date"],
    }