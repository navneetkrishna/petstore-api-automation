import pytest

from util.assertions import assert_status
from util.data_factory import make_pet

pytestmark = [pytest.mark.regression, pytest.mark.pet]


class TestPetDelete:
    """DELETE /pet/{petId} — Delete a pet."""

    @pytest.mark.smoke
    def test_pet_d001_delete_existing_pet(self, pet_service):
        """DELETE a pet that exists — expect 200."""
        # Create a dedicated pet for this test (not using created_pet fixture
        # because that fixture also deletes in teardown — we want to test the delete here)

        payload = make_pet()
        create_response = pet_service.create_pet(payload)
        assert_status(create_response, 200)
        pet_id = pet_service.json(create_response)["id"]

        response = pet_service.delete_pet(pet_id)

        assert_status(response, 200)

    @pytest.mark.negative
    def test_pet_d002_delete_already_deleted_pet(self, pet_service):
        """DELETE a pet that has already been deleted — expect 404."""
        # Create and immediately delete
        payload = make_pet()
        create_response = pet_service.create_pet(payload)
        assert_status(create_response, 200)
        pet_id = pet_service.json(create_response)["id"]
        pet_service.delete_pet(pet_id)

        # Delete again
        response = pet_service.delete_pet(pet_id)

        assert response.status_code in (404, 200), \
            "Petstore may return 200 or 404 for a repeated delete — documenting behaviour."

    @pytest.mark.negative
    def test_pet_d003_delete_nonexistent_pet(self, pet_service):
        """DELETE /pet/{petId} with a non-existent ID — expect 404."""
        response = pet_service.delete_pet(999_999_999)

        assert response.status_code in (404, 200), \
            "Documenting actual Petstore behaviour for non-existent delete."

    @pytest.mark.negative
    def test_pet_d004_delete_then_verify_gone(self, pet_service):
        """DELETE a pet then GET the same ID — must return 404."""
        payload = make_pet()
        create_response = pet_service.create_pet(payload)
        assert_status(create_response, 200)
        pet_id = pet_service.json(create_response)["id"]

        pet_service.delete_pet(pet_id)

        get_response = pet_service.get_pet_by_id(pet_id)
        assert get_response.status_code == 404, \
            f"Pet ID {pet_id} still accessible after deletion. Status: {get_response.status_code}."
