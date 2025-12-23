# app.py  (HOME PAGE)
import streamlit as st
from streamlit_lottie import st_lottie
import os, json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="The Reading Frame",
    layout="wide"
)

# ---------------- LOAD ANIMATION SAFELY ----------------
def load_lottie(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

dna_animation = load_lottie("assets/dna_animation.json")

# ---------------- INLINE CSS ----------------
st.markdown("""
<style>

/* Smooth scrolling */
html { scroll-behavior: smooth; }

/* NAVBAR */
.navbar {
    display: flex;
    justify-content: center;
    gap: 35px;
    padding: 10px 0;
    margin: 20px 0 30px 0;
}
.nav-item {
    font-size: 1.1rem;
    font-weight: 500;
    color: #aaa;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.3s ease;
}
.nav-item:hover {
    color: #00E5FF;
    background-color: #1f1f1f;
}
.nav-item.active {
    color: #00E5FF;
    border-bottom: 2px solid #00E5FF;
}

/* FEATURE CARD FIX */
.feature-card {
    padding: 18px;
    border-radius: 14px;
    background: #1F1F1F;
    border: 1px solid #333;
    transition: all 0.25s ease;
    height: 100% !important;
    min-height: 250px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 0px 18px rgba(0, 200, 255, 0.25);
    border: 1px solid #00C8FF;
}
.card-content { flex-grow: 1; }
.card-button-link { margin-top: 1rem; }

/* BUTTON */
.tool-btn {
    padding: 8px 18px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: 0.25s;
}
.tool-btn:hover {
    transform: scale(1.05);
    filter: brightness(1.15);
}

/* ABOUT SECTION */
.about-section {
    max-width: 1000px;
    margin: 60px auto;
    padding: 40px 45px;
    background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
    border-radius: 16px;
    border: 1px solid #00E5FF;
    box-shadow: 0 8px 32px rgba(0, 229, 255, 0.1);
}
.about-section h2 {
    text-align: center;
    color: #00E5FF;
    margin-bottom: 40px;
    font-size: 2.5rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}
.about-section h3 {
    color: #00E5FF;
    font-size: 1.6rem;
    font-weight: 600;
    margin-top: 35px;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #00E5FF;
    position: relative;
}
.about-section h3::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 60px;
    height: 2px;
    background: #00BFFF;
}
.about-section p {
    color: #d4d4d4;
    font-size: 1.1rem;
    line-height: 1.8;
    margin-bottom: 20px;
    text-align: justify;
}
.about-section ul {
    margin-left: 0;
    padding-left: 0;
    list-style: none;
}
.about-section li {
    color: #d4d4d4;
    font-size: 1.1rem;
    line-height: 1.9;
    margin-bottom: 12px;
    padding-left: 30px;
    position: relative;
}
.about-section li::before {
    content: '▹';
    position: absolute;
    left: 0;
    color: #00E5FF;
    font-size: 1.4rem;
    font-weight: bold;
}
.about-section li b {
    color: #00BFFF;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER WITH ANIMATION ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <h1 style='font-size:3.1rem; color:#00E5FF; margin-top: 20px;'>
        The Reading Frame
    </h1>
    <p style='font-size:1.2rem; color:#ccc; margin-top:-10px;'>
        A Modern Bioinformatics Toolkit for DNA, Protein & ORF Exploration
    </p>
    """, unsafe_allow_html=True)

with col2:
    if dna_animation:
        st_lottie(dna_animation, height=200, quality="high")
    else:
        st.info("Upload assets/dna_animation.json to display animation here.")

# ---------------- NAVBAR ----------------
st.markdown("""
<div class="navbar">
    <a class="nav-item active" href="/">Overview</a>
    <a class="nav-item" href="/Translation_Engine" target="_self">Translator</a>
    <a class="nav-item" href="/Alignment_Tool" target="_self">Aligner</a>
    <a class="nav-item" href="/Protein_Properties" target="_self">Analyzer</a>
    <a class="nav-item" href="#about">About</a>
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURE CARDS ----------------
st.markdown("### Core Toolkit")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-content">
            <h3 style='color:#00BFFF;'>Translation Engine</h3>
            <p style='color:#aaa;'>DNA → Protein, ORFs, multi-frame translation.</p>
        </div>
        <a class="card-button-link" href='/Translation_Engine' target="_self">
            <button class="tool-btn" style='background:#00BFFF; color:black;'>Open Translator</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-content">
            <h3 style='color:#00FFAA;'>Alignment Tool</h3>
            <p style='color:#aaa;'>Local & global DNA/protein alignment.</p>
        </div>
        <a class="card-button-link" href='/Alignment_Tool' target="_self">
            <button class="tool-btn" style='background:#00FFAA; color:black;'>Open Aligner</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-content">
            <h3 style='color:#FFDD55;'>Protein Properties</h3>
            <p style='color:#aaa;'>MW, pI, stability, GRAVY & more.</p>
        </div>
        <a class="card-button-link" href='/Protein_Properties' target="_self">
            <button class="tool-btn" style='background:#FFDD55; color:black;'>Open Analyzer</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ABOUT SECTION ----------------
st.markdown("""
<div class="about-section" id="about">
    <h2>About</h2>
    <h3>Introduction</h3>
    <p>
       The rapid advancement of high-throughput sequencing technologies has led to an exponential increase in biological sequence data, necessitating efficient computational tools for its analysis and interpretation. Core bioinformatics tasks such as DNA-to-protein translation, open reading frame (ORF) identification, sequence alignment, and protein property analysis form the foundation of molecular biology and genomics research.
The Reading Frame is a web-based bioinformatics application developed to support these fundamental sequence analysis tasks within a unified and accessible framework. The platform integrates multiple analytical functionalities into a single system, enabling the systematic analysis of nucleotide and protein sequences while minimizing the need for multiple independent software tools.
The application is designed with an emphasis on computational accuracy, reproducibility, and usability, making it particularly suitable for academic and educational environments. By providing an intuitive interface coupled with established bioinformatics methodologies, The Reading Frame facilitates both exploratory analysis and conceptual understanding of sequence-based biological data.
This project demonstrates the application of bioinformatics principles through modern web technologies and serves as an academic resource for students, educators, and researchers engaged in molecular sequence analysis.
    </p>
    <h3>Why This Toolkit?</h3>
    <p>
      Bioinformatics workflows often require the use of multiple independent tools to perform fundamental tasks such as sequence translation, open reading frame detection, alignment, and protein property analysis. For students and early-stage researchers, managing these fragmented tools can be inefficient, time-consuming, and conceptually challenging.
        The Reading Frame was developed to address this gap by integrating essential bioinformatics functionalities into a single, coherent platform. The toolkit simplifies routine sequence analysis tasks while maintaining computational accuracy and academic relevance. Its design prioritizes usability and clarity, allowing users to focus on biological interpretation rather than software complexity.
        By providing a unified workflow environment, The Reading Frame supports efficient analysis, structured learning, and practical application of core bioinformatics concepts in educational and research-oriented settings.
    </p>
    <h3>Core Features</h3>
    <ul>
        <li><b>Advanced Translation</b> — Six-frame translation with selectable genetic codes.</li>
        <li><b>ORF Visualization</b> — Interactive mapping of protein-coding regions.</li>
        <li><b>Sequence Alignment</b> — Global & local alignment algorithms.</li>
        <li><b>Protein Analysis</b> — MW, pI, GRAVY, instability index & more.</li>
    </ul>
    <h3>Development Roadmap</h3>
    <ul>
        <li>3D protein structure modeling support.</li>
        <li>Domain & motif prediction modules.</li>
        <li>NCBI BLAST integration.</li>
        <li>AI-assisted functional interpretation.</li>
    </ul>
</div>
""", unsafe_allow_html=True)