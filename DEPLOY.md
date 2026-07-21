# Deploy

Backend (FastAPI) → **Railway**; frontend (Next.js in `web/`) → **Vercel**. Push to GitHub first.

## Backend → Railway
1. New Project → Deploy from GitHub repo → `adr-advisor`. Uses the `Dockerfile`.
2. **Variables:** `ANTHROPIC_API_KEY` (+ `AD_CORS_ORIGINS` = your custom domain if attached).
3. Settings → **Networking → Generate Domain**. Set the domain's target port to the deploy-log port.
4. `GET /health` → `{"status":"ok"}`.

## Frontend → Vercel
1. Import `adr-advisor`, **Root Directory = `web`**.
2. Env var `NEXT_PUBLIC_API_URL` = the Railway URL.
3. Deploy. Optionally attach `adr-advisor.kareemghazal.com` and add it to `AD_CORS_ORIGINS`.
