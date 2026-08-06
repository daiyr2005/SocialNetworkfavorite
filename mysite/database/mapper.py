def glovo_document_to_response(document: dict):
    return {
        "id": str(document["_id"]),

        "user_id": document["user_id"],

        "store_id": document["store_id"],
        "store_name": document["store_name"],

        "product_id": document["product_id"],
        "product_name": document["product_name"],

        "quantity": document["quantity"],

        "price": document["price"],
        "total_price": document["total_price"],

        "address": document["address"],

        "status": document["status"],

        "created_date": document["created_date"],
        "update_date": document["update_date"]
    }