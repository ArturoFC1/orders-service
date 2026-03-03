# orders-service

Proyecto backend en Python desarrollado de forma incremental a lo largo de 11 módulos, cubriendo desde los fundamentos del lenguaje hasta arquitectura hexagonal con FastAPI, pruebas y machine learning.

---

## Tabla de contenidos

- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Módulos desarrollados](#módulos-desarrollados)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tests](#tests)
- [Cobertura](#cobertura)

---

## Tecnologías

- **Python 3.12**
- **FastAPI** — API REST
- **SQLAlchemy 2.0** — ORM
- **Alembic** — Migraciones de base de datos
- **Pydantic** — Validación de datos
- **SQLite** — Base de datos
- **httpx** — Cliente HTTP
- **python-jose** — JWT
- **passlib + bcrypt** — Hash de contraseñas
- **pytest + hypothesis** — Pruebas unitarias y property-based testing
- **scikit-learn + pandas** — Machine learning
- **black + isort + ruff + mypy** — Calidad de código
- **pre-commit** — Hooks de Git

---

## Estructura del proyecto

```
orders-service/
├── app/
│   ├── domain/                          # Capa de dominio
│   │   ├── entities/
│   │   │   ├── item.py                  # Entidad Item
│   │   │   └── order.py                 # Entidad Order
│   │   └── ports/
│   │       ├── order_repository.py      # Puerto de repositorio
│   │       └── notification_port.py     # Puerto de notificaciones
│   ├── application/                     # Capa de aplicación
│   │   ├── dtos/
│   │   │   └── order_dtos.py            # DTOs de entrada y salida
│   │   └── use_cases/
│   │       └── order_use_cases.py       # Casos de uso
│   ├── infrastructure/                  # Capa de infraestructura
│   │   ├── repositories/
│   │   │   ├── memory_order_repository.py
│   │   │   └── sql_order_repository.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routers/
│   │   │       ├── auth.py
│   │   │       └── orders.py
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   ├── engine.py
│   │   │   ├── models.py
│   │   │   └── crud.py
│   │   └── notifications/
│   │       └── http_notification_adapter.py
│   ├── clients/
│   │   └── order_client.py              # Cliente HTTP con httpx
│   ├── loaders/
│   │   ├── order_loader.py              # Carga desde JSON
│   │   └── csv_order_loader.py          # Carga desde CSV
│   ├── ml/
│   │   └── order_classifier.py          # Clasificador de órdenes
│   ├── models/
│   │   ├── order_schemas.py             # Schemas Pydantic legacy
│   │   └── type_definitions.py          # TypedDict y Protocols
│   ├── patterns/
│   │   ├── pricing_strategy.py          # Patrón Strategy
│   │   ├── cached_repository.py         # Patrón Decorator
│   │   └── external_provider_adapter.py # Patrón Adapter
│   ├── services/
│   │   ├── order_service.py
│   │   ├── metrics_service.py
│   │   ├── descuento_service.py
│   │   ├── concurrencia_service.py
│   │   └── order_domain_service.py
│   └── utils/
│       ├── logger.py
│       ├── validators.py
│       ├── order_mapper.py
│       └── retry.py
├── tests/
│   ├── test_orders_api.py
│   ├── test_descuento.py
│   ├── test_hexagonal.py
│   ├── test_patterns.py
│   └── test_solid.py
├── migrations/                          # Migraciones Alembic
├── data/                                # Archivos de datos
├── main_api.py                          # Entry point FastAPI
├── pyproject.toml
└── alembic.ini
```

---

## Módulos desarrollados

### Módulo 1 — Entorno y herramientas
Configurar un entorno de desarrollo profesional desde cero, antes de escribir lógica de negocio, 
se preparó la base del proyecto.
Se utilizó Poetry como gestor de dependencias y entorno virtual. Esto permite que cualquier persona que clone el repositorio pueda reproducir exactamente el mismo entorno.
Se integraron herramientas de calidad:
•	black → formatea automáticamente el código
•	isort → ordena imports correctamente
•	ruff → detecta errores y malas prácticas
•	pre-commit → ejecuta validaciones automáticamente antes de cada commit

### Módulo 2 — Fundamentos del lenguaje
Implementación de un decorador de reintentos con backoff exponencial.
Creación de un generador por lotes.
Desarrollo de un context manager para medir tiempos de ejecución.
Se aplicaron funciones avanzadas, manejo de errores y control de flujo de manera profesional.

### Módulo 3 — Funciones y programación “pythonic”
Enfocado en escribir código más limpio, expresivo y alineado con buenas prácticas de Python.
Implementación de dataclass Order con propiedades derivadas y métodos de comparación.
Modelado con Pydantic (OrderIn / OrderOut), decorador, batching, context-manager
Separar validación, transporte de datos y lógica de negocio siguiendo principios de diseño limpio.

### Módulo 4 — Objetos y modelos de datos
Migración de diccionarios a clases con `@dataclass`. Implementación de `Order` e `Item` con validaciones, cálculo de totales y comparaciones. Schemas Pydantic con validadores y mapper bidireccional entre entidades y DTOs.

### Módulo 5 — Tipado estático y calidad
Configuración de `mypy`, `ruff`, `black`, `isort` y `pre-commit`. Definición de `TypedDict` y `Protocol` con `@runtime_checkable`. Corrección de violaciones del principio de Liskov detectadas por mypy.

### Módulo 6 — Librería estándar y E/S
Sistema de logging estructurado con handlers para consola y archivo. Carga de datos desde JSON y CSV. Servicio de métricas con exportación a JSON. Generadores y context managers.

### Módulo 7 — HTTP y consumo de APIs
Cliente HTTP con `httpx` con reintentos automáticos y manejo de errores. Descarga de archivos en modo streaming. Mock server con Smocker para pruebas.

### Módulo 8 — Acceso a datos y ORM
Modelos ORM con SQLAlchemy 2.0 (`User`, `OrderModel`, `OrderItemModel`). Sistema de migraciones con Alembic. CRUD completo con sesiones y cascade delete.

### Módulo 9 — APIs web con FastAPI
API REST con routers, dependencias y documentación OpenAPI automática. Autenticación JWT con registro y login. Middleware CORS. Validación con Pydantic. 6 tests de integración con base de datos temporal.

### Módulo 10 — Pruebas y TDD
Implementación de `DescuentoService` siguiendo el ciclo Red-Green-Refactor. Fixtures reutilizables, parametrización con `@pytest.mark.parametrize`. Property-based testing con Hypothesis generando 100 ejemplos aleatorios. Reporte de cobertura con `pytest-cov`.

### Módulo 11 — Concurrencia y rendimiento
Fetcher asíncrono con `httpx.AsyncClient` y semáforo, logrando 5x más velocidad que la versión síncrona en operaciones I/O-bound. Cálculo CPU-bound con `ProcessPoolExecutor`. Comparación de tiempos con `time.time()`.

### Módulo 12 — Principios SOLID
Aplicación de SRP, OCP, LSP, ISP y DIP con `Protocol`. Separación en puertos y adaptadores. `OrderDomainService` depende de `OrderRepositoryPort` y no de implementaciones concretas. Verificación de LSP con `isinstance` en tests.

### Módulo 13 — Patrones de diseño
Implementación de tres patrones con casos reales:
- **Strategy** — tres algoritmos de precio intercambiables (`PrecioNormal`, `DescuentoVolumen`, `PrecioVIP`)
- **Decorator** — `CachedOrderRepository` agrega caché transparente a cualquier repositorio
- **Adapter** — `ExternalProviderAdapter` convierte formato externo al dominio interno

### Módulo 14 — Arquitectura Hexagonal
Reorganización del proyecto en tres capas: dominio, aplicación e infraestructura. Puertos estables e implementaciones intercambiables. Casos de uso `CreateOrder`, `GetOrder`, `DeleteOrder`, `ListOrders`. Adaptador de notificaciones HTTP simulado. 9 tests de contrato verificando intercambiabilidad de adaptadores.

---

## Instalación

```bash
git clone https://github.com/tu-usuario/orders-service.git
cd orders-service
poetry install
poetry shell
alembic upgrade head
```

---

## Uso

Correr la API:

```bash
uvicorn main_api:app --reload
```

Documentación disponible en `http://127.0.0.1:8000/docs`

Correr el script de demos:

```bash
python -m app.main
```

---

## Tests

```bash
pytest tests/ -v
```

Resultado actual: **41 tests pasando**

```
tests/test_descuento.py     10 tests  — TDD y property-based testing
tests/test_hexagonal.py      9 tests  — Arquitectura hexagonal y contratos
tests/test_orders_api.py     6 tests  — Integración con API y BD temporal
tests/test_patterns.py       9 tests  — Patrones de diseño
tests/test_solid.py          7 tests  — Principios SOLID
```

---

## Cobertura

```bash
pytest tests/ --cov=app --cov-report=term-missing
pytest tests/ --cov=app --cov-report=html
```

El reporte HTML se genera en `htmlcov/index.html`.

---

## Calidad de código

El proyecto usa pre-commit con los siguientes hooks:

```bash
pre-commit run --all-files
```

- **black** — formato de código
- **isort** — orden de imports
- **ruff** — linting PEP 8
- **mypy** — tipado estático
