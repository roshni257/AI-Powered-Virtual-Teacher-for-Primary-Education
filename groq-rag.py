from groq import Groq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Path to your ChromaDB folder
DB_PATH = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\vector_db\grade3_evs_db"

# Load embeddings and Chroma vector database
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(
    persist_directory=DB_PATH,
    collection_name="textbook_db",   # MUST match vectordb.py
    embedding_function=embeddings
)

# Groq client
API_KEY = "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"
client = Groq(api_key=API_KEY)

print("Chatbot is ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    # Step 1: Search Chroma vector database
    docs = db.similarity_search(user_input, k=3)
    if not docs:
        print("Bot: Sorry, I couldn’t find this in your textbook.")
        continue

    context = "\n".join([d.page_content for d in docs])

    print("\nRetrieved context:\n", context[:300], "\n---")  # Debugging

    # Step 2: Send context + user query to Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a kind teacher for primary school students. ONLY use the provided context to answer. If the context is empty or irrelevant, reply with: 'Sorry, I couldn’t find this in your textbook.'"},
            {"role": "user", "content": f"Context from textbook:\n{context}\n\nQuestion: {user_input}"}
        ],
        temperature=0,
        max_completion_tokens=512,
        top_p=1,
        stream=True,
    )

    # Step 3: Stream the answer
    print("Bot:", end=" ", flush=True)
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="", flush=True)
    print("\n")
