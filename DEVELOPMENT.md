# 🚀 GUÍA DE DESARROLLO LOCAL

Esta guía te ayudará a configurar SafeCity Pro en tu máquina local para desarrollo.

---

## 📋 Requisitos

- **Python 3.9+** ([descargar](https://www.python.org/downloads/))
- **Docker Desktop** ([descargar](https://www.docker.com/products/docker-desktop/))
- **Git** ([descargar](https://git-scm.com/))
- **Visual Studio Code** (recomendado, [descargar](https://code.visualstudio.com/))
- **Postman** (opcional, para testing de APIs)

---

## 🔧 Configuración Inicial

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/safecity-project.git
cd safecity-project
```

### Paso 2: Instalar Extensiones VS Code (Recomendado)

```
- Docker
- Python
- FastAPI
- Kubernetes
```

### Paso 3: Crear Archivo de Variables de Entorno

Crea `.env` en la raíz:

```env
# Database
POSTGRES_PASSWORD=safepass123
POSTGRES_DB=safecity_alerts
POSTGRES_USER=postgres

# Services
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Frontend
API_ALERTS_URL=http://localhost:8001
API_USERS_URL=http://localhost:8002
```

---

## 🐍 Desarrollo Backend (Python)

### Alerts Service

```bash
# Navegar al directorio
cd services/alerts

# Crear virtual environment
python -m venv venv

# Activar virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python main.py
# O con auto-reload:
uvicorn main:app --reload --port 8001

# Acceder a documentación
# http://localhost:8001/docs
```

### Users Service

```bash
# Similar a Alerts
cd services/users
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
# http://localhost:8002/docs
```

---

## 🎨 Desarrollo Frontend

### Servidor Local

```bash
cd services/frontend

# Opción 1: Con Python (simple HTTP server)
python -m http.server 8000

# Opción 2: Con Node.js (recomendado)
npx http-server

# Acceder
# http://localhost:8000
```

### Edición

- Editar `index.html` con VS Code
- El cambio se refleja al recargar el navegador
- Usar DevTools de Chrome para debugging

---

## 🐘 Base de Datos PostgreSQL

### Con Docker (Recomendado)

```bash
# Crear contenedor PostgreSQL
docker run --name safecity-postgres \
  -e POSTGRES_PASSWORD=safepass123 \
  -e POSTGRES_DB=safecity_alerts \
  -p 5432:5432 \
  -d postgres:latest

# Verificar
docker ps

# Ver logs
docker logs safecity-postgres

# Conectarse con psql
# Opción 1: Desde host
psql -h localhost -U postgres -d safecity_alerts

# Opción 2: Desde dentro del contenedor
docker exec -it safecity-postgres psql -U postgres -d safecity_alerts
```

### Crear Tablas

```sql
-- Conectarse primero
psql -h localhost -U postgres -d safecity_alerts

-- Crear tabla de alertas
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(200) NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'activa',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de usuarios (si lo necesitas)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user'
);

-- Verificar tablas
\dt
```

### Limpieza

```bash
# Detener y eliminar contenedor
docker stop safecity-postgres
docker rm safecity-postgres

# Para resetear datos:
docker volume rm safecity-postgres  # si usaste volumen
```

---

## 🐳 Docker Compose (All-in-One)

### Iniciar Todos los Servicios

```bash
# Desde la raíz del proyecto
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Detener y limpiar (WARNING: elimina datos)
docker-compose down -v
```

### Verificar Servicios

```bash
# Frontend
curl http://localhost

# Alerts Service
curl http://localhost:8001/docs

# Users Service
curl http://localhost:8002/docs

# PostgreSQL
docker-compose exec postgres psql -U postgres -d safecity_alerts -c "SELECT COUNT(*) FROM alerts;"
```

---

## 🧪 Testing de APIs

### Con curl

```bash
# Login
curl -X POST http://localhost:8002/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Crear alerta
TOKEN="token-seguro-safecity-2026"

curl -X POST http://localhost:8001/alerts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tipo": "Robo",
    "ubicacion": "CUCEI Campus",
    "descripcion": "Robo en estacionamiento"
  }'

# Listar alertas
curl http://localhost:8001/alerts

# Health check
curl http://localhost:8001/
```

### Con Postman

1. Importar colección (si existe)
2. O crear manualmente:
   - **Login**: POST `http://localhost:8002/login`
   - **Crear Alerta**: POST `http://localhost:8001/alerts`
   - **Listar Alertas**: GET `http://localhost:8001/alerts`

---

## 🐛 Debugging

### Logs en Desarrollo

```bash
# Ver logs de un servicio
docker-compose logs alerts-service

# Tiempo real
docker-compose logs -f alerts-service

# Últimas 50 líneas
docker-compose logs --tail 50 alerts-service

# Formato combinado
docker-compose logs -f --timestamps
```

### Debugger de Python

En `services/alerts/main.py`:

```python
import pdb

@app.post("/alerts")
async def create_alert(incident: dict):
    pdb.set_trace()  # Se pausará aquí
    # ... resto del código
```

Ejecutar con:
```bash
python main.py  # sin --reload
```

### Browser DevTools

1. Abiir Chrome/Firefox
2. Presionar `F12`
3. Console, Network, Sources
4. Inspeccionar tráfico HTTP

---

## 📦 Construcción de Imágenes Docker

### Alerts Service

```bash
docker build -t safecity-alerts:dev ./services/alerts
docker run -p 8001:8000 -e DATABASE_HOST=host.docker.internal safecity-alerts:dev
```

### Users Service

```bash
docker build -t safecity-users:dev ./services/users
docker run -p 8002:8000 safecity-users:dev
```

### Frontend

```bash
docker build -t safecity-frontend:dev ./services/frontend
docker run -p 80:80 safecity-frontend:dev
```

---

## ⚡ Optimizaciones para Desarrollo

### Hot Reload

```bash
# FastAPI con uvicorn ya tiene auto-reload
uvicorn main:app --reload

# Frontend: usar live-server
npm install -g live-server
live-server services/frontend/
```

### Database Migrations (si usas Alembic)

```bash
# Crear migración
alembic revision --autogenerate -m "Create alerts table"

# Aplicar
alembic upgrade head

# Verificar
alembic current
```

---

## 🔒 Variables Sensibles

### NO Commitar Nunca:

- `.env` (usar `.env.example` en su lugar)
- Contraseñas hardcodeadas
- API Keys
- Tokens

### Template `.env.example`:

```env
POSTGRES_PASSWORD=SET_THIS
POSTGRES_DB=safecity_alerts
POSTGRES_USER=postgres
DATABASE_HOST=localhost
```

---

## 📚 Recursos Útiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Python venv Guide](https://docs.python.org/3/library/venv.html)

---

## ✅ Checklist de Setup

- [ ] Python 3.9+ instalado
- [ ] Docker Desktop corriendo
- [ ] Repositorio clonado
- [ ] `.env` creado
- [ ] Virtual environments creados
- [ ] Dependencias instaladas
- [ ] PostgreSQL corriendo
- [ ] Todos los servicios accesibles
- [ ] Dashboard abierto en navegador
- [ ] Alerta de prueba creada exitosamente

✨ **¡Listo para desarrollar!**
