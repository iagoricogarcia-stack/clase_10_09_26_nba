
import pandas as pd


# PARTE 1: Carga de datos y limpieza

# Cargamos el nuevo dataset
df = pd.read_csv("games.csv")

# Limpieza: eliminamos filas donde no hay puntos registrados (NaN)
df = df.dropna(subset=['PTS_home', 'PTS_away'])


# PARTE 2: Ordenar muestra con Bubble Sort O(n^2)

# Filtramos por la temporada 2019 usando la columna 'SEASON'
season = df[df['SEASON'] == 2019].copy()

# Calculamos los puntos totales usando las nuevas columnas
season['TOTAL_POINTS'] = season['PTS_home'] + season['PTS_away']

# Seleccionamos las columnas correspondientes en el nuevo CSV
columnas_muestra = ['GAME_DATE_EST', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'PTS_home', 'PTS_away', 'TOTAL_POINTS']
sample = season[columnas_muestra].head(500).to_dict('records')

def bubble_sort(arr, key):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][key] < arr[j + 1][key]:  # Orden descendente
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

sorted_games = bubble_sort(sample, "TOTAL_POINTS")

print("--- TOP 10 PARTIDOS CON MÁS PUNTOS (MUESTRA 2019) ---")
for g in sorted_games[:10]:
    # Mostramos los IDs de los equipos al no disponer de los nombres en formato texto
    print(f"{g['GAME_DATE_EST']}: Eq_Local({g['HOME_TEAM_ID']}) {int(g['PTS_home'])} - "
          f"Eq_Visitante({g['VISITOR_TEAM_ID']}) {int(g['PTS_away'])} "
          f"(Total: {int(g['TOTAL_POINTS'])})")


# PARTE 3: Las 10 mayores palizas de la historia O(n log n)

# Calculamos la diferencia absoluta de puntos con las nuevas columnas
df['POINT_DIFF'] = abs(df['PTS_home'] - df['PTS_away'])

# Usamos sort_values() de Pandas (Timsort) que tiene eficiencia O(n log n)
biggest_blowouts = df.sort_values(by="POINT_DIFF", ascending=False)

print("\n--- LAS 10 MAYORES PALIZAS DE LA HISTORIA ---")
# Seleccionamos las columnas a mostrar
top_10_blowouts = biggest_blowouts[['GAME_DATE_EST', 'HOME_TEAM_ID', 'PTS_home', 'VISITOR_TEAM_ID', 'PTS_away', 'POINT_DIFF']].head(10)

# Convertimos los puntos a enteros para una lectura más limpia (vienen como decimales en el CSV)
cols_enteros = ['PTS_home', 'PTS_away', 'POINT_DIFF']
top_10_blowouts[cols_enteros] = top_10_blowouts[cols_enteros].astype(int)

print(top_10_blowouts.to_string(index=False))