# Datos Procesados de Cromatogramas - Nomenclatura Alfanumérica

Este directorio contiene los datos crudos extraídos y procesados de los archivos Excel originales,
organizados por experimento con nomenclatura alfanumérica consistente.

---

## 📊 Sistema de Nomenclatura

Todas las muestras usan nomenclatura **E[experimento][letra]** para facilitar identificación y trazabilidad:

- **Experimento 1:** E1a, E1b, E1c, E1d, E1e, E1f (6 muestras)
- **Experimento 2:** E2a, E2b, E2c, E2d, E2e, E2f (6 muestras)
- **Experimento 3:** E3a, E3b, E3c, E3d, E3e, E3f (6 muestras)

**Total:** 18 muestras

---

## 📁 Estructura de Carpetas

```
Procesados/
├── Experimento1/          # E1a-E1f (03/10/2025)
│   ├── muestra_*_raw.csv  # Datos crudos originales
│   ├── metadata.json      # Info + mapeo nomenclatura
│   └── resultados_procesados.json
│
├── Experimento2/          # E2a-E2f (20/10/2025)
│   ├── muestra_*_raw.csv
│   ├── metadata.json
│   └── resultados_procesados.json
│
├── Experimento3/          # E3a-E3f (07/11/2025)
│   ├── muestra_*_raw.csv
│   ├── metadata.json
│   └── resultados_procesados.json
│
├── figuras/               # 10 visualizaciones
│   ├── fig1_evolucion_temporal_exp1.png
│   ├── fig2_comparacion_experimentos.png
│   ├── fig3_composicion_apilada.png
│   ├── fig4_comparacion_temporal.png
│   ├── fig5_estadisticas_boxplot.png
│   ├── fig6_scatter_conversion_pureza.png
│   ├── fig7_gliceridos_promedio.png
│   ├── fig8_area_fames.png
│   ├── fig9_picos_fames.png
│   └── fig10_heatmap_calidad.png
│
├── tabla_resumen.csv                    # Resultados consolidados
├── resultados_consolidados.json         # JSON con nomenclatura
└── README.md                            # Este archivo
```

---

## 📋 Mapeo de Nomenclatura

### Experimento 1 (03/10/2025) - Transesterificación con monitoreo temporal

| Nombre Original | Nomenclatura | Orden | Tiempo (min) |
|-----------------|--------------|-------|--------------|
| 2.1 | **E1a** | 1 | 0 |
| 3.1 | **E1b** | 2 | 24 |
| 5.1 | **E1c** | 3 | 48 |
| 6.1 | **E1d** | 4 | 72 |
| 9.1 | **E1e** | 5 | 96 |
| 12.1 | **E1f** | 6 | 120 |

### Experimento 2 (20/10/2025) - Diferentes condiciones

| Nombre Original | Nomenclatura | Orden |
|-----------------|--------------|-------|
| 1.1 | **E2a** | 1 |
| 8.1 | **E2b** | 2 |
| 10.1 | **E2c** | 3 |
| 11.1 | **E2d** | 4 |
| SN1 | **E2e** | 5 |
| SN2 | **E2f** | 6 |

### Experimento 3 (07/11/2025) - Puntos de control temporal

| Nombre Original | Nomenclatura | Orden | Tipo |
|-----------------|--------------|-------|------|
| RXN5 | **E3a** | 1 | Reacción 5 min |
| RXN10 | **E3b** | 2 | Reacción 10 min |
| MITAD | **E3c** | 3 | Punto medio |
| FINAL | **E3d** | 4 | Punto final |
| 6.2 | **E3e** | 5 | Repetición muestra 6 |
| 12.2 | **E3f** | 6 | Repetición muestra 12 |

---

## 📄 Formato de Archivos

### Archivos CSV (`muestra_*_raw.csv`)

Datos crudos del cromatógrafo con las siguientes columnas:

- `Index`: Número de pico detectado
- `Name`: Nombre del compuesto (si está identificado)
- `Time`: Tiempo de retención (minutos)
- `Quantity`: Cantidad relativa (%)
- `Height`: Altura del pico (µV)
- `Area`: Área del pico (µV·Min)
- `Area %`: Porcentaje de área total

### Archivos metadata.json

Cada carpeta de experimento contiene un `metadata.json` con estructura actualizada:

```json
{
  "experimento": "Experimento 1",
  "fecha": "2025-10-03",
  "muestras": [
    {
      "nombre_original": "2.1",
      "nomenclatura": "E1a",
      "archivo_csv": "...",
      "tiempo": "17:25 (0 min)",
      "orden": 1
    }
  ]
}
```

---

## 📊 Archivos Consolidados

### tabla_resumen.csv

Tabla con todas las muestras usando nomenclatura E1a-E3f:

```csv
Experimento,Fecha,Muestra,Nombre_Original,Orden,Conversión FAMEs (%),Pureza (%),...
Experimento1,2025-10-03,E1a,2_1,1,96.83,41.51,...
Experimento1,2025-10-03,E1b,3_1,2,98.01,37.97,...
```

- **Ordenado por:** Experimento y Orden (cronológico)
- **18 filas** de datos (6 por experimento)
- Preserva nombres originales en columna `Nombre_Original`

---

## 🖼️ Figuras (10 visualizaciones)

Todas usan nomenclatura E1a-E3f, 300 dpi, formato PNG.

---

## 🔍 Origen de los Datos

| Experimento | Archivo Fuente | Nomenclatura |
|-------------|----------------|--------------|
| **Experimento 1** | `Experimento1/Cromatograma/cromatogramaExperimento1.xlsx` | E1a-E1f |
| **Experimento 2** | `20251020_MORAN 20-10-25/2025-10-20 MORAN.XLS` | E2a-E2f |
| **Experimento 3** | `20251107_MORAN 7-11-25/2025-11-07 MORAN.XLS` | E3a-E3f |

**Nota:** Experimento del 24/10/2025 fue identificado como duplicado y excluido del análisis.

---

**Última actualización:** 23/11/2025 | **Versión:** 2.0 (Nomenclatura alfanumérica)
