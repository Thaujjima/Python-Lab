
import os
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Insurance Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Insurance Analytics Dashboard")
st.caption("Upload the provided **insurance.csv** or place it in the same folder as this app and click *Use sample file* in the sidebar.")

# -----------------------------
# Data loading
# -----------------------------
@st.cache_data(show_spinner=False)
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    # Normalize column names just in case
    df.columns = [c.strip().lower() for c in df.columns]
    # Coerce numeric columns if needed
    num_cols = ["age", "bmi", "children", "charges"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=["age","bmi","children","charges"])

with st.sidebar:
    st.header("⚙️ Controls")
    uploaded = st.file_uploader("Upload insurance.csv", type=["csv"])
    use_sample = st.checkbox("Use sample file (insurance.csv in app folder)", value=True if not uploaded else False, help="If checked and no file uploaded, the app will try to read ./insurance.csv")

    # Try to locate a local sample file for convenience
    default_candidates = [
        "insurance.csv",
        os.path.join(os.getcwd(), "insurance.csv")
    ]
    # Also consider an absolute path provided in code comments if the app was pre-bundled with data
    absolute_hint = os.environ.get("INS_ABS_PATH", "").strip()
    if absolute_hint:
        default_candidates.append(absolute_hint)

if uploaded is not None:
    df = pd.read_csv(uploaded)
    df.columns = [c.strip().lower() for c in df.columns]
else:
    df = pd.read_csv("insurance.csv")

    # df = None
    # if use_sample:
    #     for cand in default_candidates:
    #         if cand and os.path.exists(cand):
    #             try:
    #                 df = load_data(cand)
    #                 break
    #             except Exception:
    #                 pass

if df is None:
    st.info("👈 Please upload **insurance.csv** from the provided file, or place it next to this script and tick **Use sample file**.")
    st.stop()

# Ensure expected columns exist
expected_cols = {"age","sex","bmi","children","smoker","region","charges"}
missing = expected_cols - set(df.columns)
if missing:
    st.error(f"Required columns missing: {', '.join(sorted(missing))}")
    st.stop()

# -----------------------------
# Filters
# -----------------------------
with st.sidebar:
    st.subheader("🔎 Filters")

    age_min, age_max = int(df["age"].min()), int(df["age"].max())
    age_range = st.slider("Age range", min_value=age_min, max_value=age_max, value=(age_min, age_max))

    bmi_min, bmi_max = float(np.floor(df["bmi"].min())), float(np.ceil(df["bmi"].max()))
    bmi_range = st.slider("BMI range", min_value=bmi_min, max_value=bmi_max, value=(bmi_min, bmi_max))

    child_min, child_max = int(df["children"].min()), int(df["children"].max())
    children_sel = st.slider("Children (0+)", min_value=child_min, max_value=child_max, value=(child_min, child_max))

    sex_options = sorted(df["sex"].dropna().unique().tolist())
    sex_sel = st.multiselect("Sex", options=sex_options, default=sex_options)

    smoker_options = sorted(df["smoker"].dropna().unique().tolist())
    smoker_sel = st.multiselect("Smoker", options=smoker_options, default=smoker_options)

    region_options = sorted(df["region"].dropna().unique().tolist())
    region_sel = st.multiselect("Region", options=region_options, default=region_options)

# Apply filters
mask = (
    (df["age"].between(age_range[0], age_range[1]))
    & (df["bmi"].between(bmi_range[0], bmi_range[1]))
    & (df["children"].between(children_sel[0], children_sel[1]))
    & (df["sex"].isin(sex_sel))
    & (df["smoker"].isin(smoker_sel))
    & (df["region"].isin(region_sel))
)

fdf = df.loc[mask].copy()

# -----------------------------
# KPI Metrics
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Records (filtered)", f"{len(fdf):,}")
with col2:
    st.metric("Avg Charges", f"${fdf['charges'].mean():,.2f}")
with col3:
    st.metric("Median Charges", f"${fdf['charges'].median():,.2f}")
with col4:
    smoker_rate = (fdf["smoker"].eq("yes").mean() * 100.0) if "yes" in fdf["smoker"].unique() else 0.0
    st.metric("Smoker %", f"{smoker_rate:.1f}%")

st.divider()

# -----------------------------
# Charts
# -----------------------------
st.subheader("📈 Charts")

# 1) Average charges by region (bar)
bar_data = fdf.groupby("region", as_index=False)["charges"].mean().sort_values("charges", ascending=False)
bar_chart = (
    alt.Chart(bar_data, title="Average Charges by Region")
    .mark_bar()
    .encode(
        x=alt.X("region:N", sort='-y', title="Region"),
        y=alt.Y("charges:Q", title="Avg Charges"),
        tooltip=["region","charges"]
    )
).properties(height=320)
st.altair_chart(bar_chart, use_container_width=True)

# 2) Charges distribution (histogram)
hist = (
    alt.Chart(fdf, title="Charges Distribution")
    .mark_bar()
    .encode(
        alt.X("charges:Q", bin=alt.Bin(maxbins=40), title="Charges"),
        alt.Y("count()", title="Count"),
        tooltip=[alt.Tooltip("count()", title="Count")]
    )
).properties(height=320)
st.altair_chart(hist, use_container_width=True)

# 3) Age vs. Charges scatter with smoker color + trendline
scatter = (
    alt.Chart(fdf, title="Age vs Charges (colored by smoker)")
    .mark_circle(opacity=0.6)
    .encode(
        x=alt.X("age:Q", title="Age"),
        y=alt.Y("charges:Q", title="Charges"),
        color=alt.Color("smoker:N", title="Smoker"),
        tooltip=["age","bmi","children","smoker","region","charges"]
    )
).properties(height=360)

trend = (
    alt.Chart(fdf)
    .transform_regression("age", "charges", groupby=["smoker"])
    .mark_line()
    .encode(x="age:Q", y="charges:Q", color="smoker:N")
)
st.altair_chart(scatter + trend, use_container_width=True)

st.divider()

# -----------------------------
# Table
# -----------------------------
st.subheader("🧾 Data Table (Filtered)")
st.caption("Tip: Use the column headers to sort. Use the download button below to export the filtered data.")
st.dataframe(fdf, use_container_width=True)

# Summary table by smoker/region (optional helpful pivot)
st.subheader("🔁 Summary: Avg Charges by Smoker & Region")
pivot = fdf.pivot_table(index="region", columns="smoker", values="charges", aggfunc="mean").round(2)
st.dataframe(pivot, use_container_width=True)

# -----------------------------
# Downloads
# -----------------------------
@st.cache_data
def to_csv_bytes(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download filtered data (CSV)",
    data=to_csv_bytes(fdf),
    file_name="insurance_filtered.csv",
    mime="text/csv"
)

st.info("💡 Run locally: `streamlit run streamlit_insurance_dashboard.py`")
