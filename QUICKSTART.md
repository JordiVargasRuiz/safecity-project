# ⚡ QUICK START GUIDE - SafeCity Pro

**Guía de inicio rápido en 5 minutos**

---

## 🚀 Opción 1: Ejecutar Localmente (Recomendado para Principiantes)

### Paso 1: Clonar
```bash
git clone https://github.com/tu-usuario/safecity-project.git
cd safecity-project
```

### Paso 2: Iniciar
```bash
docker-compose up -d
```

### Paso 3: Acceder
- **Frontend**: http://localhost
- **API Docs**: http://localhost:8001/docs
- **Database**: localhost:5432

### Paso 4: Crear Alerta
1. Ir a http://localhost
2. Seleccionar tipo: "Robo"
3. Ubicación: "CUCEI"
4. Botón: "Transmitir"

✅ **¡Listo en 5 minutos!**

---

## 🐳 Opción 2: Desplegar en Kubernetes

### Requisitos
- Cluster K8s corriendo
- `kubectl` configurado

### Comandos
```bash
# Crear namespace
kubectl create namespace safecity

# Desplegar
kubectl apply -f k8s/postgres-db.yaml -n safecity
kubectl apply -f k8s/alerts-deployment.yaml -n safecity
kubectl apply -f k8s/users-deployment.yaml -n safecity
kubectl apply -f k8s/frontend-deployment.yaml -n safecity

# Acceder
kubectl port-forward svc/frontend-service 80:80 -n safecity
# http://localhost
```

---

## 📚 Documentación

| Para... | Archivo |
|---------|---------|
| **Visión general** | [README.md](README.md) |
| **Desarrollo local** | [DEVELOPMENT.md](DEVELOPMENT.md) |
| **Producción** | [PRODUCTION.md](PRODUCTION.md) |
| **APIs** | [API.md](API.md) |
| **Presentación** | [PRESENTATION.md](PRESENTATION.md) |
| **Problemas** | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Índice completo** | [DOCUMENTATION.md](DOCUMENTATION.md) |

---

## 🔌 Testing Rápido

### Login
```bash
curl -X POST http://localhost:8002/login \
  -d "username=admin&password=admin123"
```

### Crear Alerta
```bash
curl -X POST http://localhost:8001/alerts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-seguro-safecity-2026" \
  -d '{
    "tipo": "Robo",
    "ubicacion": "CUCEI"
  }'
```

### Listar Alertas
```bash
curl http://localhost:8001/alerts
```

---

## 🔧 Comandos Útiles

### Ver Estado
```bash
docker-compose ps              # Docker
kubectl get pods -n safecity   # Kubernetes
```

### Ver Logs
```bash
docker-compose logs -f alerts-service
kubectl logs -f deployment/alerts-service -n safecity
```

### Parar/Iniciar
```bash
docker-compose down            # Detener
docker-compose up -d           # Iniciar

kubectl delete namespace safecity  # Detener K8s
kubectl create namespace safecity  # Crear K8s
```

---

## 🆘 Problemas?

### No puedo acceder a http://localhost
```bash
docker-compose ps              # Verificar servicios
docker-compose logs            # Ver logs
docker-compose down -v
docker-compose up -d           # Reiniciar
```

### API devuelve error
```bash
curl http://localhost:8001/docs    # Ver documentación
curl http://localhost:8001/        # Health check
```

### Más problemas?
→ Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📞 Contacto

- 📧 Email: safecity@cucei.udg.mx
- 📖 Docs: [DOCUMENTATION.md](DOCUMENTATION.md)
- 🐛 Issues: [GitHub Issues](https://github.com/issues)

---

**Versión**: 2.6 | **Última actualización**: Mayo 2026

> 💡 Para documentación completa, ver [README.md](README.md)
