# Error Handling Guidelines

> Strategies for handling errors in Django and Django REST Framework (DRF).

---

## Error Categories

| Error Type              | Mechanism                               | Handler / Outcome                          |
| ----------------------- | --------------------------------------- | ------------------------------------------ |
| **Input Validation**    | `serializers.ValidationError`           | DRF returns `400 Bad Request`              |
| **Data Integrity / DB** | `django.db.utils.IntegrityError`        | Transactions rollback, returns `500/400`   |
| **Not Found**           | `.get_object_or_404()` or `Http404`     | DRF returns `404 Not Found`                |
| **Permission Denied**   | `exceptions.PermissionDenied`           | DRF returns `403 Forbidden`                |
| **External Dependency** | `httpx.HTTPStatusError`, Retry logic    | Caught by services, re-raised as `502/503` |

---

## Pattern 1: Input Validation - Raise ValidationError

Rely on serializers to check inputs. Calling `.is_valid(raise_exception=True)` cleans up View logic.

```python
# CORRECT: Will automatically return a 400 Bad Request with field errors
serializer = ProjectInputSerializer(data=request.data)
serializer.is_valid(raise_exception=True)
project = Project.objects.create(**serializer.validated_data)

# WRONG: Manual dictionary checks
if 'name' not in request.data:
    return Response({"error": "Name is required"}, status=400)
```

---

## Pattern 2: Service Layer Exceptions - DRF APIException

When deep in a Service layer (e.g., `services.py`), you often encounter business rule violations. Raise a DRF `APIException` subclass so that DRF's global error handler formats the JSON response properly.

```python
from rest_framework.exceptions import APIException
from rest_framework import status

class PaymentGatewayError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'The payment gateway is currently down.'
    default_code = 'gateway_error'

def charge_customer(amount):
    try:
        remote_payment_call(amount)
    except TimeoutError:
        # Proper DRF exception
        raise PaymentGatewayError()
```

---

## Pattern 3: Transaction Safety (DB Integrity)

Using `@transaction.atomic` requires unhandled exceptions to occur inside the block for it to roll back. 

```python
# CORRECT: IntegrityError causes atomic block to abort, then the View layer can catch it or let it become a 500
@transaction.atomic
def transfer_funds(from_account, to_account, amount):
    from_account.balance -= amount
    from_account.save()
    to_account.balance += amount
    to_account.save()
    if to_account.is_frozen:
        raise ValueError("Cannot transfer to frozen account.") # Automatically rolls back

# WRONG: Catching the error inside the block without re-raising commits partial state
@transaction.atomic
def transfer_funds(from_account, to_account, amount):
    try:
        from_account.balance -= amount
        from_account.save()
        raise ValueError("Oops")
    except ValueError:
        pass # The from_account balance was subtracted and COMMITTED!
```

---

## Pattern 4: External Dependencies (Proxies)

When proxying to FastAPI/DataFlow-System via `httpx`:

```python
# Non-critical: Log warning and return degraded response
try:
    await trigger_optional_analytics_task()
except httpx.RequestError as e:
    logger.warning(f"Analytics disabled: {e}")

# Critical: return graceful HTTP Error
try:
    response = await client.post("http://fastapi-service/critical", json=data)
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    logger.error("FastAPI backend failed")
    # Wrap in a DRF Response
    return Response({"error": "Backend processing failed"}, status=e.response.status_code)
except httpx.RequestError:
    return Response({"error": "Service Unavailable"}, status=503)
```

---

## Standard DRF Exception Handler

By default, DRF catches its own exceptions (e.g., `Http404`, `PermissionDenied`, subclasses of `APIException`) and returns standardized JSON content like:

```json
// 400 Bad Request
{
    "name": ["This field is required."],
    "email": ["Enter a valid email address."]
}
```

If you need uniform wrappers around all errors (like `{ "success": false, "error": "details"}`), implement a **Custom Exception Handler** in `core/settings.py`.

```python
# backend/core/exceptions.py
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'success': False,
            'error': response.data
        }

    return response

# backend/core/settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler'
}
```

---

## Summary

| Situation            | Action                         |
| -------------------- | ------------------------------ |
| Validation fails     | `serializer.is_valid(raise_exception=True)` |
| Entity Missing       | `get_object_or_404(Model, id=x)` |
| DB operations error  | Raise exception inside `@transaction.atomic`|
| Business rule fail   | Raise subclass of `rest_framework.exceptions.APIException`|
| Non-critical failure | `logger.warning()` + continue     |
