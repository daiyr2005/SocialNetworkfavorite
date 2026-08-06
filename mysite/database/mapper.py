def favorite_document_to_response(document: dict):

    return {
        "id": str(document["_id"]),

        "user_id": document["user_id"],

        "items": document.get("items", []),

        "created_date": document["created_date"],

        "update_date": document["update_date"],
    }