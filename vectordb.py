# Install required libraries first:
# pip install chromadb pymupdf sentence-transformers

import os
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import chromadb

# Step 1: Setup

# Path to folder with chapter-wise PDFs
PDF_FOLDER = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\textbooks\grade1\MATHS_joyful-mathematics_grade1"   
DB_DIR = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\vector_db\grade1_maths_db"  # where the ChromaDB database will be saved

# Initialize embedding model
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")  # lightweight & fast

# Initialize ChromaDB (persistent so data is saved)
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="textbook_db")

# Step 2: Text Chunking

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# Step 3: Process PDFs

def process_pdf(pdf_path, subject,grade, chapter_name):
    """Extract text, chunk it, embed, and add to ChromaDB."""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():  # skip empty pages
            full_text += f"\n\nPage {page_num}:\n{text}"

    # Split into chunks
    chunks = chunk_text(full_text)

    # Create embeddings
    embeddings = model.encode(chunks).tolist()

    # Store in ChromaDB with metadata
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i]],
            metadatas=[{
                "subject": subject,
                "grade": grade,
                "chapter": chapter_name,
                "pdf_file": os.path.basename(pdf_path)
            }],
            ids=[f"{chapter_name}_{i}"]
        )

    print(f"Added {len(chunks)} chunks from {chapter_name}")


# Step 4: Loop over PDFs

for filename in os.listdir(PDF_FOLDER):
    if filename.endswith(".pdf"):
        chapter_name = os.path.splitext(filename)[0]
        pdf_path = os.path.join(PDF_FOLDER, filename)
        process_pdf(pdf_path, subject="Maths", grade=1,chapter_name=chapter_name)

print("Vector database built successfully!")
