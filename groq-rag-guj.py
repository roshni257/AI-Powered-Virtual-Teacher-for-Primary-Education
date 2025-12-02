# groq-rag-guj.py - Improved version with better context validation
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import re

# ---------- CONFIG ----------
DB_DIR = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\vector_db\grade3_gujarati_evs_db"
COLLECTION_NAME = "gujarati_textbook_db"

# Initialize embedding model
embed_model = SentenceTransformer("intfloat/multilingual-e5-base")

# Initialize Groq client
groq_client = Groq(api_key="YOUR_API_KEY")

# Connect to ChromaDB
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Add after connecting to ChromaDB
print(f"Database path: {DB_DIR}")
print(f"Collection: {COLLECTION_NAME}")

# Check collection size
count = collection.count()
print(f"Total documents in database: {count}")

if count == 0:
    print("❌ Database is EMPTY! Run vectordb_guj_batch.py first.")
    exit()
'''
# Sample a few documents
sample = collection.get(limit=3)
print("\n--- Sample Documents ---")
for i, doc in enumerate(sample['documents']):
    print(f"\nDoc {i+1}: {doc[:200]}...")
    print(f"Metadata: {sample['metadatas'][i]}")
'''
# ---------- HELPER FUNCTIONS ----------
def is_gujarati_text_valid(text):
    """Check if text contains meaningful Gujarati characters"""
    gujarati_chars = re.findall(r'[\u0A80-\u0AFF]', text)
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return False
    
    # At least 30% should be valid Gujarati characters
    gujarati_ratio = len(gujarati_chars) / total_chars
    return gujarati_ratio > 0.1

def clean_ocr_text(text):
    """Basic cleaning of OCR artifacts"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove common OCR artifacts
    text = re.sub(r'[^\u0A80-\u0AFF\s\w.,!?():-]', '', text)
    return text.strip()

# ---------- RETRIEVAL ----------
def retrieve_relevant_chunks(query, n_results=5):
    """Encode query and retrieve relevant chunks from ChromaDB"""
    query_embedding = embed_model.encode([query]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    '''
    # DEBUG: Print raw results
    print("\n--- RAW RETRIEVAL RESULTS ---")
    for i, (doc, dist) in enumerate(zip(documents, distances)):
        print(f"\n[{i+1}] Distance: {dist}")
        print(f"Raw text: {doc[:200]}...")
        print(f"Has Gujarati: {is_gujarati_text_valid(doc)}")
        print(f"Cleaned: {clean_ocr_text(doc)[:200]}...")
    '''
    # Filter and clean documents
    valid_docs = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        cleaned = clean_ocr_text(doc)
        if is_gujarati_text_valid(cleaned) and dist < 1.5:
            valid_docs.append(cleaned)
    
    print(f"\nValid docs after filtering: {len(valid_docs)}")
    return valid_docs, metadatas

# ---------- GENERATION ----------
def generate_answer(query, context_texts):
    if not context_texts:
        return "માફ કરશો, મને તમારી પાઠ્યપુસ્તકમાં આ માહિતી મળી નથી. (Sorry, I couldn't find this information in your textbook.)"
    
    context = "\n\n".join(context_texts)
    print("\n--- Retrieved Context ---\n")
    print(context[:500])  # Show first 500 chars
    
    # Stronger system prompt
    system_prompt = """You are a kind Gujarati teacher for primary school students.

CRITICAL RULES:
1. You MUST answer ONLY using the provided textbook context
2. If the context is corrupted, unclear, or doesn't contain the answer, respond: "માફ કરશો, મને આ પ્રશ્નનો જવાબ પાઠ્યપુસ્તકમાં સ્પષ્ટ રીતે મળ્યો નથી."
3. Always respond in Gujarati (ગુજરાતી ભાષામાં)
4. Keep answers simple for primary students
5. Do NOT use your general knowledge - ONLY the textbook context

If the context below is unreadable or doesn't answer the question, you MUST say so."""

    user_prompt = f"""પાઠ્યપુસ્તકમાંથી સંદર્ભ (Textbook Context):
{context}

પ્રશ્ન (Question): {query}

જવાબ આપો (Answer):"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,  # Lower temperature for more faithful responses
        max_completion_tokens=1000,
        top_p=0.9
    )

    return response.choices[0].message.content

# ---------- MAIN ----------
if __name__ == "__main__":
    print("ગુજરાતી RAG ચેટબોટ | Gujarati RAG Chatbot")
    print("'exit' લખો બહાર નીકળવા માટે | Type 'exit' to quit\n")
    
    while True:
        query = input("\nતમારો પ્રશ્ન (Your question): ")
        
        if query.lower() in ['exit', 'quit', 'બહાર']:
            print("આવજો! Goodbye!")
            break
        
        if not query.strip():
            continue
        
        # Retrieve and generate
        docs, meta = retrieve_relevant_chunks(query, n_results=5)
        
        if not docs:
            print("\n⚠️ Warning: No valid Gujarati text found in database!")
            print("Your OCR quality may be very poor. Consider:")
            print("1. Higher DPI (400-600) in pdf2image")
            print("2. Image preprocessing (denoising, contrast)")
            print("3. Manual text extraction if PDF has text layer")
            continue
        
        answer = generate_answer(query, docs)
        print("\n--- જવાબ (Answer) ---\n")
        print(answer)