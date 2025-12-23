"""
Translation Engine
Part of The Reading Frame bioinformatics suite

Convert DNA to Protein using multiple genetic codes, detect ORFs, and analyze translations
"""

import streamlit as st
from Bio import SeqIO, Entrez
from Bio.Seq import Seq
import io
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DEFAULT_EMAIL = os.getenv("NCBI_EMAIL", "user@example.com")

# Initialize session state
if 'fetched_sequence' not in st.session_state:
    st.session_state.fetched_sequence = ""
if 'fetch_success' not in st.session_state:
    st.session_state.fetch_success = False

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Translation Engine",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Center container */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a7b 100%);
        border: 1px solid #00E5FF;
        border-radius: 12px;
        padding: 20px 30px;
        margin: 20px 0 30px 0;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.15);
    }
    
    .info-box p {
        color: #e0e0e0;
        font-size: 1.05rem;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.8rem;
        font-weight: 600;
        color: #ffffff;
        margin: 30px 0 20px 0;
    }
    
    .section-icon {
        font-size: 2rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1a1a1a;
        border-radius: 8px;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="color: #00E5FF; font-size: 3rem; margin-bottom: 10px;">
        🧬 Translation Engine
    </h1>
</div>
""", unsafe_allow_html=True)

# ---------------- INFO BOX ----------------
st.markdown("""
<div class="info-box">
    <p>
        💡 Convert DNA → Protein using multiple genetic codes. Detect Open Reading Frames (ORFs), 
        fetch sequences from NCBI, view 6-frame translation, and download protein FASTA output.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURES EXPANDER ----------------
with st.expander("✨ Features"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **Six-Frame Translation**: Analyze all possible reading frames
        - **Multiple Genetic Codes**: Standard, Mitochondrial, Bacterial, etc.
        - **ORF Detection**: Automatically identify protein-coding regions
        """)
    with col2:
        st.markdown("""
        - **NCBI Integration**: Fetch sequences directly by accession
        - **FASTA Support**: Upload or paste sequences
        - **Visual Frame Display**: Color-coded translation views
        """)

# ---------------- MAIN CONTENT ----------------
col_left, col_right = st.columns([1.5, 1])

# ---------------- LEFT COLUMN: INPUT ----------------
with col_left:
    st.markdown('<div class="section-header"><span class="section-icon">📥</span> Input Sequences</div>', unsafe_allow_html=True)
    
    # Text input with session state
    st.markdown("**Paste DNA sequence:**")
    
    # Check if we have a fetched sequence
    if st.session_state.fetched_sequence:
        sequence_text = st.text_area(
            "Paste DNA sequence:",
            value=st.session_state.fetched_sequence,
            height=200,
            placeholder="Paste raw DNA or FASTA ...",
            label_visibility="collapsed",
            key="dna_input_fetched"
        )
    else:
        sequence_text = st.text_area(
            "Paste DNA sequence:",
            value="",
            height=200,
            placeholder="Paste raw DNA or FASTA ...",
            label_visibility="collapsed",
            key="dna_input_normal"
        )
    
    # Sample DNA
    sample_dna = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"
    st.markdown(f"**Sample DNA:** `{sample_dna}`")
    if st.button("Load Sample"):
        st.session_state.fetched_sequence = sample_dna
        st.session_state.fetch_success = False
        st.rerun()
    
    # File upload
    st.markdown("**Or upload FASTA/TXT:**")
    uploaded_file = st.file_uploader(
        "Upload file",
        type=["fa", "fasta", "txt"],
        label_visibility="collapsed"
    )
    
    # NCBI fetch option
    st.markdown("**Or fetch from NCBI:**")
    ncbi_id = st.text_input(
        "Enter NCBI Accession ID (e.g., NM_000546)",
        placeholder="Enter accession ID...",
        key="ncbi_accession"
    )
    
    if st.button("🔍 Fetch from NCBI", type="primary"):
        if not ncbi_id.strip():
            st.error("⚠️ Please enter an accession ID.")
        else:
            with st.spinner("Fetching from NCBI..."):
                try:
                    Entrez.email = DEFAULT_EMAIL
                    handle = Entrez.efetch(
                        db="nucleotide",
                        id=ncbi_id.strip(),
                        rettype="fasta",
                        retmode="text"
                    )
                    fetched = handle.read()
                    handle.close()
                    
                    # Store in session state
                    st.session_state.fetched_sequence = fetched
                    st.session_state.fetch_success = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ NCBI fetch failed: {str(e)}")
                    st.info("💡 Check your accession ID and internet connection.")
    
    if st.session_state.fetch_success:
        st.success("✅ Sequence fetched successfully from NCBI!")
        if st.button("Clear fetched sequence"):
            st.session_state.fetched_sequence = ""
            st.session_state.fetch_success = False
            st.rerun()

# ---------------- RIGHT COLUMN: OPTIONS ----------------
with col_right:
    st.markdown('<div class="section-header"><span class="section-icon">⚙️</span> Options</div>', unsafe_allow_html=True)
    
    # Genetic code selection
    st.markdown("**Genetic code**")
    genetic_code_map = {
        "Standard": 1,
        "Vertebrate Mitochondrial": 2,
        "Yeast Mitochondrial": 3,
        "Bacterial": 11,
        "Alternative Yeast Nuclear": 12
    }
    genetic_code_name = st.selectbox(
        "Genetic code",
        options=list(genetic_code_map.keys()),
        label_visibility="collapsed"
    )
    genetic_code = genetic_code_map[genetic_code_name]
    
    # Visualization options
    st.markdown("**Display options**")
    show_viz = st.checkbox("Show visualizations", value=True)
    show_reverse = st.checkbox("Show reverse complement", value=False)
    translate_reverse = st.checkbox("Translate reverse frames", value=True)
    stop_at_first = st.checkbox("Stop at first stop codon", value=False)
    
    # ORF settings
    st.markdown("**ORF detection**")
    min_orf_length = st.number_input(
        "Min ORF AA length",
        min_value=10,
        max_value=1000,
        value=30,
        step=10
    )
    
    show_protein_props = st.checkbox("Show protein properties", value=False)

# ---------------- HELPER FUNCTIONS ----------------
def clean_dna_sequence(seq):
    """Clean and validate DNA sequence"""
    seq = seq.upper().replace("\n", "").replace(" ", "").replace("\r", "")
    seq = re.sub(r'[^ATGCN]', '', seq)
    return seq

def extract_sequence(text, uploaded):
    """Extract sequence from text or file"""
    if uploaded:
        data = uploaded.read().decode("utf-8")
        if data.startswith(">"):
            records = list(SeqIO.parse(io.StringIO(data), "fasta"))
            return str(records[0].seq) if records else ""
        return clean_dna_sequence(data)
    
    if text.strip().startswith(">"):
        records = list(SeqIO.parse(io.StringIO(text), "fasta"))
        return str(records[0].seq) if records else ""
    
    return clean_dna_sequence(text)

def find_orfs(sequence, genetic_code, min_length):
    """Find all ORFs in sequence"""
    seq_obj = Seq(sequence)
    orfs = []
    
    # Search all 3 forward frames
    for frame in range(3):
        frame_seq = seq_obj[frame:]
        frame_seq = frame_seq[:len(frame_seq) - (len(frame_seq) % 3)]
        
        translated = str(frame_seq.translate(table=genetic_code))
        
        # Find ORFs (from M to *)
        pattern = r'M[^*]*'
        for match in re.finditer(pattern, translated):
            orf_protein = match.group()
            if len(orf_protein) >= min_length:
                start_nt = frame + match.start() * 3
                end_nt = frame + match.end() * 3
                orfs.append({
                    'frame': f'+{frame + 1}',
                    'start': start_nt,
                    'end': end_nt,
                    'length_aa': len(orf_protein),
                    'sequence': orf_protein
                })
    
    return orfs

# ---------------- PROCESS SEQUENCE ----------------
sequence = extract_sequence(sequence_text, uploaded_file)

if not sequence:
    st.info("👆 Add DNA, upload FASTA, or fetch from NCBI to begin.")
    st.stop()

if len(sequence) < 3:
    st.error("Sequence too short for translation (minimum 3 nucleotides).")
    st.stop()

# Create sequence object
seq_obj = Seq(sequence)

# ---------------- RUN BUTTON ----------------
st.markdown("---")
if st.button("🧬 Translate Sequence", type="primary", use_container_width=True):
    
    # ---------------- SEQUENCE INFO ----------------
    st.markdown("---")
    st.markdown("## 📊 Sequence Information")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Length", f"{len(sequence)} nt")
    col2.metric("GC Content", f"{((sequence.count('G') + sequence.count('C')) / len(sequence) * 100):.1f}%")
    col3.metric("Genetic Code", genetic_code_name)
    col4.metric("Reading Frames", "6" if translate_reverse else "3")
    
    # Show reverse complement if requested
    if show_reverse:
        st.markdown("### Reverse Complement")
        rev_comp = str(seq_obj.reverse_complement())
        st.code(rev_comp, language="text")
    
    # ---------------- 6-FRAME TRANSLATION ----------------
    st.markdown("---")
    st.markdown("## 🔬 Six-Frame Translation")
    
    frames_data = []
    
    # Forward frames
    for frame in range(3):
        frame_seq = seq_obj[frame:]
        # Make length multiple of 3
        frame_seq = frame_seq[:len(frame_seq) - (len(frame_seq) % 3)]
        translated = str(frame_seq.translate(table=genetic_code, to_stop=stop_at_first))
        frames_data.append((f"Frame +{frame + 1}", translated))
    
    # Reverse frames
    if translate_reverse:
        rev_seq = seq_obj.reverse_complement()
        for frame in range(3):
            frame_seq = rev_seq[frame:]
            frame_seq = frame_seq[:len(frame_seq) - (len(frame_seq) % 3)]
            translated = str(frame_seq.translate(table=genetic_code, to_stop=stop_at_first))
            frames_data.append((f"Frame -{frame + 1}", translated))
    
    # Display frames
    for frame_name, protein in frames_data:
        with st.expander(f"{frame_name} ({len(protein)} aa)", expanded=False):
            st.code(protein, language="text")
    
    # ---------------- ORF DETECTION ----------------
    st.markdown("---")
    st.markdown("## 🎯 Open Reading Frames (ORFs)")
    
    orfs = find_orfs(sequence, genetic_code, min_orf_length)
    
    if orfs:
        st.success(f"Found {len(orfs)} ORF(s) ≥ {min_orf_length} amino acids")
        
        for i, orf in enumerate(orfs, 1):
            with st.expander(f"ORF #{i} | Frame {orf['frame']} | Position {orf['start']}-{orf['end']} | {orf['length_aa']} aa"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Frame", orf['frame'])
                    st.metric("Start", orf['start'])
                    st.metric("End", orf['end'])
                    st.metric("Length", f"{orf['length_aa']} aa")
                
                with col2:
                    st.markdown("**Protein Sequence:**")
                    st.code(orf['sequence'], language="text")
                    
                    # Download button for individual ORF
                    fasta_orf = f">ORF_{i}_{orf['frame']}_pos_{orf['start']}-{orf['end']}\n{orf['sequence']}"
                    st.download_button(
                        f"Download ORF #{i} (FASTA)",
                        fasta_orf,
                        file_name=f"orf_{i}.fasta",
                        mime="text/plain"
                    )
    else:
        st.info(f"No ORFs found with minimum length of {min_orf_length} amino acids.")
    
    # ---------------- EXPORT OPTIONS ----------------
    st.markdown("---")
    st.markdown("## 💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download all translations
        all_translations = ""
        for frame_name, protein in frames_data:
            all_translations += f">{frame_name}\n{protein}\n\n"
        
        st.download_button(
            "Download All Frames (FASTA)",
            all_translations,
            file_name="translations_all_frames.fasta",
            mime="text/plain"
        )
    
    with col2:
        # Download all ORFs
        if orfs:
            all_orfs = ""
            for i, orf in enumerate(orfs, 1):
                all_orfs += f">ORF_{i}_{orf['frame']}_pos_{orf['start']}-{orf['end']}\n{orf['sequence']}\n\n"
            
            st.download_button(
                "Download All ORFs (FASTA)",
                all_orfs,
                file_name="orfs_all.fasta",
                mime="text/plain"
            )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#777;'>"
    "Part of The Reading Frame • Bioinformatics Toolkit"
    "</p>",
    unsafe_allow_html=True
)