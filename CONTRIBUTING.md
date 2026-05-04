# 🤝 CONTRIBUTING - Guía de Contribución

¡Gracias por tu interés en contribuir a SafeCity Pro! Esta guía te ayudará a entender cómo participar en el proyecto.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Reportar Bugs](#cómo-reportar-bugs)
- [Cómo Sugerir Features](#cómo-sugerir-features)
- [Proceso de Contribución](#proceso-de-contribución)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Preguntas?](#preguntas)

---

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a mantener un ambiente respetuoso, inclusivo y profesional.

### Estándares

Se esperan estos comportamientos:

- ✅ Sé respetuoso y constructivo
- ✅ Usa lenguaje inclusivo
- ✅ Respeta las opiniones diferentes
- ✅ Acepta crítica constructiva
- ✅ Enfócate en lo mejor para la comunidad

### Inaceptable

- ❌ Acoso, insultos, discriminación
- ❌ Ataques personales
- ❌ Contenido violento
- ❌ Spam

### Reportar Violaciones

📧 Contacta: safecity@cucei.udg.mx

---

## 🐛 Cómo Reportar Bugs

### Antes de Reportar

- ✅ Verifica [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- ✅ Busca issues existentes
- ✅ Intenta reproducir el bug localmente

### Crear Reporte

Usa este template en [GitHub Issues](https://github.com/issues):

```markdown
## Descripción del Bug
[Descripción clara del problema]

## Pasos para Reproducir
1. ...
2. ...
3. ...

## Comportamiento Esperado
[Qué debería pasar]

## Comportamiento Actual
[Qué pasó realmente]

## Capturas de Pantalla
[Si aplica]

## Información del Entorno
- **OS**: [Windows/Mac/Linux]
- **Docker**: [Versión]
- **Kubernetes**: [Si aplica]
- **Python**: [3.9+]

## Logs
```bash
[Pegar logs relevantes]
```

## Información Adicional
[Cualquier otra información útil]
```

---

## 💡 Cómo Sugerir Features

### Evaluar Primero

- ¿Es una mejora claramente definida?
- ¿Está en línea con la visión del proyecto?
- ¿Es viable técnicamente?

### Crear Sugerencia

Usa [GitHub Discussions](https://github.com) o [Issues](https://github.com/issues):

```markdown
## Resumen de Feature
[Descripción clara]

## Motivación
¿Por qué necesitamos esto?

## Descripción Detallada
[Detalles de la implementación deseada]

## Ejemplo de Uso
[Cómo se usaría]

## Alternativas Consideradas
[Otras posibilidades]

## Contexto Adicional
[Links, referencias, screenshots]
```

---

## 🔄 Proceso de Contribución

### 1. Fork el Repositorio

```bash
# En GitHub: Click "Fork"
# Localmente:
git clone https://github.com/tu-usuario/safecity-project.git
cd safecity-project
git remote add upstream https://github.com/original/safecity-project.git
```

### 2. Crea una Rama

```bash
git checkout -b feature/nombre-descriptivo
# O para bugs:
git checkout -b fix/descripcion-bug
# O para docs:
git checkout -b docs/titulo
```

**Nomenclatura de ramas:**
- `feature/` - Nuevas funcionalidades
- `fix/` - Correcciones de bugs
- `docs/` - Cambios de documentación
- `refactor/` - Refactorización de código
- `test/` - Tests

### 3. Haz tus Cambios

Sigue [Estándares de Código](#estándares-de-código)

```bash
# Develop localmente
# Ver: DEVELOPMENT.md

# Commit frecuentes y descriptivos
git add .
git commit -m "type: descripción clara

- Punto 1
- Punto 2

Closes #123"
```

**Mensajes de commit:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

Ejemplos:
- `feat(alerts): add email notifications`
- `fix(auth): resolve token expiration bug`
- `docs: update deployment guide`

### 4. Push a tu Fork

```bash
git push origin feature/nombre-descriptivo
```

### 5. Crea Pull Request

En GitHub:
1. Click "Compare & pull request"
2. Llena el template del PR
3. Asigna reviewers
4. Espera feedback

---

## 💻 Estándares de Código

### Python

```python
# ✅ BIEN
def create_alert(
    alert_type: str,
    location: str,
    description: Optional[str] = None
) -> Alert:
    """Create a new alert.
    
    Args:
        alert_type: Type of alert (Robo, Accidente, Vandalismo)
        location: Location of the incident
        description: Optional description
        
    Returns:
        Created Alert object
    """
    # Implementation
    pass

# ❌ MAL
def create_alert(t, l, d=None):
    # No docstring
    pass
```

**Reglas:**
- Usa type hints
- Escribe docstrings
- Líneas máx 100 caracteres
- PEP 8 compliant
- 4 espacios indentación

**Linting:**
```bash
pip install black flake8 mypy
black services/
flake8 services/
mypy services/
```

### JavaScript/HTML

```javascript
// ✅ BIEN
function createAlert(type, location, description = null) {
    // Clear comments explaining why, not what
    const validated = validateInput(type, location);
    
    if (!validated) {
        console.error('Invalid input');
        return;
    }
    
    return sendAlert(type, location, description);
}

// ❌ MAL
function ca(t, l, d) {
    // No explanation
    return send(t, l, d);
}
```

### YAML

```yaml
# ✅ BIEN
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alerts-service
  namespace: safecity
  labels:
    app: alerts
spec:
  replicas: 3
  # Comments explain the why
  
# ❌ MAL
apiVersion: apps/v1
kind: Deployment
metadata: {name: alerts, namespace: safecity}
spec: {replicas: 3}
```

---

## 🧪 Testing

### Python

```bash
# Instalar pytest
pip install pytest pytest-cov

# Crear tests en services/alerts/tests/

# Ejecutar tests
pytest services/alerts/tests/ -v --cov
```

**Ejemplo test:**
```python
def test_create_alert():
    """Test creating an alert"""
    alert = create_alert(
        alert_type="Robo",
        location="CUCEI"
    )
    
    assert alert.tipo == "Robo"
    assert alert.ubicacion == "CUCEI"
```

### Cobertura

- Mínimo: 70% cobertura
- Objetivo: 80%+

---

## 📝 Documentación

### Actualizar Docs

1. **README.md** - Cambios generales
2. **DEVELOPMENT.md** - Setup/desarrollo
3. **PRODUCTION.md** - Despliegue
4. **API.md** - Cambios en endpoints
5. **TROUBLESHOOTING.md** - Nuevos problemas

### Formato

```markdown
## Título

Descripción clara.

### Subtitle

Más detalles.

```bash
# Ejemplo de código
```

**Links:**
- Usa markdown links: [texto](ruta)
- Referencia archivos: [README.md](README.md)
- Usa línea de código: \`variable\`
```

---

## 📤 Proceso de Pull Request

### Template de PR

```markdown
## Descripción
[Qué hace este PR]

## Tipo de Cambio
- [ ] Bug fix
- [ ] Feature
- [ ] Documentation

## Issue Relacionado
Closes #123

## Cambios Propuestos
- Cambio 1
- Cambio 2

## Testing Realizado
- [ ] Tests unitarios pasados
- [ ] Testeado localmente
- [ ] No hay cambios breaking

## Checklist
- [ ] Mi código sigue los estándares
- [ ] He actualizado documentación
- [ ] No hay conflictos merge
- [ ] Commits son descriptivos
```

### Feedback

- ✅ Acepta crítica constructiva
- ✅ Responde preguntas claramente
- ✅ Solicita cambios si no está claro
- ✅ Aprecia el tiempo del reviewer

### Merge

- Un PR requiere ≥ 1 approval
- Todos los checks deben pasar
- Rama debe estar actualizada
- Squash commits si es necesario

---

## 🔧 Herramientas de Desarrollo

### Pre-requisitos
- Python 3.9+
- Docker & Docker Compose
- Git
- VS Code (recomendado)

### Setup

```bash
# Clonar y configurar
git clone https://github.com/tu-usuario/safecity-project.git
cd safecity-project
cp .env.example .env

# Instalaciones
pip install black flake8 mypy pytest

# Ejecutar
docker-compose up -d
```

### VS Code Extensions

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "ms-kubernetes-tools.vscode-kubernetes-tools",
        "ms-azuretools.vscode-docker"
    ]
}
```

---

## 📚 Recursos

- [Git Workflow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8](https://pep8.org/)
- [GitHub Docs](https://docs.github.com)

---

## 🎯 Roadmap de Contribución

### Fácil (Good First Issue)
- 📝 Mejorar documentación
- 🐛 Bugs pequeños
- 🧪 Agregar tests
- 📋 Ejemplos

### Intermedio
- ✨ Nuevas features pequeñas
- 🔧 Refactoring
- 📊 Mejoras de rendimiento

### Avanzado
- 🚀 Grandes features
- 🏗️ Cambios arquitectónicos
- 🔐 Seguridad

---

## ⚖️ Licencia

Al contribuir, aceptas que tu código será bajo licencia MIT.

---

## 📞 Preguntas?

- 📧 Email: safecity@cucei.udg.mx
- 💬 Discussions: [GitHub Discussions](https://github.com)
- 🐛 Issues: [Create Issue](https://github.com/issues)

---

**¡Gracias por contribuir a SafeCity Pro!** 🎉

> Cada contribución, sin importar el tamaño, es valiosa. ¡Bienvenido al equipo!
