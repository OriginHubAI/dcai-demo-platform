# Pagination Guidelines

> LimitOffset, PageNumber, vs Cursor pagination for DRF list APIs.

---

## When to Use Each Approach

| Approach   | Performance                | Use Case                          |
| ---------- | -------------------------- | --------------------------------- |
| **Cursor** | O(1) - constant            | User-facing infinite feeds, large datasets |
| **PageNumber** | O(n) - degrades with depth | Internal APIs, standard UI tables, total count required |
| **LimitOffset**| O(n) - degrades with depth | Complex multi-filter endpoints, arbitrary querying |

**Default recommendation**: Use **PageNumberPagination** for administrative tables (when "Total Results" counts are necessary) and **CursorPagination** for consumer-facing infinite scroll lists (like the Chat History or Dataset feed).

---

## Why Cursor is Faster

```sql
Offset pagination (page 90,000 of 1M records):
  SELECT * FROM items ORDER BY updated_at LIMIT 20 OFFSET 1800000;
  -- Database scans 1,800,000 rows, discards them, returns 20.
  -- Time: ~700ms, heavily CPU bound. Also requires an expensive COUNT(*) query usually.

Cursor pagination (same position):
  SELECT * FROM items
  WHERE (updated_at < cursor_time) 
  ORDER BY updated_at DESC LIMIT 20;
  -- Database jumps straight to the index key and grabs 20 items.
  -- Time: ~4ms
```

---

## Pagination in DRF

DRF provides built-in Support. Set global defaults in `core/settings.py`, or override them per ViewSet.

### Global Setup
```python
# backend/core/settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### Implementing PageNumber Pagination

Standard table logic. `?page=3&page_size=10`. This allows users to jump pages.

```python
# backend/core/pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size' # Allows client to specify size
    max_page_size = 100

# backend/dataset/views.py
from core.pagination import StandardResultsSetPagination

class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    pagination_class = StandardResultsSetPagination
```

### Implementing Cursor Pagination

Notice there's no `count` in the response natively, only `next` and `previous` URLs. This is for infinite scroll arrays.

```python
# backend/core/pagination.py
from rest_framework.pagination import CursorPagination

class FeedCursorPagination(CursorPagination):
    page_size = 20
    ordering = '-created_at' # Needs a reliable ordering tuple (timestamp is good)
    page_size_query_param = 'page_size'
    max_page_size = 100

# backend/chat/views.py
class MessageHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = FeedCursorPagination
```

---

## Response Schemas

### PageNumber Output
```json
{
    "count": 1023,
    "next": "http://api.example.org/accounts/?page=5",
    "previous": "http://api.example.org/accounts/?page=3",
    "results": [
       {...}, {...}
    ]
}
```

### Cursor Output
```json
{
    "next": "http://api.example.org/accounts/?cursor=cD0yMDE1LTEwLTI4KzA5JTNBNTElM0E1Mi43ODg1MDAlMkIwMCUzQTAw",
    "previous": "http://api.example.org/accounts/?cursor=cj0xJnA9MjAxNS0xMC0yOCswOSUzQTUyJTNBNTAuMTc4MTE4JTJCMDAlM0EwMA%3D%3D",
    "results": [
       {...}, {...}
    ]
}
```

---

## Customizing Response Envelopes

To match specific frontend demands (like omitting URL strings entirely and just sending the cursor hash manually), you can override `.get_paginated_response(self, data)`.

```python
class CustomCursorPagination(CursorPagination):
    ordering = '-updated_at'

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'next_cursor': self.get_next_link(), # You might parse the raw hash here
            'results': data
        })
```

---

## Summary

| Rule                            | Reason                        |
| ------------------------------- | ----------------------------- |
| Offset/PageNumber needs Total Count | Exposes full DB sizes, slower over time |
| Cursor ordering must be deterministic | Usually `-created_at` or `-updated_at`  |
| Respect `max_page_size`         | Prevent clients requesting 1 Million items  |
| Customize the Envelope if needed | DRF `.get_paginated_response()` hook exists|
