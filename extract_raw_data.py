#!/usr/bin/env python3
"""
Script para extraer datos crudos de cromatogramas Excel a archivos CSV
Organiza los datos por experimento en la carpeta Procesados/
"""

import pandas as pd
from pathlib import Path
import json

class ExtractorDatosCromatogramas:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.procesados_dir = self.base_dir / 'Procesados'
        self.metadata = {}

    def extraer_experimento1(self):
        """Extrae datos del Experimento 1 (03/10/2025)"""
        print("Extrayendo Experimento 1...")

        exp1_dir = self.procesados_dir / 'Experimento1'
        source_file = self.base_dir / 'Experimento1/Cromatograma/cromatogramaExperimento1.xlsx'

        if not source_file.exists():
            print(f"ERROR: No se encuentra {source_file}")
            return

        # Leer todas las hojas
        df_dict = pd.read_excel(source_file, sheet_name=None)

        metadata = {
            'experimento': 'Experimento 1',
            'fecha': '2025-10-03',
            'fuente': str(source_file),
            'tipo': 'Transesterificación con CaO',
            'condiciones': {
                'aceite_ml': 100,
                'metanol_ml': 25.51,
                'catalizador': 'CaO 1%',
                'temperatura': '50-55°C',
                'rpm': '100-600',
                'duracion_min': 120,
                'relacion_molar': '6:1'
            },
            'muestras': []
        }

        # Procesar cada muestra
        for sheet_name in ['2.1', '3.1', '5.1', '6.1', '9.1', '12.1']:
            if sheet_name in df_dict:
                df = df_dict[sheet_name]

                # Guardar CSV
                csv_file = exp1_dir / f'muestra_{sheet_name.replace(".", "_")}_raw.csv'
                df.to_csv(csv_file, index=False)

                metadata['muestras'].append({
                    'nombre': sheet_name,
                    'archivo_csv': str(csv_file.relative_to(self.procesados_dir))
                })

                print(f"  ✓ Extraída muestra {sheet_name} -> {csv_file.name}")

        # Guardar metadata
        with open(exp1_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        self.metadata['Experimento1'] = metadata
        print(f"  ✓ Metadata guardada\n")

    def extraer_experimento2(self):
        """Extrae datos del MORAN 20/10/2025"""
        print("Extrayendo Experimento 2 (MORAN 20/10/2025)...")

        exp2_dir = self.procesados_dir / 'Experimento2'
        source_file = self.base_dir / '20251020_MORAN 20-10-25/2025-10-20 MORAN.XLS'

        if not source_file.exists():
            print(f"ERROR: No se encuentra {source_file}")
            return

        df_dict = pd.read_excel(source_file, sheet_name=None)

        metadata = {
            'experimento': 'MORAN Experimento 1',
            'fecha': '2025-10-20',
            'fuente': str(source_file),
            'tipo': 'Análisis de diferentes condiciones',
            'muestras': []
        }

        for sheet_name in ['1.1', '8.1', '10.1', '11.1', 'SN1', 'SN2']:
            if sheet_name in df_dict:
                df = df_dict[sheet_name]

                csv_file = exp2_dir / f'muestra_{sheet_name.replace(".", "_")}_raw.csv'
                df.to_csv(csv_file, index=False)

                metadata['muestras'].append({
                    'nombre': sheet_name,
                    'archivo_csv': str(csv_file.relative_to(self.procesados_dir))
                })

                print(f"  ✓ Extraída muestra {sheet_name} -> {csv_file.name}")

        # También extraer el estándar interno
        if 'std interno_20_10_2025 02_32_28' in df_dict:
            df_std = df_dict['std interno_20_10_2025 02_32_28']
            csv_file = exp2_dir / 'estandar_interno_raw.csv'
            df_std.to_csv(csv_file, index=False)
            print(f"  ✓ Extraído estándar interno -> {csv_file.name}")

        with open(exp2_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        self.metadata['Experimento2'] = metadata
        print(f"  ✓ Metadata guardada\n")

    def extraer_experimento3(self):
        """Extrae datos del MORAN 07/11/2025"""
        print("Extrayendo Experimento 3 (MORAN 07/11/2025)...")

        exp3_dir = self.procesados_dir / 'Experimento3'
        source_file = self.base_dir / '20251107_MORAN 7-11-25/2025-11-07 MORAN.XLS'

        if not source_file.exists():
            print(f"ERROR: No se encuentra {source_file}")
            return

        df_dict = pd.read_excel(source_file, sheet_name=None)

        metadata = {
            'experimento': 'MORAN Experimento 2',
            'fecha': '2025-11-07',
            'fuente': str(source_file),
            'tipo': 'Nuevas reacciones y puntos de control',
            'muestras': []
        }

        sheets_map = {
            '6.2': 'muestra_6_2',
            '12.2': 'muestra_12_2',
            '5_07_11_2025 12_25_25 p. m.': 'muestra_RXN5',
            '10_07_11_2025 12_52_05 p. m.': 'muestra_RXN10',
            'MITAD': 'muestra_MITAD',
            'FINAL': 'muestra_FINAL'
        }

        for sheet_name, nombre_archivo in sheets_map.items():
            if sheet_name in df_dict:
                df = df_dict[sheet_name]

                csv_file = exp3_dir / f'{nombre_archivo}_raw.csv'
                df.to_csv(csv_file, index=False)

                metadata['muestras'].append({
                    'nombre': sheet_name,
                    'archivo_csv': str(csv_file.relative_to(self.procesados_dir))
                })

                print(f"  ✓ Extraída muestra {sheet_name} -> {csv_file.name}")

        # Extraer estándar interno
        std_sheet = 'STD INT_07_11_2025 09_45_09 a. m.'
        if std_sheet in df_dict:
            df_std = df_dict[std_sheet]
            csv_file = exp3_dir / 'estandar_interno_raw.csv'
            df_std.to_csv(csv_file, index=False)
            print(f"  ✓ Extraído estándar interno -> {csv_file.name}")

        with open(exp3_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        self.metadata['Experimento3'] = metadata
        print(f"  ✓ Metadata guardada\n")

    def crear_documentacion(self):
        """Crea archivo README con documentación de los datos"""
        readme_content = """# Datos Procesados de Cromatogramas

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
"""

        readme_file = self.procesados_dir / 'README.md'
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        print(f"✓ Documentación creada: {readme_file}\n")

    def guardar_metadata_global(self):
        """Guarda metadata de todos los experimentos"""
        global_metadata = {
            'proyecto': 'Análisis de Cromatogramas de Biodiesel',
            'fecha_extraccion': '2025-11-23',
            'total_experimentos': len(self.metadata),
            'experimentos': self.metadata
        }

        metadata_file = self.procesados_dir / 'metadata_global.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(global_metadata, f, indent=2, ensure_ascii=False)

        print(f"✓ Metadata global guardada: {metadata_file}\n")

    def ejecutar_extraccion(self):
        """Ejecuta la extracción completa"""
        print("=" * 80)
        print("EXTRACCIÓN DE DATOS CRUDOS DE CROMATOGRAMAS")
        print("=" * 80)
        print()

        self.extraer_experimento1()
        self.extraer_experimento2()
        self.extraer_experimento3()

        self.crear_documentacion()
        self.guardar_metadata_global()

        print("=" * 80)
        print("EXTRACCIÓN COMPLETADA")
        print("=" * 80)
        print(f"\nDatos guardados en: {self.procesados_dir}")
        print(f"Total de experimentos procesados: {len(self.metadata)}")

        total_muestras = sum(len(exp['muestras']) for exp in self.metadata.values())
        print(f"Total de muestras extraídas: {total_muestras}")

if __name__ == '__main__':
    base_dir = '/home/user/ExperimentosBiodiesel_row'
    extractor = ExtractorDatosCromatogramas(base_dir)
    extractor.ejecutar_extraccion()
