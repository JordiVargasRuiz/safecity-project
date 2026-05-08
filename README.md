# SafeCity Pro 🚨

**Centro de Comando Inteligente para Gestión de Alertas en Tiempo Real**

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com) [![Version](https://img.shields.io/badge/version-2.6-blue)](https://github.com) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org) [![Kubernetes](https://img.shields.io/badge/kubernetes-ready-brightblue)](https://kubernetes.io)

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características Principales](#características-principales)
- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Guía de Despliegue](#guía-de-despliegue)
  - [Opción 1: Despliegue Local con Docker](#opción-1-despliegue-local-con-docker)
  - [Opción 2: Despliegue en Kubernetes](#opción-2-despliegue-en-kubernetes)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Servicios](#servicios)
- [Configuración](#configuración)
- [Uso](#uso)
- [Troubleshooting](#troubleshooting)
- [Contribuciones](#contribuciones)
- [Equipo](#equipo)

---

## 📖 Descripción del Proyecto

**SafeCity Pro** es una plataforma de monitoreo y gestión de alertas en tiempo real. Proporciona un **centro de comando centralizado** que permite:

- 🎯 Recibir y gestionar múltiples tipos de alertas (robos, accidentes, vandalismo, etc.)
- 📊 Visualizar incidentes en tiempo real mediante dashboards interactivos
- 🔐 Autenticación y control de acceso basado en roles
- 📱 API RESTful escalable con microservicios
- ☁️ Despliegue en contenedores y orquestación con Kubernetes

El proyecto está optimizado para el campus de **Guadalajara** y es completamente escalable para múltiples ubicaciones.

---

## ✨ Características Principales

| Característica | Descripción |
|---|---|
| **Dashboard Interactivo** | Interfaz moderna con diseño glassmorphism y actualizaciones en tiempo real |
| **Gestión de Alertas** | Crear, rastrear y resolver incidentes de múltiples categorías |
| **Autenticación Segura** | Sistema de login con tokens OAuth2 |
| **API RESTful** | Endpoints documentados con FastAPI (Swagger/OpenAPI) |
| **Base de Datos** | PostgreSQL para persistencia de datos |
| **Microservicios** | Arquitectura desacoplada: Users, Alerts, Frontend |
| **Kubernetes Ready** | Manifiestos YAML completos para despliegue en K8s |
| **Escalabilidad** | Soporte para múltiples réplicas y load balancing |

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                     Frontend (Nginx)                 │
│         Dashboard Interactivo (HTML/CSS/JS)         │
└────────┬────────────────────────────────┬───────────┘
         │                                │
         ▼                                ▼
┌──────────────────────┐        ┌──────────────────────┐
│   Alerts Service     │        │    Users Service     │
│   (FastAPI/Python)   │        │  (FastAPI/Python)    │
│  Port: 8001          │        │  Port: 8002          │
└──────────┬───────────┘        └──────────┬───────────┘
           │                               │
           └───────────────┬───────────────┘
                           │
                           ▼
                    ┌──────────────────┐
                    │   PostgreSQL DB  │
                    │    Port: 5432    │
                    └──────────────────┘
```

### Flujo de Datos

1. **Usuario** accede al dashboard frontend
2. **Usuarios** emiten alertas al Alerts Service
3. **Alerts Service** valida y almacena en PostgreSQL
4. **Dashboard** recibe actualizaciones en tiempo real
<img width="1919" height="990" alt="image" src="https://github.com/user-attachments/assets/45507eca-3541-478f-b6cd-2bd2771a4e43" />

---

## 📋 Requisitos Previos

### Para Despliegue Local:
- Docker y Docker Compose instalados (v20.10+)
- Python 3.9+ (para desarrollo local)
- 2GB de RAM mínimo disponible
<img width="1917" height="400" alt="image" src="https://github.com/user-attachments/assets/d0b441ec-130a-41b1-ab31-6a4cbe2f01b4" />

### Para Despliegue en Kubernetes:
- Kubernetes cluster (v1.20+) accesible
- `kubectl` configurado y conectado al cluster
- 4GB de RAM y 2 CPU cores disponibles
- Helm (opcional, para gráficos personalizados)

### Herramientas Recomendadas:
- Visual Studio Code con Docker extension
- Postman o similar para testing de APIs
- `watch` command para monitoreo de pods

---

## 🚀 Guía de Despliegue

### Opción 1: Despliegue Local con Docker

#### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/safecity-project.git
cd safecity-project
```

#### Paso 2: Construir Imágenes Docker

```bash
# Construir imagen de Alerts Service
docker build -t safecity-alerts:latest ./services/alerts

# Construir imagen de Users Service
docker build -t safecity-users:latest ./services/users

# Construir imagen de Frontend
docker build -t safecity-frontend:latest ./services/frontend
```

#### Paso 3: Crear Docker Compose (Opcional - si no existe)

Crea un archivo `docker-compose.yml` en la raíz del proyecto:

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: safepass123
      POSTGRES_DB: safecity_alerts
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  alerts-service:
    build: ./services/alerts
    ports:
      - "8001:8000"
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PASSWORD: safepass123
      POSTGRES_DB: safecity_alerts
    restart: unless-stopped

  users-service:
    build: ./services/users
    ports:
      - "8002:8000"
    restart: unless-stopped

  frontend:
    build: ./services/frontend
    ports:
      - "80:80"
    depends_on:
      - alerts-service
      - users-service
    restart: unless-stopped

volumes:
  postgres-data:
```

#### Paso 4: Iniciar Servicios

```bash
# Con Docker Compose
docker-compose up -d

# Esperar a que todos los servicios estén saludables
docker-compose ps

# Ver logs
docker-compose logs -f
```

---

### Opción 2: Despliegue en Kubernetes

#### Paso 1: Preparar el Cluster

```bash
# Verificar conexión a cluster
kubectl cluster-info

# Crear namespace para SafeCity
kubectl create namespace safecity
kubectl config set-context --current --namespace=safecity

# Verificar acceso
kubectl get nodes
```

#### Paso 2: Construir y Registrar Imágenes

```bash
# Opción A: Usar Docker Hub (requiere cuenta)
docker tag safecity-alerts:latest tu-docker-user/safecity-alerts:latest
docker push tu-docker-user/safecity-alerts:latest

docker tag safecity-users:latest tu-docker-user/safecity-users:latest
docker push tu-docker-user/safecity-users:latest

docker tag safecity-frontend:latest tu-docker-user/safecity-frontend:latest
docker push tu-docker-user/safecity-frontend:latest

# Opción B: Usar registro local (para desarrollo)
# (Consultar documentación de tu cluster K8s)
```

#### Paso 3: Actualizar Manifiestos Kubernetes

En `k8s/`, actualiza las imágenes en los archivos YAML según tu registro:

```yaml
# Ejemplo: k8s/alerts-deployment.yaml
image: tu-docker-user/safecity-alerts:latest
```

#### Paso 4: Desplegar en Kubernetes

```bash
# Desplegar PostgreSQL
kubectl apply -f k8s/postgres-db.yaml

# Esperar a que PostgreSQL esté listo
kubectl wait --for=condition=ready pod -l app=postgres -n safecity --timeout=300s

# Desplegar Alerts Service
kubectl apply -f k8s/alerts-deployment.yaml

# Desplegar Users Service
kubectl apply -f k8s/users-deployment.yaml

# Desplegar Frontend
kubectl apply -f k8s/frontend-deployment.yaml

# Verificar deployments
kubectl get deployments -n safecity
kubectl get pods -n safecity
```

#### Paso 5: Exponer Servicios

```bash
# Para acceso local/interno
kubectl get svc -n safecity

# Para exposición externa (usar uno de estos):

# Opción A: Port-forward (desarrollo)
kubectl port-forward svc/frontend-service 80:80 -n safecity

# Opción B: NodePort (simple)
kubectl patch svc frontend-service -p '{"spec":{"type":"NodePort"}}' -n safecity

# Opción C: LoadBalancer (producción)
kubectl patch svc frontend-service -p '{"spec":{"type":"LoadBalancer"}}' -n safecity
```

#### Paso 6: Monitorear Despliegue

```bash
# Ver estado de pods
kubectl get pods -n safecity -w


# Ver logs de un servicio
kubectl logs -f deployment/alerts-service -n safecity

# Ver eventos del cluster
kubectl describe pod <pod-name> -n safecity

# Acceder a shell del contenedor
kubectl exec -it <pod-name> -n safecity -- /bin/bash
```
<img width="584" height="255" alt="image" src="https://github.com/user-attachments/assets/8a80dcff-4baf-41d5-8ead-3ddfc6c296e3" />

---

## 📁 Estructura del Proyecto

```
safecity-project/
├── README.md                          # Este archivo
├── docker-compose.yml                 # Configuración Docker Compose
├── .gitignore
│
├── k8s/                              # Manifiestos Kubernetes
│   ├── postgres-db.yaml              # Base de datos PostgreSQL
│   ├── alerts-deployment.yaml        # Deployment Alerts Service
│   ├── users-deployment.yaml         # Deployment Users Service
│   └── frontend-deployment.yaml      # Deployment Frontend
│
├── scripts/                          # Scripts de utilidad
│   └── ...
│
└── services/                         # Microservicios
    ├── alerts/
    │   ├── main.py                   # Endpoint para gestión de alertas
    │   ├── requirements.txt           # Dependencias Python
    │   └── Dockerfile                # Imagen Docker
    │
    ├── users/
    │   ├── main.py                   # Endpoint autenticación y usuarios
    │   ├── requirements.txt
    │   └── Dockerfile
    │
    ├── frontend/
    │   ├── index.html                # Dashboard interactivo
    │   └── Dockerfile                # Nginx configuration
    │
    └── process/                      # (Próximos servicios)
```

---

## 🔧 Servicios

### 1. **Frontend Service** 
- **Puerto**: 8080
- **Tecnología**: HTML5, CSS3, Tailwind CSS, JavaScript
- **Funcionalidad**: Dashboard de monitoreo en tiempo real
- **Features**:
  - Interfaz glassmorphism moderna
  - Formulario de emisión de alertas
  - Historial de incidentes
  - Clock en tiempo real
<img width="1919" height="990" alt="image" src="https://github.com/user-attachments/assets/c299856b-c3d5-4172-a583-38fd54b89d04" />


### 2. **PostgreSQL Database**
- **Puerto**: 5432
- **Database**: `safecity_alerts`
- **User**: `postgres`
- **Password**: `safepass123` (cambiar en producción)

---

## ⚙️ Configuración

### Variables de Entorno

```bash
# PostgreSQL
POSTGRES_PASSWORD=safepass123
POSTGRES_DB=safecity_alerts
POSTGRES_USER=postgres

# Servicios
DATABASE_HOST=postgres-service
DATABASE_PORT=5432
FASTAPI_ENV=production

```

### Archivos de Configuración

- **K8s**: Todos los manifiestos están en `k8s/`
- **Docker Compose**: Ver `docker-compose.yml`
- **Variables**: Se pueden sobrescribir con ConfigMaps en K8s

---

## 💻 Uso

### Accediendo al Dashboard

1. **Local**: `http://localhost:8080/`
2. **Kubernetes**: 
   ```bash
   kubectl port-forward svc/frontend-service 80:80 -n safecity
   # Luego: http://localhost:8080/
   ```

### Crear una Alerta

1. Ir al dashboard
2. Seleccionar tipo de incidente (Robo, Accidente, Vandalismo)
3. Ingresar ubicación
4. Hacer clic en "Transmitir"
<img width="1919" height="571" alt="image" src="https://github.com/user-attachments/assets/a9157bbc-6a7e-45e7-be7f-5b5ef200bdad" />

---

## 🔍 Troubleshooting

### Problema: Servicios no se conectan
```bash
# Verificar conectividad entre contenedores
docker-compose exec alerts-service ping postgres
docker-compose logs postgres

# En Kubernetes
kubectl logs deployment/alerts-service -n safecity
kubectl get endpoints -n safecity
```

### Problema: PostgreSQL no inicia
```bash
# Verificar volúmenes
docker volume ls
docker volume inspect safecity-project_postgres-data

# Recrear
docker-compose down -v
docker-compose up -d
```

### Problema: Permisos en Kubernetes
```bash
# Verificar RBAC
kubectl auth can-i create deployments --as=system:serviceaccount:safecity:default

# Debug de service discovery
kubectl run -it --image=busybox --restart=Never -- nslookup postgres-service
```

### Problema: Puertos en uso
```bash
# Docker
docker ps  # Identificar puerto en uso
docker stop <container-id>
docker rm <container-id>

# Sistema local (Windows)
netstat -ano | findstr :80
taskkill /PID <PID> /F
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 👥 Equipo

**SafeCity Pro** es desarrollado por el equipo de:
- **CUCEI - Centro Universitario de Ciencias Exactas e Ingenierías**
- **Universidad de Guadalajara**

### Contacto
- 📧 Email: safecity@cucei.udg.mx
- 🔗 Repositorio: [github.com/JordiVargasRuiz/safecity-project](https://github.com)
- 📱 Issues: [Reportar problemas](https://github.com/JordiVargasRuiz/safecity-project/issues)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 📚 Documentación Adicional

- [Guía de Desarrollo Local](DEVELOPMENT.md)
- [Guía de Producción](PRODUCTION.md)
- [Troubleshooting Avanzado](TROUBLESHOOTING.md)

---

## 🎉 Estado del Proyecto

- ✅ Frontend Interactivo
- ✅ API Alerts Service
- ✅ Servicio de Autenticación
- ✅ Base de Datos PostgreSQL
- ✅ Manifiestos Kubernetes
- 🔄 Sistema de Notificaciones (En desarrollo)
- 🔄 Gráficos de Estadísticas (En desarrollo)
- 🔄 Integración con SMS/Email (Próximo)

---

**Última actualización**: Mayo 2026 | **Versión**: 2.6

---

> 🚨 **Aviso**: Este es un sistema de demostración educativo. Para producción, implementar seguridad adicional, encriptación, y auditoría completa.
