from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
import chromadb
import fitz 
import os
import re
from PIL import Image
import pytesseract
import io
import docx
from pathlib import Path


app = FastAPI()

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, replace with ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq API Key
API_KEY = "YOUR_API_KEY"
client = Groq(api_key=API_KEY)

# Embeddings for English
embeddings_en = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Embeddings for Gujarati
embeddings_gu = SentenceTransformer("intfloat/multilingual-e5-base")

# Base DB path
BASE_PATH = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\vector_db"

def is_gujarati_text_valid(text):
    """Check if text contains meaningful Gujarati characters"""
    gujarati_chars = re.findall(r'[\u0A80-\u0AFF]', text)
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return False
    
    # At least 10% should be valid Gujarati characters
    gujarati_ratio = len(gujarati_chars) / total_chars
    return gujarati_ratio > 0.1

def clean_ocr_text(text):
    """Basic cleaning of OCR artifacts"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove common OCR artifacts but keep Gujarati characters
    text = re.sub(r'[^\u0A80-\u0AFF\s\w.,!?():-]', '', text)
    return text.strip()

def detect_language(subject: str):
    """Detect if subject is Gujarati based on naming convention"""
    subject_lower = subject.lower()
    return "gujarati" if "gujarati" in subject_lower else "english"

def extract_text_from_pdf(pdf_bytes):
    """Extract text from PDF, use OCR for images if no text is available"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    full_text = ""
    
    for page_num, page in enumerate(doc):
        # Try to extract text directly
        text = page.get_text("text").strip()
        
        # If no text found or very little text, use OCR
        if len(text) < 50:  # Threshold for considering it as image-based
            print(f"Page {page_num + 1}: Using OCR (little/no text found)")
            # Convert page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            
            # Perform OCR with Gujarati + English support
            ocr_text = pytesseract.image_to_string(img, lang='guj+eng')
            full_text += ocr_text + "\n"
        else:
            print(f"Page {page_num + 1}: Using direct text extraction")
            full_text += text + "\n"
    
    return full_text

def extract_text_from_image(image_bytes):
    """Extract text from image using OCR"""
    img = Image.open(io.BytesIO(image_bytes))
    # Use both Gujarati and English for OCR
    text = pytesseract.image_to_string(img, lang='guj+eng')
    return text

def extract_text_from_docx(file_bytes):
    """Extract text from DOCX file"""
    doc = docx.Document(io.BytesIO(file_bytes))
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_txt(file_bytes):
    """Extract text from TXT file with encoding detection"""
    # Try different encodings
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            text = file_bytes.decode(encoding)
            return text
        except (UnicodeDecodeError, AttributeError):
            continue
    
    # If all encodings fail, use utf-8 with errors ignored
    return file_bytes.decode('utf-8', errors='ignore')

def load_subject_db(grade: str, subject: str):
    """Load the Chroma database for the given grade & subject."""
    subject_lower = subject.lower()
    language = detect_language(subject)
    
    # Determine DB path based on language
    if language == "gujarati":
        # For Gujarati subjects, use the specific gujarati DB naming
        if "evs" in subject_lower or "environmental" in subject_lower:
            db_path = os.path.join(BASE_PATH, f"grade{grade}_gujarati_evs_db")
            collection_name = "gujarati_textbook_db"
        elif "maths" in subject_lower:
            db_path = os.path.join(BASE_PATH, f"grade{grade}_gujarati_maths_db")
            collection_name = "gujarati_textbook_db"
        else:
            db_path = os.path.join(BASE_PATH, f"grade{grade}_gujarati_gujarati_db")
            collection_name = "gujarati_textbook_db"
    else:
        # English subjects use the original naming
        if "evs" in subject_lower or "environmental" in subject_lower:
            subject_name = "evs"
        elif "maths" in subject_lower:
            subject_name = "maths"
        else:
            subject_name = "english"
        db_path = os.path.join(BASE_PATH, f"grade{grade}_{subject_name}_db")
        collection_name = "textbook_db"
    
    if not os.path.exists(db_path):
        return None, language
    
    if language == "gujarati":
        # Use ChromaDB client directly for Gujarati
        chroma_client = chromadb.PersistentClient(path=db_path)
        collection = chroma_client.get_or_create_collection(name=collection_name)
        return collection, language
    else:
        # Use LangChain wrapper for English
        return Chroma(
            persist_directory=db_path,
            collection_name=collection_name,
            embedding_function=embeddings_en,
        ), language

def retrieve_gujarati_chunks(collection, query, n_results=5):
    """Retrieve relevant chunks for Gujarati text"""
    query_embedding = embeddings_gu.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    documents = results["documents"][0]
    distances = results["distances"][0]
    
    # Filter and clean documents
    valid_docs = []
    for doc, dist in zip(documents, distances):
        cleaned = clean_ocr_text(doc)
        if is_gujarati_text_valid(cleaned) and dist < 1.5:
            valid_docs.append(cleaned)
    
    return valid_docs

