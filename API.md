# 📚 API Reference - SafeCity Pro

Documentación completa de los endpoints disponibles en SafeCity Pro.

---

## 📌 Base URLs

- **Desarrollo Local**: `http://localhost`
- **Alerts Service**: `http://localhost:8001`
- **Users Service**: `http://localhost:8002`
- **Producción**: `https://safecity.tucei.mx`

---

## 🔑 Autenticación

### Token JWT

Todos los endpoints protegidos requieren:

```
Authorization: Bearer <token>
```

### Obtener Token

**Endpoint**: `POST /login`  
**Service**: Users Service  
**URL**: `http://localhost:8002/login`

#### Parámetros (Form Data)

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|----------|-------------|
| `username` | string | ✅ | Nombre de usuario |
| `password` | string | ✅ | Contraseña |

#### Ejemplo Request

```bash
curl -X POST http://localhost:8002/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### Ejemplo Response

```json
{
  "access_token": "token-seguro-safecity-2026",
  "token_type": "bearer"
}
```

#### Códigos HTTP

| Código | Descripción |
|--------|-------------|
| `200` | Éxito |
| `401` | Credenciales inválidas |
| `500` | Error del servidor |

---

## 🚨 Alerts Service

### Base URL
`http://localhost:8001` (o `http://alerts-service:8001` en Kubernetes)

### Crear Alerta

**Endpoint**: `POST /alerts`  
**Autenticación**: Requerida (Bearer Token)  
**Content-Type**: `application/json`

#### Parámetros

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|----------|-------------|---------|
| `tipo` | string | ✅ | Tipo de incidente | `"Robo"` |
| `ubicacion` | string | ✅ | Ubicación del incidente | `"CUCEI, Guadalajara"` |
| `descripcion` | string | ❌ | Descripción adicional | `"Robo en estacionamiento"` |

#### Tipos Válidos
- `Robo` - Robo o asalto
- `Accidente` - Accidente vial
- `Vandalismo` - Acto de vandalismo

#### Ejemplo Request

```bash
curl -X POST http://localhost:8001/alerts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-seguro-safecity-2026" \
  -d '{
    "tipo": "Robo",
    "ubicacion": "CUCEI, Guadalajara",
    "descripcion": "Robo en estacionamiento de motos"
  }'
```

#### Ejemplo Response (201 Created)

```json
{
  "id": 42,
  "tipo": "Robo",
  "ubicacion": "CUCEI, Guadalajara",
  "descripcion": "Robo en estacionamiento de motos",
  "estado": "activa",
  "timestamp": "2026-05-03T14:32:10.123456"
}
```

#### Códigos HTTP

| Código | Descripción |
|--------|-------------|
| `201` | Alerta creada exitosamente |
| `400` | Parámetros inválidos |
| `401` | No autenticado |
| `422` | Datos incompletos |
| `500` | Error del servidor |

---

### Listar Alertas

**Endpoint**: `GET /alerts`  
**Autenticación**: Opcional  
**Query Parameters**: 
- `limit` (int, default=100): Máximo número de resultados
- `offset` (int, default=0): Desplazamiento para paginación
- `tipo` (string, optional): Filtrar por tipo
- `estado` (string, optional): Filtrar por estado

#### Ejemplo Request

```bash
# Obtener todas las alertas
curl http://localhost:8001/alerts

# Con filtros
curl "http://localhost:8001/alerts?tipo=Robo&limit=50&offset=0"

# Filtrar por estado
curl "http://localhost:8001/alerts?estado=activa"
```

#### Ejemplo Response (200 OK)

```json
{
  "total": 245,
  "limit": 100,
  "offset": 0,
  "data": [
    {
      "id": 42,
      "tipo": "Robo",
      "ubicacion": "CUCEI, Guadalajara",
      "descripcion": "Robo en estacionamiento",
      "estado": "activa",
      "timestamp": "2026-05-03T14:32:10.123456"
    },
    {
      "id": 41,
      "tipo": "Accidente",
      "ubicacion": "Av. Vallarta",
      "descripcion": "Choque vehicular",
      "estado": "resuelta",
      "timestamp": "2026-05-03T13:15:22.654321"
    }
  ]
}
```

