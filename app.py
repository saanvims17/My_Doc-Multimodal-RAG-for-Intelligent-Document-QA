import json
import tempfile
import os
import streamlit as st

# ── Import all RAG logic from the separate module ──────────────────────────
from my_doc_new import (
    partition_document,
    create_chunks_by_title,
    separate_content_types,
    create_ai_enhanced_summary,
    create_vector_store,
    retrieve,
    generate_final_answer,
)


# PAGE CONFIG ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MyDOC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');

/* global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f7f7f5;
    color: #1a1a1a;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1.5px solid #ebebea;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.6rem 1.25rem 1rem !important;
}

/* brand */
.brand-title {
    font-size: 1.55rem;
    font-weight: 700;
    letter-spacing: -0.6px;
    color: #111;
    line-height: 1;
}
.brand-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    color: #999;
    margin-top: 3px;
    letter-spacing: 0.03em;
}

/* section labels */
.sb-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    color: #bbb;
    text-transform: uppercase;
    margin: 1.4rem 0 0.5rem 0;
}

/* engine card */
.engine-card {
    background: #fafaf8;
    border: 1px solid #ebebea;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
}
.engine-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #22c55e;
    flex-shrink: 0;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.15);
}
.engine-name  { font-weight: 600; font-size: 0.88rem; color: #111; }
.engine-models {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem; color: #999; margin-top: 1px;
}

/* filename */
.file-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    color: #3b82f6;
    word-break: break-all;
    margin: 0.3rem 0 0 0;
}

