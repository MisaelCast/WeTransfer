# WeTransfer

Aplicación web de transferencia de archivos con generación de enlaces únicos y expiración automática, inspirada en WeTransfer. Desarrollada con Python y FastAPI, implementando una arquitectura distribuida con PostgreSQL como base de datos principal y Supabase como capa secundaria.

---

## Objetivo

Desarrollar un sistema que permita subir archivos, generar enlaces de descarga únicos y gestionar la expiración automática, utilizando una arquitectura distribuida donde:

- **PostgreSQL** → Base de datos principal (metadata, tokens, expiración, estado)
- **Supabase** → Almacenamiento de archivos físicos (Supabase Storage) y autenticación de usuarios (Supabase Auth)

---

## Stack tecnológico

| Capa                       | Tecnología                   |
| -------------------------- | ---------------------------- |
| Backend                    | Python 3.10+ / FastAPI       |
| Base de datos principal    | PostgreSQL                   |
| Almacenamiento de archivos | Supabase Storage             |
| Autenticación              | Supabase Auth (Google OAuth) |
| Job de expiración          | APScheduler                  |
| Rate limiting              | slowapi                      |
| Despliegue                 | Railway                      |

---

## Estructura del proyecto

```
WeTransfer/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── file_routes.py      # Endpoints de la API
│   ├── db/
│   │   ├── connection.py           # Conexión a PostgreSQL
│   │   └── queries.py              # Queries SQL reutilizables
│   ├── schemas/
│   │   └── file_schema.py          # Schemas Pydantic (request/response)
│   ├── services/
│   │   ├── expiration_service.py   # Job de expiración automática
│   │   ├── storage_service.py      # Capa de Supabase Storage
│   │   └── token_service.py        # Generación de tokens UUID
│   ├── static/
│   │   └── index.html              # Frontend
│   ├── utils/
│   │   ├── auth.py                 # Validación de tokens JWT
│   │   ├── limiter.py              # Rate limiter compartido
│   │   └── validators.py           # Validaciones de seguridad
│   ├── config.py                   # Variables de entorno
│   ├── main.py                     # Entry point FastAPI
│   └── supabase_client.py          # Cliente de Supabase
├── migrations/
│   └── init.sql                    # Schema de PostgreSQL
├── Procfile                        # Comando de inicio para Railway
├── requirements.txt
└── .env.example
```

---

## Schema de base de datos

```sql
CREATE TABLE files (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_name   TEXT NOT NULL,
    mime_type       TEXT NOT NULL,
    size_bytes      BIGINT NOT NULL,
    storage_path    TEXT NOT NULL,
    download_token  UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    expires_at      TIMESTAMP NOT NULL,
    status          TEXT NOT NULL DEFAULT 'active',
    user_id         TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## API

| Método | Ruta                | Descripción                   |
| ------ | ------------------- | ----------------------------- |
| POST   | `/upload`           | Subir archivo                 |
| GET    | `/file/{token}`     | Ver información del archivo   |
| GET    | `/download/{token}` | Descargar archivo             |
| DELETE | `/file/{token}`     | Eliminar archivo              |
| GET    | `/config`           | Obtener configuración pública |
| GET    | `/docs`             | Documentación Swagger         |

---
