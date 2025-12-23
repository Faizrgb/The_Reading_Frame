import streamlit as st

st.set_page_config(
    page_title="About | The Reading Frame",
    layout="wide"
)

# ---------- PAGE TITLE ----------
st.markdown(
    """
    <h1 style='text-align:center; color:#00E5FF;'>
        About This Project
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- ABOUT CONTENT ----------
st.markdown(
    """
    **The Reading Frame** is a web-based bioinformatics application developed as a  
    **Minor Project during the Third Semester of the M.Sc. Bioinformatics programme**  
    at **Jamia Millia Islamia, New Delhi**, under the **Department of Computer Sciences**.

    The primary objective of this project is to provide an integrated and user-friendly
    platform for performing essential bioinformatics analyses related to nucleotide
    and protein sequences. In modern biological research, tasks such as DNA-to-protein
    translation, identification of open reading frames (ORFs), sequence alignment, and
    protein property analysis are fundamental. However, these tasks are often carried
    out using multiple independent tools, which can be challenging for students and
    beginners in bioinformatics.

    **The Reading Frame** addresses this challenge by combining multiple core
    bioinformatics functionalities into a single unified interface. The application
    enables users to translate DNA sequences using standard genetic codes, detect ORFs
    across multiple reading frames, perform global and local sequence alignment for DNA
    and protein sequences, and analyze important protein properties such as molecular
    weight, isoelectric point (pI), GRAVY score, and stability index. Additionally, the
    tool supports FASTA file uploads and sequence retrieval directly from the NCBI
    database using accession IDs.

    The project has been designed with a strong emphasis on **academic learning,
    usability, and accessibility**, making it particularly suitable for students,
    educators, and early-stage researchers. By providing an interactive and visually
    intuitive environment, this application aims to simplify fundamental bioinformatics
    workflows while maintaining computational accuracy.
    """
)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# ---------- DEVELOPER INFORMATION ----------
st.markdown(
    """
    <h2 style='color:#00E5FF;'>Developer Information</h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    - **Name:** Mohd Faiz Khan  
    - **Programme:** M.Sc. Bioinformatics  
    - **Semester:** Third Semester (Minor Project)  
    - **Department:** Department of Computer Sciences  
    - **University:** Jamia Millia Islamia, New Delhi  
    """
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- FOOTER NOTE ----------
st.markdown(
    """
    <p style='color:#aaa; font-size:0.95rem;'>
        This project has been developed strictly for academic and educational purposes
        as part of the M.Sc. Bioinformatics curriculum.
    </p>
    """,
    unsafe_allow_html=True
)
