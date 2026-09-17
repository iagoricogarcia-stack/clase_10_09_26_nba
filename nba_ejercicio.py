
import csv


# PARTE 1: Carga de datos y limpieza usando 'csv'

all_games = []
sample_2019 = []

# Abrimos el archivo en modo lectura
with open("games.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Limpieza: omitir filas donde falten los puntos (cadenas vacías)
        if not row['PTS_home'] or not row['PTS_away']:
            continue
            
        # Convertimos los datos de texto a números. 
        # Los puntos vienen como '120.0' en el csv, así que pasamos a float y luego a int
        pts_home = int(float(row['PTS_home']))
        pts_away = int(float(row['PTS_away']))
        season = int(row['SEASON'])
        
        # Creamos un diccionario con la estructura exacta que necesitamos
        game_data = {
            'GAME_DATE_EST': row['GAME_DATE_EST'],
            'HOME_TEAM_ID': row['HOME_TEAM_ID'],
            'VISITOR_TEAM_ID': row['VISITOR_TEAM_ID'],
            'PTS_home': pts_home,
            'PTS_away': pts_away,
            'TOTAL_POINTS': pts_home + pts_away,
            'POINT_DIFF': abs(pts_home - pts_away)
        }
        
        # Guardamos el partido en el histórico general
        all_games.append(game_data)
        
        # Si es de la temporada 2019 y nuestra muestra aún no llega a 500, lo añadimos
        if season == 2019 and len(sample_2019) < 500:
            sample_2019.append(game_data)


# PARTE 2: Ordenar muestra con Bubble Sort O(n^2)

def bubble_sort(arr, key):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][key] < arr[j + 1][key]:  # Orden descendente
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Ejecutamos Bubble Sort solo sobre los 500 primeros partidos de 2019
sorted_sample = bubble_sort(sample_2019, "TOTAL_POINTS")

print("--- TOP 10 PARTIDOS CON MÁS PUNTOS (MUESTRA 2019) ---")
for g in sorted_sample[:10]:
    print(f"{g['GAME_DATE_EST']}: Eq_Local({g['HOME_TEAM_ID']}) {g['PTS_home']} - "
          f"Eq_Visitante({g['VISITOR_TEAM_ID']}) {g['PTS_away']} "
          f"(Total: {g['TOTAL_POINTS']})")

print("\n" + "="*60 + "\n")


# PARTE 3: Las 10 mayores palizas de la historia O(n log n)

# Usamos el método nativo de Python .sort() que implementa Timsort O(n log n).
# Le indicamos mediante una función lambda que ordene usando la clave 'POINT_DIFF'
all_games.sort(key=lambda x: x['POINT_DIFF'], reverse=True)

print("--- LAS 10 MAYORES PALIZAS DE LA HISTORIA ---")
# Creamos una cabecera para que parezca una tabla
print(f"{'FECHA':<15} {'LOCAL_ID':<15} {'PTS_L':<6} {'VISIT_ID':<15} {'PTS_V':<6} {'DIFERENCIA'}")
print("-" * 75)

for g in all_games[:10]:
    print(f"{g['GAME_DATE_EST']:<15} {g['HOME_TEAM_ID']:<15} {g['PTS_home']:<6} "
          f"{g['VISITOR_TEAM_ID']:<15} {g['PTS_away']:<6} {g['POINT_DIFF']}")

