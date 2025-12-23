"""
Protein Properties Analyzer
Part of The Reading Frame bioinformatics suite

Analyze physicochemical properties and visualize protein characteristics
"""

import streamlit as st
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import io
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Protein Properties",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style="text-align:center;color:#00E5FF;">
        Protein Properties Analyzer
    </h1>
    <p style="text-align:center;color:#BBBBBB;">
        Part of <b>The Reading Frame</b> Bioinformatics Suite<br>
        Physicochemical analysis & visualization of protein sequences
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- INPUT ----------------
col1, col2 = st.columns([3, 2])

with col1:
    sequence_text = st.text_area(
        "Paste Protein Sequence / FASTA",
        height=200,
        placeholder="Paste amino acid sequence or FASTA format here"
    )
    uploaded_file = st.file_uploader(
        "Or upload FASTA file",
        type=["fa", "fasta", "txt"]
    )

with col2:
    st.subheader("Analysis Options")
    remove_stops = st.checkbox("Remove stop codons (*)", value=True)
    window_size = st.slider(
        "Hydrophobicity sliding window",
        min_value=3,
        max_value=21,
        step=2,
        value=9
    )

# ---------------- HELPER FUNCTIONS ----------------
def clean_sequence(seq):
    seq = seq.upper().replace("\n", "").replace(" ", "")
    allowed = set("ACDEFGHIKLMNPQRSTVWY*")
    return "".join([aa for aa in seq if aa in allowed])

def extract_sequence(text, uploaded):
    if uploaded:
        data = uploaded.read().decode("utf-8")
        records = list(SeqIO.parse(io.StringIO(data), "fasta"))
        return str(records[0].seq) if records else clean_sequence(data)

    if text.strip().startswith(">"):
        records = list(SeqIO.parse(io.StringIO(text), "fasta"))
        return str(records[0].seq)

    return clean_sequence(text)

# ---------------- LOAD SEQUENCE ----------------
sequence = extract_sequence(sequence_text, uploaded_file)

if not sequence:
    st.info("Please provide a protein sequence.")
    st.stop()

if remove_stops:
    sequence = sequence.replace("*", "")

if len(sequence) == 0:
    st.error("No valid amino acids found.")
    st.stop()

analysis = ProteinAnalysis(sequence)

# ---------------- METRICS ----------------
st.subheader("Physicochemical Properties")

mw = analysis.molecular_weight()
pi = analysis.isoelectric_point()
instability = analysis.instability_index()
gravy = analysis.gravy()
aromaticity = analysis.aromaticity()
helix, turn, sheet = analysis.secondary_structure_fraction()

colA, colB, colC, colD = st.columns(4)

colA.metric("Length (aa)", len(sequence))
colA.metric("Molecular Weight (Da)", f"{mw:.2f}")

colB.metric("Isoelectric Point (pI)", f"{pi:.2f}")
colB.metric("Aromaticity", f"{aromaticity:.3f}")

colC.metric(
    "Instability Index",
    f"{instability:.2f}",
    delta="Stable" if instability < 40 else "Unstable"
)

colD.metric("GRAVY Score", f"{gravy:.3f}")

# ---------------- HYDROPHOBICITY ----------------
st.markdown("---")
st.subheader("Hydrophobicity Profile (Kyte–Doolittle)")

try:
    # Try the newer method first
    from Bio.SeqUtils.ProtParam import ProtParamData
    kd_scale = ProtParamData.kd
    kd = analysis.protein_scale(kd_scale, window=window_size)
except (AttributeError, ImportError):
    # Fallback for older versions
    try:
        kd = analysis.protein_scale(window=window_size)
    except:
        st.warning("Hydrophobicity profile unavailable for this sequence length or Biopython version.")
        kd = None

if kd:
    fig_hydro = go.Figure()
    fig_hydro.add_trace(go.Scatter(
        y=kd,
        mode="lines",
        name="Hydrophobicity",
        line=dict(color="#00E5FF", width=2)
    ))

    fig_hydro.update_layout(
        xaxis_title="Amino Acid Position",
        yaxis_title="Hydrophobicity Score",
        plot_bgcolor="white",
        hovermode="x unified"
    )

    st.plotly_chart(fig_hydro, use_container_width=True)
