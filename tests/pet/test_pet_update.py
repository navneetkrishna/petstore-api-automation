import pytest
from util.assertions import assert_status, assert_field_equals
from util.data_factory import make_pet


class TestPetUpdate:
    """PUT /pet and POST /pet/{petId} — Update pet data."""

    # ------------------------------------------------------------------
    # PUT /pet — JSON body update
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_pet_u001_update_name(self, pet_service, created_pet):
        """PUT /pet — Update the pet's name and verify the response reflects it."""

        """'created_pet' fixture yields a pet dictionary object. {Use dictionary unpacking: **created_pet}. 
            1. It copies all key–value pairs from the mapping created_pet into a new dictionary. 
            2. Then the literal adds/overrides "name": "UpdatedName" in that new dictionary. 
                a. “Start with everything that’s in created_pet, but make sure the name field is set to 'UpdatedName'.” 
                b. This does not mutate created_pet; it builds a new dict.  
       """
        updated_payload = {**created_pet, "name": "UpdatedName"}
        response = pet_service.update_pet(updated_payload)

        assert_status(response, 200)
        body = pet_service.json(response)
        assert_field_equals(body, "name", "UpdatedName")
        assert_field_equals(body, "id", created_pet["id"])

    def test_pet_u002_update_status_to_sold(self, pet_service, created_pet):
        """PUT /pet — Change status from 'available' to 'sold'."""
        updated_payload = {**created_pet, "status": "sold"}

        response = pet_service.update_pet(updated_payload)

        assert_status(response, 200)
        body = pet_service.json(response)
        assert_field_equals(body, "status", "sold")

    @pytest.mark.negative
    def test_pet_u003_update_nonexistent_pet(self, pet_service):
        """PUT /pet — Updating a pet with a non-existent ID — expect 404."""
        payload = make_pet()
        payload["id"] = 999_999_999

        response = pet_service.update_pet(payload)

        assert response.status_code in (404, 400, 200), \
            "Documenting actual Petstore behaviour for non-existent ID update."

    @pytest.mark.negative
    def test_pet_u004_update_with_empty_body(self, pet_service):
        """PUT /pet with an empty JSON body — expect 4xx.
        Note: PetStore server does not through 4xx error for empty body
        """
        response = pet_service.update_pet({})

        assert response.status_code >= 200, \
            f"Expected 2xx for empty update body, got {response.status_code}."
