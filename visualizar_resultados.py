#!/usr/bin/env python3
"""
Script para visualizar resultados del análisis de cromatogramas
Genera gráficos de evolución temporal, comparaciones y composición
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class VisualizadorResultados:
    def __init__(self, procesados_dir):
        self.procesados_dir = Path(procesados_dir)
        self.figuras_dir = self.procesados_dir / 'figuras'
        self.figuras_dir.mkdir(exist_ok=True)

        # Cargar datos
        self.tabla = pd.read_csv(self.procesados_dir / 'tabla_resumen.csv')

        with open(self.procesados_dir / 'resultados_consolidados.json', 'r') as f:
            self.resultados = json.load(f)

    def graficar_evolucion_temporal(self):
        """Gráfico de evolución temporal para Experimento 1"""
        print("\nGenerando gráfico de evolución temporal...")

        # Filtrar Experimento 1
        df_exp1 = self.tabla[self.tabla['Experimento'] == 'Experimento1'].copy()

        # Extraer número de muestra y crear eje temporal
        df_exp1['Num_muestra'] = df_exp1['Muestra'].str.extract(r'(\d+)').astype(int)
        df_exp1 = df_exp1.sort_values('Num_muestra')

        # Tiempos en minutos (cada muestra a 24 min)
        tiempos = [0, 24, 48, 72, 96, 120]
        df_exp1['Tiempo_min'] = tiempos[:len(df_exp1)]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Gráfico 1: Conversión vs Tiempo
        ax1.plot(df_exp1['Tiempo_min'], df_exp1['Conversión FAMEs (%)'],
                marker='o', linewidth=2, markersize=8, label='Conversión FAMEs')
        ax1.set_xlabel('Tiempo (minutos)', fontsize=12)
        ax1.set_ylabel('Conversión FAMEs (%)', fontsize=12)
        ax1.set_title('Evolución Temporal de la Conversión a Biodiesel\nExperimento 1 (03/10/2025)',
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([95, 100])
        ax1.legend()

        # Añadir anotaciones
        for i, row in df_exp1.iterrows():
            ax1.annotate(f"{row['Conversión FAMEs (%)']:.2f}%",
                        (row['Tiempo_min'], row['Conversión FAMEs (%)']),
                        textcoords="offset points", xytext=(0,10),
                        ha='center', fontsize=9)

        # Gráfico 2: Pureza y Glicéridos
        ax2.plot(df_exp1['Tiempo_min'], df_exp1['Pureza (%)'],
                marker='s', linewidth=2, markersize=8, label='Pureza Biodiesel', color='green')
        ax2.plot(df_exp1['Tiempo_min'], df_exp1['Triglicéridos (%)'],
                marker='^', linewidth=2, markersize=8, label='Triglicéridos', color='red')
        ax2.set_xlabel('Tiempo (minutos)', fontsize=12)
        ax2.set_ylabel('Porcentaje (%)', fontsize=12)
        ax2.set_title('Evolución de Pureza y Contenido de Triglicéridos',
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'evolucion_temporal_exp1.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: evolucion_temporal_exp1.png")
        plt.close()

    def graficar_comparacion_experimentos(self):
        """Comparación de conversión entre todos los experimentos"""
        print("\nGenerando gráfico comparativo entre experimentos...")

        fig, ax = plt.subplots(figsize=(14, 8))

        # Preparar datos
        experimentos = []
        conversiones = []
        colores_exp = {'Experimento1': '#1f77b4', 'Experimento2': '#ff7f0e',
                      'Experimento3': '#2ca02c', 'Experimento4': '#d62728'}

        for exp in self.tabla['Experimento'].unique():
            df_exp = self.tabla[self.tabla['Experimento'] == exp]
            for _, row in df_exp.iterrows():
                experimentos.append(f"{exp}\n{row['Muestra']}")
                conversiones.append(row['Conversión FAMEs (%)'])

        # Crear gráfico de barras
        colors = [colores_exp[exp.split('\n')[0]] for exp in experimentos]
        bars = ax.bar(range(len(conversiones)), conversiones, color=colors, alpha=0.7, edgecolor='black')

        ax.set_xlabel('Experimento / Muestra', fontsize=12)
        ax.set_ylabel('Conversión FAMEs (%)', fontsize=12)
        ax.set_title('Comparación de Conversión a Biodiesel entre Todos los Experimentos',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(experimentos)))
        ax.set_xticklabels(experimentos, rotation=45, ha='right', fontsize=8)
        ax.set_ylim([95, 100])
        ax.grid(True, axis='y', alpha=0.3)

        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color, edgecolor='black', label=exp)
                          for exp, color in colores_exp.items()]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'comparacion_experimentos.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: comparacion_experimentos.png")
        plt.close()

    def graficar_composicion_muestras(self):
        """Gráfico de composición de muestras (FAMEs vs Glicéridos)"""
        print("\nGenerando gráfico de composición...")

        fig, ax = plt.subplots(figsize=(14, 8))

        # Preparar datos para gráfico de barras apiladas
        muestras_nombres = []
        purezas = []
        monogliceridos = []
        digliceridos = []
        trigliceridos = []

        for _, row in self.tabla.iterrows():
            muestras_nombres.append(f"{row['Experimento'][-1]}.{row['Muestra']}")
            purezas.append(row['Pureza (%)'])
            monogliceridos.append(row['Monoglicéridos (%)'])
            digliceridos.append(row['Diglicéridos (%)'])
            trigliceridos.append(row['Triglicéridos (%)'])

        x = np.arange(len(muestras_nombres))
        width = 0.8

        # Crear barras apiladas
        p1 = ax.bar(x, purezas, width, label='Pureza FAMEs', color='#2ecc71')
        p2 = ax.bar(x, monogliceridos, width, bottom=purezas,
                   label='Monoglicéridos', color='#e74c3c')
        p3 = ax.bar(x, digliceridos, width,
                   bottom=np.array(purezas)+np.array(monogliceridos),
                   label='Diglicéridos', color='#f39c12')
        p4 = ax.bar(x, trigliceridos, width,
                   bottom=np.array(purezas)+np.array(monogliceridos)+np.array(digliceridos),
                   label='Triglicéridos', color='#9b59b6')

        ax.set_xlabel('Muestra (Experimento.ID)', fontsize=12)
        ax.set_ylabel('Composición (%)', fontsize=12)
        ax.set_title('Composición de Muestras: FAMEs vs Glicéridos Residuales',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(muestras_nombres, rotation=45, ha='right', fontsize=8)
        ax.legend(loc='upper right')
        ax.grid(True, axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'composicion_muestras.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: composicion_muestras.png")
        plt.close()

    def graficar_reproducibilidad(self):
        """Comparación de reproducibilidad entre Experimento 1 y 3"""
        print("\nGenerando gráfico de reproducibilidad...")

        df_exp1 = self.tabla[self.tabla['Experimento'] == 'Experimento1'].copy()
        df_exp3 = self.tabla[self.tabla['Experimento'] == 'Experimento3'].copy()

        # Ordenar por muestra
        df_exp1 = df_exp1.sort_values('Muestra')
        df_exp3 = df_exp3.sort_values('Muestra')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Gráfico 1: Conversión
        x = np.arange(len(df_exp1))
        width = 0.35

        ax1.bar(x - width/2, df_exp1['Conversión FAMEs (%)'], width,
               label='Experimento 1 (03/10)', color='#3498db', alpha=0.8)
        ax1.bar(x + width/2, df_exp3['Conversión FAMEs (%)'], width,
               label='Experimento 3 (24/10)', color='#e74c3c', alpha=0.8)

        ax1.set_xlabel('Muestra', fontsize=12)
        ax1.set_ylabel('Conversión FAMEs (%)', fontsize=12)
        ax1.set_title('Reproducibilidad: Conversión a Biodiesel',
                     fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df_exp1['Muestra'])
        ax1.legend()
        ax1.grid(True, axis='y', alpha=0.3)
        ax1.set_ylim([96, 100])

        # Gráfico 2: Pureza
        ax2.bar(x - width/2, df_exp1['Pureza (%)'], width,
               label='Experimento 1 (03/10)', color='#3498db', alpha=0.8)
        ax2.bar(x + width/2, df_exp3['Pureza (%)'], width,
               label='Experimento 3 (24/10)', color='#e74c3c', alpha=0.8)

        ax2.set_xlabel('Muestra', fontsize=12)
        ax2.set_ylabel('Pureza (%)', fontsize=12)
        ax2.set_title('Reproducibilidad: Pureza del Biodiesel',
                     fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(df_exp3['Muestra'])
        ax2.legend()
        ax2.grid(True, axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'reproducibilidad_exp1_vs_exp3.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: reproducibilidad_exp1_vs_exp3.png")
        plt.close()

    def graficar_estadisticas_globales(self):
        """Gráficos de estadísticas globales"""
        print("\nGenerando gráficos estadísticos...")

        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

        # 1. Boxplot de conversión por experimento
        ax1 = fig.add_subplot(gs[0, 0])
        data_conv = [self.tabla[self.tabla['Experimento'] == exp]['Conversión FAMEs (%)'].values
                     for exp in ['Experimento1', 'Experimento2', 'Experimento3', 'Experimento4']]
        bp1 = ax1.boxplot(data_conv, labels=['Exp1', 'Exp2', 'Exp3', 'Exp4'], patch_artist=True)
        for patch in bp1['boxes']:
            patch.set_facecolor('#3498db')
        ax1.set_ylabel('Conversión FAMEs (%)')
        ax1.set_title('Distribución de Conversión por Experimento')
        ax1.grid(True, alpha=0.3)

        # 2. Boxplot de pureza por experimento
        ax2 = fig.add_subplot(gs[0, 1])
        data_pur = [self.tabla[self.tabla['Experimento'] == exp]['Pureza (%)'].values
                    for exp in ['Experimento1', 'Experimento2', 'Experimento3', 'Experimento4']]
        bp2 = ax2.boxplot(data_pur, labels=['Exp1', 'Exp2', 'Exp3', 'Exp4'], patch_artist=True)
        for patch in bp2['boxes']:
            patch.set_facecolor('#2ecc71')
        ax2.set_ylabel('Pureza (%)')
        ax2.set_title('Distribución de Pureza por Experimento')
        ax2.grid(True, alpha=0.3)

        # 3. Histograma de conversión
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.hist(self.tabla['Conversión FAMEs (%)'], bins=15, color='#9b59b6', alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Conversión FAMEs (%)')
        ax3.set_ylabel('Frecuencia')
        ax3.set_title('Distribución Global de Conversión')
        ax3.axvline(self.tabla['Conversión FAMEs (%)'].mean(), color='red', linestyle='--',
                   label=f'Media: {self.tabla["Conversión FAMEs (%)"].mean():.2f}%')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Scatter: Conversión vs Pureza
        ax4 = fig.add_subplot(gs[1, :2])
        colors = {'Experimento1': '#1f77b4', 'Experimento2': '#ff7f0e',
                 'Experimento3': '#2ca02c', 'Experimento4': '#d62728'}
        for exp in self.tabla['Experimento'].unique():
            df_exp = self.tabla[self.tabla['Experimento'] == exp]
            ax4.scatter(df_exp['Conversión FAMEs (%)'], df_exp['Pureza (%)'],
                       label=exp, s=100, alpha=0.6, color=colors[exp])
        ax4.set_xlabel('Conversión FAMEs (%)')
        ax4.set_ylabel('Pureza (%)')
        ax4.set_title('Relación entre Conversión y Pureza')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # 5. Promedio de glicéridos
        ax5 = fig.add_subplot(gs[1, 2])
        gliceridos_prom = {
            'Monoglicéridos': self.tabla['Monoglicéridos (%)'].mean(),
            'Diglicéridos': self.tabla['Diglicéridos (%)'].mean(),
            'Triglicéridos': self.tabla['Triglicéridos (%)'].mean()
        }
        ax5.bar(gliceridos_prom.keys(), gliceridos_prom.values(),
               color=['#e74c3c', '#f39c12', '#9b59b6'], alpha=0.7, edgecolor='black')
        ax5.set_ylabel('Contenido Promedio (%)')
        ax5.set_title('Contenido Promedio de Glicéridos')
        ax5.grid(True, axis='y', alpha=0.3)
        plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.savefig(self.figuras_dir / 'estadisticas_globales.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: estadisticas_globales.png")
        plt.close()

    def generar_todos_graficos(self):
        """Genera todos los gráficos"""
        print("=" * 80)
        print("GENERACIÓN DE GRÁFICOS")
        print("=" * 80)

        self.graficar_evolucion_temporal()
        self.graficar_comparacion_experimentos()
        self.graficar_composicion_muestras()
        self.graficar_reproducibilidad()
        self.graficar_estadisticas_globales()

        print("\n" + "=" * 80)
        print("GENERACIÓN COMPLETADA")
        print("=" * 80)
        print(f"\nTodas las figuras guardadas en: {self.figuras_dir}")
        print(f"Total de gráficos generados: 5")

if __name__ == '__main__':
    procesados_dir = '/home/user/ExperimentosBiodiesel_row/Procesados'
    visualizador = VisualizadorResultados(procesados_dir)
    visualizador.generar_todos_graficos()
