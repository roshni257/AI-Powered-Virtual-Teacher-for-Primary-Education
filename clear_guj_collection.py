# vectordb_guj_improved.py - Better OCR for Gujarati textbooks
import os
from pdf2image import convert_from_path
import pytesseract
from sentence_transformers import SentenceTransformer
import chromadb
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

# -------- CONFIG --------
PDF_PATH = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\textbooks\gujarati\grade3\GUJARATI_evs_grade3.pdf"
DB_DIR = r"C:\Users\HP\Desktop\uni\seventh_sem\rms\vector_db\grade3_gujarati_evs_db"


# Initialize ChromaDB
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="gujarati_textbook_db")


# -------- MAIN --------
if __name__ == "__main__":
    # Clear existing collection if rebuilding
    try:
        client.delete_collection(name="gujarati_textbook_db")
        collection = client.create_collection(name="gujarati_textbook_db")
        print("🗑️ Cleared old database\n")
    except:
        pass