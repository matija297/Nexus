import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json

# Učitavanje CSV datoteka (lokacije i uzorci)
df_lokacije = pd.read_csv('mars_lokacije.csv', sep=';', decimal=',')
df_uzorci = pd.read_csv('mars_uzorci.csv', sep=';', decimal=',')

# Spajanje podataka po ID-u uzorka
df = pd.merge(df_lokacije, df_uzorci, on='ID_Uzorka')

# Definiranje uvjeta za anomalije:
# temperatura izvan raspona (-80 do -30) ili vlaga > 6
uvjet_anomalije = (df['Temperatura'] < -80) | (df['Temperatura'] > -30) | (df['Vlaga'] > 6)

# Odvajanje anomalnih i "čistih" podataka
df_anomalije = df[uvjet_anomalije]
df_cisto = df[~uvjet_anomalije]

# -------------------------
# GRAPH 1: Temperatura vs vlaga (boja = metan)
# -------------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_cisto, x='Temperatura', y='Vlaga', hue='Metan')
plt.title('Odnos temperature i vlage')
plt.savefig('graph1_temp_h2o.png')
plt.close()

# -------------------------
# GRAPH 2: "Heatmap" dubine (veličina i boja = dubina)
# -------------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_cisto,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='Dubina',
    palette='viridis',
    size='Dubina'
)
plt.title('Karta dubine bušenja')
plt.savefig('graph2_heatmap_depth.png')
plt.close()

# -------------------------
# GRAPH 3: Prisutnost metana (crveno = pozitivno, plavo = negativno)
# -------------------------
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_cisto,
    x='GPS_LONG',
    y='GPS_LAT',
    hue='Metan',
    palette={'Pozitivno': 'red', 'Negativno': 'blue'}
)
plt.title('Prisutnost metana')
plt.savefig('graph3_methane_scatter.png')
plt.close()

# -------------------------
# GRAPH 4: Kandidati za bušenje
# (metan + organske molekule)
# -------------------------
plt.figure(figsize=(10, 6))

# Prikaz svih točaka (vlaga kao boja)
sns.scatterplot(data=df_cisto, x='GPS_LONG', y='GPS_LAT', hue='Vlaga', alpha=0.5)

# Filtriranje kandidata
kandidati = df_cisto[
    (df_cisto['Metan'] == 'Pozitivno') &
    (df_cisto['Organske_molekule'] == True)
]

# Isticanje kandidata crvenom zvjezdicom
plt.scatter(
    kandidati['GPS_LONG'],
    kandidati['GPS_LAT'],
    marker='*',
    s=250,
    color='red',
    label='Kandidati'
)

plt.legend()
plt.title('Potencijalni kandidati za bušenje')
plt.savefig('scatter_plot.png')
plt.close()

# -------------------------
# GRAPH 5: Satelitska mapa (Jezero krater)
# -------------------------
plt.figure(figsize=(12, 8))

# Definiranje granica slike prema GPS koordinatama
extent_koordinate = [
    df_cisto['GPS_LONG'].min(),
    df_cisto['GPS_LONG'].max(),
    df_cisto['GPS_LAT'].min(),
    df_cisto['GPS_LAT'].max()
]

# Učitavanje satelitske slike
slika_kratera = plt.imread('jezero_crater_satellite_map.jpg')

# Prikaz slike kao pozadine
plt.imshow(slika_kratera, extent=extent_koordinate, aspect='auto', alpha=0.7)

# Sve točke
sns.scatterplot(
    data=df_cisto,
    x='GPS_LONG',
    y='GPS_LAT',
    color='cyan',
    alpha=0.5,
    label='Obična očitanja'
)

# Kandidati istaknuti
plt.scatter(
    kandidati['GPS_LONG'],
    kandidati['GPS_LAT'],
    marker='*',
    s=300,
    color='red',
    edgecolor='black',
    label='Kandidati'
)

plt.title('Satelitska karta kratera Jezero s lokacijama')
plt.legend()
plt.savefig('jezero_mission_map.jpg')
plt.close()

# -------------------------
# Generiranje komandi za rover
# -------------------------
komande_za_rover = []

# Za svakog kandidata kreira se niz akcija
for index, row in kandidati.iterrows():
    paket_akcija = [
        {"akcija": "NAVIGACIJA", "lokacija": {"lat": row['GPS_LAT'], "long": row['GPS_LONG']}},
        {"akcija": "SONDIRANJE", "dubina_m": row['Dubina']},
        {"akcija": "SLANJE_PODATAKA"}
    ]

    komande_za_rover.append({
        "ID_tocke": row['ID'],
        "zadatci": paket_akcija
    })

# Završni JSON payload
payload = {
    "tim": "Matija_Božić",
    "misija": "Jezero_Crater_Drill",
    "nalozi": komande_za_rover
}

# API endpoint (test webhook)
api_url = "https://webhook.site/03f33f00-c3a0-4a66-8b06-63f1af147efa"

# Slanje podataka POST zahtjevom
try:
    response = requests.post(api_url, json=payload)
    print(f"Status koda: {response.status_code}")

    if response.status_code == 200:
        print("Misija uspješna! JSON paket je prihvaćen.")
    else:
        print(f"Greška na serveru. Odgovor: {response.text}")

# Hvatanje grešaka (npr. nema interneta)
except Exception as e:
    print(f"Došlo je do greške u komunikaciji: {e}")
