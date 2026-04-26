# Manual d'Usuari AgenticOS

> **Versió:** 0.2.0
> **Data:** 2026-04-10
> **Estat:** Actualitzat amb separació registry/secrets (feat-039, feat-042, feat-043)

---

## 1. Configuració de Providers

### 1.1 Fonts de Configuració

| Fitxer | Ubicació | Propòsit | Committable |
|--------|----------|----------|-------------|
| `providers.json` | `agenticos_data/config/` | **Registry**: catàleg de providers (id, name, type, endpoint, models) | ✅ Sí |
| `secrets.providers.json` | `agenticos_data/config/` | **Secrets**: API keys locals | ❌ No (gitignored) |
| `llm.json` | `agenticos_data/config/` | **Knobs + legacy**: default_provider, default_model, rate limiting, logging | Depèn |

### 1.2 Schema: `providers.json` (Registry)

Font canònica de providers. **No conté secrets.**

```json
{
  "version": "v1.1",
  "providers": [
    {
      "id": "zen",
      "name": "OpenCode (zen)",
      "type": "openai-compatible",
      "endpoint": "https://opencode.ai/zen",
      "auth_type": "bearer",
      "capabilities": ["chat"],
      "models": [
        { "name": "gpt-5.4-mini", "context_window": 0 }
      ]
    }
  ]
}
```

### 1.3 Schema: `secrets.providers.json` (Secrets)

Secrets locals per provider. **Mai commitejar.**

```json
{
  "version": "v1",
  "providers": {
    "zen": { "api_key": "sk-..." },
    "minimax": { "api_key": "sk-cp-..." }
  }
}
```

**Precedència de secrets:**
1. `secrets.providers.json` (prioritat alta)
2. `llm.json` (legacy fallback, temporal)

### 1.4 Schema: `llm.json` (Knobs)

Knobs globals i fallback legacy.

```json
{
  "default_provider": "minimax",
  "logging": { "level": "INFO" },
  "rate_limiting": { "requests_per_minute": 60 },
  "providers": {
    "zen": { "api_key": "...", "base_url": "...", "models": [...] }
  }
}
```

> **Nota**: Els `providers` a `llm.json` son legacy. Els secrets es recomanen a `secrets.providers.json`.

---

## 2. Endpoints API

### 2.1 Providers

**`GET /api/v1/providers`** — Llista de providers (registry)

```bash
curl http://localhost:8080/api/v1/providers
```

Resposta:
```json
{
  "version": "v1.1",
  "providers": [
    {
      "id": "zen",
      "name": "OpenCode (zen)",
      "type": "openai-compatible",
      "endpoint": "https://opencode.ai/zen",
      "configured": true
    }
  ],
  "total_count": 4,
  "configured_count": 3
}
```

> **Important**: L'API **mai exposa** `api_key`. Només retorna `configured: true/false`.

---

### 2.2 LLM Chat

**`POST /api/v1/llm/chat`** — Chat amb LLM

```bash
curl -X POST http://localhost:8080/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"provider":"zen","model":"gpt-5.4-mini"}'
```

**CORS Preflight** (`OPTIONS /api/v1/llm/chat`):

```bash
curl -X OPTIONS http://localhost:8080/api/v1/llm/chat \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Authorization, Content-Type" \
  -H "Origin: http://localhost:5173"
```

Resposta (204 No Content):
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
```

---

### 2.3 FileTree

**`GET /api/v1/files`** — Arbre de fitxers

```bash
# Amb root per defecte (directori actual)
curl "http://localhost:8080/api/v1/files"

# Amb root i depth
curl "http://localhost:8080/api/v1/files?root=.&depth=2"

# Amb root específic
curl "http://localhost:8080/api/v1/files?root=K:/AgenticOsGen&depth=3"
```

Paràmetres:
| Param | Tipus | Descripció | Defecte |
|-------|-------|------------|---------|
| `root` | string | Directori arrel a explorar | `.` |
| `depth` | int | Profunditat màxima (max 10) | 3 |

---

## 3. Checklist: Verificació del Sistema

### Configuració

- [ ] `providers.json` existeix a `agenticos_data/config/`
- [ ] `secrets.providers.json` creat (o `llm.json` té API keys legacy)
- [ ] `.gitignore` conté `secrets.*.json`

### API

- [ ] `GET /api/v1/providers` respon (204/200)
- [ ] `GET /api/v1/providers` no exposa `api_key`
- [ ] `OPTIONS /api/v1/llm/chat` retorna 204 (CORS preflight)
- [ ] `POST /api/v1/llm/chat` funciona
- [ ] `GET /api/v1/files?root=.&depth=1` respon

### Build

```bash
cd 02_implementation
go build -o bin/api-server.exe ./cmd/api-server
./bin/api-server.exe
```

---

## 4. Migració (de legacy a nou estil)

### Passos per migrar secrets a `secrets.providers.json`:

1. **Crear fitxer nou** `agenticos_data/config/secrets.providers.json`:
   ```json
   {
     "version": "v1",
     "providers": {
       "zen": { "api_key": "COPIAR_DE_llm.json" }
     }
   }
   ```

2. **Esborrar API keys de `llm.json`** (deixar noms de provider buits o amb placeholders)

3. **Verificar**:
   ```bash
   # Reiniciar servidor
   curl http://localhost:8080/api/v1/providers
   # Hauria de mostrar configured=true pels providers amb secret
   ```

---

## 5. Seguretat

- **Secrets mai commitejats**: `.gitignore` ignora `secrets.*.json`
- **API no exposa secrets**: L'endpoint `/providers` retorna `configured` però mai `api_key`
- **CORS**: Permet origens localhost per al Dashboard

---

*Manual d'Usuari AgenticOS v0.2.0 - 2026-04-10*
