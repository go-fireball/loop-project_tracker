# Simplification Guidance

1. Prefer straightforward modular monolith structures.
2. Keep interfaces small and explicit.
3. Add abstractions only when repeated pain is proven.
4. Preserve existing business behavior unless requirements say otherwise.
5. Bias toward maintainability over novelty.

## Project-Tracker Guardrails (added by SENIOR_JUDGMENTAL_ENGINEER)

6. **No generic CRUD base class** — write views directly. Three similar view sets (projects, tasks, tags) do not justify a shared abstraction.
7. **Function-based views preferred** — simpler, easier to read, no class hierarchy to follow for a small CRUD surface.
8. **Manual dict serialization** — convert ORM objects to plain dicts inline in each view. Do not create a serializer class; the fields are small and stable.
9. **Plain ManyToManyField** — no `through` table needed for tags since the relationship carries no extra fields. Use `.add()` / `.remove()` / `.set()` directly.
10. **ORM aggregation for dashboard** — use `.count()` and `.filter()` on QuerySets. No raw SQL.
11. **Vanilla JS: no build step** — one shared static JS file (`static/tracker/app.js`) or per-template `<script>` blocks. No bundler, no transpiler.
12. **CSRF for fetch calls** — vanilla JS must read the `csrftoken` cookie and send `X-CSRFToken` header on POST/PUT/DELETE. Use Django's `{% csrf_token %}` in templates and read it client-side. Do NOT use `@csrf_exempt` in production-bound code.
13. **Timezone-aware overdue check** — use `django.utils.timezone.now().date()` when filtering overdue tasks; do not use `datetime.date.today()` if `USE_TZ=True`.
14. **Flat URL structure** — no URL namespaces needed for a single-app project. Keep `urls.py` flat and readable.
15. **Stack override in effect** — `judgment.yaml` defaults (aspnet_core, react_nextjs, postgresql) are superseded by the goal. No exception entry required.
