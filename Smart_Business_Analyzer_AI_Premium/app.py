import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Smart Business Analyzer AI",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff 0%, #ecfeff 45%, #fdf2f8 100%);
}
.hero {
    padding: 30px;
    border-radius: 25px;
    background: linear-gradient(120deg, #0f766e, #2563eb, #9333ea);
    color: white;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.18);
}
.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}
.card {
    padding: 22px;
    border-radius: 20px;
    background: rgba(255,255,255,0.88);
    box-shadow: 0px 8px 24px rgba(0,0,0,0.10);
    border: 1px solid rgba(255,255,255,0.7);
}
.good {
    padding: 16px;
    border-radius: 15px;
    background: #dcfce7;
    border-left: 6px solid #16a34a;
    margin-bottom: 10px;
}
.warn {
    padding: 16px;
    border-radius: 15px;
    background: #fef3c7;
    border-left: 6px solid #f59e0b;
    margin-bottom: 10px;
}
.risk {
    padding: 16px;
    border-radius: 15px;
    background: #fee2e2;
    border-left: 6px solid #dc2626;
    margin-bottom: 10px;
}
.info {
    padding: 16px;
    border-radius: 15px;
    background: #dbeafe;
    border-left: 6px solid #2563eb;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🚀 Smart Business Analyzer AI</h1>
<p>Upload Excel → AI explains your business, creates charts, KPIs, insights and recommendations.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("📌 Smart Analyzer")
page = st.sidebar.radio("Select Page", ["🏠 Home", "📂 Upload / Demo Data", "📊 Dashboard", "🤖 AI Insights", "📁 Dataset", "📄 Report"])

@st.cache_data
def load_demo(kind):
    if kind == "Academy / School":
        return pd.read_excel("sample_data/academy_school_demo.xlsx")
    if kind == "Hospital / Clinic":
        return pd.read_excel("sample_data/hospital_demo.xlsx")
    if kind == "Restaurant":
        return pd.read_excel("sample_data/restaurant_demo.xlsx")
    return pd.read_excel("sample_data/shop_demo.xlsx")

def detect_business(df):
    cols = " ".join([c.lower() for c in df.columns])
    if "student" in cols or "attendance" in cols or "teacher" in cols or "course" in cols:
        return "Academy / School"
    if "patient" in cols or "department" in cols or "appointments" in cols:
        return "Hospital / Clinic"
    if "category" in cols and "product" in cols:
        return "Restaurant"
    if "stock" in cols or "product" in cols:
        return "Shop / Retail"
    return "General Business"

def find_col(df, keys):
    for c in df.columns:
        lc = c.lower()
        for k in keys:
            if k in lc:
                return c
    return None

if "df" not in st.session_state:
    st.session_state.df = load_demo("Academy / School")

if page == "🏠 Home":
    st.markdown("## ✨ What this app can do")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><h3>🏫 Academy / School</h3><p>Attendance, progress, fee status, weak students and teacher overview.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>🏥 Hospital / Clinic</h3><p>Appointments, revenue, departments and patient satisfaction analysis.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h3>🍽️ Restaurant / Shop</h3><p>Sales, profit, stock, top products and slow products.</p></div>', unsafe_allow_html=True)
    st.success("Demo tagline: Upload Excel → AI does the analysis.")

elif page == "📂 Upload / Demo Data":
    st.subheader("📂 Choose Demo Data or Upload Your Own Excel/CSV")
    mode = st.radio("Data Source", ["Use Demo Data", "Upload File"])
    if mode == "Use Demo Data":
        kind = st.selectbox("Select Business Type", ["Academy / School", "Hospital / Clinic", "Restaurant", "Shop / Retail"])
        st.session_state.df = load_demo(kind)
        st.success(f"{kind} demo loaded successfully.")
    else:
        uploaded = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])
        if uploaded:
            if uploaded.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded)
            else:
                st.session_state.df = pd.read_excel(uploaded)
            st.success("File uploaded successfully.")
    st.dataframe(st.session_state.df.head(), use_container_width=True)

