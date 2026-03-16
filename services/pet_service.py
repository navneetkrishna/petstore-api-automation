from .base_service import BaseService


class PetService(BaseService):
    """API client for the /pet domain.

    Endpoint reference:
        POST   /pet                          — Create a new pet
        PUT    /pet                          — Update an existing pet
        GET    /pet/findByStatus?status=X    — Find pets by status
        GET    /pet/{petId}                  — Get pet by ID
        POST   /pet/{petId}                  — Update pet with form data
        DELETE /pet/{petId}                  — Delete a pet
        POST   /pet/{petId}/uploadFile       — Upload a pet image
    """
    # End points
    PET_BY_ID_ENDPOINT = "/pet/{pet_id}"
    PET_ENDPOINT       = "/pet"
    FIND_BY_STATUS     = "/pet/findByStatus"


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

    def find_by_status(self, status):
        return self.get(self.FIND_BY_STATUS, params={"status": status})
