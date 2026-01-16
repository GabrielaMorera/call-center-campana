# 🗳️ Sistema de Gestión de Llamadas - Campaña Electoral 2026

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)

*Plataforma web para la coordinación eficiente de equipos de contacto telefónico*

---

## 📋 Descripción General

Este sistema fue desarrollado para optimizar la gestión de contactos telefónicos en el marco de una campaña electoral regional. La plataforma permite a múltiples operadoras trabajar de forma simultánea y coordinada, evitando duplicidad de llamadas y proporcionando métricas en tiempo real sobre el avance de la gestión.

### Características Principales

- **🔐 Sistema de autenticación** con roles diferenciados (administrador/operadora)
- **📊 Dashboard en tiempo real** con visualización de métricas y estadísticas
- **🤝 Coordinación multi-operadora** con distribución automática de contactos
- **🔄 Sistema de reintentos** para contactos que no respondieron
- **📈 Seguimiento de conversión** mediante sistema de semáforo (verde/amarillo/rojo)
- **☁️ Persistencia en la nube** con Google Sheets como base de datos

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Login     │  │  Operadora  │  │  Administrador  │  │
│  │   Screen    │  │  Dashboard  │  │    Dashboard    │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                   LÓGICA DE NEGOCIO                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │  • Distribución equitativa de contactos         │    │
│  │  • Sistema de caché con TTL para optimización   │    │
│  │  • Manejo de reintentos y actualizaciones       │    │
│  │  • Zona horaria Colombia (UTC-5)                │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                    PERSISTENCIA                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │            Google Sheets API v4                  │    │
│  │  ┌──────────────┐    ┌──────────────┐           │    │
│  │  │  contactos   │    │   llamadas   │           │    │
│  │  └──────────────┘    └──────────────┘           │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 🚦 Sistema de Clasificación

El sistema implementa un modelo de semáforo para clasificar las respuestas obtenidas:

| Estado | Significado | Acción |
|--------|-------------|--------|
| 🟢 **Verde** | Respuesta positiva confirmada | Se registra como conversión exitosa |
| 🟡 **Amarillo** | Respuesta indecisa o "tal vez" | Candidato para seguimiento posterior |
| 🔴 **Rojo** | Respuesta negativa | Se registra y no se vuelve a contactar |
| ⚫ **No contesta** | Sin respuesta | Disponible para reintento |

---

## 🔧 Aspectos Técnicos Destacados

### Coordinación Multi-Operadora

Para evitar que dos operadoras contacten al mismo registro simultáneamente, se implementó un algoritmo de distribución determinista:

```python
# Cada operadora recibe contactos según su índice en el sistema
# Operadora 0: índices 0, 2, 4, 6...
# Operadora 1: índices 1, 3, 5, 7...
contactos_asignados = df[df.index % num_operadoras == indice_operadora]
```

### Gestión de Caché

Se utiliza un sistema de caché con TTL (Time To Live) de 5 segundos para balancear entre rendimiento y frescura de datos:

- **Lecturas frecuentes**: Utilizan caché para minimizar llamadas a la API
- **Escrituras**: Invalidan el caché inmediatamente después de registrar
- **Modo reintento**: Bypass completo del caché para datos en tiempo real

### Zona Horaria

Todas las marcas de tiempo se registran en hora de Colombia (UTC-5), independientemente de la ubicación del servidor:

```python
zona_colombia = timezone(timedelta(hours=-5))
hora_actual = datetime.now(zona_colombia)
```

---

## 📊 Métricas y Reportes

El panel de administración incluye:

- **Gráfico de distribución**: Visualización circular de resultados por categoría
- **Rendimiento por operadora**: Comparativo de productividad del equipo
- **Tasa de conversión**: Porcentaje de respuestas positivas sobre total
- **Exportación de datos**: Descarga en formato CSV para análisis externo

---

## 🔒 Seguridad

- Credenciales de servicio almacenadas en Streamlit Secrets
- Sin exposición de contraseñas en código fuente
- Autenticación requerida para todas las operaciones
- Separación de permisos por rol

---

## 📁 Estructura del Proyecto

```
call_center_campana_v2/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── .streamlit/
│   └── secrets.toml      # Configuración de credenciales (no versionado)
└── README.md             # Documentación
```

---

## 🚀 Despliegue

La aplicación está configurada para despliegue en **Streamlit Cloud**, conectándose directamente al repositorio de GitHub para actualizaciones automáticas.

### Variables de Entorno Requeridas

```toml
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key = "..."
client_email = "..."

[usuarios.admin]
password = "..."
nombre = "Admin"
rol = "admin"

[usuarios.operadora1]
password = "..."
nombre = "Nombre Operadora"
rol = "operadora"
```

---

## 📈 Evolución del Proyecto

| Versión | Características |
|---------|-----------------|
| **v1.0** | Funcionalidad básica de registro de llamadas |
| **v1.1** | Implementación de sistema de reintentos |
| **v1.2** | Coordinación multi-operadora con distribución automática |
| **v1.3** | Optimización de caché y tiempos de respuesta |
| **v1.4** | Mejoras en visualización, métricas y zona horaria Colombia |

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito |
|------------|-----------|
| **Streamlit** | Framework web para interfaces de datos |
| **Pandas** | Manipulación y análisis de datos |
| **Plotly** | Visualizaciones interactivas |
| **gspread** | Integración con Google Sheets API |
| **Google OAuth2** | Autenticación segura con servicios de Google |

---

## 👥 Equipo

Desarrollado para la coordinación del equipo de contacto telefónico en la región de Gualivá, Cundinamarca.

---

*Sistema desarrollado con ❤️ para facilitar la comunicación ciudadana*

**Campaña 2026**