---

### Obtener Alerta por ID

**Endpoint**: `GET /alerts/{id}`  
**Autenticación**: Opcional

#### Ejemplo Request

```bash
curl http://localhost:8001/alerts/42
```

#### Ejemplo Response (200 OK)

```json
{
  "id": 42,
  "tipo": "Robo",
  "ubicacion": "CUCEI, Guadalajara",
  "descripcion": "Robo en estacionamiento",
  "estado": "activa",
  "timestamp": "2026-05-03T14:32:10.123456"
}
```

#### Códigos HTTP

| Código | Descripción |
|--------|-------------|
| `200` | Éxito |
| `404` | Alerta no encontrada |
| `500` | Error del servidor |

---

### Actualizar Estado de Alerta

**Endpoint**: `PATCH /alerts/{id}`  
**Autenticación**: Requerida  
**Content-Type**: `application/json`

#### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `estado` | string | Nuevo estado: `activa`, `en_proceso`, `resuelta` |

#### Ejemplo Request

```bash
curl -X PATCH http://localhost:8001/alerts/42 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-seguro-safecity-2026" \
  -d '{
    "estado": "resuelta"
  }'
```

#### Ejemplo Response (200 OK)

```json
{
  "id": 42,
  "tipo": "Robo",
  "ubicacion": "CUCEI, Guadalajara",
  "estado": "resuelta",
  "timestamp": "2026-05-03T14:32:10.123456",
  "updated_at": "2026-05-03T14:45:33.456789"
}
```

---

### Eliminar Alerta

**Endpoint**: `DELETE /alerts/{id}`  
**Autenticación**: Requerida (Admin solo)

#### Ejemplo Request

```bash
curl -X DELETE http://localhost:8001/alerts/42 \
  -H "Authorization: Bearer token-admin-admin123"
```

#### Ejemplo Response (204 No Content)

```
(sin contenido)
```

---

### Health Check

**Endpoint**: `GET /`  
**Autenticación**: No requerida

#### Ejemplo Request

```bash
curl http://localhost:8001/
```

#### Ejemplo Response (200 OK)

```json
{
  "status": "healthy",
  "service": "SafeCity Alerts",
  "version": "2.6"
}
```

---

## 👤 Users Service

### Base URL
`http://localhost:8002` (o `http://users-service:8002` en Kubernetes)

### Login