else:
    st.info("Sequence too short for hydrophobicity window analysis.")

# ---------------- AMINO ACID COMPOSITION ----------------
st.markdown("---")
st.subheader("Amino Acid Composition")

aa_counts = analysis.count_amino_acids()
aa_df = pd.DataFrame.from_dict(
    aa_counts, orient="index", columns=["Count"]
).reset_index()
aa_df.columns = ["Amino Acid", "Count"]
aa_df["Frequency"] = aa_df["Count"] / len(sequence)

fig_aa = go.Figure()
fig_aa.add_trace(go.Bar(
    x=aa_df["Amino Acid"],
    y=aa_df["Frequency"],
    marker=dict(color="#00FFAA")
))

fig_aa.update_layout(
    xaxis_title="Amino Acid",
    yaxis_title="Frequency",
    plot_bgcolor="white"
)

st.plotly_chart(fig_aa, use_container_width=True)

# ---------------- AA CLASSIFICATION ----------------
st.markdown("---")
st.subheader("Amino Acid Property Classification")

groups = {
    "Hydrophobic": list("AILMFWV"),
    "Polar": list("STNQY"),
    "Positive": list("KRH"),
    "Negative": list("DE")
}

group_counts = {
    g: sum(aa_counts.get(aa, 0) for aa in aas)
    for g, aas in groups.items()
}

fig_pie = go.Figure(
    data=[go.Pie(
        labels=list(group_counts.keys()),
        values=list(group_counts.values()),
        marker=dict(colors=["#00BFFF", "#00FFAA", "#FFDD55", "#FF6B6B"])
    )]
)

st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- CHARGE vs pH ----------------
st.markdown("---")
st.subheader("Net Charge vs pH")

ph_range = np.linspace(0, 14, 100)
charge = [analysis.charge_at_pH(p) for p in ph_range]

fig_charge = go.Figure()
fig_charge.add_trace(go.Scatter(
    x=ph_range,
    y=charge,
    mode="lines",
    line=dict(color="#FFDD55", width=2)
))

fig_charge.add_vline(
    x=pi,
    line_dash="dash",
    line_color="#00E5FF",
    annotation_text=f"pI = {pi:.2f}"
)

fig_charge.update_layout(
    xaxis_title="pH",
    yaxis_title="Net Charge",
    plot_bgcolor="white",
    hovermode="x unified"
)

st.plotly_chart(fig_charge, use_container_width=True)

# ---------------- SECONDARY STRUCTURE ----------------
st.markdown("---")
st.subheader("Secondary Structure Composition")

fig_ss = go.Figure()
fig_ss.add_trace(go.Bar(
    x=["Helix", "Turn", "Sheet"],
    y=[helix, turn, sheet],
    marker=dict(color=["#00BFFF", "#00FFAA", "#FFDD55"])
))

fig_ss.update_layout(
    yaxis_title="Fraction",
    plot_bgcolor="white"
)

st.plotly_chart(fig_ss, use_container_width=True)

# ---------------- EXPORT ----------------
st.markdown("---")
st.subheader("Export Results")

report = f"""
Protein Properties Report
--------------------------
Length: {len(sequence)}
Molecular Weight: {mw:.2f} Da
Isoelectric Point: {pi:.2f}
Instability Index: {instability:.2f}
GRAVY: {gravy:.3f}
Aromaticity: {aromaticity:.3f}

Secondary Structure:
Helix: {helix:.3f}
Turn: {turn:.3f}
Sheet: {sheet:.3f}

Amino Acid Classification:
"""

for group, count in group_counts.items():
    report += f"{group}: {count} ({count/len(sequence)*100:.1f}%)\n"

st.download_button(
    "Download TXT Report",
    report,
    file_name="protein_properties.txt"
)

st.download_button(
    "Download AA Composition (CSV)",
    aa_df.to_csv(index=False),
    file_name="amino_acid_composition.csv"
)

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center;color:#777;'>"
    "Part of The Reading Frame • Bioinformatics Toolkit"
    "</p>",
    unsafe_allow_html=True
)