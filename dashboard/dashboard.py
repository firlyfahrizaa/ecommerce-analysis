import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="E-Commerce Public Data Analysis Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# Menentukan tema visualisasi
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

# ==============================================================================
# 2. FUNGSI LOAD DATA (DENGAN CACHING & RELATIVE PATH HANDLING)
# ==============================================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    # Jalur cadangan jika file dieksekusi dari direktori root atau subfolder
    if not os.path.exists(file_path):
        if os.path.exists("dashboard/main_data.csv"):
            file_path = "dashboard/main_data.csv"
        elif os.path.exists("main_data.csv"):
            file_path = "main_data.csv"
        else:
            st.error("File 'main_data.csv' tidak ditemukan. Pastikan file berada di folder yang tepat.")
            st.stop()
            
    df = pd.read_csv(file_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

df = load_data()

# ==============================================================================
# 3. SIDEBAR (FILTER RENTANG WAKTU)
# ==============================================================================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=180)
    st.title("Filter Analisis")
    st.markdown("Sesuaikan rentang waktu transaksi:")
    
    min_date = df["order_purchase_timestamp"].min().date()
    max_date = df["order_purchase_timestamp"].max().date()
    
    date_range = st.date_input(
        label="Rentang Waktu Transaksi:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Validasi input rentang tanggal
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Silakan pilih tanggal awal dan tanggal akhir secara lengkap.")
        st.stop()

# Filter data utama berdasarkan rentang tanggal yang dipilih
filtered_df = df[
    (df["order_purchase_timestamp"].dt.date >= start_date) &
    (df["order_purchase_timestamp"].dt.date <= end_date)
].copy()

# ==============================================================================
# 4. HALAMAN UTAMA - HEADER & METRIK UTAMA (KPI)
# ==============================================================================
st.title("🛍️ E-Commerce Performance & Customer Insights Dashboard")
st.markdown(
    """
    Dashboard interaktif ini menyajikan evaluasi performa bisnis **E-Commerce Public Dataset (Olist)**, 
    meliputi pendapatan kategori produk, korelasi logistik terhadap ulasan pelanggan, serta segmentasi **RFM**.
    """
)

st.subheader("📌 Key Performance Indicators (KPI)")
col1, col2, col3, col4 = st.columns(4)

total_orders = filtered_df["order_id"].nunique()
total_revenue = filtered_df["price"].sum()
avg_review = filtered_df["review_score"].mean() if len(filtered_df) > 0 else 0
ontime_rate = (filtered_df["delivery_status"] == "On Time").mean() * 100 if len(filtered_df) > 0 else 0

with col1:
    st.metric("Total Pesanan", f"{total_orders:,}")
with col2:
    st.metric("Total Pendapatan", f"R$ {total_revenue:,.2f}")
with col3:
    st.metric("Rata-Rata Skor Ulasan", f"{avg_review:.2f} / 5.0")
with col4:
    st.metric("Ketepatan Waktu", f"{ontime_rate:.1f}%")

st.divider()

# ==============================================================================
# 5. PERTANYAAN BISNIS 1: PERFORMA REVENUE PER KATEGORI PRODUK
# ==============================================================================
st.subheader("📦 Performa Kategori Produk Berdasarkan Revenue")
st.markdown("**Pertanyaan Bisnis 1:** Kategori produk apa saja yang mencatatkan total pendapatan (*revenue*) tertinggi dan terendah?")

category_rev = (
    filtered_df.groupby("product_category_name_english")["price"]
    .sum()
    .reset_index()
    .rename(columns={"price": "total_revenue"})
    .sort_values(by="total_revenue", ascending=False)
)

col_top, col_bot = st.columns(2)

with col_top:
    st.write("##### 5 Kategori Produk Tertinggi (Top Revenue)")
    top_5 = category_rev.head(5)
    fig_top, ax_top = plt.subplots(figsize=(8, 5))
    colors_top = ["#2b5c8f", "#aec7e8", "#aec7e8", "#aec7e8", "#aec7e8"]
    sns.barplot(
        x="total_revenue",
        y="product_category_name_english",
        data=top_5,
        palette=colors_top,
        hue="product_category_name_english",
        legend=False,
        ax=ax_top
    )
    ax_top.set_title("Top 5 Kategori Produk Berdasarkan Revenue", fontsize=12, fontweight="bold")
    ax_top.set_xlabel("Total Pendapatan (BRL)")
    ax_top.set_ylabel(None)
    for p in ax_top.patches:
        ax_top.annotate(
            f"R$ {p.get_width():,.0f}", 
            (p.get_width(), p.get_y() + p.get_height() / 2.),
            ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=9
        )
    sns.despine()
    st.pyplot(fig_top)
    plt.close(fig_top)

with col_bot:
    st.write("##### 5 Kategori Produk Terendah (Bottom Revenue)")
    bot_5 = category_rev.tail(5).sort_values(by="total_revenue", ascending=True)
    fig_bot, ax_bot = plt.subplots(figsize=(8, 5))
    colors_bot = ["#c0392b", "#f5b7b1", "#f5b7b1", "#f5b7b1", "#f5b7b1"]
    sns.barplot(
        x="total_revenue",
        y="product_category_name_english",
        data=bot_5,
        palette=colors_bot,
        hue="product_category_name_english",
        legend=False,
        ax=ax_bot
    )
    ax_bot.set_title("Bottom 5 Kategori Produk Berdasarkan Revenue", fontsize=12, fontweight="bold")
    ax_bot.set_xlabel("Total Pendapatan (BRL)")
    ax_bot.set_ylabel(None)
    for p in ax_bot.patches:
        ax_bot.annotate(
            f"R$ {p.get_width():,.0f}", 
            (p.get_width(), p.get_y() + p.get_height() / 2.),
            ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=9
        )
    sns.despine()
    st.pyplot(fig_bot)
    plt.close(fig_bot)

st.divider()

# ==============================================================================
# 6. PERTANYAAN BISNIS 2: PENGARUH KETEPATAN WAKTU PENGIRIMAN
# ==============================================================================
st.subheader("🚚 Pengaruh Ketepatan Waktu Pengiriman terhadap Kepuasan Pelanggan")
st.markdown("**Pertanyaan Bisnis 2:** Bagaimana perbandingan skor ulasan antara pesanan tepat waktu (*On Time*) vs terlambat (*Delayed*)?")

col_deliv1, col_deliv2 = st.columns([1, 1.2])

delivery_stat = (
    filtered_df.groupby("delivery_status")
    .agg(
        total_orders=("order_id", "nunique"),
        avg_score=("review_score", "mean")
    )
    .reset_index()
)

with col_deliv1:
    st.write("##### Rata-Rata Skor Ulasan Pelanggan")
    fig_deliv, ax_deliv = plt.subplots(figsize=(6, 5))
    palette_deliv = {"On Time": "#2ca02c", "Delayed": "#d62728"}
    sns.barplot(
        x="delivery_status",
        y="avg_score",
        data=delivery_stat,
        palette=palette_deliv,
        hue="delivery_status",
        legend=False,
        ax=ax_deliv
    )
    ax_deliv.set_title("Rata-Rata Skor Ulasan (1 - 5)", fontsize=12, fontweight="bold")
    ax_deliv.set_ylabel("Skor Ulasan (Skala 1 - 5)")
    ax_deliv.set_xlabel("Status Pengiriman")
    ax_deliv.set_ylim(0, 5)
    for p in ax_deliv.patches:
        ax_deliv.annotate(
            f"{p.get_height():.2f} ★", 
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center', va='bottom', xytext=(0, 6), textcoords='offset points', fontsize=11, fontweight="bold"
        )
    sns.despine()
    st.pyplot(fig_deliv)
    plt.close(fig_deliv)

with col_deliv2:
    st.write("##### Proporsi Sebaran Rating (Bintang 1 - 5)")
    score_cross = (
        pd.crosstab(filtered_df["delivery_status"], filtered_df["review_score"], normalize="index") * 100
    )
    fig_dist, ax_dist = plt.subplots(figsize=(7, 5))
    score_cross.plot(
        kind="bar",
        stacked=True,
        colormap="RdYlGn",
        ax=ax_dist,
        edgecolor="black",
        linewidth=0.5
    )
    ax_dist.set_title("Distribusi Rating Ulasan per Status Pengiriman (%)", fontsize=12, fontweight="bold")
    ax_dist.set_ylabel("Persentase (%)")
    ax_dist.set_xlabel("Status Pengiriman")
    ax_dist.legend(title="Rating", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=0)
    sns.despine()
    st.pyplot(fig_dist)
    plt.close(fig_dist)

st.divider()

# ==============================================================================
# 7. ANALISIS LANJUTAN: RFM ANALYSIS (RECENCY, FREQUENCY, MONETARY)
# ==============================================================================
st.subheader("👥 Analisis Lanjutan: RFM Analysis")
st.markdown("Segmentasi perilaku belanja pelanggan berdasarkan parameter **Recency (hari)**, **Frequency (pesanan)**, dan **Monetary (pengeluaran)**.")

rfm_raw = (
    filtered_df.groupby("customer_unique_id")
    .agg(
        max_purchase=("order_purchase_timestamp", "max"),
        Frequency=("order_id", "nunique"),
        Monetary=("price", "sum")
    )
    .reset_index()
)

snapshot_date = filtered_df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm_raw["Recency"] = (snapshot_date - rfm_raw["max_purchase"]).dt.days
rfm_raw["customer_short_id"] = rfm_raw["customer_unique_id"].apply(lambda x: str(x)[:8] + "...")

c_rfm1, c_rfm2, c_rfm3 = st.columns(3)
with c_rfm1:
    st.metric("Rata-Rata Recency", f"{rfm_raw['Recency'].mean():.1f} hari")
with c_rfm2:
    st.metric("Rata-Rata Frequency", f"{rfm_raw['Frequency'].mean():.2f} transaksi")
with c_rfm3:
    st.metric("Rata-Rata Monetary", f"R$ {rfm_raw['Monetary'].mean():.2f}")

fig_rfm, ax_rfm = plt.subplots(nrows=1, ncols=3, figsize=(22, 6))
colors_rfm = ["#72BCD4"] * 5

# 1. Recency Plot (Terendah = Terbaik/Terbaru)
top_recency = rfm_raw.sort_values(by="Recency", ascending=True).head(5)
sns.barplot(
    y="Recency", x="customer_short_id", 
    data=top_recency, palette=colors_rfm, hue="customer_short_id", legend=False, ax=ax_rfm[0]
)
ax_rfm[0].set_ylabel("Hari")
ax_rfm[0].set_xlabel("Customer ID (Prefix)")
ax_rfm[0].set_title("By Recency (Days - Transaksi Terbaru)", fontsize=13, fontweight="bold")
ax_rfm[0].tick_params(axis='x', rotation=45)

# 2. Frequency Plot (Terbanyak Transaksi)
top_frequency = rfm_raw.sort_values(by="Frequency", ascending=False).head(5)
sns.barplot(
    y="Frequency", x="customer_short_id", 
    data=top_frequency, palette=colors_rfm, hue="customer_short_id", legend=False, ax=ax_rfm[1]
)
ax_rfm[1].set_ylabel("Total Pesanan")
ax_rfm[1].set_xlabel("Customer ID (Prefix)")
ax_rfm[1].set_title("By Frequency (Total Pesanan)", fontsize=13, fontweight="bold")
ax_rfm[1].tick_params(axis='x', rotation=45)

# 3. Monetary Plot (Pengeluaran Terbesar)
top_monetary = rfm_raw.sort_values(by="Monetary", ascending=False).head(5)
sns.barplot(
    y="Monetary", x="customer_short_id", 
    data=top_monetary, palette=colors_rfm, hue="customer_short_id", legend=False, ax=ax_rfm[2]
)
ax_rfm[2].set_ylabel("Total Belanja (BRL)")
ax_rfm[2].set_xlabel("Customer ID (Prefix)")
ax_rfm[2].set_title("By Monetary (Total Pengeluaran)", fontsize=13, fontweight="bold")
ax_rfm[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig_rfm)
plt.close(fig_rfm)

st.caption("Dicoding Data Analysis Submission | Proyek Akhir Belajar Analisis Data dengan Python")