# Authentication & RBAC

## Tokens

| Token | Lifetime | Storage |
|-------|----------|---------|
| **Access** | 30 min (configurable) | `Authorization: Bearer …` or `localStorage` |
| **Refresh** | 30 days | **httpOnly cookie** `refresh_token` on path `/api/auth` |

When the access token expires, call `POST /api/auth/refresh` with `credentials: 'include'`. The API rotates the refresh cookie and returns a new access token.

## Default admin (seed)

- Email: `admin@vikingsinnerwear.in`
- Password: `Admin@123456`

Override via `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_NAME` in `.env`.

## Roles

| Role | Permissions |
|------|-------------|
| `user` | Own cart, wishlist, orders; create reviews |
| `admin` | Full CRUD on products, users, orders, contact, newsletter |

## Auth endpoints

| Method | Path | Auth |
|--------|------|------|
| POST | `/api/auth/register` | Public |
| POST | `/api/auth/login` | Public |
| POST | `/api/auth/refresh` | Refresh cookie |
| POST | `/api/auth/logout` | Refresh cookie |
| POST | `/api/auth/logout-all` | Bearer (revokes all sessions) |
| GET | `/api/auth/me` | Bearer |

## CRUD summary

| Resource | GET list | GET one | POST | PUT | DELETE |
|----------|----------|---------|------|-----|--------|
| Products | Public | Public | Admin | Admin | Admin |
| Reviews | Public | Public | Public* | Owner/Admin | Owner/Admin |
| Users | Admin | Self/Admin | Admin | Self/Admin | Admin |
| Orders | Self/Admin | Self/Admin | Public** | Self/Admin | Admin |
| Cart | User | User | User | User | User |
| Wishlist | User | User | User | — | User |
| Contact | Admin | Admin | Public | — | Admin |
| Newsletter | Admin | Admin | Public | — | Admin |

\* Logged-in user id attached when Bearer present.  
\*\* Guest checkout allowed without login.

## Production cookies

```env
COOKIE_SECURE=true
COOKIE_SAMESITE=lax
CORS_ORIGINS=https://your-domain.com
```

Frontend must use `credentials: 'include'` on all API calls (see `src/api.js`).
