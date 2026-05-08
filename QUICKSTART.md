# ⚡ QUICK START GUIDE - SafeCity Pro

**Guía de inicio rápido en 5 minutos**

---

## 🚀 Opción 1: Ejecutar Localmente (Recomendado para Principiantes)

### Paso 1: Clonar
```bash
git clone https://github.com/JordiVargasRuiz/safecity-project.git
cd safecity-project
```

### Paso 2: Iniciar
```bash
docker-compose up -d
```

### Paso 3: Acceder
- **Frontend**: http://localhost:8080/

### Paso 4: Crear Alerta
1. Ir a http://localhost:8080/
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
| **Presentación** | [PRESENTATION.md](PRESENTATION.md) |
| **Problemas** | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| **Índice completo** | [DOCUMENTATION.md](DOCUMENTATION.md) |

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

### No puedo acceder a http://localhost:8080/
```bash
docker-compose ps              # Verificar servicios
docker-compose logs            # Ver logs
docker-compose down -v
docker-compose up -d           # Reiniciar
```

### Más problemas?
→ Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📞 Contacto

- 📧 Email: jordi.vargas3669@alumnos.udg.mx
- 📖 Docs: [DOCUMENTATION.md](DOCUMENTATION.md)
- 🐛 Issues: [GitHub Issues](https://github.com/issues)

---

**Versión**: 2.6 | **Última actualización**: Mayo 2026

> 💡 Para documentación completa, ver [README.md](README.md)
