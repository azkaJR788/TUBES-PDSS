import pandas as pd
import matplotlib.pyplot as plt

# Baca data dari file excel 
data = pd.read_excel("data_disabilitas_1000.xlsx")

# Set ukuran canvas grafik
plt.figure(figsize=(10,5))

# Plotting jumlah per wilayah
data['Wilayah'].value_counts().head(10).plot(kind='bar', color='teal')

# Nama-nama label
plt.title('Data Disabilitas Jabar (10 Wilayah Teratas)')
plt.ylabel('Jumlah')
plt.xlabel('Kabupaten/Kota')
plt.xticks(rotation=45)

# Biar layout pas 
plt.tight_layout()

# Simpan hasil gambarnya
plt.savefig('output_visualisasi.png')

# grafik
print("Grafik sudah siap, cek file output_visualisasi.png")
plt.show()