Ver sección [Autenticación](#-autenticación) arriba.

### Obtener Información del Usuario

**Endpoint**: `GET /me`  
**Autenticación**: Requerida

#### Ejemplo Request

```bash
curl -H "Authorization: Bearer token-seguro-safecity-2026" \
  http://localhost:8002/me
```

#### Ejemplo Response (200 OK)

```json
{
  "username": "admin",
  "role": "admin",
  "permissions": [
    "alerts.create",
    "alerts.read",
    "alerts.update",
    "alerts.delete",
    "users.manage"
  ]
}
```

---

### Crear Usuario (Admin)

**Endpoint**: `POST /users`  
**Autenticación**: Requerida (Admin solo)  
**Content-Type**: `application/json`

#### Parámetros

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|----------|-------------|
| `username` | string | ✅ | Nombre único |
| `password` | string | ✅ | Contraseña |
| `role` | string | ✅ | `admin`, `supervisor`, `user` |

#### Ejemplo Request

```bash
curl -X POST http://localhost:8002/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-admin-admin123" \
  -d '{
    "username": "nuevo_usuario",
    "password": "password_seguro",
    "role": "supervisor"
  }'
```

#### Ejemplo Response (201 Created)

```json
{
  "id": 3,
  "username": "nuevo_usuario",
  "role": "supervisor",
  "created_at": "2026-05-03T14:32:10.123456"
}
```

---

### Listar Usuarios (Admin)

**Endpoint**: `GET /users`  
**Autenticación**: Requerida (Admin)

#### Ejemplo Request

```bash
curl -H "Authorization: Bearer token-admin-admin123" \
  http://localhost:8002/users
```

#### Ejemplo Response (200 OK)

```json
{
  "total": 3,
  "data": [
    {
      "id": 1,
      "username": "admin",
      "role": "admin",
      "created_at": "2026-01-01T00:00:00.000000"
    },
    {
      "id": 2,
      "username": "supervisor",
      "role": "supervisor",
      "created_at": "2026-02-15T10:30:22.123456"
    },
    {
      "id": 3,
      "username": "nuevo_usuario",
      "role": "user",
      "created_at": "2026-05-03T14:32:10.123456"
    }
  ]
}
```

---

### Health Check

**Endpoint**: `GET /`  
**Autenticación**: No requerida

#### Ejemplo Request

```bash
curl http://localhost:8002/
```

#### Ejemplo Response (200 OK)

```json
{
  "status": "healthy",
  "service": "Users & Auth Service",
  "version": "2.6"
}
```

---

## 🌐 Frontend Service

**Base URL**: `http://localhost` (Nginx serving static files)

### Obtener Dashboard

**Endpoint**: `GET /`  
**Content-Type**: `text/html`

#### Ejemplo Request

```bash
curl http://localhost/
```

#### Ejemplo Response (200 OK)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <title>SafeCity Pro - Centro de Comando</title>
    ...
</head>
<body>
    ...
</body>
</html>
```

---

## 📊 Ejemplos de Flujos

### Flujo 1: Crear y Listar Alertas

```bash
#!/bin/bash

# 1. Autenticarse
TOKEN=$(curl -s -X POST http://localhost:8002/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')

echo "Token obtenido: $TOKEN"

# 2. Crear alerta
curl -X POST http://localhost:8001/alerts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tipo": "Robo",
    "ubicacion": "CUCEI Campus",
    "descripcion": "Incidente de seguridad"
  }'

# 3. Listar alertas
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/alerts?limit=10
```

### Flujo 2: Filtrar Alertas por Tipo

```bash
# Obtener todas las alertas de tipo "Robo"
curl "http://localhost:8001/alerts?tipo=Robo&limit=50"
```

### Flujo 3: Actualizar Estado

```bash
TOKEN="token-aqui"

# Cambiar estado de alerta a "resuelta"
curl -X PATCH http://localhost:8001/alerts/42 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"estado": "resuelta"}'
```

---

## ⚠️ Códigos de Error

### 400 Bad Request
```json
{
  "detail": [
    {
      "loc": ["body", "tipo"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Alert not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "tipo"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## 📖 Documentación Interactiva

### Swagger UI (Recomendado)

- **Alerts Service**: http://localhost:8001/docs
- **Users Service**: http://localhost:8002/docs

### ReDoc (Alternativa)

- **Alerts Service**: http://localhost:8001/redoc
- **Users Service**: http://localhost:8002/redoc

---

## 🔗 Integración con Postman

### Importar Collection

1. Crear nueva colección en Postman
2. Crear requests:

```
POST {{base_url}}/login
POST {{base_url}}/alerts
GET {{base_url}}/alerts
PATCH {{base_url}}/alerts/{{alert_id}}
```

3. Usar variables de entorno:

```json
{
  "base_url": "http://localhost:8001",
  "token": "{{ obtener de login }}",
  "alert_id": "42"
}
```

---

## 🚀 Rate Limiting

Actualmente no hay limitaciones, pero se planea implementar:

- 100 requests/minuto por usuario
- 1000 requests/minuto por IP

---

## 📝 Changelog API

### v2.6 (Mayo 2026)
- ✅ Endpoints base funcionales
- ✅ Autenticación OAuth2
- ✅ CRUD de alertas

### v2.7 (Próximo)
- 🔄 Rate limiting
- 🔄 Paginación mejorada
- 🔄 Filtros avanzados

---

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://spec.openapis.org/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Última actualización**: Mayo 2026 | **Versión API**: 2.6
