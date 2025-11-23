# Datos Procesados de Cromatogramas

Este directorio contiene los datos crudos extraídos de los archivos Excel originales,
organizados por experimento.

## Estructura de carpetas

```
Procesados/
├── Experimento1/          # Experimento inicial (03/10/2025)
├── Experimento2/          # MORAN 20/10/2025
├── Experimento3/          # MORAN 24/10/2025 (Repetición)
└── Experimento4/          # MORAN 07/11/2025
```

## Contenido de cada carpeta

Cada carpeta de experimento contiene:
- `muestra_*_raw.csv`: Datos crudos de cada muestra analizada
- `metadata.json`: Información sobre el experimento (fecha, condiciones, fuente)
- `estandar_interno_raw.csv`: Datos del estándar interno (cuando aplica)

## Formato de los datos CSV

Los archivos CSV contienen las siguientes columnas (cuando están disponibles):
- `Index`: Número de pico detectado
- `Name`: Nombre del compuesto (si está identificado)
- `Time`: Tiempo de retención en minutos
- `Quantity`: Cantidad relativa (% de área)
- `Height`: Altura del pico en µV
- `Area`: Área del pico en µV.Min
- `Area %`: Porcentaje de área total

## Origen de los datos

Los datos fueron extraídos de:
1. Experimento1: `Experimento1/Cromatograma/cromatogramaExperimento1.xlsx`
2. Experimento2: `20251020_MORAN 20-10-25/2025-10-20 MORAN.XLS`
3. Experimento3: `20251024_MORAN 24-10-25/RESULTADOS MORAN RXN 1.xlsx`
4. Experimento4: `20251107_MORAN 7-11-25/2025-11-07 MORAN.XLS`

## Metadata

Consulta el archivo `metadata.json` en cada carpeta para información detallada sobre:
- Fecha del experimento
- Condiciones de reacción
- Archivo fuente original
- Lista de muestras analizadas
