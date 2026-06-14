import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re
import streamlit.components.v1 as components

# ==========================================
# Konfigurasi Halaman & Tema Warna (CSS)
# ==========================================
st.set_page_config(
    page_title="Hybrid Recommendation System",
    page_icon="🛒",
    layout="wide"
)

# Injeksi CSS Radikal tingkat lanjut untuk menjebol paksa tema bawaan Streamlit
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
    /* ==========================================
       1. FORCE THEME KESELURUHAN (LATAR BELAKANG)
       ========================================== */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainBlockContainer"] {
        background-color: #CAF0F8 !important; 
        color: #03045E !important;            
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
    }
    
    /* Memaksa semua teks utama berwarna gelap kontras */
    p, span, label, th, td, [data-testid="stMarkdownContainer"] p {
        color: #03045E !important; 
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #03045E !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* ==========================================
       2. SIDEBAR STYLING & FIX TEXT KEYWORD (HILANG TOTAL)
       ========================================== */
    [data-testid="stSidebar"] {
        background-color: #03045E !important;
    }
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }
    
    /* SOLUSI KUNCI MUTLAK: Menghancurkan teks keyword aneh di tombol sidebar, baik di kiri maupun kanan */
    [data-testid="stSidebarCollapseButton"] button, 
    [data-testid="collapsedControl"] button,
    div[class*="stSidebarCollapseButton"] button,
    div[class*="collapsedControl"] button {
        background-color: #0077B6 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    
    /* Menyembunyikan string teks pembantu aksesibilitas ('keyboard_double_arrow_right', dll) */
    [data-testid="stSidebarCollapseButton"] button *, 
    [data-testid="collapsedControl"] button *,
    div[class*="stSidebarCollapseButton"] button *,
    div[class*="collapsedControl"] button * {
        font-size: 0px !important;
        color: transparent !important;
        line-height: 0 !important;
        display: none !important;
    }
    
    /* Memunculkan kembali simbol ikon panah asli bawaan Streamlit secara bersih */
    [data-testid="stSidebarCollapseButton"] button svg, 
    [data-testid="collapsedControl"] button svg,
    div[class*="stSidebarCollapseButton"] button svg,
    div[class*="collapsedControl"] button svg {
        width: 24px !important;
        height: 24px !important;
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        display: block !important;
    }

    /* ==========================================
       3. MODIFIKASI KOTAK METRIC DASHBOARD (BIRU MUDA CARDS)
       ========================================== */
    [data-testid="stMetricVitals"] {
        background-color: #90E0EF !important; /* Latar Belakang Kotak Biru Muda Sesuai Palet Anda */
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #00B4D8 !important;
        box-shadow: 0px 6px 15px rgba(0, 119, 182, 0.15) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Efek interaktif saat kursor diarahkan ke kotak metrik */
    [data-testid="stMetricVitals"]:hover {
        transform: translateY(-3px);
        box-shadow: 0px 10px 20px rgba(0, 119, 182, 0.25) !important;
    }
    
    /* Judul kecil di atas angka (misal: "Jumlah Customer") */
    [data-testid="stMetricLabel"] p {
        color: #03045E !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Angka/Value utama di dalam kotak metrik (misal: "2000 User") */
    [data-testid="stMetricValue"] div {
        color: #03045E !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }

    /* ==========================================
       4. FIX MUTLAK DROPDOWN / SELECTBOX (ANTI GELAP)
       ========================================== */
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 2px solid #0077B6 !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    [data-testid="stSelectbox"] div[role="button"] {
        color: #03045E !important;
        background-color: transparent !important;
        -webkit-text-fill-color: #03045E !important; 
    }
    
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    ul[role="listbox"] li, ul[role="listbox"] li * {
        color: #03045E !important;
        background-color: #FFFFFF !important;
    }

    /* ==========================================
       5. TOMBOL GENERATE REKOMENDASI INTERAKTIF
       ========================================== */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0077B6 0%, #00B4D8 100%) !important;
        color: #FFFFFF !important; 
        border-radius: 8px !important;
        border: none !important;
        padding: 0.7rem 2rem !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        box-shadow: 0px 4px 15px rgba(0, 119, 182, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02) !important;
        box-shadow: 0px 6px 20px rgba(0, 180, 216, 0.5) !important;
    }

    /* ==========================================
       6. PERBAIKAN KONTRAS TABEL DATAFRAME
       ========================================== */
    [data-testid="stDataFrameData"] {
        background-color: #FFFFFF !important;
        border: 1px solid #0077B6 !important;
        border-radius: 8px !important;
    }
            
    /* ==========================================
       7. FIX KONTRAS POP-UP (TOOLTIP) KHUSUS st.bar_chart (VEGA-LITE)
       ========================================== */
    /* Memaksa Kotak Pop-up berwarna Biru Gelap Kontras */
    #vg-tooltip-element {
        background-color: #03045E !important;
        border: 2px solid #00B4D8 !important;
        border-radius: 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Memaksa semua Teks di dalam Pop-up menjadi Putih Terang */
    #vg-tooltip-element table td,
    #vg-tooltip-element table th,
    #vg-tooltip-element table td span,
    #vg-tooltip-element table th span,
    #vg-tooltip-element span {
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Memberi aksen Biru Muda pada nama kategori agar lebih estetik */
    #vg-tooltip-element table td.key {
        color: #90E0EF !important; 
        font-weight: 500 !important;
    }
    
    /* Memaksa angka/value menjadi tebal (Bold) */
    #vg-tooltip-element table td.value {
        font-weight: 700 !important;
    }

    /* ==========================================
       8. FIX WARNA TASKBAR (TOOLBAR DI ATAS GRAFIK)
       ========================================== */
    /* Menargetkan toolbar bawaan Streamlit (ikon 3 titik & fullscreen) */
    [data-testid="stElementToolbar"] {
        background-color: #CAF0F8 !important; /* Latar belakang biru sangat muda */
        border-radius: 6px !important;
        padding: 2px !important;
    }
    
    /* Memaksa ikon toolbar menjadi biru gelap agar terlihat */
    [data-testid="stElementToolbar"] button svg {
        color: #03045E !important;
        fill: #03045E !important;
    }
