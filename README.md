# databricks-hackathon-memori

## Docker

Run the backend:

```bash
docker compose up --build
```

When the frontend is ready, start both services:

```bash
docker compose --profile frontend up --build
```

| Service  | URL                   |
|----------|-----------------------|
| Backend  | http://localhost:8000 |
| Frontend | http://localhost:3000 |

Copy `backend/.env.example` to `backend/.env` and set your API keys before starting.

If image pulls time out, check your network/VPN and Docker Hub access, then retry the build.