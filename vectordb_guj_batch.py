# vectordb_guj_batch.py - Batch process multiple textbooks into separate databases
import os
from pdf2image import convert_from_path
import pytesseract
from sentence_transformers import SentenceTransformer
import chromadb
from PIL import Image
import cv2
import numpy as np
from pathlib import Path

# -------- CONFIG --------
# Base directory for vector databases
VECTOR_DB_BASE_DIR = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\vector_db"
TEXTBOOK_BASE_DIR = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\textbooks\gujarati"

POPPLER_PATH = r"C:\Program Files\poppler-25.07.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define your textbooks to process
TEXTBOOKS = [
    {
        "path": r"C:\Users\HP\Desktop\uni\seventh_sem\rms\textbooks\gujarati\grade1\GUJARATI_maths_grade1.pdf",
        "subject": "Maths",
        "grade": 1,
        "language": "gujarati"
    },
    {
        "path": r"C:\Users\HP\Desktop\uni\seventh_sem\rms\textbooks\gujarati\grade1\GUJARATI_gujarati_grade1.pdf",
        "subject": "Gujarati",
        "grade": 1,
        "language": "gujarati"
    },
    # Add more textbooks here as needed
]

# Collection name (same for all databases)
COLLECTION_NAME = "gujarati_textbook_db"

# Initialize embedding model (shared across all processing)
model = SentenceTransformer("intfloat/multilingual-e5-base")

# -------- IMAGE PREPROCESSING --------
def preprocess_image(pil_image):
    """Enhance image quality for better OCR"""
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(denoised)
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)

# -------- TEXT CHUNKING --------
def chunk_text(text, chunk_size=400, overlap=50):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# -------- DATABASE NAME GENERATOR --------
def get_database_path(grade, language, subject):
    """Generate database directory path based on grade, language, and subject"""
    # Clean subject name for directory (remove spaces, lowercase)
    subject_clean = subject.lower().replace(" ", "_").replace("-", "_")
    
    # Create database name: grade{X}_{language}_{subject}_db
    db_name = f"grade{grade}_{language}_{subject_clean}_db"
    db_path = os.path.join(VECTOR_DB_BASE_DIR, db_name)
    
    return db_path

# -------- CHECK IF FILE ALREADY PROCESSED --------
def is_already_processed(collection, pdf_filename):
    """Check if this PDF has already been added to the database"""
    try:
        results = collection.get(where={"pdf_file": pdf_filename})
        return len(results['ids']) > 0
    except:
        return False

# -------- OCR PROCESSING --------
def ocr_pdf(pdf_path, subject, grade, language, skip_if_exists=True):
    """Convert PDF pages to text using enhanced OCR and store in appropriate database"""
    pdf_filename = os.path.basename(pdf_path)
    
    # Get the appropriate database path for this textbook
    db_path = get_database_path(grade, language, subject)
    
    # Initialize ChromaDB client for this specific database
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    
    # Check if already processed
    if skip_if_exists and is_already_processed(collection, pdf_filename):
        print(f"⏭️  Skipping {pdf_filename} - already in database")
        return 0, db_path
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return 0, db_path
    
    print(f"\n{'='*60}")
    print(f"📚 Processing: {pdf_filename}")
    print(f"   Subject: {subject} | Grade: {grade} | Language: {language}")
    print(f"   Database: {os.path.basename(db_path)}")
    print(f"{'='*60}")
    
    try:
        # Convert PDF to images
        pages = convert_from_path(pdf_path, dpi=400, poppler_path=POPPLER_PATH)
        print(f"✓ Converted {len(pages)} pages to images at 400 DPI")
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        return 0, db_path
    
    all_chunks = []
    all_embeddings = []
    all_metadata = []
    
    for page_num, page in enumerate(pages, start=1):
        print(f"   Page {page_num}/{len(pages)}...", end=" ")
        
        try:
            # Preprocess and OCR
            processed_page = preprocess_image(page)
            custom_config = r'--oem 3 --psm 6 -l guj'  # Remove +eng
            text = pytesseract.image_to_string(processed_page, config=custom_config)
            
            if not text.strip():
                print("⚠️ No text")
                continue
            
            # Chunk the text
            chunks = chunk_text(text)
            
            if not chunks:
                print("⚠️ No chunks")
                continue
            
            # Generate embeddings
            embeddings = model.encode(chunks).tolist()
            
            # Store chunks and metadata
            for idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_embeddings.append(embeddings[idx])
                all_metadata.append({
                    "subject": subject,
                    "grade": grade,
                    "language": language,
                    "pdf_file": pdf_filename,
                    "page": page_num,
                    "chunk_index": idx
                })
            
            print(f"✓ {len(chunks)} chunks")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    # Batch insert into ChromaDB
    if all_chunks:
        print(f"\n💾 Saving {len(all_chunks)} chunks to database...")
        batch_size = 100
        saved_count = 0
        
        for i in range(0, len(all_chunks), batch_size):
            batch_chunks = all_chunks[i:i+batch_size]
            batch_embeddings = all_embeddings[i:i+batch_size]
            batch_metadata = all_metadata[i:i+batch_size]
            batch_ids = [f"{pdf_filename}_p{m['page']}_c{m['chunk_index']}" 
                        for m in batch_metadata]
            
            try:
                collection.add(
                    documents=batch_chunks,
                    embeddings=batch_embeddings,
                    metadatas=batch_metadata,
                    ids=batch_ids
                )
                saved_count += len(batch_chunks)
                print(f"   ✓ Saved batch {i//batch_size + 1} ({saved_count}/{len(all_chunks)})")
            except Exception as e:
                print(f"   ⚠️ Error saving batch: {e}")
        
        print(f"✅ Successfully added {saved_count} chunks from {pdf_filename}!")
        return saved_count, db_path
    else:
        print(f"❌ No valid text extracted from {pdf_filename}")
        return 0, db_path

