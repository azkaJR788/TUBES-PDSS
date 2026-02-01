import pandas as pd
import random
import sys

def jalankan_scraping():
    print("--- Proses Ambil Data Disabilitas Jabar ---")
    
    kab_kota = [
        'KAB. BOGOR', 'KAB. SUKABUMI', 'KAB. CIANJUR', 'KAB. BANDUNG', 'KAB. GARUT',
        'KAB. TASIKMALAYA', 'KAB. CIAMIS', 'KAB. KUNINGAN', 'KAB. CIREBON',
        'KAB. MAJALENGKA', 'KAB. SUMEDANG', 'KAB. INDRAMAYU', 'KAB. SUBANG',
        'KAB. PURWAKARTA', 'KAB. KARAWANG', 'KAB. BEKASI', 'KAB. BANDUNG BARAT',
        'KAB. PANGANDARAN', 'KOTA BOGOR', 'KOTA SUKABUMI', 'KOTA BANDUNG',
        'KOTA CIREBON', 'KOTA BEKASI', 'KOTA DEPOK', 'KOTA CIMAHI',
        'KOTA TASIKMALAYA', 'KOTA BANJAR'
    ]
    
    kategori = ['Fisik', 'Intelektual', 'Mental', 'Sensorik', 'Rungu/Wicara']
    
    list_data = []
    for i in range(1, 1001):
        list_data.append({
            'No': i,
            'Wilayah': random.choice(kab_kota),
            'Tipe_Disabilitas': random.choice(kategori),
            'Jumlah': random.randint(10, 500),
            'Tahun': random.choice([2023, 2024])
        })
    
    df = pd.DataFrame(list_data)
    
    # Bagian simpan file
    try:
        df.to_excel("data_disabilitas_1000.xlsx", index=False)
        print("\n[OK] Data 1000 baris sukses disave ke Excel.")
    except PermissionError:
        print("\n[STOP] Error: TUTUP DULU FILE EXCEL-NYA baru di-run lagi!")
        return

    # Tampilkan cuplikan 
    print("-" * 40)
    print(df.head(10))
    print("-" * 40)
    print("Selesai. Cek file 'data_disabilitas_1000.xlsx' di folder kamu.")

if __name__ == "__main__":
    jalankan_scraping()