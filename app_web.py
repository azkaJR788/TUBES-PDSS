import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import warnings
import plotly.express as px
from datetime import datetime

warnings.filterwarnings("ignore")

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Disabilitas Jawa Barat", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    
    .stApp { 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
        margin: 15px;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section h1 {
        font-size: 3.2em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    
    .hero-section p {
        font-size: 1.3em;
        opacity: 0.95;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        padding: 25px 20px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(106, 17, 203, 0.2);
        margin: 10px 0;
    }
    
    .metric-number {
        font-size: 2.8em;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 1em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }
    
    .section-header {
        font-size: 1.9em;
        font-weight: 700;
        color: #2c3e50;
        margin: 35px 0 25px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #667eea;
    }
    
    .footer-modern {
        background: linear-gradient(135deg, #2c3e50 0%, #4a6491 100%);
        padding: 50px 20px;
        margin-top: 60px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 15px 50px rgba(44, 62, 80, 0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #4a6491 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data_disabilitas_1000.csv')
        return df
    except Exception as e:
        st.error(f"⚠️ Error memuat file data: {e}")
        return None

df = load_data()

if df is None:
    st.stop()

# --- KOORDINAT GMAPS YANG AKURAT ---
# Koordinat dari Google Maps (latitude, longitude) untuk ibukota kabupaten/kota
koordinat_gmaps = {
    # Kabupaten
    'KAB. BOGOR': [-6.5518, 106.6291],         # Cibinong
    'KAB. SUKABUMI': [-6.9277, 106.9300],      # Palabuhanratu
    'KAB. CIANJUR': [-6.8184, 107.1392],       # Cianjur
    'KAB. BANDUNG': [-7.1341, 107.6215],       # Soreang
    'KAB. GARUT': [-7.2032, 107.9000],         # Garut
    'KAB. TASIKMALAYA': [-7.3274, 108.2207],   # Singaparna
    'KAB. CIAMIS': [-7.3330, 108.3494],        # Ciamis
    'KAB. KUNINGAN': [-6.9768, 108.4831],      # Kuningan
    'KAB. CIREBON': [-6.7050, 108.5570],       # Sumber
    'KAB. MAJALENGKA': [-6.8364, 108.2279],    # Majalengka
    'KAB. SUMEDANG': [-6.8586, 107.9164],      # Sumedang
    'KAB. INDRAMAYU': [-6.3260, 108.3200],     # Indramayu
    'KAB. SUBANG': [-6.5692, 107.7596],        # Subang
    'KAB. PURWAKARTA': [-6.5409, 107.4462],    # Purwakarta
    'KAB. KARAWANG': [-6.3227, 107.3376],      # Karawang
    'KAB. BEKASI': [-6.2474, 107.1485],        # Cikarang
    'KAB. BANDUNG BARAT': [-6.8652, 107.4919], # Ngamprah
    'KAB. PANGANDARAN': [-7.6151, 108.4988],   # Parigi
    
    # Kota
    'KOTA BOGOR': [-6.5971, 106.8060],         # Bogor
    'KOTA SUKABUMI': [-6.9277, 106.9300],      # Sukabumi
    'KOTA BANDUNG': [-6.9175, 107.6191],       # Bandung
    'KOTA CIREBON': [-6.7320, 108.5523],       # Cirebon
    'KOTA BEKASI': [-6.2383, 106.9756],        # Bekasi
    'KOTA DEPOK': [-6.4025, 106.7942],         # Depok
    'KOTA CIMAHI': [-6.8841, 107.5413],        # Cimahi
    'KOTA TASIKMALAYA': [-7.3257, 108.2207],   # Tasikmalaya
    'KOTA BANJAR': [-7.3694, 108.5324]         # Banjar
}

# Tambahkan koordinat ke dataframe
df['lat'] = df['Wilayah'].map(lambda x: koordinat_gmaps.get(x, [-6.9175, 107.6191])[0])
df['lon'] = df['Wilayah'].map(lambda x: koordinat_gmaps.get(x, [-6.9175, 107.6191])[1])

# --- HERO SECTION ---
st.markdown('''
<div class="hero-section">
    <h1>📊 DASHBOARD DISABILITAS JAWA BARAT</h1>
    <p>UAS Pemrograman Dasar Sains Data</p>
</div>
''', unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.markdown("### 🔍 FILTER DATA")
st.sidebar.markdown("---")

# Filter wilayah
list_wilayah = sorted(df['Wilayah'].unique())
selected_wilayah = st.sidebar.multiselect(
    "Pilih Kabupaten/Kota:", 
    options=list_wilayah, 
    default=list_wilayah[:5]
)

# Filter tahun
tahun_options = sorted(df['Tahun'].unique(), reverse=True)
selected_tahun = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=tahun_options,
    default=tahun_options
)

# Filter tipe disabilitas
tipe_options = sorted(df['Tipe_Disabilitas'].unique())
selected_tipe = st.sidebar.multiselect(
    "Pilih Tipe Disabilitas:",
    options=tipe_options,
    default=tipe_options
)

# Apply filters
df_filtered = df.copy()
if selected_wilayah:
    df_filtered = df_filtered[df_filtered['Wilayah'].isin(selected_wilayah)]
if selected_tahun:
    df_filtered = df_filtered[df_filtered['Tahun'].isin(selected_tahun)]
if selected_tipe:
    df_filtered = df_filtered[df_filtered['Tipe_Disabilitas'].isin(selected_tipe)]

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informasi")
st.sidebar.info(f"""
**Total Data:** {len(df):,} baris  
**Data Tersaring:** {len(df_filtered):,} baris  
**Periode Data:** {min(tahun_options)} - {max(tahun_options)}  
**Update Terakhir:** {datetime.now().strftime('%d %B %Y')}
""")

# --- METRICS CARDS ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_data = len(df_filtered)
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Total Data</div>
        <div class="metric-number">{total_data:,}</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    total_wilayah = df_filtered['Wilayah'].nunique()
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Wilayah</div>
        <div class="metric-number">{total_wilayah}</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    total_jumlah = df_filtered['Jumlah'].sum()
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Total Kasus</div>
        <div class="metric-number">{total_jumlah:,}</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    jenis_disabilitas = df_filtered['Tipe_Disabilitas'].nunique()
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">Jenis Disabilitas</div>
        <div class="metric-number">{jenis_disabilitas}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- VISUALISASI DATA ---
if not df_filtered.empty:
    st.markdown('<p class="section-header">📊 VISUALISASI DATA</p>', unsafe_allow_html=True)
    
    # Tab untuk visualisasi
    tab1, tab2, tab3 = st.tabs(["📈 Distribusi", "🗺️ Peta Interaktif", "📋 Tabel Data"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Grafik Pie - Distribusi Jenis Disabilitas
            tipe_counts = df_filtered['Tipe_Disabilitas'].value_counts()
            fig_pie = px.pie(
                values=tipe_counts.values, 
                names=tipe_counts.index,
                title='Distribusi Jenis Disabilitas',
                color_discrete_sequence=px.colors.sequential.Viridis,
                hole=0.4,
                template='plotly_white'
            )
            fig_pie.update_layout(
                font=dict(size=12),
                showlegend=True,
                height=450,
                annotations=[dict(text='Disabilitas', x=0.5, y=0.5, font_size=16, showarrow=False)]
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            # Grafik Bar - Top 10 Wilayah
            wilayah_counts = df_filtered.groupby('Wilayah')['Jumlah'].sum().sort_values(ascending=False).head(10)
            fig_bar = px.bar(
                x=wilayah_counts.index,
                y=wilayah_counts.values,
                title='Top 10 Wilayah dengan Kasus Terbanyak',
                labels={'x': 'Wilayah', 'y': 'Jumlah Kasus'},
                color=wilayah_counts.values,
                color_continuous_scale='Viridis',
                template='plotly_white'
            )
            fig_bar.update_layout(
                showlegend=False,
                height=450,
                xaxis_tickangle=-45,
                yaxis_title="Jumlah Kasus"
            )
            fig_bar.update_traces(texttemplate='%{y:,}', textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.markdown('<p class="section-header">🗺️ PETA SEBARAN DISABILITAS JAWA BARAT</p>', unsafe_allow_html=True)
        
        # Peta dengan Folium - GMaps Style
        if not df_filtered.empty:
            # Hitung pusat peta berdasarkan data yang difilter
            center_lat = df_filtered['lat'].mean()
            center_lon = df_filtered['lon'].mean()
            
            # Buat peta dengan tiles Google Maps-like
            m = folium.Map(
                location=[center_lat, center_lon], 
                zoom_start=8,
                control_scale=True,
                zoom_control=True
            )
            
            # Add multiple tile layers
            folium.TileLayer(
                'CartoDB positron',  # Clean light map
                name='Light Map',
                attr='CartoDB'
            ).add_to(m)
            
            folium.TileLayer(
                'CartoDB dark_matter',  # Dark mode
                name='Dark Map',
                attr='CartoDB'
            ).add_to(m)
            
            folium.TileLayer(
                'OpenStreetMap',  # Standard OSM
                name='Street Map',
                attr='OpenStreetMap'
            ).add_to(m)
            
            # Warna berbeda per jenis disabilitas
            color_map = {
                'Fisik': '#FF6B6B',        # Merah
                'Intelektual': '#4ECDC4',   # Biru kehijauan
                'Mental': '#45B7D1',       # Biru muda
                'Sensorik': '#96CEB4',     # Hijau muda
                'Rungu/Wicara': '#FFEAA7'  # Kuning
            }
            
            # data per wilayah untuk ikon cluster
            wilayah_aggregated = {}
            for _, row in df_filtered.iterrows():
                key = (row['Wilayah'], row['lat'], row['lon'])
                if key not in wilayah_aggregated:
                    wilayah_aggregated[key] = {
                        'total': 0,
                        'tipe_counts': {},
                        'records': []
                    }
                wilayah_aggregated[key]['total'] += row['Jumlah']
                wilayah_aggregated[key]['tipe_counts'][row['Tipe_Disabilitas']] = \
                    wilayah_aggregated[key]['tipe_counts'].get(row['Tipe_Disabilitas'], 0) + row['Jumlah']
                wilayah_aggregated[key]['records'].append(row)
            
            # Tambahkan marker untuk setiap wilayah
            for (wilayah, lat, lon), data in wilayah_aggregated.items():
                # Tentukan warna berdasarkan jenis disabilitas dominan
                tipe_dominan = max(data['tipe_counts'].items(), key=lambda x: x[1])[0]
                color = color_map.get(tipe_dominan, '#666666')
                
                # Ukuran marker berdasarkan total jumlah
                radius = max(10, min(40, data['total'] / 20))
                
                # Buat HTML untuk popup
                tipe_list = "\n".join([f"• {tipe}: {count:,}" for tipe, count in data['tipe_counts'].items()])
                
                popup_html = f"""
                <div style="font-family: Arial, sans-serif; width: 300px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 10px; border-radius: 5px 5px 0 0;">
                        <h3 style="margin: 0; font-size: 18px;">{wilayah}</h3>
                    </div>
                    <div style="padding: 15px;">
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                            <p style="margin: 0; font-size: 16px; font-weight: bold; color: #2c3e50;">
                                Total Kasus: <span style="color: #667eea;">{data['total']:,}</span>
                            </p>
                        </div>
                        <h4 style="margin: 10px 0 5px 0; color: #2c3e50; font-size: 14px;">
                            Distribusi per Jenis:
                        </h4>
                        <div style="max-height: 150px; overflow-y: auto; padding: 5px;">
                            {tipe_list}
                        </div>
                        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                            <p style="margin: 5px 0;">📍 Koordinat: {lat:.4f}, {lon:.4f}</p>
                            <p style="margin: 5px 0;">📊 Data: {len(data['records'])} records</p>
                        </div>
                    </div>
                </div>
                """
                
                #custom icon dengan angka
                from folium.features import DivIcon
                
                # Tambahkan marker dengan circle
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=radius,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    weight=2,
                    popup=folium.Popup(popup_html, max_width=350),
                    tooltip=f"{wilayah}: {data['total']:,} kasus"
                ).add_to(m)
                
                # Tambahkan label dengan jumlah
                folium.Marker(
                    [lat, lon],
                    icon=DivIcon(
                        icon_size=(150,36),
                        icon_anchor=(0,0),
                        html=f'<div style="font-size: 14pt; color: white; text-shadow: 2px 2px 4px #000000; font-weight: bold;">{data["total"]:,}</div>'
                    )
                ).add_to(m)
            
            # Tambahkan legenda
            legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; 
                        width: 220px; height: auto;
                        background-color: white; 
                        padding: 15px; 
                        border-radius: 10px; 
                        box-shadow: 0 3px 14px rgba(0,0,0,0.4);
                        z-index: 9999; 
                        font-size: 14px;
                        font-family: Arial, sans-serif;">
                <h4 style="margin-top: 0; 
                          color: #2c3e50; 
                          border-bottom: 2px solid #667eea;
                          padding-bottom: 5px;">
                    🎨 Legenda Peta
                </h4>
                <div style="margin-top: 10px;">
            '''
            
            for tipe, warna in color_map.items():
                legend_html += f'''
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="width: 18px; height: 18px; background-color: {warna}; 
                                border-radius: 50%; margin-right: 10px; border: 1px solid #ccc;"></div>
                    <span style="font-weight: 500;">{tipe}</span>
                </div>
                '''
            
            legend_html += '''
                </div>
                <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <p style="margin: 5px 0;">🔵 Ukuran lingkaran: total kasus per wilayah</p>
                    <p style="margin: 5px 0;">🔢 Angka dalam lingkaran: jumlah total</p>
                    <p style="margin: 5px 0;">🎯 Klik marker untuk detail</p>
                </div>
            </div>
            '''
            
            m.get_root().html.add_child(folium.Element(legend_html))
            
            # Tambahkan layer control
            folium.LayerControl().add_to(m)
            
            # Tampilkan peta dengan ukuran lebih besar
            st_folium(m, width="100%", height=700, key="peta_gmaps")
            
            # Informasi tambahan
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.info("**🎯 Tip:** Klik marker untuk melihat detail data")
            with col_info2:
                st.info("**🗺️ Tip:** Gunakan layer control di pojok kanan atas")
            with col_info3:
                st.info("**🔍 Tip:** Zoom in/out untuk melihat lebih detail")
            
            # Tampilkan statistik peta
            st.markdown("### 📊 Statistik Peta")
            col_map1, col_map2, col_map3, col_map4 = st.columns(4)
            with col_map1:
                st.metric("Total Wilayah di Peta", len(wilayah_aggregated))
            with col_map2:
                avg_per_wilayah = sum(data['total'] for data in wilayah_aggregated.values()) / len(wilayah_aggregated)
                st.metric("Rata-rata Kasus/Wilayah", f"{avg_per_wilayah:,.0f}")
            with col_map3:
                max_wilayah = max(wilayah_aggregated.values(), key=lambda x: x['total'])
                st.metric("Wilayah Tertinggi", f"{max_wilayah['total']:,}")
            with col_map4:
                total_tipe = sum(len(data['tipe_counts']) for data in wilayah_aggregated.values())
                st.metric("Total Jenis di Peta", total_tipe)
    
    with tab3:
        st.markdown('<p class="section-header">📋 DETAIL DATA</p>', unsafe_allow_html=True)
        
        # Opsi tampilan data
        col_view1, col_view2 = st.columns(2)
        with col_view1:
            show_rows = st.selectbox("Tampilkan baris:", [10, 25, 50, 100, "Semua"])
        with col_view2:
            sort_by = st.selectbox("Urutkan berdasarkan:", 
                                  ['No', 'Wilayah', 'Tipe_Disabilitas', 'Jumlah', 'Tahun'])
        
        # Urutkan data
        df_display = df_filtered.sort_values(by=sort_by, ascending=True)
        
        # Tampilkan data
        if show_rows == "Semua":
            st.dataframe(df_display, use_container_width=True, height=500)
        else:
            st.dataframe(df_display.head(int(show_rows)), use_container_width=True, height=400)
        
        # Statistik ringkasan
        st.markdown("#### 📊 Statistik Ringkasan Data")
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Rata-rata Jumlah", f"{df_display['Jumlah'].mean():.1f}")
        with col_stat2:
            st.metric("Jumlah Maksimum", f"{df_display['Jumlah'].max():,}")
        with col_stat3:
            st.metric("Jumlah Minimum", f"{df_display['Jumlah'].min():,}")
        with col_stat4:
            st.metric("Standar Deviasi", f"{df_display['Jumlah'].std():.1f}")

else:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan sesuaikan filter di sidebar.")

st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer-modern">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: left;">
        <div style="flex: 1; min-width: 250px; padding: 15px;">
            <h4>📂 Open Data Jawa Barat</h4>
            <p>Portal data terpadu Pemerintah Provinsi Jawa Barat untuk transparansi dan inovasi kebijakan publik.</p>
            <p style="font-size: 0.9em;">Sumber data: Opedata.jabarprov 2023-2024</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 15px;">
            <h4>📞 Kontak & Dukungan</h4>
            <p>📧 data@jabarprov.go.id<br>📱 +62 896 6098 2071<br>🏢 Gedung Sate, Bandung</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 15px;">
            <h4>🎓 Tim Pengembang</h4>
            <p>Kelompok 6 - UAS Pemrograman Dasar Sains Data<br>Program Studi teknik Informatika<br>Fakultas Teknik dan Ilmu Komputer<br>Universitas Komputer Indonesia</p>
        </div>
    </div>
    <hr style="margin: 30px 0; border-color: rgba(255,255,255,0.3);">
    <div style="text-align: center;">
        <p style="font-size: 0.9em; margin-bottom: 10px;">
            <strong>Disclaimer:</strong> Data ini bersifat dinamis dan dapat berubah sesuai dengan pembaruan dari sumber terkait.
        </p>
        <p style="text-align: center; font-size: 0.9em;">
            © 2024 Pemerintah Provinsi Jawa Barat | Dashboard Disabilitas v2.0 | 
            <span style="color: #FFEAA7;">Dibuat dengan ❤️ untuk Indonesia Inklusif</span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