""", unsafe_allow_html=True)

# Sisa kode fungsi (load_data, get_hybrid_bundle, pipeline, menu dll.) tetap sama dan tidak perlu diubah.
# ==========================================
# Load Data & Cache (Mempercepat Loading)
# ==========================================
@st.cache_data
def load_data():
    customer_profile = pd.read_csv(r"data/processed_customer_segmented.csv")
    rules = pd.read_csv(r"data/processed_association_rules.csv")
    similarity_matrix = joblib.load(r"src/customer_similarity.pkl")
    return customer_profile, rules, similarity_matrix

try:
    customer_profile, rules, similarity_matrix = load_data()
except Exception as e:
    st.error(f"Gagal memuat data. Error: {e}")
    st.stop()

# ==========================================
# Alur Fungsi Rekomendasi (Hybrid Engine)
# ==========================================

def get_similar_customers(customer_id, top_n=5):
    idx = customer_profile[customer_profile["CustomerID"] == customer_id].index[0]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:top_n+1]
    similar_indices = [i[0] for i in similarity_scores]
    return customer_profile.iloc[similar_indices]

def get_promotion(segment):
    if segment == "Loyal Customer":
        return ["Cashback 20%", "Voucher Rp50.000"]
    elif segment == "Potential Customer":
        return ["Diskon 15%", "Voucher Rp25.000"]
    elif segment == "At Risk Customer":
        return ["Voucher Rp100.000", "Free Shipping"]
    else:
        return ["Welcome Voucher", "Diskon Pembelian Pertama"]

def get_hybrid_bundle(customer_id, favorite_category, similar_cust_df):
    categories_pool = list(similar_cust_df["FavoriteCategory"].unique())
    if favorite_category not in categories_pool:
        categories_pool.append(favorite_category)
        
    matched_rules = rules[rules["antecedents"].apply(
        lambda x: any(cat in x for cat in categories_pool)
    )].copy()
    
    if matched_rules.empty:
        return "Tidak ada rekomendasi bundling"

    scores = []
    for idx, row in matched_rules.iterrows():
        base_score = (row['confidence'] * 0.7) + (min(row['lift'] / 10.0, 1.0) * 0.3)
        if favorite_category in row['antecedents'] or favorite_category in row['consequents']:
            base_score += 0.2  
        scores.append(base_score)
        
    matched_rules['hybrid_score'] = scores
    matched_rules = matched_rules.sort_values(by="hybrid_score", ascending=False)
    best_rule = matched_rules.iloc[0]
    
    def clean_item_set(text):
        cleaned = re.sub(r"frozenset", "", text)
        cleaned = re.sub(r"[\{\}\(\)\'\"\[\]]", "", cleaned)
        return cleaned.strip()

    ant_clean = clean_item_set(str(best_rule["antecedents"]))
    con_clean = clean_item_set(str(best_rule["consequents"]))
    return f"{ant_clean} + {con_clean}"

def hybrid_recommendation_pipeline(customer_id):
    customer = customer_profile[customer_profile["CustomerID"] == customer_id]
    segment = customer["Segment"].values[0]
    favorite_category = customer["FavoriteCategory"].values[0]
    
    similar_customers = get_similar_customers(customer_id, top_n=5)
    promo = get_promotion(segment)
    single_bundle = get_hybrid_bundle(customer_id, favorite_category, similar_customers)
    
    return {
        "Segment": segment,
        "FavoriteCategory": favorite_category,
        "Promo": promo,
        "Bundling": single_bundle,
        "SimilarCustomers": similar_customers
    }

# ==========================================
# Antarmuka Navigasi Sidebar 
# ==========================================
st.sidebar.title("🧭 Menu Navigasi")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Dashboard", "Rekomendasi & Promosi"]
)


# ==========================================
# HALAMAN 1: Dashboard
# ==========================================
if menu == "Dashboard":
    st.title("Sistem Rekomendasi Promosi Personal dan Bundling Produk")
    
    total_customers = customer_profile["CustomerID"].nunique()
    total_regions = customer_profile["Region"].nunique() if "Region" in customer_profile.columns else 4
    total_categories = customer_profile["FavoriteCategory"].nunique() if "FavoriteCategory" in customer_profile.columns else 5
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div style="background-color: #90E0EF; padding: 22px; border-radius: 12px; border: 2px solid #00B4D8; box-shadow: 0px 4px 12px rgba(3,4,94,0.1);">
                <p style="margin:0; color:#03045E; font-size:14px; font-weight:600; font-family:'Plus Jakarta Sans';">Jumlah Customer</p>
                <h2 style="margin:8px 0 0 0; color:#03045E; font-size:28px; font-weight:700; font-family:'Plus Jakarta Sans';">{total_customers} User</h2>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div style="background-color: #90E0EF; padding: 22px; border-radius: 12px; border: 2px solid #00B4D8; box-shadow: 0px 4px 12px rgba(3,4,94,0.1);">
                <p style="margin:0; color:#03045E; font-size:14px; font-weight:600; font-family:'Plus Jakarta Sans';">Jenis Produk</p>
                <h2 style="margin:8px 0 0 0; color:#03045E; font-size:28px; font-weight:700; font-family:'Plus Jakarta Sans';">{total_categories} Kategori</h2>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div style="background-color: #90E0EF; padding: 22px; border-radius: 12px; border: 2px solid #00B4D8; box-shadow: 0px 4px 12px rgba(3,4,94,0.1);">
                <p style="margin:0; color:#03045E; font-size:14px; font-weight:600; font-family:'Plus Jakarta Sans';">Jumlah Region</p>
                <h2 style="margin:8px 0 0 0; color:#03045E; font-size:28px; font-weight:700; font-family:'Plus Jakarta Sans';">{total_regions} Wilayah</h2>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div style="background-color: #90E0EF; padding: 22px; border-radius: 12px; border: 2px solid #00B4D8; box-shadow: 0px 4px 12px rgba(3,4,94,0.1);">
                <p style="margin:0; color:#03045E; font-size:14px; font-weight:600; font-family:'Plus Jakarta Sans';">Produk Terlaris</p>
                <h2 style="margin:8px 0 0 0; color:#03045E; font-size:28px; font-weight:700; font-family:'Plus Jakarta Sans';">Electronics</h2>
            </div>
        """, unsafe_allow_html=True)
    st.divider()
    
    col_graph1, col_graph2 = st.columns(2)
    with col_graph1:
        st.write("### 📈 Distribusi Segmentasi Pelanggan")
        st.bar_chart(customer_profile["Segment"].value_counts(), color="#0077B6")
        
    with col_graph2:
        st.write("### 🛒 Distribusi Kategori Favorit Transaksi")
        if "FavoriteCategory" in customer_profile.columns:
            st.bar_chart(customer_profile["FavoriteCategory"].value_counts(), color="#00B4D8")
        else:
            dummy_data = {"Beauty": 1988, "Electronics": 1989, "Fashion": 1982, "Home": 1989, "Sport": 1987}
            st.bar_chart(pd.Series(dummy_data), color="#00B4D8")

