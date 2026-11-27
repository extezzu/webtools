# FastAPI refresh token rotation with reuse detection

A ~60-line, self-contained example. Each refresh token is single use; replaying an already-used token revokes the whole token family (the legitimate client and the thief are both logged out).

```bash
pip install -r requirements.txt
pytest -q          # 2 tests
uvicorn app:app --reload
```

## What it shows

- `/login` returns an access token (15 min) and a refresh token (7 days) that carries a unique `jti` and a `family` id.
- `/refresh` revokes the presented token and issues a new pair in the same family.
- Presenting a revoked token revokes every token in the family and returns 401.
- An access token is rejected at `/refresh` because the `type` claim is checked.

## What it leaves out (on purpose)

In-memory storage (use a database table with `jti`, `family`, `user_id`, `expires_at`, `revoked_at`), password hashing, rate limiting, and revoking all tokens on password change.

Read the walkthrough: https://dev.to/launchpadkits

The full multi-tenant version (orgs and roles, hashed API keys, Stripe billing, 50 tests) is a paid starter: https://www.creem.io/product/prod_7LIIfd0Y6cBufZxtRTfNO9 . This example is MIT licensed and stands on its own.
