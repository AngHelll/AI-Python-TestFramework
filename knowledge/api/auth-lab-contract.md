# API — Auth lab

Contrato in-memory (`FakeAuthApi`):

| Método | Entrada | Éxito | Error |
|--------|---------|-------|-------|
| `Login` | username/password | `AccessToken` | `INVALID_INPUT`, `INVALID_CREDENTIALS`, `ACCOUNT_LOCKED` |
| `RefreshToken` | refresh token `lab-refresh-*` | nuevo access token | `INVALID_REFRESH` |
| `GetProfile` | access token `lab-token-*` | `UserProfile` | `null` |

Usuarios sintéticos: `valid_user` / `valid_password`.