# ==========================================
# HALAMAN 2: Rekomendasi & Promosi
# ==========================================
elif menu == "Rekomendasi & Promosi":
    st.title("🎯 Sistem Rekomendasi Promosi Personal dan Bundling Produk")
    st.markdown("---")
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        selected_cust_id = st.selectbox(
            "Silahkan Pilih ID Customer untuk Memulai Analisis :",
            customer_profile["CustomerID"].unique()
        )
    with right_col:
        st.write("<br>", unsafe_allow_html=True) 
        btn_generate = st.button("Generate Recommendation ✨", use_container_width=True)
        
    st.markdown("---")
    
    if btn_generate:
        result = hybrid_recommendation_pipeline(selected_cust_id)
        current_customer_info = customer_profile[customer_profile["CustomerID"] == selected_cust_id]
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("#### 👤 Profil Pelanggan Terpilih")
            st.dataframe(current_customer_info[["CustomerID", "Gender", "AgeGroup", "Region"]])
        with c2:
            st.write("#### 🏆 Hasil Segmentasi & Minat Utama")
            st.info(f"**Segmen:** {result['Segment']} | **Kategori Utama:** {result['FavoriteCategory']}")
            
        st.write("<br>", unsafe_allow_html=True)
        
        col_promo, col_bundle = st.columns(2)
        
        with col_promo:
            st.write("### 🎁 Personal Voucher & Promosi")
            for promo_item in result["Promo"]:
                st.success(f"✔️ {promo_item}")
                
        with col_bundle:
            st.write("### 📦 Rekomendasi Bundling Produk")
            
            # TEKNIK BARU: Menggunakan Native HTML, CSS, dan JS Terisolasi untuk interaktivitas maksimal
            html_card = f"""
            <div class="card-container">
                <div class="bundling-box" id="bundleCard">
                    <div class="pulse-icon">📦</div>
                    <p class="bundling-text">{result['Bundling']}</p>
                </div>
            </div>

            <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&display=swap');
            
            .card-container {{
                padding: 5px;
                perspective: 1000px;
            }}
            .bundling-box {{
                background: linear-gradient(135deg, #0F203C 0%, #1A305C 100%);
                border-radius: 12px;
                padding: 22px 28px;
                border-left: 6px solid #00B4D8;
                box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.3);
                display: flex;
                align-items: center;
                gap: 15px;
                cursor: pointer;
                transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            }}
            /* Efek Interaktif JS/CSS Hover dari gambar yang kamu inginkan */
            .bundling-box.hovered {{
                transform: scale(1.02) translateY(-5px);
                box-shadow: 0px 15px 35px rgba(0, 180, 216, 0.4);
                border-left-color: #90E0EF;
            }}
            .pulse-icon {{
                font-size: 1.6rem;
                animation: pulse 2s infinite;
            }}
            .bundling-text {{
                color: #00B4D8 !important;
                font-size: 1.35rem !important;
                font-weight: 700 !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                margin: 0 !important;
                letter-spacing: 0.5px;
                text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
            }}
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.15); }}
                100% {{ transform: scale(1); }}
            }}
            </style>

            <script>
            // Menambahkan Interaktivitas Event Listener JavaScript asli
            const card = document.getElementById('bundleCard');
            card.addEventListener('mouseenter', () => {{
                card.classList.add('hovered');
            }});
            card.addEventListener('mouseleave', () => {{
                card.classList.remove('hovered');
            }});
            </script>
            """
            # Render component HTML + JS
            components.html(html_card, height=140)
            
        st.write("<br>", unsafe_allow_html=True)
        st.divider()
        
        st.write("### 👥 Evaluasi Kedekatan: 5 Similar Customers (Content-Based Filtering)")
        st.write("Aturan bundling di atas dipengaruhi oleh preferensi transaksi kolektif dari pelanggan sejenis berikut:")
        st.dataframe(
            result["SimilarCustomers"][["CustomerID", "Gender", "AgeGroup", "Region", "FavoriteCategory"]],
            use_container_width=True
        )