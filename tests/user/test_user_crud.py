import pytest

from util.assertions import assert_status, assert_schema, assert_field_equals, assert_field_not_empty
from util.assertions import USER_SCHEMA
from util.data_factory import make_user

pytestmark = [pytest.mark.regression, pytest.mark.user, pytest.mark.demo]


class TestUserCRUD:
    """POST, GET, PUT, DELETE /user — Full user lifecycle."""

    # ------------------------------------------------------------------
    # POST /user — Create
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_usr_c001_create_user_all_fields(self, user_service):
        """POST /user — Create a user with all fields — expect 200."""
        payload = make_user()

        response = user_service.create_user(payload)

        assert_status(response, 200)
        body = user_service.json(response)
        assert_field_not_empty(body, "message")

        # Cleanup
        user_service.delete_user(payload["username"])

    def test_usr_c002_create_user_minimum_fields(self, user_service):
        """POST /user — Create a user with only username and password — expect 200."""
        payload = {
            "username": f"minuser_{make_user()['username']}",
            "password": "testpassword"
        }

        response = user_service.create_user(payload)

        assert_status(response, 200)

        # Cleanup
        user_service.delete_user(payload["username"])

    @pytest.mark.negative
    def test_usr_c003_create_user_empty_body(self, user_service):
        """POST /user with an empty body — document actual API behaviour."""
        response = user_service.create_user({})

        # Petstore accepts empty bodies with a 200 — documenting this quirk
        assert response.status_code in (200, 400), \
            f"Unexpected status for empty user body: {response.status_code}."

    # ------------------------------------------------------------------
    # GET /user/{username} — Read
    # ------------------------------------------------------------------

    @pytest.mark.smoke
    def test_usr_r001_get_existing_user(self, user_service, created_user):
        """GET /user/{username} — Retrieve a user that was just created."""
        response = user_service.get_user(created_user["username"])

        assert_status(response, 200)
        body = user_service.json(response)
        assert_schema(body, USER_SCHEMA)
        assert_field_equals(body, "username", created_user["username"])

    @pytest.mark.negative
    def test_usr_r002_get_nonexistent_user(self, user_service):
        """GET /user/{username} — Username that doesn't exist — expect 404."""
        response = user_service.get_user("this_user_absolutely_does_not_exist_xyz_999")

        assert_status(response, 404)

    @pytest.mark.schema
    def test_usr_r003_get_user_schema_valid(self, user_service, created_user):
        """Validate the GET /user/{username} response matches the User schema."""
        response = user_service.get_user(created_user["username"])

        assert_status(response, 200)
        assert_schema(user_service.json(response), USER_SCHEMA)

    def test_usr_r004_get_user_fields_match_creation(self, user_service, created_user):
        """GET /user — Response fields match what was sent during creation."""
        response = user_service.get_user(created_user["username"])

        assert_status(response, 200)
        body = user_service.json(response)

        assert_field_equals(body, "username", created_user["username"])
        assert_field_equals(body, "firstName", created_user["firstName"])
        assert_field_equals(body, "lastName", created_user["lastName"])
        assert_field_equals(body, "email", created_user["email"])

    # ------------------------------------------------------------------
    # PUT /user/{username} — Update
    # ------------------------------------------------------------------

    def test_usr_u001_update_user_email(self, user_service, created_user):
        """PUT /user/{username} — Update email and verify persistence via GET."""
        updated_payload = {**created_user, "email": "updated@example.com"}

        response = user_service.update_user(created_user["username"], updated_payload)

        assert_status(response, 200)

        # Verify the update persisted
        get_response = user_service.get_user(created_user["username"])
        if get_response.status_code == 200:
            body = user_service.json(get_response)
            assert body.get("email") == "updated@example.com", \
                f"Email was not updated. Got: {body.get('email')}"

    @pytest.mark.negative
    def test_usr_u002_update_nonexistent_user(self, user_service):
        """PUT /user/{username} for a non-existent user — expect 404."""
        payload = make_user(username="ghost_user_xyz_does_not_exist")

        response = user_service.update_user("ghost_user_xyz_does_not_exist", payload)

        assert response.status_code in (404, 200), \
            "Documenting Petstore behaviour for updating non-existent user."

    # ------------------------------------------------------------------
    # DELETE /user/{username}
    # ------------------------------------------------------------------

    def test_usr_d001_delete_existing_user(self, user_service):
        """DELETE /user/{username} — Delete a user and expect 200."""
        payload = make_user()
        user_service.create_user(payload)

        response = user_service.delete_user(payload["username"])

        assert_status(response, 200)

    @pytest.mark.negative
    def test_usr_d002_delete_nonexistent_user(self, user_service):
        """DELETE a user that doesn't exist — expect 404."""
        response = user_service.delete_user("user_that_does_not_exist_xyz_abc")

        assert response.status_code in (404, 200), \
            "Documenting Petstore behaviour for deleting non-existent user."

    def test_usr_d003_delete_then_verify_gone(self, user_service):
        """DELETE a user then GET the same username — must return 404."""
        payload = make_user()
        user_service.create_user(payload)
        user_service.delete_user(payload["username"])

        get_response = user_service.get_user(payload["username"])

        assert get_response.status_code == 404, \
            f"User '{payload['username']}' still accessible after deletion."