elif page == "📊 Dashboard":
    df = st.session_state.df
    business = detect_business(df)
    st.subheader(f"📊 Dashboard — {business}")

    sales_col = find_col(df, ["sales", "revenue", "income"])
    cost_col = find_col(df, ["cost", "expense"])
    attendance_col = find_col(df, ["attendance"])
    progress_col = find_col(df, ["progress"])
    qty_col = find_col(df, ["quantity", "qty", "appointments"])
    stock_col = find_col(df, ["stock"])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Records", len(df))

    if sales_col:
        k2.metric("Total Sales / Revenue", f"{df[sales_col].sum():,.0f}")
    elif attendance_col:
        k2.metric("Average Attendance", f"{df[attendance_col].mean():.1f}%")
    else:
        k2.metric("Columns", df.shape[1])

    if cost_col and sales_col:
        profit = df[sales_col].sum() - df[cost_col].sum()
        k3.metric("Estimated Profit", f"{profit:,.0f}")
    elif progress_col:
        k3.metric("Average Progress", f"{df[progress_col].mean():.1f}%")
    else:
        k3.metric("Numeric Columns", len(df.select_dtypes(include="number").columns))

    if qty_col:
        k4.metric("Total Quantity / Appointments", f"{df[qty_col].sum():,.0f}")
    elif stock_col:
        k4.metric("Total Stock", f"{df[stock_col].sum():,.0f}")
    else:
        k4.metric("Business Type", business)

    st.markdown("---")
    numeric_cols = list(df.select_dtypes(include="number").columns)
    text_cols = list(df.select_dtypes(exclude="number").columns)

    if numeric_cols and text_cols:
        col1, col2 = st.columns(2)
        with col1:
            x = st.selectbox("Category Column", text_cols)
            y = st.selectbox("Numeric Column", numeric_cols)
            chart_data = df.groupby(x)[y].sum().sort_values(ascending=False).head(10)
            fig, ax = plt.subplots()
            chart_data.plot(kind="bar", ax=ax)
            ax.set_title(f"Top {x} by {y}")
            st.pyplot(fig)
        with col2:
            pie_col = st.selectbox("Pie Category", text_cols, key="pie")
            fig2, ax2 = plt.subplots()
            df[pie_col].value_counts().head(6).plot(kind="pie", autopct="%1.1f%%", ax=ax2)
            ax2.set_ylabel("")
            ax2.set_title(f"{pie_col} Distribution")
            st.pyplot(fig2)

    if len(numeric_cols) >= 2:
        st.write("### Relationship Chart")
        a = st.selectbox("X Axis", numeric_cols, key="xaxis")
        b = st.selectbox("Y Axis", numeric_cols, index=1, key="yaxis")
        fig3, ax3 = plt.subplots()
        ax3.scatter(df[a], df[b])
        ax3.set_xlabel(a)
        ax3.set_ylabel(b)
        ax3.set_title(f"{a} vs {b}")
        st.pyplot(fig3)

elif page == "🤖 AI Insights":
    df = st.session_state.df
    business = detect_business(df)
    st.subheader(f"🤖 AI Insights — {business}")

    sales_col = find_col(df, ["sales", "revenue", "income"])
    cost_col = find_col(df, ["cost", "expense"])
    attendance_col = find_col(df, ["attendance"])
    progress_col = find_col(df, ["progress"])
    product_col = find_col(df, ["product", "item"])
    fee_col = find_col(df, ["fee_status", "fee status", "payment"])
    satisfaction_col = find_col(df, ["satisfaction", "rating"])

    insights = []

    if sales_col:
        insights.append(("good", f"Total sales/revenue is {df[sales_col].sum():,.0f}."))
        if cost_col:
            profit = df[sales_col].sum() - df[cost_col].sum()
            margin = profit / df[sales_col].sum() * 100 if df[sales_col].sum() else 0
            insights.append(("info", f"Estimated profit is {profit:,.0f} with margin {margin:.1f}%."))
    if product_col and sales_col:
        best = df.groupby(product_col)[sales_col].sum().sort_values(ascending=False)
        insights.append(("good", f"Best performing product/item: {best.index[0]}"))
        insights.append(("warn", f"Slowest product/item: {best.index[-1]}"))
    if attendance_col:
        low = df[df[attendance_col] < 60]
        insights.append(("risk", f"{len(low)} students/records have attendance below 60%."))
    if progress_col:
        weak = df[df[progress_col] < 60]
        insights.append(("warn", f"{len(weak)} students/records have progress below 60%."))
    if fee_col:
        pending = df[df[fee_col].astype(str).str.lower().str.contains("pending|unpaid", na=False)]
        insights.append(("risk", f"{len(pending)} records have pending/unpaid fees."))
    if satisfaction_col:
        avg = df[satisfaction_col].mean()
        insights.append(("info", f"Average satisfaction/rating is {avg:.1f}."))

    if not insights:
        insights.append(("info", "Data uploaded successfully. Add sales, cost, attendance, progress or product columns for stronger insights."))

    for kind, msg in insights:
        st.markdown(f'<div class="{kind}"><b>{kind.upper()}:</b> {msg}</div>', unsafe_allow_html=True)

    st.markdown("### ✅ AI Recommendations")
    st.markdown('<div class="good">Focus on weak/low-performing areas first.</div>', unsafe_allow_html=True)
    st.markdown('<div class="info">Use monthly data to improve future predictions.</div>', unsafe_allow_html=True)
    st.markdown('<div class="warn">Export this dashboard as a client report for business owners.</div>', unsafe_allow_html=True)

elif page == "📁 Dataset":
    df = st.session_state.df
    st.subheader("📁 Dataset")
    st.dataframe(df, use_container_width=True)
    st.write("### Shape")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    st.write("### Summary")
    st.dataframe(df.describe(include="all"), use_container_width=True)

elif page == "📄 Report":
    df = st.session_state.df
    business = detect_business(df)
    st.subheader("📄 Simple Report")
    report = f"""
Smart Business Analyzer AI Report

Detected Business Type: {business}
Total Records: {len(df)}
Total Columns: {df.shape[1]}

This demo app can analyze academy, school, hospital, restaurant, shop and general business data.
It provides KPIs, charts, AI-style insights and recommendations.
"""
    st.text_area("Generated Report", report, height=250)
    st.download_button("Download Report TXT", report, file_name="business_ai_report.txt")