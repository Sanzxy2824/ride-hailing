"""Dashboard Ride-Hailing - studi kasus portofolio (dataset simulasi). Satu halaman, filter di atas."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Ride Pulse", page_icon="🚗", layout="wide")
BLUE, ORANGE, INK, SOFT = "#2563EB", "#FF7A1A", "#0B1B3A", "#E6EEFF"
rupiah = lambda x: f"Rp {x:,.0f}".replace(",", ".")

st.markdown(f"""<style>
header[data-testid="stHeader"] {{background: transparent;}}
.hero {{background: linear-gradient(120deg,{BLUE},#7C3AED); color:#fff; border-radius:22px; padding:26px 32px;}}
.hero h1 {{color:#fff; margin:0; font-size:2.2rem;}} .hero p {{color:#DDE7FF; margin:4px 0 0;}}
.pill {{display:inline-block; background:{ORANGE}; color:#fff; border-radius:999px; padding:2px 12px; font-size:.75rem; font-weight:700;}}
.stat {{background:#fff; border-radius:18px; padding:16px 18px; box-shadow:0 6px 20px rgba(37,99,235,.12);}}
.stat .l {{color:#5B6B8C; font-size:.8rem; font-weight:600;}} .stat .v {{color:{INK}; font-size:1.6rem; font-weight:800; white-space:nowrap;}}
.sec {{font-size:1.35rem; font-weight:800; color:{INK}; margin:26px 0 2px;}} .q {{color:#5B6B8C; margin:0 0 10px;}}
.tip {{background:{SOFT}; border-left:5px solid {ORANGE}; border-radius:10px; padding:10px 14px; color:{INK}; margin:8px 0;}}
</style>""", unsafe_allow_html=True)


@st.cache_data
def load(path="data/ride_hailing_trip_analysis_raw.csv"):
    df = pd.read_csv(path).drop_duplicates(subset="trip_id").copy()
    for c in ["dropoff_area", "payment_method", "customer_type"]:
        df[c] = df[c].fillna("Unknown")
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["time"].str[:2].astype(int)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["fare_per_km"] = df["fare"] / df["distance_km"]
    df["speed"] = df["distance_km"] / (df["duration_minutes"] / 60)
    df["bucket"] = pd.cut(df["distance_km"], [0, 2, 5, 10, 100], labels=["≤ 2 km", "2–5 km", "5–10 km", "> 10 km"])
    return df


def fmt(fig, h=380):
    fig.update_layout(height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=20, b=10),
                      font=dict(color=INK), legend_title_text="")
    return fig


def stat(col, l, v):
    col.markdown(f'<div class="stat"><div class="l">{l}</div><div class="v">{v}</div></div>', unsafe_allow_html=True)


def section(title, q):
    st.markdown(f'<div class="sec">{title}</div><div class="q">{q}</div>', unsafe_allow_html=True)


def tip(t):
    st.markdown(f'<div class="tip">🧭 {t}</div>', unsafe_allow_html=True)


df = load()
st.markdown('<div class="hero"><span class="pill">STUDI KASUS · DATASET SIMULASI</span><h1>🚗 Ride Pulse Semarang</h1><p>Denyut permintaan, aliran perjalanan, dan tarif · Jan–Jun 2026</p></div>', unsafe_allow_html=True)
st.write("")
c1, c2, c3 = st.columns(3)
months = sorted(df["month"].unique())
sel_m = c1.multiselect("Bulan", months, default=months)
sel_v = c2.multiselect("Kendaraan", sorted(df["vehicle_type"].unique()), default=sorted(df["vehicle_type"].unique()))
sel_c = c3.multiselect("Tipe pelanggan", sorted(df["customer_type"].unique()), default=sorted(df["customer_type"].unique()))
f = df[df["month"].isin(sel_m) & df["vehicle_type"].isin(sel_v) & df["customer_type"].isin(sel_c)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini."); st.stop()
k = st.columns(4)
stat(k[0], "Total pendapatan", rupiah(f["fare"].sum()))
stat(k[1], "Perjalanan", f"{len(f):,}".replace(",", "."))
stat(k[2], "Rata-rata tarif", rupiah(f["fare"].mean()))
stat(k[3], "Kecepatan rata-rata", f"{f['speed'].mean():.1f} km/jam")

# 1. Jam radial
section("⏰ Jam Siaga", "Jam berapa armada harus paling banyak tersedia?")
a, b = st.columns([3, 2])
h = f.groupby("hour", as_index=False).size()
with a:
    fig = px.bar_polar(h, r="size", theta=h["hour"] * 15, color="size", color_continuous_scale=["#BFD3FF", BLUE, ORANGE], labels={"size": "Perjalanan"})
    fig.update_layout(polar=dict(angularaxis=dict(tickmode="array", tickvals=[i * 15 for i in range(0, 24, 3)], ticktext=[f"{i:02d}:00" for i in range(0, 24, 3)], direction="clockwise", rotation=90)), coloraxis_showscale=False)
    st.plotly_chart(fmt(fig, 430), width="stretch")
with b:
    top3 = h.nlargest(3, "size")
    st.markdown("**3 jam tersibuk**")
    for _, r in top3.iterrows():
        st.progress(float(r["size"] / h["size"].max()), text=f"{int(r['hour']):02d}.00 · {int(r['size'])} perjalanan")
    st.markdown(f"**Paling sepi:** {int(h.nsmallest(1, 'size')['hour'].iloc[0]):02d}.00 ({int(h['size'].min())} perjalanan)")
    tip("Dua puncak komuter: pagi (07.00) dan sore (17.00–19.00). Dini hari sangat sepi.")

# 2. Sankey
section("🔀 Aliran Perjalanan", "Dari area mana ke area mana orang paling sering bergerak?")
od = f[f["dropoff_area"] != "Unknown"].groupby(["pickup_area", "dropoff_area"], as_index=False).size().nlargest(25, "size")
src = sorted(od["pickup_area"].unique()); dst = sorted(od["dropoff_area"].unique())
labels = [f"{s} (jemput)" for s in src] + [f"{d} (tujuan)" for d in dst]
idx = {l: i for i, l in enumerate(labels)}
fig = go.Figure(go.Sankey(node=dict(label=labels, pad=14, color=[BLUE] * len(src) + [ORANGE] * len(dst)),
                          link=dict(source=[idx[f"{s} (jemput)"] for s in od["pickup_area"]], target=[idx[f"{d} (tujuan)"] for d in od["dropoff_area"]],
                                    value=od["size"], color="rgba(37,99,235,.25)")))
st.plotly_chart(fmt(fig, 480), width="stretch")
tip("Rute-rute teratas tersebar tipis (rute terpadat hanya ±56 perjalanan dari 4.000), jadi tidak ada koridor tunggal yang mendominasi. Rute terpadat: Simpang Lima ke Simpang Lima (perjalanan dalam area sama).")

# 3 & 4
a, b = st.columns(2)
with a:
    section("📏 Tarif vs Jarak", "Apakah perjalanan pendek 'terlalu mahal' per km?")
    bk = f.groupby("bucket", observed=True).agg(per_km=("fare_per_km", "mean"), n=("fare", "size")).reset_index()
    fig = px.bar(bk, x="bucket", y="per_km", text=bk["per_km"].round(-1).astype(int).astype(str), color_discrete_sequence=[BLUE], labels={"bucket": "Jarak", "per_km": "Tarif per km (Rp)"})
    fig.update_traces(marker_cornerradius=10); st.plotly_chart(fmt(fig, 340), width="stretch")
    tip("Perjalanan ≤ 2 km bertarif ±Rp10.500/km, lebih dari dua kali lipat perjalanan > 10 km (±Rp4.500/km): efek tarif dasar.")
with b:
    section("🐢 Kecepatan", "Adakah pola kemacetan sepanjang hari?")
    sp = f.groupby("hour", as_index=False)["speed"].mean()
    fig = px.area(sp, x="hour", y="speed", color_discrete_sequence=[ORANGE], labels={"hour": "Jam", "speed": "Kecepatan rata-rata (km/jam)"})
    fig.update_yaxes(range=[0, 25]); st.plotly_chart(fmt(fig, 340), width="stretch")
    tip("Kecepatan datar di kisaran 13–14 km/jam sepanjang hari: jam puncak tidak membuat perjalanan melambat di data ini.")

# 5
section("🔁 Retensi Pelanggan", "Apakah pelanggan lama tetap setia dari bulan ke bulan?")
a, b = st.columns([3, 2])
rt = df.groupby("month")["customer_type"].apply(lambda s: (s == "Returning Customer").mean() * 100).reset_index(name="pct")
with a:
    fig = px.line(rt, x="month", y="pct", markers=True, color_discrete_sequence=[BLUE], labels={"month": "", "pct": "% pelanggan lama"})
    fig.update_yaxes(range=[60, 80]); st.plotly_chart(fmt(fig, 320), width="stretch")
with b:
    p = f.groupby("payment_method", as_index=False).size()
    st.plotly_chart(fmt(px.pie(p, names="payment_method", values="size", hole=0.55, color_discrete_sequence=[BLUE, ORANGE, "#7C3AED", "#93B4FF", "#999"]), 320), width="stretch")
tip("Porsi pelanggan lama turun dari ±74–75% (Jan–Feb) ke ±69,6% (Apr dan Jun). Perlu dipantau lewat program loyalitas.")

with st.expander("📋 Data perjalanan"):
    st.dataframe(f.drop(columns=["hour", "month", "fare_per_km", "speed", "bucket"]), width="stretch")
