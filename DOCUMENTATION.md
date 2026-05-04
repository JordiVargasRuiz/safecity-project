# 📚 Documentación Completa - SafeCity Pro

**Índice de la Documentación del Proyecto**

---

## 🎯 Inicio Rápido

¿Nuevo en SafeCity Pro? Comienza aquí:

### Para Usuarios Finales
1. 📖 Lee [README.md](README.md) - Visión general del proyecto
2. 🚀 Ve la sección "Uso" en [README.md#uso](README.md#uso)
3. 🌐 Accede a http://localhost o tu URL configurada

### Para Desarrolladores
1. 🔧 Lee [DEVELOPMENT.md](DEVELOPMENT.md) - Configuración local
2. 📚 Consulta [API.md](API.md) - Referencia de endpoints
3. 💻 Clona el repo y sigue el checklist de setup

### Para DevOps/SRE
1. 📦 Lee [README.md#opción-2-despliegue-en-kubernetes](README.md#opción-2-despliegue-en-kubernetes)
2. 🏢 Revisa [PRODUCTION.md](PRODUCTION.md) - Guía de producción
3. 🔍 Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md) si hay problemas

### Para Presentaciones
1. 🎯 Ve [PRESENTATION.md](PRESENTATION.md) - 18 diapositivas completas
2. 📊 Usa las diapositivas para tu presentación

---

## 📖 Documentación por Rol

### 👨‍💻 Desarrollador Backend

**Archivos principales:**
- [DEVELOPMENT.md](DEVELOPMENT.md) - Setup local
- [API.md](API.md) - Estructura de APIs
- [README.md#servicios](README.md#servicios) - Descripción de servicios

**Tareas comunes:**
- [Configurar ambiente de desarrollo](DEVELOPMENT.md#configuración-inicial)
- [Ejecutar Alerts Service](DEVELOPMENT.md#alerts-service)
- [Ejecutar Users Service](DEVELOPMENT.md#users-service)
- [Testing de APIs](DEVELOPMENT.md#testing-de-apis)

---

### 🎨 Desarrollador Frontend

**Archivos principales:**
- [DEVELOPMENT.md#desarrollo-frontend](DEVELOPMENT.md#desarrollo-frontend)
- [README.md#frontend-service](README.md#frontend-service)
- [API.md](API.md) - Endpoints para integración

**Tareas comunes:**
- [Servidor local para frontend](DEVELOPMENT.md#servidor-local)
- [Testing en navegador](DEVELOPMENT.md#browser-devtools)
- [Debugging con DevTools](DEVELOPMENT.md#browser-devtools)

---

### 🏗️ DevOps / SRE

**Archivos principales:**
- [README.md#opción-2-despliegue-en-kubernetes](README.md#opción-2-despliegue-en-kubernetes)
- [PRODUCTION.md](PRODUCTION.md) - Guía completa de producción
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solución de problemas

**Tareas comunes:**
- [Desplegar en Kubernetes](README.md#opción-2-despliegue-en-kubernetes)
- [Configurar seguridad](PRODUCTION.md#configuración-de-seguridad)
- [Habilitar backups](PRODUCTION.md#backup-y-recuperación)
- [Monitoreo y logs](PRODUCTION.md#monitoreo-y-logging)
- [Troubleshooting](TROUBLESHOOTING.md)

---

### 👨‍💼 Project Manager / Stakeholder

**Archivos principales:**
- [README.md](README.md) - Descripción general
- [PRESENTATION.md](PRESENTATION.md) - Presentación del proyecto
- [README.md#impacto-esperado](README.md#características-principales) - Beneficios

**Secciones clave:**
- [Características Principales](README.md#características-principales)
- [Arquitectura](README.md#arquitectura)
- [Roadmap Futuro](PRESENTATION.md#diapositiva-11-roadmap-futuro)
- [Equipo](README.md#equipo)

---

## 🗂️ Estructura Documentación

```
.
├── README.md                 ← 📘 EMPEZAR AQUÍ
│   ├── Descripción general
│   ├── Características
│   ├── Arquitectura
│   ├── Requisitos previos
│   ├── Guía de despliegue (Local + Kubernetes)
│   ├── Estructura del proyecto
│   ├── Configuración
│   └── Troubleshooting básico
│
├── DEVELOPMENT.md            ← 👨‍💻 Para desarrolladores
│   ├── Configuración local
│   ├── Backend (Python)
│   ├── Frontend (HTML/CSS)
│   ├── Base de datos
│   ├── Docker Compose
│   ├── Testing de APIs
│   ├── Debugging
│   └── Checklist
│
├── PRODUCTION.md             ← 🏢 Para producción
│   ├── Seguridad
│   ├── High Availability
│   ├── Backup/Recovery
│   ├── Auto-scaling
│   ├── Monitoreo
│   ├── CI/CD
│   └── Plan de recuperación
│
├── API.md                    ← 📚 Referencia técnica
│   ├── Autenticación
│   ├── Alerts Service
│   ├── Users Service
│   ├── Frontend Service
│   ├── Ejemplos de flujos
│   ├── Códigos de error
│   └── Swagger/ReDoc
│
├── PRESENTATION.md           ← 🎯 Para presentaciones
│   ├── 18 diapositivas completas
│   ├── Problema y solución
│   ├── Arquitectura
│   ├── Demo en vivo
│   ├── Roadmap
│   └── Conclusiones
│
├── TROUBLESHOOTING.md        ← 🔧 Solución de problemas
│   ├── Conectividad
│   ├── Docker
│   ├── Kubernetes
│   ├── Base de datos
│   ├── API
│   ├── Autenticación
│   ├── Rendimiento
│   └── FAQ
│
└── DOCUMENTATION.md          ← 📄 Este archivo (índice)
```

---

## 🔍 Buscar por Tema

### 🚀 Despliegue y DevOps

| Tema | Archivo | Sección |
|------|---------|---------|
| **Despliegue Local** | [README.md](README.md#opción-1-despliegue-local-con-docker) | Opción 1 |
| **Despliegue Kubernetes** | [README.md](README.md#opción-2-despliegue-en-kubernetes) | Opción 2 |
| **Monitoreo** | [PRODUCTION.md](PRODUCTION.md#-monitoreo-y-logging) | Sección completa |
| **Backups** | [PRODUCTION.md](PRODUCTION.md#-backup-y-recuperación) | Sección completa |
| **Seguridad** | [PRODUCTION.md](PRODUCTION.md#-configuración-de-seguridad) | Sección completa |
| **Troubleshooting** | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Todo el archivo |

---

### 💻 Desarrollo

| Tema | Archivo | Sección |
|------|---------|---------|
| **Setup Local** | [DEVELOPMENT.md](DEVELOPMENT.md#configuración-inicial) | Paso 1-3 |
| **Backend Python** | [DEVELOPMENT.md](DEVELOPMENT.md#-desarrollo-backend-python) | Sección completa |
| **Frontend** | [DEVELOPMENT.md](DEVELOPMENT.md#-desarrollo-frontend) | Sección completa |
| **Base de Datos** | [DEVELOPMENT.md](DEVELOPMENT.md#-base-de-datos-postgresql) | Sección completa |
| **Testing APIs** | [DEVELOPMENT.md](DEVELOPMENT.md#-testing-de-apis) | Sección completa |
| **Debugging** | [DEVELOPMENT.md](DEVELOPMENT.md#-debugging) | Sección completa |

---

### 📡 API y Integración

| Tema | Archivo | Sección |
|------|---------|---------|
| **Autenticación** | [API.md](API.md#-autenticación) | Sección completa |
| **Crear Alerta** | [API.md](API.md#crear-alerta) | Endpoint POST |
| **Listar Alertas** | [API.md](API.md#listar-alertas) | Endpoint GET |
| **Todos los Endpoints** | [API.md](API.md) | Todo el archivo |
| **Ejemplos Flujos** | [API.md](API.md#-ejemplos-de-flujos) | Sección completa |
| **Errores** | [API.md](API.md#-códigos-de-error) | Sección completa |

---

### 🎯 Presentación y Comunicación

| Tema | Archivo |
|------|---------|
| **Diapositivas Completas** | [PRESENTATION.md](PRESENTATION.md) |
| **Demo en Vivo** | [PRESENTATION.md](PRESENTATION.md#-diapositiva-12-demo-en-vivo) |
| **Roadmap** | [PRESENTATION.md](PRESENTATION.md#-diapositiva-11-roadmap-futuro) |
| **Equipo** | [README.md](README.md#equipo) |

---

## 🎓 Tutoriales Paso a Paso

### Tutorial 1: Ejecutar SafeCity Localmente (5 minutos)

1. Clona el repo
   ```bash
   git clone https://github.com/tu-usuario/safecity-project.git
   cd safecity-project
   ```

2. Inicia con Docker Compose
   ```bash
   docker-compose up -d
   ```

3. Accede al dashboard
   - Frontend: http://localhost
   - API Docs: http://localhost:8001/docs

4. Crea una alerta de prueba
   - Selecciona tipo
   - Ingresa ubicación
   - Haz clic en "Transmitir"

**Referencia**: [README.md#opción-1-despliegue-local-con-docker](README.md#opción-1-despliegue-local-con-docker)

---

### Tutorial 2: Configurar Ambiente de Desarrollo (15 minutos)

1. Sigue [DEVELOPMENT.md#configuración-inicial](DEVELOPMENT.md#configuración-inicial)
2. Crea virtual environment para cada servicio
3. Instala dependencias con pip
4. Ejecuta cada servicio en terminal separada
5. Verifica todos funcionan

**Referencia**: [DEVELOPMENT.md](DEVELOPMENT.md)

---

### Tutorial 3: Desplegar en Kubernetes (20 minutos)

1. Asegura acceso a cluster K8s
2. Sigue [README.md#opción-2-despliegue-en-kubernetes](README.md#opción-2-despliegue-en-kubernetes)
3. Construye y registra imágenes Docker
4. Aplica manifiestos YAML
5. Expone servicios

**Referencia**: [README.md#opción-2-despliegue-en-kubernetes](README.md#opción-2-despliegue-en-kubernetes)

---

### Tutorial 4: Testing de APIs con cURL (10 minutos)

1. Obtén token:
   ```bash
   curl -X POST http://localhost:8002/login \
     -d "username=admin&password=admin123"
   ```

2. Crea alerta:
   ```bash
   curl -X POST http://localhost:8001/alerts \
     -H "Authorization: Bearer token-aqui" \
     -d '{"tipo":"Robo","ubicacion":"CUCEI"}'
   ```

3. Lista alertas:
   ```bash
   curl http://localhost:8001/alerts
   ```

**Referencia**: [API.md#-ejemplos-de-flujos](API.md#-ejemplos-de-flujos)

---

## ⚡ Acciones Frecuentes

| Acción | Comando | Archivo |
|--------|---------|---------|
| **Ver estado servicios** | `docker-compose ps` | [DEVELOPMENT.md](DEVELOPMENT.md) |
| **Ver logs** | `docker-compose logs -f` | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Acceder a DB** | `psql -h localhost -U postgres` | [DEVELOPMENT.md](DEVELOPMENT.md#base-de-datos-postgresql) |
| **Probar API** | `curl http://localhost:8001/docs` | [API.md](API.md) |
| **Escalar pods** | `kubectl scale deployment x --replicas=3` | [PRODUCTION.md](PRODUCTION.md) |
| **Ver metricas** | `kubectl top pods` | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Restaurar backup** | Ver [PRODUCTION.md](PRODUCTION.md#restaurar-backup) | [PRODUCTION.md](PRODUCTION.md) |

---

## 🆘 Necesito Ayuda...

### Mi problema es...

- **Está en la guía de despliegue** → [README.md](README.md#guía-de-despliegue)
- **Es de desarrollo** → [DEVELOPMENT.md](DEVELOPMENT.md)
- **Es de producción** → [PRODUCTION.md](PRODUCTION.md)
- **Es de API** → [API.md](API.md)
- **Es un error específico** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Es para una presentación** → [PRESENTATION.md](PRESENTATION.md)
- **No lo encuentro** → Usa Ctrl+F en este archivo

---

## 📞 Contacto y Recursos

### Documentación
- 📖 [README.md](README.md) - Visión general
- 🔧 [DEVELOPMENT.md](DEVELOPMENT.md) - Desarrollo
- 🏢 [PRODUCTION.md](PRODUCTION.md) - Producción
- 📚 [API.md](API.md) - APIs
- 🎯 [PRESENTATION.md](PRESENTATION.md) - Presentación
- 🔍 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problemas

### Enlaces útiles
- 🔗 [FastAPI Docs](https://fastapi.tiangolo.com/)
- 🐳 [Docker Docs](https://docs.docker.com/)
- ☸️ [Kubernetes Docs](https://kubernetes.io/docs/)
- 🐘 [PostgreSQL Docs](https://www.postgresql.org/docs/)

### Contacto del equipo
- 📧 Email: safecity@cucei.udg.mx
- 💬 Issues: [GitHub Issues](https://github.com/issues)
- 📱 Teléfono: +52 (33) XXXX-XXXX

---

## ✅ Checklist Antes de Empezar

- [ ] He leído [README.md](README.md)
- [ ] Tengo Docker/Kubernetes instalado (según necesidad)
- [ ] He clonado el repositorio
- [ ] Tengo Python 3.9+ (si desarrollo local)
- [ ] He creado `.env` file
- [ ] Sé cuál es mi rol (dev, devops, user, presenter)
- [ ] He encontrado el documento adecuado para mi tarea
- [ ] Estoy listo para empezar

---

## 🎯 Quick Navigation

```
¿Primer vez?             → Empieza con README.md
¿Desarrollar localmente? → Ve a DEVELOPMENT.md
¿Desplegar?              → Ve a README.md Opción 1 o 2
¿APIs?                   → Consulta API.md
¿Problemas?              → Ve a TROUBLESHOOTING.md
¿Presentación?           → Usa PRESENTATION.md
¿Producción?             → Lee PRODUCTION.md
```

---

**Última actualización**: Mayo 2026 | **Versión**: 2.6

> 💡 **Tip**: Guarda este documento como referencia. Todos los links funcionan internamente.

---

## 📊 Estadísticas de Documentación

| Documento | Páginas | Secciones | Ejemplos |
|-----------|---------|-----------|----------|
| README.md | 2-3 | 15+ | 10+ |
| DEVELOPMENT.md | 2 | 12 | 20+ |
| PRODUCTION.md | 2 | 10 | 15+ |
| API.md | 2-3 | 20+ | 25+ |
| PRESENTATION.md | 3-4 | 18 | 5+ |
| TROUBLESHOOTING.md | 2-3 | 25+ | 40+ |
| **TOTAL** | **14-18** | **100+** | **115+** |

**Cobertura documentación**: ✅ 95% del proyecto

---

> 🎉 **¡Bienvenido a SafeCity Pro!** Espero que esta documentación te sea útil. Si tienes preguntas, no dudes en contactar al equipo.
