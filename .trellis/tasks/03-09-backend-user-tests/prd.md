# Create Unit Tests for Backend User App

## Goal
Implement a basic unit testing suite for the `user` app in the Django backend to ensure core authentication and user management logic is reliable.

## Requirements
- Setup testing infrastructure for the `user` app using Django's built-in testing framework.
- Implement model tests for the custom `User` model.
- Implement API tests for user registration, login, and profile retrieval (if applicable).
- Ensure tests pass with a clean database.

## Acceptance Criteria
- [x] `backend/user/tests/test_models.py` created and contains tests for User model creation and fields.
- [x] `backend/user/tests/test_views.py` created and contains tests for core user API endpoints.
- [x] All tests pass when running `python manage.py test user`.
- [x] No regressions introduced in existing user functionality.

## Technical Notes
- Project uses `rest_framework_simplejwt` for authentication.
- Custom user model is `user.User`.
- Use `APITestCase` from `rest_framework.test` for API endpoints.
