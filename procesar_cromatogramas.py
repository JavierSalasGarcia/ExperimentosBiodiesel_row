#!/usr/bin/env python3
"""
Script para procesar datos de cromatogramas y calcular parámetros de calidad
Implementa la metodología descrita en analisis_biodiesel.tex
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

class ProcesadorCromatogramas:
    def __init__(self, procesados_dir):
        self.procesados_dir = Path(procesados_dir)
        self.resultados = {}

        # Rangos de tiempo de retención para identificación de componentes
        self.rangos_tr = {
            'heptano': (0.96, 0.99),
            'metanol': (2.20, 2.35),
            'fames': (6.50, 11.50),
            'monogliceridos': (7.40, 8.60),
            'digliceridos': (7.70, 8.40),
            'trigliceridos': (7.00, 7.25)
        }

        # Parámetros del estándar interno
        self.peso_si = 103.8  # mg
        self.volumen_total_si = 10.0  # mL
        self.conc_si = self.peso_si / self.volumen_total_si  # mg/mL

    def identificar_picos_rango(self, df, t_min, t_max):
        """Identifica picos en un rango de tiempo de retención"""
        if 'Time' not in df.columns:
            return pd.DataFrame()

        mask = (df['Time'] >= t_min) & (df['Time'] <= t_max)
        return df[mask].copy()

    def identificar_componente(self, df, componente):
        """Identifica un componente específico por su rango de TR"""
        if componente not in self.rangos_tr:
            return pd.DataFrame()

        t_min, t_max = self.rangos_tr[componente]
        return self.identificar_picos_rango(df, t_min, t_max)

    def calcular_area_total_componente(self, df, componente):
        """Calcula el área total de un componente"""
        picos = self.identificar_componente(df, componente)
        if picos.empty or 'Area' not in picos.columns:
            return 0.0

        return picos['Area'].sum()

    def calcular_conversion_fames(self, df):
        """Calcula el porcentaje de conversión a FAMEs"""
        area_fames = self.calcular_area_total_componente(df, 'fames')
        area_heptano = self.calcular_area_total_componente(df, 'heptano')

        if 'Area' in df.columns:
            area_total = df['Area'].sum()
        else:
            return 0.0

        # Excluir heptano del área total
        area_total_sin_si = area_total - area_heptano

        if area_total_sin_si > 0:
            conversion = (area_fames / area_total_sin_si) * 100
        else:
            conversion = 0.0

        return conversion

    def calcular_pureza_biodiesel(self, df):
        """Calcula la pureza del biodiesel"""
        area_fames = self.calcular_area_total_componente(df, 'fames')
        area_mag = self.calcular_area_total_componente(df, 'monogliceridos')
        area_dag = self.calcular_area_total_componente(df, 'digliceridos')
        area_tag = self.calcular_area_total_componente(df, 'trigliceridos')

        area_total_productos = area_fames + area_mag + area_dag + area_tag

        if area_total_productos > 0:
            pureza = (area_fames / area_total_productos) * 100
        else:
            pureza = 0.0

        return pureza

    def calcular_contenido_gliceridos(self, df):
        """Calcula el contenido relativo de glicéridos"""
        area_total = df['Area'].sum() if 'Area' in df.columns else 1.0
        area_heptano = self.calcular_area_total_componente(df, 'heptano')
        area_total_sin_si = area_total - area_heptano

        if area_total_sin_si == 0:
            area_total_sin_si = 1.0

        resultados = {
            'monogliceridos_pct': (self.calcular_area_total_componente(df, 'monogliceridos') / area_total_sin_si) * 100,
            'digliceridos_pct': (self.calcular_area_total_componente(df, 'digliceridos') / area_total_sin_si) * 100,
            'trigliceridos_pct': (self.calcular_area_total_componente(df, 'trigliceridos') / area_total_sin_si) * 100
        }

        return resultados

    def cuantificar_fames(self, df, peso_muestra_mg):
        """Cuantificación absoluta de FAMEs usando estándar interno"""
        area_fames = self.calcular_area_total_componente(df, 'fames')
        area_heptano = self.calcular_area_total_componente(df, 'heptano')

        if area_heptano == 0:
            return 0.0

        # C_FAMEs = (A_FAMEs / A_SI) * (m_SI / m_muestra) * C_SI
        conc_fames = (area_fames / area_heptano) * (self.peso_si / peso_muestra_mg) * self.conc_si

        return conc_fames

    def procesar_muestra(self, csv_file, nombre_muestra, peso_muestra_mg=None):
        """Procesa una muestra completa y calcula todos los parámetros"""
        try:
            df = pd.read_csv(csv_file)

            # Limpiar datos: remover filas de encabezados repetidos
            if 'Time' in df.columns:
                # Convertir Time a numérico, marcando errores como NaN
                df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
                df = df[pd.notna(df['Time'])]

            # Convertir Area a numérico
            if 'Area' in df.columns:
                df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
                df = df[pd.notna(df['Area'])]

            resultados = {
                'nombre': nombre_muestra,
                'archivo': str(csv_file),
                'conversion_fames_pct': self.calcular_conversion_fames(df),
                'pureza_biodiesel_pct': self.calcular_pureza_biodiesel(df),
                'gliceridos': self.calcular_contenido_gliceridos(df),
                'area_heptano': self.calcular_area_total_componente(df, 'heptano'),
                'area_fames': self.calcular_area_total_componente(df, 'fames'),
                'num_picos_total': len(df),
                'num_picos_fames': len(self.identificar_componente(df, 'fames'))
            }

            if peso_muestra_mg:
                resultados['concentracion_fames_mg_ml'] = self.cuantificar_fames(df, peso_muestra_mg)

            return resultados

        except Exception as e:
            print(f"Error procesando {csv_file}: {e}")
            return None

    def procesar_experimento(self, experimento_dir, experimento_num):
        """Procesa todas las muestras de un experimento"""
        print(f"\nProcesando Experimento {experimento_num}...")

        exp_path = self.procesados_dir / experimento_dir
        metadata_file = exp_path / 'metadata.json'

        if not metadata_file.exists():
            print(f"  ERROR: No se encuentra metadata.json")
            return

        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        resultados_exp = {
            'experimento': metadata['experimento'],
            'fecha': metadata['fecha'],
            'muestras': []
        }

        # Crear mapeo de archivos CSV a nomenclatura
        nomenclatura_map = {}
        for muestra_info in metadata.get('muestras', []):
            archivo_csv = muestra_info.get('archivo_csv', '')
            nombre_archivo = Path(archivo_csv).stem.replace('muestra_', '').replace('_raw', '')
            nomenclatura_map[nombre_archivo] = {
                'nomenclatura': muestra_info.get('nomenclatura', nombre_archivo),
                'orden': muestra_info.get('orden', 0)
            }

        # Procesar cada muestra
        csv_files = sorted(exp_path.glob('muestra_*_raw.csv'))

        for csv_file in csv_files:
            nombre_archivo = csv_file.stem.replace('muestra_', '').replace('_raw', '')

            # Obtener nomenclatura actualizada
            if nombre_archivo in nomenclatura_map:
                nomenclatura = nomenclatura_map[nombre_archivo]['nomenclatura']
                orden = nomenclatura_map[nombre_archivo]['orden']
            else:
                nomenclatura = nombre_archivo
                orden = 0

            print(f"  Procesando {nombre_archivo} → {nomenclatura}...")

            resultado = self.procesar_muestra(csv_file, nomenclatura)
            if resultado:
                resultado['nombre_original'] = nombre_archivo
                resultado['orden'] = orden
                resultados_exp['muestras'].append(resultado)

        # Calcular estadísticas del experimento
        if resultados_exp['muestras']:
            conversiones = [m['conversion_fames_pct'] for m in resultados_exp['muestras']]
            purezas = [m['pureza_biodiesel_pct'] for m in resultados_exp['muestras']]

            resultados_exp['estadisticas'] = {
                'conversion_promedio': np.mean(conversiones),
                'conversion_std': np.std(conversiones),
                'conversion_max': np.max(conversiones),
                'conversion_min': np.min(conversiones),
                'pureza_promedio': np.mean(purezas),
                'pureza_std': np.std(purezas)
            }

        self.resultados[f'Experimento{experimento_num}'] = resultados_exp

        # Guardar resultados del experimento
        output_file = exp_path / 'resultados_procesados.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultados_exp, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Resultados guardados en {output_file.name}")

    def procesar_todos_experimentos(self):
        """Procesa todos los experimentos"""
        print("=" * 80)
        print("PROCESAMIENTO DE CROMATOGRAMAS")
        print("=" * 80)

        self.procesar_experimento('Experimento1', 1)
        self.procesar_experimento('Experimento2', 2)
        self.procesar_experimento('Experimento3', 3)

        # Guardar resultados consolidados
        output_file = self.procesados_dir / 'resultados_consolidados.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 80)
        print("PROCESAMIENTO COMPLETADO")
        print("=" * 80)
        print(f"\nResultados consolidados guardados en: {output_file}")

    def generar_tabla_resumen(self):
        """Genera una tabla resumen de todos los resultados"""
        data = []

        for exp_name, exp_data in self.resultados.items():
            for muestra in exp_data['muestras']:
                data.append({
                    'Experimento': exp_name,
                    'Fecha': exp_data['fecha'],
                    'Muestra': muestra['nombre'],
                    'Nombre_Original': muestra.get('nombre_original', muestra['nombre']),
                    'Orden': muestra.get('orden', 0),
                    'Conversión FAMEs (%)': round(muestra['conversion_fames_pct'], 2),
                    'Pureza (%)': round(muestra['pureza_biodiesel_pct'], 2),
                    'Monoglicéridos (%)': round(muestra['gliceridos']['monogliceridos_pct'], 2),
                    'Diglicéridos (%)': round(muestra['gliceridos']['digliceridos_pct'], 2),
                    'Triglicéridos (%)': round(muestra['gliceridos']['trigliceridos_pct'], 2),
                    'Área FAMEs': round(muestra['area_fames'], 2),
                    'Picos FAMEs': muestra['num_picos_fames']
                })

        df = pd.DataFrame(data)

        # Ordenar por Experimento y Orden
        df = df.sort_values(['Experimento', 'Orden'])

        # Guardar tabla CSV
        tabla_file = self.procesados_dir / 'tabla_resumen.csv'
        df.to_csv(tabla_file, index=False)

        print(f"\n✓ Tabla resumen guardada en: {tabla_file}")
        print(f"\nResumen de resultados:")
        print(df.to_string(index=False))

        return df

    def generar_resumen_final(self):
        """Genera un resumen final de todos los experimentos"""
        print("\n" + "=" * 80)
        print("RESUMEN DE TODOS LOS EXPERIMENTOS")
        print("=" * 80)

        for exp_name in ['Experimento1', 'Experimento2', 'Experimento3']:
            if exp_name in self.resultados:
                exp = self.resultados[exp_name]
                print(f"\n{exp['experimento']} ({exp['fecha']}):")
                print(f"  Muestras analizadas: {len(exp['muestras'])}")
                if 'estadisticas' in exp:
                    print(f"  Conversión promedio: {exp['estadisticas']['conversion_promedio']:.2f}% ± {exp['estadisticas']['conversion_std']:.2f}%")
                    print(f"  Pureza promedio: {exp['estadisticas']['pureza_promedio']:.2f}% ± {exp['estadisticas']['pureza_std']:.2f}%")
                    print(f"  Coeficiente de variación: {(exp['estadisticas']['conversion_std'] / exp['estadisticas']['conversion_promedio'] * 100):.2f}%")

if __name__ == '__main__':
    procesados_dir = '/home/user/ExperimentosBiodiesel_row/Procesados'
    procesador = ProcesadorCromatogramas(procesados_dir)

    procesador.procesar_todos_experimentos()
    procesador.generar_tabla_resumen()
    procesador.generar_resumen_final()
