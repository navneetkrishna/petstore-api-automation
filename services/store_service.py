from services.base_service import BaseService

class StoreService(BaseService):
    """API client for the /store domain.

    Endpoint reference:
        GET    /store/inventory          — Returns pet inventories by status
        POST   /store/order              — Place an order for a pet
        GET    /store/order/{orderId}    — Find purchase order by ID
        DELETE /store/order/{orderId}    — Delete purchase order by ID
    """



    INVENTORY_ENDPOINT  = "/store/inventory"
    ORDER_ENDPOINT      = "/store/order"
    ORDER_BY_ID         = "/store/order/{order_id}"

    def get_inventory(self):
        return self.get(self.INVENTORY_ENDPOINT)

    def place_order(self, payload):
        return self.post(self.ORDER_ENDPOINT, payload)

    def get_order_by_id(self, order_id):
        return self.get(
            self.ORDER_BY_ID.format(order_id=order_id)
        )

    def delete_order(self, order_id):
        return self.delete(
            self.ORDER_BY_ID.format(order_id=order_id)
        )