/* process log */
.proc-log {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    line-height: 1.75;
    color: #555;
    background: #fafaf8;
    border: 1px solid #ebebea;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-top: 0.6rem;
}
.log-ok   { color: #16a34a; font-weight: 600; }
.log-info { color: #3b82f6; font-weight: 500; }

/* index stats */
.idx-grid {
    display: flex; gap: 0.5rem; margin-top: 0.5rem;
}
.idx-cell {
    flex: 1;
    background: #fafaf8;
    border: 1px solid #ebebea;
    border-radius: 8px;
    text-align: center;
    padding: 0.6rem 0.25rem;
}
.idx-num {
    display: block;
    font-size: 1.35rem;
    font-weight: 700;
    color: #3b82f6;
    line-height: 1.1;
}
.idx-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.57rem;
    color: #bbb;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* buttons */
div[data-testid="stButton"] button {
    width: 100% !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.52rem 1rem !important;
    border: 1px solid #ddd !important;
    background: #f4f4f2 !important;
    color: #555 !important;
    transition: background 0.15s !important;
}
div[data-testid="stButton"] button:hover {
    background: #e8e8e6 !important;
    color: #222 !important;
}

/* ── main header bar ── */
.main-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 0 0.6rem 0;
    border-bottom: 1px solid #e8e8e4;
    margin-bottom: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #999;
}
.main-bar .doc-name { color: #444; }
.tag-row { margin-left: auto; display: flex; gap: 0.4rem; }
.tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    background: #f0f0ee;
    border: 1px solid #e0e0de;
    border-radius: 20px;
    padding: 0.18rem 0.6rem;
    color: #777;
}
.tag.on { background: #111; color: #fff; border-color: #111; }

/* ── chat messages ── */
.u-row { display: flex; justify-content: flex-end; margin-bottom: 1rem; }
.u-bubble {
    background: #2563eb;
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.15rem;
    max-width: 70%;
    font-size: 0.875rem;
    line-height: 1.55;
}

.a-row { display: flex; justify-content: flex-start; margin-bottom: 0.4rem; }
.a-inner { max-width: 82%; }
.a-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #bbb;
    letter-spacing: 0.07em;
    margin-bottom: 0.3rem;
}
.a-bubble {
    background: #fff;
    border: 1px solid #e8e8e4;
    border-radius: 4px 18px 18px 18px;
    padding: 1rem 1.25rem;
    font-size: 0.875rem;
    line-height: 1.65;
    color: #1a1a1a;
    white-space: pre-wrap;
}

/* ── sources ── */
.src-card {
    background: #fff;
    border: 1px solid #ebebea;
    border-radius: 8px;
    padding: 0.7rem 0.95rem;
    margin-bottom: 0.4rem;
    font-size: 0.775rem;
    line-height: 1.55;
    color: #444;
}
.src-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.57rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-radius: 4px;
    padding: 0.13rem 0.45rem;
    margin-bottom: 0.3rem;
}
.b-text  { background:#eff6ff; color:#3b82f6; border:1px solid #bfdbfe; }
.b-table { background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; }
.b-image { background:#fffbeb; color:#d97706; border:1px solid #fde68a; }

/* empty state */
.empty {
    text-align: center;
    padding: 5rem 1rem 2rem;
    font-family: 'JetBrains Mono', monospace;
    color: #ccc;
    font-size: 0.8rem;
}
.empty-icon { font-size: 2.8rem; opacity: 0.3; margin-bottom: 0.9rem; }

/* hint */
.hint {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #ccc;
    text-align: center;
    margin-top: 0.3rem;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# SESSION STATE INIT ─────────────────────────────────────────────────────────────────────────────
if "db"           not in st.session_state: st.session_state.db           = None
if "messages"     not in st.session_state: st.session_state.messages     = []
if "proc_log"     not in st.session_state: st.session_state.proc_log     = []
if "index_stats"  not in st.session_state: st.session_state.index_stats  = {"text": 0, "tables": 0, "images": 0}
if "pdf_name"     not in st.session_state: st.session_state.pdf_name     = None
if "processed"    not in st.session_state: st.session_state.processed    = False


# HELPERS ─────────────────────────────────────────────────────────────────────────────
def get_source_type(chunk) -> str:
    try:
        original = json.loads(chunk.metadata.get("original_content", "{}"))
        types = original.get("types", ["text"])
        if "image" in types:
            return "image"
        if "table" in types:
            return "table"
    except Exception:
        pass
    return "text"


def render_log(lines: list) -> str:
    html = "<div class='proc-log'>"
    for line in lines:
        if "✅" in line or "Ready" in line:
            html += f"<div class='log-ok'>{line}</div>"
        elif "❌" in line:
            html += f"<div style='color:#dc2626;font-weight:600'>{line}</div>"
        else:
            html += f"<div>{line}</div>"
    html += "</div>"
    return html


def summarise_chunks_with_counts(chunks):
    """
    Same logic as summarise_chunks() in my_doc_rag, but also
    returns (text_count, table_count, image_count) for the index panel.
    """
    from langchain_core.documents import Document

    docs = []
    text_count = table_count = image_count = 0

    for chunk in chunks:
        content = separate_content_types(chunk)
        text_count += 1
        if "table" in content["types"]:
            table_count += 1
        if "image" in content["types"]:
            image_count += 1

        if content["tables"] or content["images"]:
            enhanced = create_ai_enhanced_summary(
                content["text"], content["tables"], content["images"]
            )
        else:
            enhanced = content["text"]

        doc = Document(
            page_content=enhanced,
            metadata={
                "original_content": json.dumps({
                    "raw_text":       content["text"],
                    "tables_html":    content["tables"],
                    "images_base64":  content["images"],
                    "types":          content["types"],
                })
            },
        )
        docs.append(doc)

    return docs, text_count, table_count, image_count


# SIDEBAR ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:1.5rem'>
        <div class='brand-title'>MyDOC</div>
        <div class='brand-sub'>document intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-label'>AI Engine</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='engine-card'>
        <div class='engine-dot'></div>
        <div>
            <div class='engine-name'>OpenAI</div>
            <div class='engine-models'>gpt-4o &nbsp;·&nbsp; text-embedding-3-small</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sb-label'>Document</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "", type=["pdf"], label_visibility="collapsed", key="pdf_uploader"
    )

    if uploaded_file:
        st.markdown(
            f"<div class='file-badge'>📄 {uploaded_file.name[:44]}{'…' if len(uploaded_file.name) > 44 else ''}</div>",
            unsafe_allow_html=True,
        )

    process_clicked = st.button(
        "Process Document",
        disabled=(uploaded_file is None or st.session_state.processed),
    )

    # Log slot — renders during AND after processing
    log_slot = st.empty()
    if st.session_state.proc_log:
        log_slot.markdown(render_log(st.session_state.proc_log), unsafe_allow_html=True)

    # Index stats (shown once processed)
    if st.session_state.processed:
        s = st.session_state.index_stats
        st.markdown("<div class='sb-label'>Index</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='idx-grid'>
            <div class='idx-cell'>
                <span class='idx-num'>{s['text']}</span>
                <span class='idx-lbl'>Text</span>
            </div>
            <div class='idx-cell'>
                <span class='idx-num'>{s['tables']}</span>
                <span class='idx-lbl'>Tables</span>
            </div>
            <div class='idx-cell'>
                <span class='idx-num'>{s['images']}</span>
                <span class='idx-lbl'>Images</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("Clear session", key="clear_btn"):
        st.session_state.db          = None
        st.session_state.messages    = []
        st.session_state.proc_log    = []
        st.session_state.index_stats = {"text": 0, "tables": 0, "images": 0}
        st.session_state.pdf_name    = None
        st.session_state.processed   = False
        st.rerun()


# PROCESS DOCUMENT ─────────────────────────────────────────────────────────────────────────────
# One straight execution — zero mid-pipeline st.rerun() calls

if process_clicked and uploaded_file and not st.session_state.processed:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.session_state.pdf_name  = uploaded_file.name
    st.session_state.proc_log  = []

    def _log(line: str):
        st.session_state.proc_log.append(line)
        log_slot.markdown(render_log(st.session_state.proc_log), unsafe_allow_html=True)

    try:
        _log("⏳ Partitioning document...")
        elements = partition_document(tmp_path)
        _log(f"✅ Extracted {len(elements)} elements")

        _log("🧩 Chunking by title...")
        chunks = create_chunks_by_title(elements)
        _log(f"✅ Created {len(chunks)} chunks")

        _log("⚙️ Summarising tables & images...")
        docs, t, tbl, img = summarise_chunks_with_counts(chunks)
        _log(f"✅ {t} text · {tbl} tables · {img} images")

        _log("🧠 Embedding & building vector store...")
        db = create_vector_store(docs)
        _log("✅ Ready to answer questions.")

        st.session_state.db          = db
        st.session_state.index_stats = {"text": t, "tables": tbl, "images": img}
        st.session_state.processed   = True

    except Exception as e:
        _log(f"❌ Error: {e}")

    finally:
        os.unlink(tmp_path)

    st.rerun()

# MAIN CHAT AREA ─────────────────────────────────────────────────────────────────────────────
fname = st.session_state.pdf_name or ""
st.markdown(f"""
<div class='main-bar'>
    <span>📄</span>
    <span class='doc-name'>{'Reading — ' + fname if fname else 'No document loaded'}</span>
    <div class='tag-row'>
        <span class='tag'>gpt-4o</span>
        <span class='tag on'>text-emb-3-small</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat history ─────────────────────────────────────────────────────────────────────────────
with st.container():
    if not st.session_state.messages:
        icon = "💬" if st.session_state.processed else "📄"
        txt  = "Document ready — ask your first question" if st.session_state.processed \
               else "Upload and process a PDF to begin"
        st.markdown(f"""
        <div class='empty'>
            <div class='empty-icon'>{icon}</div>
            <div>{txt}</div>
        </div>""", unsafe_allow_html=True)

    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f"""
            <div class='u-row'>
                <div class='u-bubble'>{m['content']}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='a-row'>
                <div class='a-inner'>
                    <div class='a-lbl'>MYDOC</div>
                    <div class='a-bubble'>{m['content']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            sources = m.get("sources", [])
            if sources:
                with st.expander(f"▾  {len(sources)} sources", expanded=False):
                    for src in sources:
                        badge_map = {"text": "b-text", "table": "b-table", "image": "b-image"}
                        bc      = badge_map.get(src["type"], "b-text")
                        preview = src["preview"][:240] + ("…" if len(src["preview"]) > 240 else "")
                        st.markdown(f"""
                        <div class='src-card'>
                            <span class='src-badge {bc}'>{src['type']}</span><br>{preview}
                        </div>""", unsafe_allow_html=True)

# Chat input ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

if prompt := st.chat_input(
    "Ask a question about your document…",
    disabled=not st.session_state.processed,
):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking…"):
        retrieved = retrieve(st.session_state.db, prompt)
        answer    = generate_final_answer(retrieved, prompt)

    source_cards = []
    for c in retrieved:
        stype = get_source_type(c)
        try:
            orig    = json.loads(c.metadata.get("original_content", "{}"))
            preview = orig.get("raw_text", c.page_content)
        except Exception:
            preview = c.page_content
        source_cards.append({"type": stype, "preview": preview})

    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": source_cards,
    })
    st.rerun()

st.markdown(
    "<div class='hint'>RETURN to send &nbsp;·&nbsp; SHIFT+RETURN for new line</div>",
    unsafe_allow_html=True,
)