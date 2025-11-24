# Sirru Deployment Guide

Sirru is a sovereign AI workspace platform for African governments and enterprises.

## Quick Start with Coolify

### 1. Connect Repository

In Coolify, create a new service and connect to this repository:
```
https://github.com/Albad221/sirru
```

### 2. Configure Build Settings

- **Build Pack**: Docker Compose
- **Docker Compose File**: `docker-compose.sirru.yml`
- **Environment**: Production

### 3. Required Environment Variables

Set these in Coolify's environment configuration:

```bash
# Required
WEBUI_SECRET_KEY=<generate with: openssl rand -hex 32>
WEBUI_URL=https://your-domain.com

# AI Backend (choose one)
OLLAMA_BASE_URL=http://your-ollama-server:11434
# OR
OPENAI_API_KEY=sk-your-key
OPENAI_API_BASE_URL=https://api.openai.com/v1
```

### 4. Deploy

Click deploy and Coolify will build and run Sirru.

---

## Deployment Options

### Option A: Sirru Only (Recommended for Coolify)

Use `docker-compose.sirru.yml` with external Ollama or OpenAI:

```bash
cp .env.sirru .env
# Edit .env with your settings
docker compose -f docker-compose.sirru.yml up -d
```

### Option B: Sirru + Local Ollama

For air-gapped deployments with local AI inference:

```bash
docker compose -f docker-compose.sirru.yml --profile with-ollama up -d
```

### Option C: Sirru + PostgreSQL

For production with PostgreSQL (recommended for multi-user):

```bash
# Set DATABASE_URL in .env
DATABASE_URL=postgresql://sirru:password@sirru-postgres:5432/sirru
POSTGRES_PASSWORD=your-secure-password

docker compose -f docker-compose.sirru.yml --profile with-postgres up -d
```

### Option D: Full Stack (Ollama + PostgreSQL)

```bash
docker compose -f docker-compose.sirru.yml \
  --profile with-ollama \
  --profile with-postgres \
  up -d
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WEBUI_SECRET_KEY` | Yes | - | Session encryption key |
| `WEBUI_URL` | Yes | - | Public URL for OAuth/sharing |
| `WEBUI_NAME` | No | Sirru | Application display name |
| `OLLAMA_BASE_URL` | No* | - | Ollama server URL |
| `OPENAI_API_KEY` | No* | - | OpenAI API key |
| `DATABASE_URL` | No | SQLite | PostgreSQL connection string |
| `ENABLE_SIGNUP` | No | true | Allow new registrations |
| `DEFAULT_USER_ROLE` | No | user | New user default role |

*At least one AI backend required

---

## Modules

Sirru includes three integrated AI modules:

### Chat AI
- OpenWebUI-based chat interface
- Multi-model support (Ollama, OpenAI, etc.)
- Conversation history and search

### Docs AI
- AI-powered document editor
- RAG-based document intelligence
- Document collaboration

### Presentations AI
- AI slide generation
- Multiple themes
- Export capabilities

---

## Health Check

Verify deployment:
```bash
curl https://your-domain.com/health
```

Expected response:
```json
{"status": true}
```

---

## Support

For issues and feature requests:
https://github.com/Albad221/sirru/issues
