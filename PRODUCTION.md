# 🏢 GUÍA DE PRODUCCIÓN

Instrucciones para desplegar SafeCity Pro en ambiente de producción con Kubernetes.

---

## ⚠️ Consideraciones de Seguridad Críticas

### Antes de Desplegar

- [ ] Cambiar todas las contraseñas por defecto
- [ ] Generar certificados SSL/TLS válidos
- [ ] Configurar RBAC en Kubernetes
- [ ] Implementar NetworkPolicies
- [ ] Habilitar encriptación de datos
- [ ] Configurar backups automáticos
- [ ] Auditar permisos de usuario
- [ ] Implementar WAF (Web Application Firewall)

---

## 🔐 Configuración de Seguridad

### 1. Cambiar Contraseñas

```bash
# Generar contraseña fuerte
openssl rand -base64 32

# Usar en ConfigMap/Secret
kubectl create secret generic postgres-credentials \
  --from-literal=password='TU_PASSWORD_GENERADO_AQUI' \
  -n safecity
```

### 2. Configurar Secrets de Kubernetes

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: safecity-secrets
  namespace: safecity
type: Opaque
stringData:
  postgres-password: "TU_PASSWORD_SEGURO"
  jwt-secret: "TU_JWT_SECRET_SEGURO"
  admin-password: "TU_ADMIN_PASSWORD"
---
apiVersion: v1
kind: Secret
metadata:
  name: safecity-tls
  namespace: safecity
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # Base64 encoded certificate
  tls.key: LS0tLS1CRUdJTi... # Base64 encoded key
```

Aplicar:
```bash
kubectl apply -f k8s/secrets.yaml
```

### 3. Configurar TLS/HTTPS

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: safecity-ingress
  namespace: safecity
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - safecity.tucei.mx
      secretName: safecity-tls
  rules:
    - host: safecity.tucei.mx
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

---

## 📊 High Availability (HA)

### Réplicas Múltiples

```yaml
# k8s/alerts-deployment-prod.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alerts-service
  namespace: safecity
spec:
  replicas: 3  # Aumentar para HA
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: alerts
  template:
    metadata:
      labels:
        app: alerts
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - alerts
                topologyKey: kubernetes.io/hostname
      containers:
        - name: alerts
          image: safecity-alerts:latest
          imagePullPolicy: Always
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /docs
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Load Balancing

```bash
# Verificar service type
kubectl get svc -n safecity

# Cambiar a LoadBalancer
kubectl patch svc alerts-service -p '{"spec":{"type":"LoadBalancer"}}' -n safecity

# Obtener IP externa
kubectl get svc alerts-service -n safecity -w
```

---

## 💾 Backup y Recuperación

### Backup Automático PostgreSQL

```yaml
# k8s/postgres-backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: safecity
spec:
  schedule: "0 2 * * *"  # 2 AM diariamente
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: postgres-backup
          containers:
            - name: backup
              image: postgres:14
              command:
                - /bin/bash
                - -c
                - |
                  export PGPASSWORD=$POSTGRES_PASSWORD
                  pg_dump -h postgres-service -U postgres safecity_alerts > /backups/safecity_alerts_$(date +%Y%m%d_%H%M%S).sql
              env:
                - name: POSTGRES_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: postgres-credentials
                      key: password
              volumeMounts:
                - name: backup-storage
                  mountPath: /backups
          volumes:
            - name: backup-storage
              persistentVolumeClaim:
                claimName: backup-pvc
          restartPolicy: OnFailure
```

### Restaurar Backup

```bash
# Copiar archivo de backup al pod
kubectl cp ./backup.sql safecity/postgres-pod:/tmp/backup.sql

# Restaurar
kubectl exec -it postgres-pod -n safecity -- psql -U postgres safecity_alerts < /tmp/backup.sql

# O con pg_restore
kubectl exec -it postgres-pod -n safecity -- pg_restore -d safecity_alerts /tmp/backup.sql
```

---

## 📈 Escalado Automático

### Horizontal Pod Autoscaler (HPA)

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: alerts-hpa
  namespace: safecity
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: alerts-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

Aplicar:
```bash
kubectl apply -f k8s/hpa.yaml
kubectl get hpa -n safecity -w
```

---

## 📊 Monitoreo y Logging

### Prometheus + Grafana