def process_uploaded_file(file: UploadFile, grade: str, subject: str):
    """Extract text from uploaded file and create temporary Chroma collection."""
    client_db = chromadb.EphemeralClient()
    collection_name = f"user_upload_{grade}_{subject}"
    collection = client_db.get_or_create_collection(name=collection_name)
    
    file_bytes = file.file.read()
    filename_lower = file.filename.lower()
    
    print(f"Processing file: {file.filename}")
    
    # Extract text based on file type
    if filename_lower.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
        text = extract_text_from_image(file_bytes)
    elif filename_lower.endswith(".docx"):
        text = extract_text_from_docx(file_bytes)
    elif filename_lower.endswith(".txt"):
        text = extract_text_from_txt(file_bytes)
    else:
        print(f"Unsupported file type: {file.filename}")
        return collection
    
    print(f"Extracted text length: {len(text)} characters")
    
    # Check if text is valid
    if not text or len(text.strip()) < 10:
        print("Warning: Very little or no text extracted!")
        return collection
    
    # Chunk into ~500 chars with overlap
    chunk_size = 500
    overlap = 50
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    
    print(f"Created {len(chunks)} chunks")
    
    # Detect language and use appropriate embeddings
    language = detect_language(subject)
    
    if language == "gujarati":
        # Use Gujarati embeddings
        vectors = embeddings_gu.encode(chunks).tolist()
    else:
        # Use English embeddings
        vectors = embeddings_en.embed_documents(chunks)
    
    # Add to collection
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[vectors[i]],
            ids=[f"{collection_name}_chunk_{i}"],
        )
    
    print(f"Added {len(chunks)} chunks to collection")
    return collection

@app.post("/ask")
async def ask(
    message: str = Form(...),
    grade: str = Form(...),
    subject: str = Form(...),
    file: UploadFile | None = None,
):
    print(f"\n=== New Query ===")
    print(f"Grade: {grade}, Subject: {subject}")
    print(f"Message: {message}")
    print(f"File uploaded: {file.filename if file else 'None'}")
    
    # 1. Load subject DB
    subject_db, language = load_subject_db(grade, subject)
    context = ""

    if subject_db:
        print(f"Language detected: {language}")
        if language == "gujarati":
            # Use Gujarati-specific retrieval
            docs = retrieve_gujarati_chunks(subject_db, message, n_results=5)
            if docs:
                context += "\n\n".join(docs)
                print(f"Retrieved {len(docs)} Gujarati chunks from textbook DB")
        else:
            # Use English retrieval
            docs = subject_db.similarity_search(message, k=3)
            if docs:
                context += "\n".join([d.page_content for d in docs])
                print(f"Retrieved {len(docs)} English chunks from textbook DB")

    # 2. If file uploaded, also search it
    upload_context = ""
    if file:
        print("Processing uploaded file...")
        upload_collection = process_uploaded_file(file, grade, subject)
        
        # Query the uploaded file collection
        if language == "gujarati":
            # Use Gujarati embeddings for query
            query_embedding = embeddings_gu.encode([message]).tolist()[0]
            results = upload_collection.query(query_embeddings=[query_embedding], n_results=3)
        else:
            # Use English embeddings for query
            results = upload_collection.query(query_texts=[message], n_results=3)
        
        if results["documents"] and results["documents"][0]:
            upload_docs = results["documents"][0]
            
            # For Gujarati, filter and clean the documents
            if language == "gujarati":
                valid_upload_docs = []
                for doc in upload_docs:
                    cleaned = clean_ocr_text(doc)
                    if is_gujarati_text_valid(cleaned):
                        valid_upload_docs.append(cleaned)
                if valid_upload_docs:
                    upload_context = "\n\n".join(valid_upload_docs)
                    print(f"Retrieved {len(valid_upload_docs)} valid Gujarati chunks from uploaded file")
            else:
                upload_context = "\n\n".join(upload_docs)
                print(f"Retrieved {len(upload_docs)} chunks from uploaded file")
            
            if upload_context:
                context += "\n\n" + upload_context

    print(f"Total context length: {len(context)} characters")

    # 3. Guardrail: no context found
    if not context.strip():
        print("No context found!")
        if language == "gujarati":
            return {
                "answer": "માફ કરશો, મને તમારી પાઠ્યપુસ્તક અથવા અપલોડ કરેલી સામગ્રીમાં આ માહિતી મળી નથી. (Sorry, I couldn't find this information in your textbook or uploaded material.)"
            }
        else:
            return {
                "answer": "Sorry, I couldn't find this in your textbook or uploaded material."
            }

    # 4. Query Groq with language-specific prompts
    if language == "gujarati":
        system_prompt = """You are a kind Gujarati teacher for primary school students.

CRITICAL RULES:
1. You MUST answer ONLY using the provided textbook context.
2. If the context is corrupted, unclear, or doesn't contain the answer, respond: "માફ કરશો, મને આ પ્રશ્નનો જવાબ પાઠ્યપુસ્તકમાં સ્પષ્ટ રીતે મળ્યો નથી."
3. Always respond in Gujarati (ગુજરાતી ભાષામાં)
4. Keep answers simple and detailed for primary students
5. Do NOT use your general knowledge - ONLY the textbook context
6. Provide complete, comprehensive answers but keep it as simple as possible, easy to understand for a child aged 5-8 years of age

If the context below is unreadable or doesn't answer the question, you MUST say so."""

        user_prompt = f"""પાઠ્યપુસ્તક અને અપલોડ કરેલી સામગ્રીમાંથી સંદર્ભ (Context from Textbook and Uploaded Material):
{context}

પ્રશ્ન (Question): {message}

કૃપા કરીને વિગતવાર જવાબ આપો (Please provide a detailed answer):"""
    else:
        system_prompt = """You are a kind teacher for primary school students of India. Synthesize and rephrase the provided context to answer the user's question in a simple, clear, and comprehensive manner. Do not copy sentences verbatim. Provide complete, detailed answers but keep them simple and easy to understand for children of age 5-8 years. If the answer cannot be found in the provided context, politely say: 'Sorry, I couldn't find this in your textbook or uploaded material.'"""
        
        user_prompt = f"Context from textbook and uploaded material:\n{context}\n\nQuestion: {message}\n\nPlease provide a detailed answer:"

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0 if language == "gujarati" else 0,
        top_p=0.9
    )

    answer = completion.choices[0].message.content
    print(f"Generated answer length: {len(answer)} characters")
    return {"answer": answer}