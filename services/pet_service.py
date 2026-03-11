from .base_service import BaseService


class PetService(BaseService):
    # End points
    PET_ENDPOINT = "/pet"
    PET_BY_ID_ENDPOINT = "/pet/{pet_id}"
    FIND_BY_STATUS = "/pet/findByStatus"

    def get_pet_by_id(self, pet_id):
        return self.get(self.PET_BY_ID_ENDPOINT.format(pet_id=pet_id))

    def create_pet(self, payload):
        return self.post(self.PET_ENDPOINT, payload)

    def update_pet(self, payload):
        return self.put(self.PET_ENDPOINT, payload)

    def delete_pet(self, pet_id):
        return self.delete(
            self.PET_BY_ID_ENDPOINT.format(pet_id=pet_id)
        )

    def find_pet_by_status(self, status):
        return self.get(self.FIND_BY_STATUS, params={"status": status})
