#!/usr/bin/env python3
"""
Script para visualizar resultados del análisis de cromatogramas
Genera gráficos de evolución temporal, comparaciones y composición
Versión actualizada con nomenclatura E1a, E1b, E2a, etc.
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

        # Colores para experimentos
        self.colores_exp = {
            'Experimento1': '#1f77b4',
            'Experimento2': '#ff7f0e',
            'Experimento3': '#2ca02c'
        }

        # Información de experimentos
        self.info_exp = {
            'Experimento1': 'Exp1 (03/10/2025)',
            'Experimento2': 'Exp2 (20/10/2025)',
            'Experimento3': 'Exp3 (07/11/2025)'
        }

    def graficar_evolucion_temporal_exp1(self):
        """Gráfico 1: Evolución temporal para Experimento 1 con ordenamiento cronológico correcto"""
        print("\nGenerando gráfico 1: Evolución temporal Experimento 1...")

        # Filtrar Experimento 1 y ordenar por campo Orden
        df_exp1 = self.tabla[self.tabla['Experimento'] == 'Experimento1'].copy()
        df_exp1 = df_exp1.sort_values('Orden')

        # Tiempos en minutos (cada muestra a 24 min)
        tiempos = [0, 24, 48, 72, 96, 120]
        df_exp1['Tiempo_min'] = tiempos[:len(df_exp1)]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Gráfico 1a: Conversión vs Tiempo
        ax1.plot(df_exp1['Tiempo_min'], df_exp1['Conversión FAMEs (%)'],
                marker='o', linewidth=2, markersize=8, label='Conversión FAMEs', color='#2E86AB')
        ax1.set_xlabel('Tiempo (minutos)', fontsize=12)
        ax1.set_ylabel('Conversión FAMEs (%)', fontsize=12)
        ax1.set_title('Evolución Temporal de la Conversión a Biodiesel\nExp1 (03/10/2025) - Muestras ordenadas cronológicamente',
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([95, 100])
        ax1.legend()

        # Añadir anotaciones con nueva nomenclatura
        for i, row in df_exp1.iterrows():
            ax1.annotate(f"{row['Muestra']}: {row['Conversión FAMEs (%)']:.2f}%",
                        (row['Tiempo_min'], row['Conversión FAMEs (%)']),
                        textcoords="offset points", xytext=(0,10),
                        ha='center', fontsize=9)

        # Gráfico 1b: Pureza y Glicéridos
        ax2.plot(df_exp1['Tiempo_min'], df_exp1['Pureza (%)'],
                marker='s', linewidth=2, markersize=8, label='Pureza Biodiesel', color='#06A77D')
        ax2.plot(df_exp1['Tiempo_min'], df_exp1['Triglicéridos (%)'],
                marker='^', linewidth=2, markersize=8, label='Triglicéridos', color='#D62828')
        ax2.set_xlabel('Tiempo (minutos)', fontsize=12)
        ax2.set_ylabel('Porcentaje (%)', fontsize=12)
        ax2.set_title('Evolución de Pureza y Contenido de Triglicéridos',
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig1_evolucion_temporal_exp1.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig1_evolucion_temporal_exp1.png")
        plt.close()

    def graficar_comparacion_experimentos(self):
        """Gráfico 2: Comparación de conversión entre todos los experimentos"""
        print("\nGenerando gráfico 2: Comparación entre experimentos...")

        fig, ax = plt.subplots(figsize=(14, 8))

        # Preparar datos
        muestras_labels = []
        conversiones = []
        colors = []

        for exp in ['Experimento1', 'Experimento2', 'Experimento3']:
            df_exp = self.tabla[self.tabla['Experimento'] == exp].sort_values('Orden')
            for _, row in df_exp.iterrows():
                muestras_labels.append(row['Muestra'])
                conversiones.append(row['Conversión FAMEs (%)'])
                colors.append(self.colores_exp[exp])

        # Crear gráfico de barras
        x_pos = np.arange(len(conversiones))
        bars = ax.bar(x_pos, conversiones, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Muestra', fontsize=12, fontweight='bold')
        ax.set_ylabel('Conversión FAMEs (%)', fontsize=12, fontweight='bold')
        ax.set_title('Comparación de Conversión a Biodiesel entre Todos los Experimentos',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(muestras_labels, rotation=45, ha='right', fontsize=9)
        ax.set_ylim([95, 100])
        ax.grid(True, axis='y', alpha=0.3)

        # Agregar líneas divisorias entre experimentos
        ax.axvline(x=5.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.axvline(x=11.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=self.colores_exp[exp], edgecolor='black',
                                label=self.info_exp[exp])
                          for exp in ['Experimento1', 'Experimento2', 'Experimento3']]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig2_comparacion_experimentos.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig2_comparacion_experimentos.png")
        plt.close()

    def graficar_composicion_apilada(self):
        """Gráfico 3: Composición de muestras (FAMEs vs Glicéridos) - Barras apiladas"""
        print("\nGenerando gráfico 3: Composición de muestras...")

        fig, ax = plt.subplots(figsize=(14, 8))

        # Preparar datos
        muestras_labels = []
        purezas = []
        monogliceridos = []
        digliceridos = []
        trigliceridos = []

        for _, row in self.tabla.iterrows():
            muestras_labels.append(row['Muestra'])
            purezas.append(row['Pureza (%)'])
            monogliceridos.append(row['Monoglicéridos (%)'])
            digliceridos.append(row['Diglicéridos (%)'])
            trigliceridos.append(row['Triglicéridos (%)'])

        x = np.arange(len(muestras_labels))
        width = 0.8

        # Crear barras apiladas
        p1 = ax.bar(x, purezas, width, label='Pureza FAMEs', color='#2ecc71', alpha=0.9)
        p2 = ax.bar(x, monogliceridos, width, bottom=purezas,
                   label='Monoglicéridos', color='#e74c3c', alpha=0.9)
        p3 = ax.bar(x, digliceridos, width,
                   bottom=np.array(purezas)+np.array(monogliceridos),
                   label='Diglicéridos', color='#f39c12', alpha=0.9)
        p4 = ax.bar(x, trigliceridos, width,
                   bottom=np.array(purezas)+np.array(monogliceridos)+np.array(digliceridos),
                   label='Triglicéridos', color='#9b59b6', alpha=0.9)

        ax.set_xlabel('Muestra', fontsize=12, fontweight='bold')
        ax.set_ylabel('Composición (%)', fontsize=12, fontweight='bold')
        ax.set_title('Composición de Muestras: FAMEs vs Glicéridos Residuales',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(muestras_labels, rotation=45, ha='right', fontsize=8)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, axis='y', alpha=0.3)

        # Agregar líneas divisorias entre experimentos
        ax.axvline(x=5.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.axvline(x=11.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig3_composicion_apilada.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig3_composicion_apilada.png")
        plt.close()

    def graficar_comparacion_temporal_experimentos(self):
        """Gráfico 4: Comparación temporal de conversión y pureza promedio por experimento"""
        print("\nGenerando gráfico 4: Comparación temporal entre experimentos...")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        experimentos = ['Experimento1', 'Experimento2', 'Experimento3']
        fechas = ['03/10/2025', '20/10/2025', '07/11/2025']
        nombres_cortos = ['Exp1', 'Exp2', 'Exp3']

        conversiones_promedio = []
        conversiones_std = []
        purezas_promedio = []
        purezas_std = []

        for exp in experimentos:
            df_exp = self.tabla[self.tabla['Experimento'] == exp]
            conversiones_promedio.append(df_exp['Conversión FAMEs (%)'].mean())
            conversiones_std.append(df_exp['Conversión FAMEs (%)'].std())
            purezas_promedio.append(df_exp['Pureza (%)'].mean())
            purezas_std.append(df_exp['Pureza (%)'].std())

        x = np.arange(len(experimentos))
        width = 0.6

        # Gráfico 4a: Conversión promedio
        ax1.bar(x, conversiones_promedio, width, yerr=conversiones_std,
               color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.7,
               capsize=5, edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Experimento', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Conversión FAMEs Promedio (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Evolución Temporal de la Conversión Promedio entre Experimentos',
                     fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels([f'{nombre}\n{fecha}' for nombre, fecha in zip(nombres_cortos, fechas)])
        ax1.grid(True, axis='y', alpha=0.3)
        ax1.set_ylim([95, 100])

        # Añadir valores
        for i, (conv, std) in enumerate(zip(conversiones_promedio, conversiones_std)):
            ax1.text(i, conv + std + 0.2, f'{conv:.2f}%\n±{std:.2f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Gráfico 4b: Pureza promedio
        ax2.bar(x, purezas_promedio, width, yerr=purezas_std,
               color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.7,
               capsize=5, edgecolor='black', linewidth=1.5)
        ax2.set_xlabel('Experimento', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Pureza Promedio (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Evolución Temporal de la Pureza Promedio entre Experimentos',
                     fontsize=14, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels([f'{nombre}\n{fecha}' for nombre, fecha in zip(nombres_cortos, fechas)])
        ax2.grid(True, axis='y', alpha=0.3)

        # Añadir valores
        for i, (pur, std) in enumerate(zip(purezas_promedio, purezas_std)):
            ax2.text(i, pur + std + 0.5, f'{pur:.2f}%\n±{std:.2f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig4_comparacion_temporal.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig4_comparacion_temporal.png")
        plt.close()

    def graficar_estadisticas_boxplot(self):
        """Gráfico 5: Boxplots de conversión y pureza por experimento"""
        print("\nGenerando gráfico 5: Distribuciones estadísticas...")

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

        # Gráfico 5a: Boxplot de conversión
        data_conv = [self.tabla[self.tabla['Experimento'] == exp]['Conversión FAMEs (%)'].values
                     for exp in ['Experimento1', 'Experimento2', 'Experimento3']]
        bp1 = ax1.boxplot(data_conv, tick_labels=['Exp1', 'Exp2', 'Exp3'], patch_artist=True,
                         showmeans=True, meanline=True)
        for patch in bp1['boxes']:
            patch.set_facecolor('#3498db')
            patch.set_alpha(0.7)
        ax1.set_ylabel('Conversión FAMEs (%)', fontweight='bold')
        ax1.set_title('Distribución de Conversión por Experimento', fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Gráfico 5b: Boxplot de pureza
        data_pur = [self.tabla[self.tabla['Experimento'] == exp]['Pureza (%)'].values
                    for exp in ['Experimento1', 'Experimento2', 'Experimento3']]
        bp2 = ax2.boxplot(data_pur, tick_labels=['Exp1', 'Exp2', 'Exp3'], patch_artist=True,
                         showmeans=True, meanline=True)
        for patch in bp2['boxes']:
            patch.set_facecolor('#2ecc71')
            patch.set_alpha(0.7)
        ax2.set_ylabel('Pureza (%)', fontweight='bold')
        ax2.set_title('Distribución de Pureza por Experimento', fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Gráfico 5c: Histograma de conversión global
        ax3.hist(self.tabla['Conversión FAMEs (%)'], bins=15, color='#9b59b6',
                alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_xlabel('Conversión FAMEs (%)', fontweight='bold')
        ax3.set_ylabel('Frecuencia', fontweight='bold')
        ax3.set_title('Distribución Global de Conversión', fontweight='bold')
        media_conv = self.tabla['Conversión FAMEs (%)'].mean()
        ax3.axvline(media_conv, color='red', linestyle='--', linewidth=2,
                   label=f'Media: {media_conv:.2f}%')
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # Gráfico 5d: Histograma de pureza global
        ax4.hist(self.tabla['Pureza (%)'], bins=15, color='#e67e22',
                alpha=0.7, edgecolor='black', linewidth=1.5)
        ax4.set_xlabel('Pureza (%)', fontweight='bold')
        ax4.set_ylabel('Frecuencia', fontweight='bold')
        ax4.set_title('Distribución Global de Pureza', fontweight='bold')
        media_pur = self.tabla['Pureza (%)'].mean()
        ax4.axvline(media_pur, color='red', linestyle='--', linewidth=2,
                   label=f'Media: {media_pur:.2f}%')
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig5_estadisticas_boxplot.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig5_estadisticas_boxplot.png")
        plt.close()

    def graficar_scatter_conversion_pureza(self):
        """Gráfico 6: Scatter plot - Relación entre Conversión y Pureza"""
        print("\nGenerando gráfico 6: Relación conversión vs pureza...")

        fig, ax = plt.subplots(figsize=(12, 8))

        for exp in ['Experimento1', 'Experimento2', 'Experimento3']:
            df_exp = self.tabla[self.tabla['Experimento'] == exp]
            ax.scatter(df_exp['Conversión FAMEs (%)'], df_exp['Pureza (%)'],
                      label=self.info_exp[exp], s=150, alpha=0.7,
                      color=self.colores_exp[exp], edgecolors='black', linewidth=1.5)

            # Añadir etiquetas de muestras
            for _, row in df_exp.iterrows():
                ax.annotate(row['Muestra'],
                           (row['Conversión FAMEs (%)'], row['Pureza (%)']),
                           textcoords="offset points", xytext=(5,5),
                           ha='left', fontsize=8, alpha=0.7)

        ax.set_xlabel('Conversión FAMEs (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Pureza (%)', fontsize=12, fontweight='bold')
        ax.set_title('Relación entre Conversión y Pureza del Biodiesel',
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig6_scatter_conversion_pureza.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig6_scatter_conversion_pureza.png")
        plt.close()

    def graficar_gliceridos_promedio(self):
        """Gráfico 7: Contenido promedio de glicéridos por experimento"""
        print("\nGenerando gráfico 7: Contenido de glicéridos...")

        fig, ax = plt.subplots(figsize=(14, 8))

        experimentos = ['Experimento1', 'Experimento2', 'Experimento3']
        nombres_cortos = ['Exp1\n03/10/25', 'Exp2\n20/10/25', 'Exp3\n07/11/25']

        mag_promedio = []
        dag_promedio = []
        tag_promedio = []

        for exp in experimentos:
            df_exp = self.tabla[self.tabla['Experimento'] == exp]
            mag_promedio.append(df_exp['Monoglicéridos (%)'].mean())
            dag_promedio.append(df_exp['Diglicéridos (%)'].mean())
            tag_promedio.append(df_exp['Triglicéridos (%)'].mean())

        x = np.arange(len(experimentos))
        width = 0.25

        bars1 = ax.bar(x - width, mag_promedio, width, label='Monoglicéridos',
                      color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
        bars2 = ax.bar(x, dag_promedio, width, label='Diglicéridos',
                      color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
        bars3 = ax.bar(x + width, tag_promedio, width, label='Triglicéridos',
                      color='#9b59b6', alpha=0.8, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Experimento', fontsize=12, fontweight='bold')
        ax.set_ylabel('Contenido Promedio (%)', fontsize=12, fontweight='bold')
        ax.set_title('Contenido Promedio de Glicéridos Residuales por Experimento',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(nombres_cortos)
        ax.legend(fontsize=11)
        ax.grid(True, axis='y', alpha=0.3)

        # Añadir valores en las barras
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig7_gliceridos_promedio.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig7_gliceridos_promedio.png")
        plt.close()

    def graficar_area_fames(self):
        """Gráfico 8: Área de picos FAMEs por muestra"""
        print("\nGenerando gráfico 8: Área de picos FAMEs...")

        fig, ax = plt.subplots(figsize=(14, 8))

        muestras = self.tabla['Muestra'].values
        areas = self.tabla['Área FAMEs'].values
        colors = [self.colores_exp[exp] for exp in self.tabla['Experimento'].values]

        x_pos = np.arange(len(muestras))
        bars = ax.bar(x_pos, areas, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Muestra', fontsize=12, fontweight='bold')
        ax.set_ylabel('Área Total de Picos FAMEs', fontsize=12, fontweight='bold')
        ax.set_title('Área Total de Picos FAMEs por Muestra',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(muestras, rotation=45, ha='right', fontsize=9)
        ax.grid(True, axis='y', alpha=0.3)

        # Agregar líneas divisorias entre experimentos
        ax.axvline(x=5.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.axvline(x=11.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=self.colores_exp[exp], edgecolor='black',
                                label=self.info_exp[exp])
                          for exp in ['Experimento1', 'Experimento2', 'Experimento3']]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig8_area_fames.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig8_area_fames.png")
        plt.close()

    def graficar_picos_fames(self):
        """Gráfico 9: Número de picos FAMEs identificados por muestra"""
        print("\nGenerando gráfico 9: Número de picos FAMEs...")

        fig, ax = plt.subplots(figsize=(14, 8))

        muestras = self.tabla['Muestra'].values
        picos = self.tabla['Picos FAMEs'].values
        colors = [self.colores_exp[exp] for exp in self.tabla['Experimento'].values]

        x_pos = np.arange(len(muestras))
        bars = ax.bar(x_pos, picos, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

        ax.set_xlabel('Muestra', fontsize=12, fontweight='bold')
        ax.set_ylabel('Número de Picos FAMEs', fontsize=12, fontweight='bold')
        ax.set_title('Número de Picos FAMEs Identificados por Muestra',
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(muestras, rotation=45, ha='right', fontsize=9)
        ax.grid(True, axis='y', alpha=0.3)

        # Agregar líneas divisorias entre experimentos
        ax.axvline(x=5.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.axvline(x=11.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

        # Añadir valores en las barras
        for i, (bar, pico) in enumerate(zip(bars, picos)):
            ax.text(bar.get_x() + bar.get_width()/2., pico + 0.5,
                   f'{int(pico)}', ha='center', va='bottom', fontsize=8)

        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=self.colores_exp[exp], edgecolor='black',
                                label=self.info_exp[exp])
                          for exp in ['Experimento1', 'Experimento2', 'Experimento3']]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig9_picos_fames.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig9_picos_fames.png")
        plt.close()

    def graficar_heatmap_calidad(self):
        """Gráfico 10: Heatmap de parámetros de calidad"""
        print("\nGenerando gráfico 10: Heatmap de parámetros de calidad...")

        fig, ax = plt.subplots(figsize=(14, 10))

        # Preparar datos para heatmap
        parametros = ['Conversión FAMEs (%)', 'Pureza (%)',
                     'Monoglicéridos (%)', 'Diglicéridos (%)', 'Triglicéridos (%)']
        muestras = self.tabla['Muestra'].values

        # Normalizar datos para visualización (0-1)
        data_matrix = []
        for param in parametros:
            values = self.tabla[param].values
            # Normalizar
            norm_values = (values - values.min()) / (values.max() - values.min())
            data_matrix.append(norm_values)

        data_matrix = np.array(data_matrix)

        # Crear heatmap
        im = ax.imshow(data_matrix, cmap='RdYlGn', aspect='auto')

        # Configurar ejes
        ax.set_xticks(np.arange(len(muestras)))
        ax.set_yticks(np.arange(len(parametros)))
        ax.set_xticklabels(muestras, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(parametros, fontsize=10)

        # Agregar colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Valor Normalizado (0-1)', rotation=270, labelpad=20, fontweight='bold')

        # Añadir valores reales en las celdas
        for i in range(len(parametros)):
            for j in range(len(muestras)):
                valor_real = self.tabla[parametros[i]].values[j]
                text = ax.text(j, i, f'{valor_real:.1f}',
                             ha="center", va="center", color="black", fontsize=7)

        ax.set_title('Mapa de Calor: Parámetros de Calidad por Muestra',
                    fontsize=14, fontweight='bold', pad=20)

        # Agregar líneas divisorias entre experimentos
        ax.axvline(x=5.5, color='white', linestyle='-', linewidth=2)
        ax.axvline(x=11.5, color='white', linestyle='-', linewidth=2)

        plt.tight_layout()
        plt.savefig(self.figuras_dir / 'fig10_heatmap_calidad.png', dpi=300, bbox_inches='tight')
        print(f"  ✓ Guardado: fig10_heatmap_calidad.png")
        plt.close()

    def generar_todos_graficos(self):
        """Genera todos los gráficos"""
        print("=" * 80)
        print("GENERACIÓN DE GRÁFICOS CON NUEVA NOMENCLATURA")
        print("=" * 80)

        self.graficar_evolucion_temporal_exp1()
        self.graficar_comparacion_experimentos()
        self.graficar_composicion_apilada()
        self.graficar_comparacion_temporal_experimentos()
        self.graficar_estadisticas_boxplot()
        self.graficar_scatter_conversion_pureza()
        self.graficar_gliceridos_promedio()
        self.graficar_area_fames()
        self.graficar_picos_fames()
        self.graficar_heatmap_calidad()

        print("\n" + "=" * 80)
        print("GENERACIÓN COMPLETADA")
        print("=" * 80)
        print(f"\nTodas las figuras guardadas en: {self.figuras_dir}")
        print(f"Total de gráficos generados: 10")
        print("\nÍndice de figuras:")
        print("  fig1_evolucion_temporal_exp1.png - Evolución temporal Exp1")
        print("  fig2_comparacion_experimentos.png - Comparación entre experimentos")
        print("  fig3_composicion_apilada.png - Composición de muestras")
        print("  fig4_comparacion_temporal.png - Comparación temporal promedio")
        print("  fig5_estadisticas_boxplot.png - Distribuciones estadísticas")
        print("  fig6_scatter_conversion_pureza.png - Relación conversión-pureza")
        print("  fig7_gliceridos_promedio.png - Contenido de glicéridos")
        print("  fig8_area_fames.png - Área de picos FAMEs")
        print("  fig9_picos_fames.png - Número de picos FAMEs")
        print("  fig10_heatmap_calidad.png - Mapa de calor de parámetros")

if __name__ == '__main__':
    procesados_dir = '/home/user/ExperimentosBiodiesel_row/Procesados'
    visualizador = VisualizadorResultados(procesados_dir)
    visualizador.generar_todos_graficos()