```yaml
# k8s/prometheus-values.yaml
prometheus:
  prometheusSpec:
    retention: 15d
    resources:
      requests:
        cpu: 250m
        memory: 512Mi
    externalLabels:
      cluster: safecity-prod

grafana:
  adminPassword: TU_PASSWORD_SEGURO
  persistence:
    enabled: true
    size: 10Gi
```

Instalar:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -f k8s/prometheus-values.yaml \
  -n safecity
```

### ELK Stack (Elasticsearch, Logstash, Kibana)

```bash
# Instalar Elasticsearch operator
helm repo add elastic https://helm.elastic.co
helm install elastic-operator elastic/eck-operator \
  -n safecity --create-namespace
```

### Alertas

```yaml
# k8s/alerting-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: safecity-alerts
  namespace: safecity
spec:
  groups:
    - name: safecity.rules
      interval: 30s
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
          for: 5m
          annotations:
            summary: "Alta tasa de errores en {{ $labels.instance }}"

        - alert: PodCrashing
          expr: rate(container_last_seen{pod=~"safecity.*"}[1m]) == 0
          for: 1m
          annotations:
            summary: "Pod {{ $labels.pod }} está crasheando"
```

---

## 🛡️ Network Policies

```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: safecity-network-policy
  namespace: safecity
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
  egress:
    - to:
        - namespaceSelector: {}
    - ports:
        - protocol: TCP
          port: 53
        - protocol: UDP
          port: 53
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy to Production

on:
  push:
    branches:
      - main

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push Alerts Service
        uses: docker/build-push-action@v4
        with:
          context: ./services/alerts
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/alerts:latest

      - name: Build and Push Users Service
        uses: docker/build-push-action@v4
        with:
          context: ./services/users
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/users:latest

      - name: Deploy to Kubernetes
        env:
          KUBE_CONFIG: ${{ secrets.KUBE_CONFIG }}
        run: |
          echo "$KUBE_CONFIG" | base64 -d > kubeconfig.yaml
          export KUBECONFIG=$(pwd)/kubeconfig.yaml
          kubectl set image deployment/alerts-service \
            alerts-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/alerts:latest \
            -n safecity
          kubectl rollout status deployment/alerts-service -n safecity
```

---

## 📋 Checklist Pre-Producción

- [ ] Todas las imágenes Docker construidas y pusheadas
- [ ] Contraseñas cambiadas (no usar defaults)
- [ ] Certificados SSL/TLS configurados
- [ ] Backups automatizados habilitados
- [ ] Monitoreo y alertas configurados
- [ ] Logging centralizado funcionando
- [ ] RBAC configurado
- [ ] Network policies implementadas
- [ ] HPA configurado
- [ ] Testing de failover completado
- [ ] Documentación actualizada
- [ ] Plan de recuperación ante desastres
- [ ] Auditoría de seguridad completada

---

## 🚨 Plan de Recuperación ante Desastres (DR)

### RTO y RPO

- **RTO** (Recovery Time Objective): 15 minutos
- **RPO** (Recovery Point Objective): 1 hora

### Procedimiento de Recuperación

```bash
# 1. Identificar el problema
kubectl describe pod <pod-name> -n safecity
kubectl logs <pod-name> -n safecity

# 2. Restaurar del backup más reciente
kubectl exec -it postgres-pod -n safecity -- \
  psql -U postgres safecity_alerts < /backups/latest.sql

# 3. Reiniciar servicios
kubectl rollout restart deployment/alerts-service -n safecity
kubectl rollout restart deployment/users-service -n safecity

# 4. Validar
kubectl rollout status deployment/alerts-service -n safecity
curl https://safecity.tucei.mx/docs
```

---

## 📞 Contacto y Escalación

| Nivel | Contacto | Tiempo Respuesta |
|-------|----------|-----------------|
| L1 - Alerts | @devops-team | 15 min |
| L2 - Critical | @engineering-lead | 5 min |
| L3 - Emergency | @cto | Inmediato |

---

## 📚 Referencias

- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes/)
- [Kubernetes Security Documentation](https://kubernetes.io/docs/concepts/security/)

---

**Última actualización**: Mayo 2026

> 🔐 **Recuerda**: La seguridad no es un producto, es un proceso. Revisa y actualiza estas configuraciones regularmente.