# -------- AUTO-DISCOVER TEXTBOOKS --------
def auto_discover_textbooks(base_dir):
    """Automatically find all PDF files in directory structure"""
    discovered = []
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"⚠️ Base directory not found: {base_dir}")
        return discovered
    
    print(f"\n🔍 Scanning for PDFs in: {base_dir}")
    
    for pdf_file in base_path.rglob("*.pdf"):
        # Try to extract grade and subject from path
        parts = pdf_file.parts
        
        # Try to find grade (e.g., grade3, grade4)
        grade = None
        for part in parts:
            if 'grade' in part.lower():
                try:
                    grade = int(''.join(filter(str.isdigit, part)))
                except:
                    pass
        
        # Try to extract subject from filename
        filename = pdf_file.stem.lower()
        subject = "Unknown"
        
        
        if 'math' in filename:
            subject = "Maths"
        elif 'gujarati' in filename:
            subject = "Gujarati"
        
        
        discovered.append({
            "path": str(pdf_file),
            "subject": subject,
            "grade": grade or 0,
            "language": "gujarati"
        })
        
        print(f"   Found: {pdf_file.name} (Grade {grade}, {subject})")
    
    return discovered

# -------- MAIN --------
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 BATCH TEXTBOOK PROCESSOR FOR GUJARATI RAG")
    print("   (Each textbook goes to its own database)")
    print("="*70)
    
    # Choose processing mode
    print("\nSelect processing mode:")
    print("1. Use predefined list (edit TEXTBOOKS in code)")
    print("2. Auto-discover all PDFs in base directory")
    print("3. Process single file")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "2":
        # Auto-discover mode
        textbooks = auto_discover_textbooks(TEXTBOOK_BASE_DIR)
        if not textbooks:
            print("❌ No PDFs found!")
            exit()
        
        print(f"\n📚 Found {len(textbooks)} textbooks")
        confirm = input("Process all? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            exit()
    
    elif choice == "3":
        # Single file mode
        pdf_path = input("Enter full path to PDF: ").strip()
        subject = input("Enter subject: ").strip() or "Unknown"
        grade = int(input("Enter grade: ").strip() or "0")
        
        textbooks = [{
            "path": pdf_path,
            "subject": subject,
            "grade": grade,
            "language": "gujarati"
        }]
    
    else:
        # Use predefined list
        textbooks = TEXTBOOKS
    
    # Process all textbooks
    print(f"\n🔄 Processing {len(textbooks)} textbook(s)...\n")
    
    total_chunks = 0
    processed = 0
    skipped = 0
    failed = 0
    databases_used = set()
    
    for book in textbooks:
        try:
            chunks_added, db_path = ocr_pdf(
                book["path"],
                book["subject"],
                book["grade"],
                book["language"],
                skip_if_exists=True
            )
            
            databases_used.add(db_path)
            
            if chunks_added > 0:
                total_chunks += chunks_added
                processed += 1
            else:
                # Check if it was skipped or failed
                temp_client = chromadb.PersistentClient(path=db_path)
                temp_collection = temp_client.get_or_create_collection(name=COLLECTION_NAME)
                if is_already_processed(temp_collection, os.path.basename(book["path"])):
                    skipped += 1
                else:
                    failed += 1
                
        except Exception as e:
            print(f"❌ Fatal error processing {book['path']}: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("📊 PROCESSING SUMMARY")
    print("="*70)
    print(f"✅ Processed: {processed} textbooks")
    print(f"⏭️  Skipped: {skipped} (already in database)")
    print(f"❌ Failed: {failed}")
    print(f"💾 Total chunks added: {total_chunks}")
    print(f"🗄️  Databases created/updated: {len(databases_used)}")
    print(f"\nDatabases location: {VECTOR_DB_BASE_DIR}")
    print("\nDatabases used:")
    for db in sorted(databases_used):
        print(f"   📁 {os.path.basename(db)}")
    print("="*70)
    print("\n🎉 Batch processing complete!")