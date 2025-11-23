#!/usr/bin/env python3
"""
Análisis sistemático de cromatogramas de biodiesel
Objetivo: Reconstruir la secuencia histórica de experimentos
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import json

class AnalizadorCromatogramas:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.experimentos = {}

    def analizar_todos_experimentos(self):
        """Analiza todos los experimentos y organiza la información"""

        # Experimento 1 (03/10/2025)
        exp1 = {
            'fecha': '2025-10-03',
            'nombre': 'Experimento 1 (Primer experimento de transesterificación)',
            'directorio': 'Experimento1',
            'condiciones': {
                'aceite_ml': 100,
                'aceite_g': 91.53,
                'metanol_ml': 25.51,
                'catalizador': 'CaO',
                'porcentaje_catalizador': '1%',
                'temperatura': '50-55°C',
                'rpm': '100-600',
                'duracion': '2 horas',
                'relacion_molar': '6:1'
            },
            'muestras': [
                {'nombre': '2.1', 'tiempo': '17:25 (0 min)', 'tipo': 'Inicio de reacción'},
                {'nombre': '3.1', 'tiempo': '17:49 (+24 min)', 'tipo': 'Muestreo intermedio'},
                {'nombre': '5.1', 'tiempo': '18:13 (+48 min)', 'tipo': 'Muestreo intermedio'},
                {'nombre': '6.1', 'tiempo': '18:37 (+72 min)', 'tipo': 'Muestreo intermedio'},
                {'nombre': '9.1', 'tiempo': '19:01 (+96 min)', 'tipo': 'Muestreo intermedio'},
                {'nombre': '12.1', 'tiempo': '19:25 (+120 min)', 'tipo': 'Final de reacción'}
            ],
            'archivos_excel': 'Experimento1/Cromatograma/cromatogramaExperimento1.xlsx',
            'archivos_pdf': [
                'Experimento1/Cromatograma/STD.pdf',
                'Experimento1/Cromatograma/2.1.pdf',
                'Experimento1/Cromatograma/3.1.pdf',
                'Experimento1/Cromatograma/5.1.pdf',
                'Experimento1/Cromatograma/6.1.pdf',
                'Experimento1/Cromatograma/9.1.pdf',
                'Experimento1/Cromatograma/12.1.pdf'
            ]
        }

        # MORAN 20-10-2025
        moran1 = {
            'fecha': '2025-10-20',
            'nombre': 'MORAN Experimento 1 (20 de octubre)',
            'directorio': '20251020_MORAN 20-10-25',
            'condiciones': {
                'tipo': 'Análisis de diferentes condiciones/muestras',
                'nota': 'Diferentes muestras con nomenclatura SN (Sample Note)'
            },
            'muestras': [
                {'nombre': '1.1', 'tipo': 'Muestra experimental', 'conversion': '96.07%'},
                {'nombre': '8.1', 'tipo': 'Muestra experimental', 'conversion': '55.83%'},
                {'nombre': '10.1', 'tipo': 'Muestra experimental', 'conversion': '79.76%'},
                {'nombre': '11.1', 'tipo': 'Muestra experimental', 'conversion': '59.39%'},
                {'nombre': 'SN1', 'tipo': 'Sample Note 1', 'conversion': '64.24%'},
                {'nombre': 'SN2', 'tipo': 'Sample Note 2', 'conversion': '76.90%'}
            ],
            'archivos_excel': '20251020_MORAN 20-10-25/2025-10-20 MORAN.XLS',
            'archivos_pdf': [
                '20251020_MORAN 20-10-25/1.1.pdf',
                '20251020_MORAN 20-10-25/8.1.pdf',
                '20251020_MORAN 20-10-25/10.1.pdf',
                '20251020_MORAN 20-10-25/11.1.pdf',
                '20251020_MORAN 20-10-25/SN1.pdf',
                '20251020_MORAN 20-10-25/SN2.pdf'
            ]
        }

        # MORAN 24-10-2025 (Repetición de Experimento 1)
        moran2 = {
            'fecha': '2025-10-24',
            'nombre': 'MORAN RXN 1 (24 de octubre - Repetición del Experimento 1)',
            'directorio': '20251024_MORAN 24-10-25',
            'condiciones': {
                'tipo': 'Repetición del Experimento 1',
                'nota': 'Mismas muestras que Experimento 1 para verificar reproducibilidad'
            },
            'muestras': [
                {'nombre': '2.1', 'tipo': 'Inicio de reacción'},
                {'nombre': '3.1', 'tipo': 'Muestreo intermedio'},
                {'nombre': '5.1', 'tipo': 'Muestreo intermedio'},
                {'nombre': '6.1', 'tipo': 'Muestreo intermedio'},
                {'nombre': '9.1', 'tipo': 'Muestreo intermedio'},
                {'nombre': '12.1', 'tipo': 'Final de reacción'}
            ],
            'archivos_excel': '20251024_MORAN 24-10-25/RESULTADOS MORAN RXN 1.xlsx',
            'archivos_pdf': [
                '20251024_MORAN 24-10-25/2.1.pdf',
                '20251024_MORAN 24-10-25/3.1.pdf',
                '20251024_MORAN 24-10-25/5.1.pdf',
                '20251024_MORAN 24-10-25/6.1.pdf',
                '20251024_MORAN 24-10-25/9.1.pdf',
                '20251024_MORAN 24-10-25/12.1.pdf'
            ]
        }

        # MORAN 07-11-2025
        moran3 = {
            'fecha': '2025-11-07',
            'nombre': 'MORAN Experimento 2 (7 de noviembre)',
            'directorio': '20251107_MORAN 7-11-25',
            'condiciones': {
                'tipo': 'Experimento con diferentes puntos de muestreo',
                'nota': 'Incluye muestras repetidas (6.2, 12.2) y nuevas reacciones (RXN 5, RXN 10, MITAD, FINAL)'
            },
            'muestras': [
                {'nombre': '6.2', 'tipo': 'Repetición de muestra 6'},
                {'nombre': '12.2', 'tipo': 'Repetición de muestra 12'},
                {'nombre': 'RXN 5 (5)', 'tipo': 'Reacción 5 - tiempo intermedio'},
                {'nombre': 'RXN 10 (10)', 'tipo': 'Reacción 10 - tiempo avanzado'},
                {'nombre': 'MITAD', 'tipo': 'Punto medio del experimento'},
                {'nombre': 'FINAL', 'tipo': 'Punto final del experimento'}
            ],
            'archivos_excel': '20251107_MORAN 7-11-25/2025-11-07 MORAN.XLS',
            'archivos_pdf': [
                '20251107_MORAN 7-11-25/6.2.pdf',
                '20251107_MORAN 7-11-25/12.2.pdf',
                '20251107_MORAN 7-11-25/RXN 5 (7-11-25).pdf',
                '20251107_MORAN 7-11-25/RXN 10 (7-11-25).pdf',
                '20251107_MORAN 7-11-25/MITAD (7-11-25).pdf',
                '20251107_MORAN 7-11-25/FINAL (7-11-25).pdf'
            ]
        }

        self.experimentos = {
            'Experimento_1': exp1,
            'MORAN_20Oct2025': moran1,
            'MORAN_24Oct2025': moran2,
            'MORAN_07Nov2025': moran3
        }

    def obtener_resultados_fames(self):
        """Extrae los porcentajes de FAMEs de todos los experimentos"""
        resultados = {}

        # Experimento 1
        exp1_file = self.base_dir / 'Experimento1/Cromatograma/cromatogramaExperimento1.xlsx'
        if exp1_file.exists():
            df_dict = pd.read_excel(exp1_file, sheet_name=None)
            resultados['Experimento_1'] = {}
            for sheet_name in ['2.1', '3.1', '5.1', '6.1', '9.1', '12.1']:
                if sheet_name in df_dict:
                    df = df_dict[sheet_name]
                    # Buscar el valor de % FAMEs en la columna Unnamed: 9
                    fames_idx = df[df.iloc[:, 9] == '% FAMEs'].index
                    if len(fames_idx) > 0:
                        fames_value = df.iloc[fames_idx[0] + 1, 9]
                        resultados['Experimento_1'][sheet_name] = float(fames_value) if pd.notna(fames_value) else None

        return resultados

    def generar_resumen(self):
        """Genera un resumen completo del análisis"""
        self.analizar_todos_experimentos()

        resumen = {
            'total_experimentos': len(self.experimentos),
            'total_muestras': sum(len(exp['muestras']) for exp in self.experimentos.values()),
            'periodo': '03/10/2025 - 07/11/2025',
            'experimentos': self.experimentos
        }

        return resumen

    def imprimir_resumen(self):
        """Imprime un resumen legible"""
        resumen = self.generar_resumen()

        print("=" * 80)
        print("ANÁLISIS DE CROMATOGRAMAS DE BIODIESEL")
        print("=" * 80)
        print(f"\nPERÍODO DE ANÁLISIS: {resumen['periodo']}")
        print(f"TOTAL DE EXPERIMENTOS: {resumen['total_experimentos']}")
        print(f"TOTAL DE MUESTRAS ANALIZADAS: {resumen['total_muestras']}")

        print("\n" + "=" * 80)
        print("SECUENCIA CRONOLÓGICA DE EXPERIMENTOS")
        print("=" * 80)

        for i, (key, exp) in enumerate(sorted(resumen['experimentos'].items(),
                                              key=lambda x: x[1]['fecha']), 1):
            print(f"\n{i}. {exp['nombre']}")
            print(f"   Fecha: {exp['fecha']}")
            print(f"   Directorio: {exp['directorio']}")

            if 'condiciones' in exp:
                print(f"   Condiciones:")
                for cond_key, cond_val in exp['condiciones'].items():
                    print(f"      - {cond_key}: {cond_val}")

            print(f"   Muestras analizadas ({len(exp['muestras'])}):")
            for muestra in exp['muestras']:
                if 'tiempo' in muestra:
                    print(f"      • {muestra['nombre']:10} - {muestra['tiempo']:20} - {muestra['tipo']}")
                elif 'conversion' in muestra:
                    print(f"      • {muestra['nombre']:10} - Conversión: {muestra['conversion']:8} - {muestra['tipo']}")
                else:
                    print(f"      • {muestra['nombre']:10} - {muestra['tipo']}")

        print("\n" + "=" * 80)
        print("TIPOS DE ANÁLISIS REALIZADOS")
        print("=" * 80)
        print("\n1. CROMATOGRAFÍA DE GASES (GC)")
        print("   - Determinación de ésteres metílicos de ácidos grasos (FAMEs)")
        print("   - Medición de conversión de aceite a biodiesel")
        print("   - Análisis cuantitativo con estándar interno (SI)")

        print("\n2. PARÁMETROS MEDIDOS EN CADA MUESTRA:")
        print("   - Tiempo de retención (min)")
        print("   - Área del pico (µV.Min)")
        print("   - Altura del pico (µV)")
        print("   - Porcentaje de área (% Area)")
        print("   - Porcentaje de FAMEs (% conversión a biodiesel)")

        print("\n3. ESTÁNDAR INTERNO:")
        print("   - Heptano utilizado como estándar interno")
        print("   - Peso del SI: 103.8 mg")
        print("   - Volumen total: 10 mL")
        print("   - Concentración: 10.38 mg/mL")

        print("\n" + "=" * 80)
        print("NOMENCLATURA DE MUESTRAS")
        print("=" * 80)
        print("\nSistema de numeración:")
        print("  - X.1: Primera serie de muestras (Experimento 1 y repetición)")
        print("  - X.2: Segunda serie de muestras (MORAN 07/11/2025)")
        print("  - SN: Sample Notes (muestras especiales)")
        print("  - RXN: Reacción específica")
        print("  - MITAD/FINAL: Puntos de control en reacción")

        print("\n" + "=" * 80)

if __name__ == '__main__':
    base_dir = '/home/user/ExperimentosBiodiesel_row'
    analizador = AnalizadorCromatogramas(base_dir)
    analizador.imprimir_resumen()

    # Guardar resumen en JSON
    resumen = analizador.generar_resumen()
    output_file = Path(base_dir) / 'resumen_analisis_cromatogramas.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)

    print(f"\nResumen guardado en: {output_file}")
