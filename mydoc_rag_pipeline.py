import json
from typing import List
from dotenv import load_dotenv

# Unstructured
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

# LangChain
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage

# OpenAI eval
from openai import OpenAI

load_dotenv()


# STEP 1: PDF PARTITIONING

def partition_document(file_path: str):
    print(f"📄 Partitioning document: {file_path}")

    elements = partition_pdf(
        filename=file_path,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )

    print(f"✅ Extracted {len(elements)} elements")
    return elements



# STEP 2: CHUNKING

def create_chunks_by_title(elements):
    print("🧩 Creating smart chunks...")

    chunks = chunk_by_title(
        elements,
        max_characters=3000,
        new_after_n_chars=2400,
        combine_text_under_n_chars=500
    )

    print(f"✅ Created {len(chunks)} chunks")
    return chunks



# STEP 3: CONTENT PROCESSING

def separate_content_types(chunk):
    content_data = {
        'text': chunk.text,
        'tables': [],
        'images': [],
        'types': ['text']
    }

    if hasattr(chunk, 'metadata') and hasattr(chunk.metadata, 'orig_elements'):
        for element in chunk.metadata.orig_elements:
            element_type = type(element).__name__

            if element_type == 'Table':
                content_data['types'].append('table')
                table_html = getattr(element.metadata, 'text_as_html', element.text)
                content_data['tables'].append(table_html)

            elif element_type == 'Image':
                if hasattr(element.metadata, 'image_base64'):
                    content_data['types'].append('image')
                    content_data['images'].append(element.metadata.image_base64)

    content_data['types'] = list(set(content_data['types']))
    return content_data


def create_ai_enhanced_summary(text: str, tables: List[str], images: List[str]) -> str:
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        prompt_text = f"""
You are creating a searchable description for document retrieval.
CRITICAL: Preserve ALL numbers, percentages, model dimensions,
hyperparameters, and named values exactly as they appear in the source.

TEXT:
{text}
"""

        if tables:
            prompt_text += "TABLES:\n"
            for i, table in enumerate(tables):
                prompt_text += f"Table {i+1}:\n{table}\n\n"

        message = HumanMessage(content=[{"type": "text", "text": prompt_text}])
        response = llm.invoke([message])

        return response.content

    except Exception as e:
        print(f"⚠️ AI summary failed: {e}")
        return text[:300]


def summarise_chunks(chunks):
    print("⚙️ Processing chunks...")

    docs = []
    for chunk in chunks:
        content = separate_content_types(chunk)

        # AI summary used for embedding/search; raw_text preserved in metadata for answer generation
        if content['tables'] or content['images']:
            enhanced = create_ai_enhanced_summary(
                content['text'],
                content['tables'],
                content['images']
            )
        else:
            enhanced = content['text']

        doc = Document(
            page_content=enhanced,          # searched by embeddings
            metadata={
                "original_content": json.dumps({
                    "raw_text": content['text'],    # used for answer generation
                    "tables_html": content['tables'],
                    "images_base64": content['images']
                })
            }
        )

        docs.append(doc)

    return docs



# STEP 4: VECTOR STORE

def create_vector_store(documents):
    print("🧠 Creating vector store...")

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    db = Chroma.from_documents(documents, embedding_model)
    return db



# STEP 5: RETRIEVAL

def retrieve(db: Chroma, query: str, k: int = 6):
    return db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "fetch_k": 20}
    ).invoke(query)



# STEP 6: ANSWER

def generate_final_answer(chunks, query):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    context_parts = []
    for c in chunks:
        original = json.loads(c.metadata.get("original_content", "{}"))
        raw = original.get("raw_text", c.page_content)   # prefer raw_text, fallback to summary
        context_parts.append(raw)

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
Answer ONLY using this context:

{context}

Question: {query}
"""

    return llm.invoke([HumanMessage(content=prompt)]).content



# STEP 7: PIPELINE

def run_complete_ingestion_pipeline(pdf_path):
    elements = partition_document(pdf_path)
    chunks = create_chunks_by_title(elements)
    docs = summarise_chunks(chunks)
    db = create_vector_store(docs)
    return db


# MAIN

if __name__ == "__main__":

    pdf_path = input("📄 Enter PDF path: ").strip()

    print("\n⏳ Processing document...\n")
    db = run_complete_ingestion_pipeline(pdf_path)

    print("\n✅ Ready! Ask questions.\n")

    while True:
        query = input("💬 Ask: ")

        if query.lower() == "exit":
            break

        chunks = retrieve(db, query)
        answer = generate_final_answer(chunks, query)

        print("\n💡 ANSWER:\n", answer)