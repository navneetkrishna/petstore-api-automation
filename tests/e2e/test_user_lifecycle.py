import pytest

from util.assertions import assert_status, assert_field_equals
from util.data_factory import make_user

pytestmark = [pytest.mark.regression, pytest.mark.e2e, pytest.mark.user]


class TestUserLifecycle:
    """End-to-end user lifecycle — Create → Login → Read → Update → Delete → Verify."""

    @pytest.mark.smoke
    def test_e2e_user_001_full_lifecycle(self, user_service):
        """Full user lifecycle: Create → Login → GET → Update → DELETE → verify gone."""

        # Step 1: Create
        payload = make_user()
        create_response = user_service.create_user(payload)
        assert_status(create_response, 200)

        # Step 2: Login
        login_response = user_service.login(
            username=payload["username"],
            password=payload["password"]
        )
        assert_status(login_response, 200)

        # Step 3: Read
        get_response = user_service.get_user(payload["username"])
        assert_status(get_response, 200)
        assert_field_equals(user_service.json(get_response), "username", payload["username"])

        # Step 4: Update email
        updated_payload = {**payload, "email": "e2e_updated@example.com"}
        update_response = user_service.update_user(payload["username"], updated_payload)
        assert_status(update_response, 200)

        # Verify update persisted
        verify_response = user_service.get_user(payload["username"])
        if verify_response.status_code == 200:
            body = user_service.json(verify_response)
            assert body.get("email") == "e2e_updated@example.com", \
                f"Email not updated. Got: {body.get('email')}"

        # Step 5: Logout
        logout_response = user_service.logout()
        assert_status(logout_response, 200)

        # Step 6: Delete
        delete_response = user_service.delete_user(payload["username"])
        assert_status(delete_response, 200)

        # Step 7: Verify gone
        gone_response = user_service.get_user(payload["username"])
        assert gone_response.status_code == 404, \
            f"User '{payload['username']}' still accessible after deletion."

    def test_e2e_user_002_create_multiple_users(self, user_service):
        """POST /user/createWithList — Create multiple users and verify each exists."""
        payloads = [make_user() for _ in range(3)]

        response = user_service.create_users_with_list(payloads)
        assert_status(response, 200)

        # Verify each user exists
        for payload in payloads:
            get_response = user_service.get_user(payload["username"])
            assert get_response.status_code == 200, \
                f"User '{payload['username']}' not found after batch creation."
            user_service.delete_user(payload["username"])
