import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# 1. Ambil data dari excel 
data_excel = pd.read_excel("data_disabilitas_1000.xlsx")

# 2. Daftar koordinat buat narik titik ke peta
lokasi_map = {
    'KAB. BOGOR': [106.82, -6.48], 'KOTA BANDUNG': [107.61, -6.91],
    'KAB. BEKASI': [107.17, -6.36], 'KOTA DEPOK': [106.82, -6.40],
    'KAB. GARUT': [107.90, -7.22], 'KAB. CIREBON': [108.55, -6.70],
    'KAB. KARAWANG': [107.29, -6.30], 'KOTA TASIKMALAYA': [108.22, -7.32]
}

# Pasang koordinat ke tiap baris data
data_excel['lon'] = data_excel['Wilayah'].map(lambda x: lokasi_map.get(x, [107.61, -6.91])[0])
data_excel['lat'] = data_excel['Wilayah'].map(lambda x: lokasi_map.get(x, [107.61, -6.91])[1])

# 3. Ubah menjadi format GIS
titik_gis = gpd.GeoDataFrame(
    data_excel, 
    geometry=gpd.points_from_xy(data_excel.lon, data_excel.lat), 
    crs="EPSG:4326"
)

# Sesuaikan koordinat agar sinkron seperti peta dunia
titik_gis = titik_gis.to_crs(epsg=3857)

# 4. Gambar Peta
fig, ax = plt.subplots(figsize=(10, 10))

# Gambar titik sebaran 
titik_gis.plot(ax=ax, color='red', markersize=20, alpha=0.5, label='Titik Warga')

#menambah peta dasar dari internet
try:
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
except:
    print("Internet lemot, peta dasar gak muncul, tapi titik aman.")

# Beri judul 
plt.title('Peta Sebaran Disabilitas Jawa Barat')
plt.axis('off')

# Simpan hasil menjadi gambar
plt.savefig('peta_uas_final.png')
print("Peta udah jadi! Cek file peta_uas_final.png di folder.")

# Munculkan di layar
plt.show()