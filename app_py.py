import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# Load the updated ECMS dataset
df = pd.read_csv("ecms_maturity_audit_data.csv")

st.set_page_config(page_title="ECMS Maturity Audit Dashboard", layout="wide")
st.title("🌱 Environmental Compliance Maturity Audit Dashboard")

# Sidebar filter
industry = st.sidebar.selectbox("Select Industry to Review:", df["Industry"].unique())
selected = df[df["Industry"] == industry].squeeze()

# Summary Metrics
st.subheader(f"📊 Audit Summary for {industry}")
st.metric("Maturity Level", selected["Maturity_Level"])
st.metric("Penalty", selected["Penalty"])

col1, col2 = st.columns(2)
with col1:
    st.write("### Key Compliance Features")
    st.write(f"- **ISO 14001 Certified:** {selected['Has_ISO14001_Certification']}")
    st.write(f"- **Leadership Commitment:** {selected['Leadership_Commitment']}")
    st.write(f"- **Supplier Engagement:** {selected['Supplier_Engagement']}")
    st.write(f"- **GHG Tracking:** {selected['GHG_Tracking']}")
    st.write(f"- **KPI Measurement:** {selected['KPI_Measurement']}")
    st.write(f"- **Corrective Actions:** {selected['Corrective_Actions']}")
    st.write(f"- **Public Environmental Report:** {selected['Public_Environmental_Report']}")

with col2:
    st.write("### Compliance Radar Chart")
    radar_labels = [
        "ISO 14001", "Leadership", "Suppliers", "GHG Tracking",
        "KPI Tracking", "Corrective Actions", "Reporting"
    ]
    radar_values = [
        selected['Has_ISO14001_Certification'] == "Yes",
        selected['Leadership_Commitment'] == "Strong",
        selected['Supplier_Engagement'] == "Yes",
        selected['GHG_Tracking'] == "Yes",
        selected['KPI_Measurement'] == "Yes",
        selected['Corrective_Actions'] == "Yes",
        selected['Public_Environmental_Report'] == "Yes"
    ]
    radar_numeric = [1 if v else 0 for v in radar_values]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    theta = [n / float(len(radar_labels)) * 2 * 3.14159 for n in range(len(radar_labels))]
    radar_numeric += radar_numeric[:1]
    theta += theta[:1]
    ax.plot(theta, radar_numeric, color='green', linewidth=2)
    ax.fill(theta, radar_numeric, color='lightgreen', alpha=0.25)
    ax.set_xticks(theta[:-1])
    ax.set_xticklabels(radar_labels)
    ax.set_yticklabels([])
    ax.set_title("Compliance Radar", size=16)
    st.pyplot(fig)

# Industry-wide comparison
st.divider()
st.subheader("📌 Industry Maturity Level Overview")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.countplot(data=df, x="Maturity_Level", palette="Set2", order=["LAGGARD", "COMPLIANT", "LEADER"], ax=ax2)
ax2.set_title("Number of Industries by Maturity Level")
ax2.set_ylabel("Count")
st.pyplot(fig2)

# Export PDF Report
if st.button("📄 Export PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"ECMS Audit Report", ln=True, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Industry: {industry}", ln=True)
    pdf.cell(200, 10, txt=f"Maturity Level: {selected['Maturity_Level']}", ln=True)
    pdf.cell(200, 10, txt=f"Penalty: {selected['Penalty']}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Key Features:", ln=True)
    for col in [
        "Has_ISO14001_Certification", "Leadership_Commitment", "Supplier_Engagement",
        "GHG_Tracking", "KPI_Measurement", "Corrective_Actions", "Public_Environmental_Report"
    ]:
        pdf.cell(200, 8, txt=f"{col.replace('_', ' ')}: {selected[col]}", ln=True)

    pdf_file = f"ECMS_Report_{industry.replace(' ', '_')}.pdf"
    pdf.output(pdf_file)

    with open(pdf_file, "rb") as f:
        st.download_button("📥 Download ECMS PDF Report", f, file_name=pdf_file)

# Downloadable version of dataset
st.download_button(
    label="📥 Download Full ECMS Dataset",
    data=df.to_csv(index=False),
    file_name="ecms_maturity_audit_data_updated.csv",
    mime="text/csv"
)
