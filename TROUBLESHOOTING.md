# 🔧 Troubleshooting - Guía de Solución de Problemas

Soluciones para problemas comunes en SafeCity Pro.

---

## 📋 Tabla de Contenidos

- [Problemas de Conectividad](#problemas-de-conectividad)
- [Problemas de Docker](#problemas-de-docker)
- [Problemas de Kubernetes](#problemas-de-kubernetes)
- [Problemas de Base de Datos](#problemas-de-base-de-datos)
- [Problemas de API](#problemas-de-api)
- [Problemas de Autenticación](#problemas-de-autenticación)
- [Problemas de Rendimiento](#problemas-de-rendimiento)
- [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 🌐 Problemas de Conectividad

### Problema: No puedo acceder a http://localhost

**Síntomas**:
- `Connection refused`
- `ERR_CONNECTION_REFUSED`

**Soluciones**:

```bash
# 1. Verificar que Docker está corriendo
docker ps

# 2. Verificar si el contenedor está activo
docker-compose ps

# 3. Ver logs
docker-compose logs frontend

# 4. Reiniciar servicios
docker-compose restart

# 5. Verificar puerto no esté en uso
# Windows:
netstat -ano | findstr :80
# macOS/Linux:
lsof -i :80

# 6. Matar proceso en el puerto
# Windows:
taskkill /PID <PID> /F
# macOS/Linux:
kill -9 <PID>
```

---

### Problema: Servicios no se comunican entre sí

**Síntomas**:
- Frontend no puede conectarse a API
- Error: `ECONNREFUSED`

**Soluciones**:

```bash
# 1. Verificar que todos los servicios están corriendo
docker-compose ps

# 2. Probar conectividad entre contenedores
docker-compose exec frontend ping alerts-service
docker-compose exec alerts-service ping postgres

# 3. Verificar DNS resolution
docker-compose exec frontend nslookup alerts-service

# 4. Revisar network
docker network ls
docker network inspect safecity-project_default

# 5. Recrear network
docker-compose down
docker network prune
docker-compose up -d
```

---

## 🐳 Problemas de Docker

### Problema: "Layer already exists"

**Síntomas**:
- Error al construir imagen
- Build lento

**Soluciones**:

```bash
# 1. Limpiar images sin usar
docker image prune

# 2. Limpiar volumes sin usar
docker volume prune

# 3. Limpiar todo (WARNING: elimina datos)
docker system prune -a

# 4. Rebuild sin cache
docker-compose build --no-cache
```

---

### Problema: "No space left on device"

**Síntomas**:
- Error al crear contenedor
- Disk space issue

**Soluciones**:

```bash
# 1. Verificar espacio disponible
docker system df

# 2. Limpiar logs
docker container prune
docker volume prune

# 3. Borrar images antiguas
docker image ls
docker rmi <image-id>

# 4. Revisar system disk
# Windows: C: Drive
# macOS/Linux: df -h

# 5. Aumentar límite de Docker Desktop
# Preferencias → Resources → Disk Image Size
```

---

### Problema: Contenedor crashea inmediatamente

**Síntomas**:
- Container exits immediately
- Status: Exited (1)

**Soluciones**:

```bash
# 1. Ver logs
docker-compose logs <service-name>

# 2. Ejecutar con modo interactivo
docker-compose run --rm alerts-service /bin/bash

# 3. Revisar Dockerfile
cat services/alerts/Dockerfile

# 4. Verificar requirements.txt
cat services/alerts/requirements.txt

# 5. Test local
cd services/alerts
python main.py
```

---

### Problema: PostgreSQL no inicia

**Síntomas**:
- `FATAL: could not create shared memory segment`
- `ERROR: could not initialize database`

**Soluciones**:

```bash
# 1. Verificar volume
docker volume ls | grep postgres

# 2. Inspeccionar volume
docker volume inspect safecity-project_postgres-data

# 3. Eliminar volume (borrará datos)
docker volume rm safecity-project_postgres-data

# 4. Limpiar completamente
docker-compose down -v
docker-compose up -d

# 5. Verificar permisos (en Linux)
chmod 755 /var/lib/docker/volumes/safecity-project_postgres-data/_data

# 6. Ver logs PostgreSQL
docker-compose logs postgres
```

---

## ☸️ Problemas de Kubernetes

### Problema: Pod en estado "Pending"

**Síntomas**:
- `kubectl get pods` muestra STATUS: Pending
- No inicia

**Soluciones**:

```bash
# 1. Describir pod
kubectl describe pod <pod-name> -n safecity

# 2. Ver eventos
kubectl get events -n safecity --sort-by='.lastTimestamp'

# 3. Verificar recursos disponibles
kubectl top nodes
kubectl top pods -n safecity

# 4. Revisar requests/limits
kubectl get deployment <deployment> -o yaml | grep -A 10 "resources:"

# 5. Actualizar recursos si es necesario
kubectl set resources deployment <deployment> \
  --requests=cpu=100m,memory=256Mi \
  --limits=cpu=500m,memory=512Mi \
  -n safecity
```

---

### Problema: Pod en estado "CrashLoopBackOff"

**Síntomas**:
- STATUS: CrashLoopBackOff
- Reinicia constantemente

**Soluciones**:

```bash
# 1. Ver logs
kubectl logs <pod-name> -n safecity
kubectl logs <pod-name> -n safecity --previous

# 2. Ver todos los logs (últimas N líneas)
kubectl logs -f <pod-name> -n safecity --tail=100

# 3. Describir pod
kubectl describe pod <pod-name> -n safecity

# 4. Shell al contenedor (si inicia)
kubectl exec -it <pod-name> -n safecity -- /bin/bash

# 5. Aumentar restart policy backoff
kubectl patch deployment <deployment> -p \
  '{"spec":{"template":{"spec":{"restartPolicy":"Never"}}}}' \
  -n safecity

# 6. Scale a 0 y luego a 1
kubectl scale deployment <deployment> --replicas=0 -n safecity
kubectl scale deployment <deployment> --replicas=1 -n safecity
```

---

### Problema: ImagePullBackOff

**Síntomas**:
- `Failed to pull image`
- `IMAGE_PULL_BACK_OFF`

**Soluciones**:

```bash
# 1. Verificar nombre de imagen
kubectl describe pod <pod-name> -n safecity | grep Image

# 2. Verificar imagen existe
docker image ls

# 3. Verificar credenciales de registry
kubectl get secrets -n safecity

# 4. Crear secret si usa registry privado
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<password> \
  -n safecity

# 5. Actualizar imagePullSecrets en deployment
kubectl patch deployment <deployment> -p \
  '{"spec":{"template":{"spec":{"imagePullSecrets":[{"name":"regcred"}]}}}}' \
  -n safecity
```

---

### Problema: Service no tiene EXTERNAL-IP

**Síntomas**:
- `kubectl get svc` muestra EXTERNAL-IP: <pending>

**Soluciones**:

```bash
# 1. Verificar tipo de service
kubectl get svc -n safecity

# 2. Cambiar a NodePort
kubectl patch svc <service> -p '{"spec":{"type":"NodePort"}}' -n safecity

# 3. Cambiar a LoadBalancer (cloud only)
kubectl patch svc <service> -p '{"spec":{"type":"LoadBalancer"}}' -n safecity

# 4. Port-forward temporal
kubectl port-forward svc/<service> 8080:80 -n safecity

# 5. Verificar ingress (si está configurado)
kubectl get ingress -n safecity
kubectl describe ingress -n safecity
```

---

### Problema: No hay suficientes recursos

**Síntomas**:
- `Insufficient cpu`, `Insufficient memory`
- Pods no schedulean

**Soluciones**:

```bash
# 1. Ver recursos del cluster
kubectl describe nodes

# 2. Ver uso actual
kubectl top nodes
kubectl top pods -n safecity

# 3. Reducir requests/limits
kubectl set resources deployment <deployment> \
  --requests=cpu=50m,memory=128Mi \
  -n safecity

# 4. Usar nodeSelector
kubectl label nodes <node-name> tier=production
# Luego en deployment YAML:
# nodeSelector:
#   tier: production

# 5. Agregar más nodos (si es posible)
# Depende del cloud provider
```

---

## 💾 Problemas de Base de Datos

### Problema: "Connection refused" a PostgreSQL

**Síntomas**:
- `psycopg2.OperationalError: connection refused`
- API no puede conectarse a DB

**Soluciones**:

```bash
# 1. Verificar que PostgreSQL está corriendo
kubectl get pods -l app=postgres -n safecity

# 2. Verificar service existe
kubectl get svc postgres-service -n safecity

# 3. Probar conectividad desde otro pod
kubectl run -it --image=postgres:14 --restart=Never -- \
  psql -h postgres-service -U postgres -d safecity_alerts -c "SELECT version();" \
  -n safecity

# 4. Ver logs de PostgreSQL
kubectl logs -f deployment/postgres-db -n safecity

# 5. Verificar variables de entorno
kubectl get configmap -n safecity
kubectl describe configmap <configmap> -n safecity

# 6. Recrear deployment
kubectl delete pod -l app=postgres -n safecity
```

---

### Problema: "Database already exists"

**Síntomas**:
- Error al crear base de datos
- `ERROR: database "safecity_alerts" already exists`

**Soluciones**:

```bash
# 1. Verificar bases de datos existentes
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -l

# 2. Dropear base de datos (cuidado)
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -c "DROP DATABASE safecity_alerts;"

# 3. Recrear
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -c "CREATE DATABASE safecity_alerts;"

# 4. O limpiar el PersistentVolume
kubectl delete pvc postgres-pvc -n safecity
# El pod recreará la DB
```

---

### Problema: Datos corruptos o inconsistentes

**Síntomas**:
- Queries retornan errores
- Data duplicate o missing

**Soluciones**:

```bash
# 1. Verificar integridad
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -d safecity_alerts -c \
  "SELECT pg_database.datname, 
          pg_size_pretty(pg_database_size(pg_database.datname)) 
   FROM pg_database;"

# 2. Ejecutar VACUUM y ANALYZE
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -d safecity_alerts -c "VACUUM ANALYZE;"

# 3. Restaurar desde backup
# Ver sección de Backups en PRODUCTION.md

# 4. Recriar tablas desde schema
# Revisar SQL schema y recrear
```

---

## 🔌 Problemas de API

### Problema: "502 Bad Gateway"

**Síntomas**:
- Error 502 al acceder a API
- `Bad Gateway`

**Soluciones**:

```bash
# 1. Verificar que servicio está corriendo
kubectl get pods -l app=alerts -n safecity

# 2. Ver logs del servicio
kubectl logs deployment/alerts-service -n safecity

# 3. Healthcheck del servicio
kubectl exec -it <alerts-pod> -n safecity -- \
  curl http://localhost:8000/

# 4. Reiniciar deployment
kubectl rollout restart deployment/alerts-service -n safecity

# 5. Verificar conectividad a DB desde pod
kubectl exec -it <alerts-pod> -n safecity -- /bin/bash
# Dentro del pod:
# psql -h postgres-service -U postgres -d safecity_alerts -c "SELECT 1;"
```

---

### Problema: "401 Unauthorized"

**Síntomas**:
- Error 401 en endpoints protegidos
- `Invalid authentication credentials`

**Soluciones**:

```bash
# 1. Verificar token
echo $TOKEN

# 2. Obtener nuevo token
TOKEN=$(curl -s -X POST http://localhost:8002/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')

# 3. Usar token en request
curl -H "Authorization: Bearer $TOKEN" http://localhost:8001/alerts

# 4. Verificar tiempo de expiración del token
# Ver código en users/main.py

# 5. Verificar configuración de CORS
kubectl get configmap -n safecity
kubectl describe configmap <configmap> -n safecity
```

---

### Problema: "422 Unprocessable Entity"

**Síntomas**:
- Error 422 al enviar datos
- `validation error`

**Soluciones**:

```bash
# 1. Revisar esquema esperado
curl http://localhost:8001/docs

# 2. Verificar tipos de datos
# Ejemplo: tipo debe ser string de lista válida
curl -X POST http://localhost:8001/alerts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tipo": "Robo",
    "ubicacion": "CUCEI"
  }'

# 3. Ver respuesta detallada
curl -X POST http://localhost:8001/alerts \
  -H "Content-Type: application/json" \
  -d '{"tipo": "invalid"}' | jq .

# 4. Revisar código en services/alerts/main.py
```

---

## 🔐 Problemas de Autenticación

### Problema: "Invalid credentials"

**Síntomas**:
- Login falla con credenciales correctas
- `Credenciales incorrectas`

**Soluciones**:

```bash
# 1. Verificar usuario existe
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -d safecity_alerts -c \
  "SELECT * FROM usuarios;"

# 2. Verificar contraseña (no debe estar en plaintext)
# Revisar users/main.py para ver cómo se hashean

# 3. Crear nuevo usuario
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -d safecity_alerts << EOF
INSERT INTO usuarios (username, password, role) 
VALUES ('admin', 'admin123', 'admin');
EOF

# 4. Reset de contraseña
# Ejecutar script desde terminal del pod
```

---

### Problema: CORS errors

**Síntomas**:
- `Cross-Origin Request Blocked`
- Browser console muestra error

**Soluciones**:

```bash
# 1. Verificar CORS configurado en FastAPI
# services/alerts/main.py debe tener:
# app.add_middleware(CORSMiddleware, allow_origins=["*"])

# 2. Ver headers CORS
curl -H "Origin: http://localhost" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS http://localhost:8001/alerts -v

# 3. Actualizar CORS en deployment
# Env var: CORS_ORIGINS="http://localhost,https://safecity.com"

# 4. Debuggear en desarrollo
# Usar browser DevTools → Network tab
```

---

## ⚡ Problemas de Rendimiento

### Problema: API Lenta

**Síntomas**:
- Requests tardan > 1 segundo
- Dashboard sin respuesta

**Soluciones**:

```bash
# 1. Ver métricas
kubectl top pods -n safecity

# 2. Revisar queries de DB
kubectl logs deployment/alerts-service -n safecity | grep "slow query"

# 3. Aumentar recursos
kubectl set resources deployment alerts-service \
  --requests=cpu=200m,memory=512Mi \
  --limits=cpu=1000m,memory=1Gi \
  -n safecity

# 4. Crear índices en DB
kubectl exec -it <postgres-pod> -n safecity -- \
  psql -U postgres -d safecity_alerts << EOF
CREATE INDEX idx_tipo ON alerts(tipo);
CREATE INDEX idx_timestamp ON alerts(timestamp);
EOF

# 5. Habilitar caching
# En FastAPI: usar @cache_control
```

---

### Problema: High CPU Usage

**Síntomas**:
- CPU 100%
- Pods lentísimos

**Soluciones**:

```bash
# 1. Identificar pod problemático
kubectl top pods -n safecity --sort-by=cpu

# 2. Ver logs
kubectl logs <pod-name> -n safecity

# 3. Scale horizontalmente
kubectl scale deployment <deployment> --replicas=3 -n safecity

# 4. Habilitar HPA
kubectl apply -f k8s/hpa.yaml

# 5. Revisar infinitos loops
# En código de servicios
```

---

### Problema: Memory Leak

**Síntomas**:
- Memoria aumenta constantemente
- Pod eventualmente crashea

**Soluciones**:

```bash
# 1. Monitorear memoria
kubectl top pods -n safecity --watch

# 2. Ver límite configurado
kubectl describe pod <pod-name> -n safecity | grep -A 5 "Limits"

# 3. Revisar código Python
# Buscar referencias circulares, closures no cerradas

# 4. Usar herramientas de profiling
# pip install memory-profiler
# @profile decorator en código

# 5. Reiniciar pod
kubectl rollout restart deployment <deployment> -n safecity
```

---

## ❓ Preguntas Frecuentes

### P: ¿Cómo reseteo todo?

```bash
# Docker
docker-compose down -v
docker-compose up -d

# Kubernetes
kubectl delete namespace safecity
kubectl create namespace safecity
kubectl apply -f k8s/
```

---

### P: ¿Cómo backup mis datos?

```bash
# PostgreSQL
kubectl exec -it <postgres-pod> -n safecity -- \
  pg_dump -U postgres safecity_alerts > backup.sql

# O usar herramienta de backup programada (ver PRODUCTION.md)
```

---

### P: ¿Cómo veo logs en tiempo real?

```bash
# Docker
docker-compose logs -f <service>

# Kubernetes
kubectl logs -f deployment/<deployment> -n safecity
kubectl logs -f <pod-name> -n safecity

# Múltiples pods
kubectl logs -f -l app=alerts -n safecity
```

---

### P: ¿Cómo cambio el puerto?

```bash
# Docker
# Editar docker-compose.yml:
# ports:
#   - "9001:8000"

# Kubernetes
# Editar deployment YAML:
# ports:
#   - containerPort: 8000
# Luego: kubectl apply -f k8s/

# O cambiar service type:
kubectl patch svc alerts-service -p '{"spec":{"ports":[{"port":9001,"targetPort":8000}]}}' -n safecity
```

---

### P: ¿Cómo escalable horizontalmente?

```bash
# Aumentar replicas
kubectl scale deployment alerts-service --replicas=5 -n safecity

# Habilitar auto-scaling
kubectl apply -f k8s/hpa.yaml
```

---

### P: ¿Cómo conecto a shell del contenedor?

```bash
# Docker
docker-compose exec <service> /bin/bash

# Kubernetes
kubectl exec -it <pod-name> -n safecity -- /bin/bash

# Si no hay bash, usar sh
kubectl exec -it <pod-name> -n safecity -- /bin/sh
```

---

## 📞 Escalación y Soporte

Si el problema persiste:

1. Recopilar información:
   ```bash
   kubectl describe pod <pod> -n safecity
   kubectl logs <pod> -n safecity
   kubectl get events -n safecity --sort-by='.lastTimestamp'
   ```

2. Contactar a soporte:
   - 📧 Email: safecity@cucei.udg.mx
   - 🐛 GitHub Issues: [Crear issue](https://github.com/issues)

3. Proporcionar:
   - Screenshots del problema
   - Logs completos
   - Pasos para reproducir
   - Versión de Kubernetes/Docker

---

**Última actualización**: Mayo 2026

> 💡 **Tip**: Guarda este documento para referencia rápida. Muchos problemas tienen soluciones simples.
