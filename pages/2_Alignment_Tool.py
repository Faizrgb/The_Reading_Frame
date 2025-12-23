import streamlit as st
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

st.set_page_config(page_title="Alignment Tool", layout="wide")

# ------------------- PAGE TITLE -------------------
st.markdown(
    """
    <h1 style='text-align:center; color:#00E5FF;'>
        🔗 Sequence Alignment Tool
    </h1>
    <p style='text-align:center; color:#bbb; font-size:1.1rem;'>
        Perform Global (Needleman–Wunsch) or Local (Smith–Waterman) alignment for DNA or Protein
    </p>
    """,
    unsafe_allow_html=True,
)


# ------------------- TWO INPUT BOXES -------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sequence 1")
    seq1 = st.text_area(
        "Paste DNA or Protein sequence:",
        height=180,
        placeholder="ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"
    )

with col2:
    st.subheader("Sequence 2")
    seq2 = st.text_area(
        "Paste DNA or Protein sequence:",
        height=180,
        placeholder="ATGACCATTGTAATGAGCCGCTGAAGGGTGCCCGTTAG"
    )


# ------------------- ALIGNMENT OPTIONS -------------------
st.markdown("### ⚙ Alignment Settings")

align_type = st.selectbox(
    "Choose alignment type:",
    ["Global Alignment (Needleman–Wunsch)", "Local Alignment (Smith–Waterman)"],
)

scoring = st.radio(
    "Scoring scheme:",
    ["Identity match (default)", "Custom scoring (match/mismatch/gap)"],
    index=0
)

if scoring == "Custom scoring (match/mismatch/gap)":
    colA, colB, colC = st.columns(3)
    with colA:
        match = st.number_input("Match Score", value=2)
    with colB:
        mismatch = st.number_input("Mismatch Penalty", value=-1)
    with colC:
        gap = st.number_input("Gap Penalty", value=-2)
else:
    match = 1
    mismatch = 0
    gap = -1


# ------------------- ALIGN BUTTON -------------------
if st.button("🔍 Run Alignment", use_container_width=True):
    if not seq1 or not seq2:
        st.error("Please enter both sequences before aligning.")
    else:
        st.success("Alignment complete!")

        if align_type.startswith("Global"):
            aligns = pairwise2.align.globalms(
                seq1, seq2, match, mismatch, gap, gap
            )
        else:
            aligns = pairwise2.align.localms(
                seq1, seq2, match, mismatch, gap, gap
            )

        top = aligns[0]

        # ---------------- OUTPUT -------------------
        st.markdown("---")
        st.markdown("## 🧾 Top Alignment Result")

        st.code(format_alignment(*top), language='text')

        # Identity %
        aligned_seq1 = top[0]
        aligned_seq2 = top[1]

        matches = sum(1 for a, b in zip(aligned_seq1, aligned_seq2) if a == b)
        identity = (matches / len(aligned_seq1)) * 100

        st.markdown(
            f"""
            **Alignment Score:** `{top[2]}`  
            **Alignment Length:** `{len(aligned_seq1)}`  
            **Identity:** `{identity:.2f}%`
            """
        )
