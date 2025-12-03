# AI-Powered Virtual Teacher for Primary Education

An intelligent, multilingual educational platform that provides personalized tutoring for primary school students (Grades 1-3) using AI-powered avatars, voice interaction, and curriculum-aligned content. Built to address **UN SDG 4: Quality Education** by democratizing access to quality learning experiences.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![React](https://img.shields.io/badge/React-19.1-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Three.js](https://img.shields.io/badge/Three.js-0.180-000000)

---

##  Problem Statement

**Educational Challenges Addressed:**
- **Language Barriers**: 60+ million Gujarati speakers lack quality educational resources in their native language
- **Limited Access**: Rural and underserved communities have limited access to personalized tutoring
- **Cost Barriers**: Private tutoring costs ₹500-2000/month per subject, excluding many families
- **Teacher Shortage**: Student-teacher ratios in India often exceed 30:1, limiting individual attention
- **Digital Divide**: Most EdTech solutions are English-centric and expensive

**Our Solution:**
An AI-powered virtual teacher that provides:
- ✅ Free, 24/7 personalized tutoring
- ✅ Multilingual support (English & Gujarati)
- ✅ Voice-based interaction for accessibility
- ✅ Curriculum-aligned responses from official textbooks
- ✅ Interactive 3D avatars for engaging learning experiences

---

##  Key Features

### 1. **Multilingual AI Tutoring**
- Supports English and Gujarati languages
- Automatic language detection and switching
- Curriculum-aligned responses from NCERT and GSEB textbooks

### 2. **Interactive 3D Avatars**
- Gender-diverse teacher avatars (male/female)
- Lip-synced animations during speech
- Smooth transitions between idle and talking states

### 3. **Voice-First Interface**
- Speech recognition for hands-free queries
- Text-to-speech with language-specific voices
- Gender-adaptive voice profiles

### 4. **Intelligent Document Processing**
- Upload PDFs, images, DOCX, or TXT files
- Automatic OCR for Gujarati and English text
- Real-time knowledge augmentation

### 5. **RAG-Based Question Answering**
- Retrieval-Augmented Generation ensures accurate, grounded responses
- Vector database with subject-specific collections
- Prevents AI hallucination by constraining to textbook content

### 6. **Multi-Subject Support**
- **Subjects**: English, Mathematics, Environmental Studies (EVS), Gujarati
- **Grades**: 1, 2, 3
- Separate vector databases for each grade-subject combination

---

##  Technology Stack

### **Frontend**
- **React 19.1** - UI framework
- **Vite 7.1** - Build tool and dev server
- **Three.js 0.180** - 3D graphics engine
- **React Three Fiber 9.4** - React renderer for Three.js
- **React Three Drei 10.7** - Helper utilities for 3D scenes
- **Web Speech API** - Voice recognition and synthesis

### **Backend**
- **FastAPI 0.115** - Modern Python web framework
- **Groq API** - LLM inference (llama-3.3-70b-versatile)
- **LangChain 0.3** - RAG orchestration framework
- **ChromaDB 1.0** - Vector database for embeddings
- **Sentence Transformers 5.1** - Text embedding models
  - `all-MiniLM-L6-v2` for English (384 dimensions)
  - `multilingual-e5-base` for Gujarati (768 dimensions)

### **Document Processing**
- **PyMuPDF 1.25** - PDF text extraction
- **Tesseract OCR 5.x** - Optical character recognition (Gujarati + English)
- **Pillow 10.4** - Image processing
- **python-docx 1.2** - DOCX file parsing
- **pdf2image** - PDF to image conversion
- **OpenCV** - Image preprocessing for OCR

### **3D Assets**
- **GLB Models** - Ready Player Me avatars
- **FBX Animations** - Mixamo animation library
- **Skeleton Retargeting** - Custom animation mapping

---

##  Prerequisites

Before setting up the project, ensure you have the following installed:

### **Required Software**
1. **Python 3.12+** - [Download](https://www.python.org/downloads/)
2. **Node.js 20+** - [Download](https://nodejs.org/)
3. **Git** - [Download](https://git-scm.com/)
4. **Tesseract OCR** - [Installation Guide](#tesseract-installation)
5. **Poppler** (for PDF processing) - [Installation Guide](#poppler-installation)

### **API Keys**
- **Groq API Key** - [Get Free Key](https://console.groq.com/)

---

## 🔧 Installation & Setup

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/roshni257/AI-Powered-Virtual-Teacher-for-Primary-Education.git
cd AI-Powered-Virtual-Teacher-for-Primary-Education
```

### **Step 2: Install Tesseract OCR**

#### **Windows:**
1. Download installer from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to `C:\Program Files\Tesseract-OCR`
3. Download Gujarati language data:
   - Download `guj.traineddata` from [tessdata repository](https://github.com/tesseract-ocr/tessdata)
   - Place in `C:\Program Files\Tesseract-OCR\tessdata\`

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-guj
```

#### **macOS:**
```bash
brew install tesseract tesseract-lang
```

### **Step 3: Install Poppler**

#### **Windows:**
1. Download from [Poppler Releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract to `C:\Program Files\poppler-25.07.0`
3. Add `C:\Program Files\poppler-25.07.0\Library\bin` to PATH

#### **Linux:**
```bash
sudo apt install poppler-utils
```

#### **macOS:**
```bash
brew install poppler
```

### **Step 4: Backend Setup**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install fastapi uvicorn groq langchain langchain-community langchain-chroma langchain-huggingface sentence-transformers chromadb pymupdf pytesseract pillow python-docx pdf2image opencv-python numpy
```

### **Step 5: Configure API Keys**

Create `API_KEY.TXT` in the project root:
```
your_groq_api_key_here
```

**Update `backend.py` (Line 28):**
```python
API_KEY = open("API_KEY.TXT").read().strip()
```

### **Step 6: Update File Paths**

**In `backend.py` (Line 36):**
```python
BASE_PATH = r"C:\path\to\your\project\vector_db"
```

**In `vectordb_guj_batch.py`:**
```python
# Update these paths to match your system
VECTOR_DB_BASE_DIR = r"C:\path\to\your\project\vector_db"
TEXTBOOK_BASE_DIR = r"C:\path\to\your\project\textbooks\gujarati"
POPPLER_PATH = r"C:\Program Files\poppler-25.07.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### **Step 7: Frontend Setup**

```bash
cd my-app
npm install
```

### **Step 8: Build Vector Databases**

**Place your textbooks in the following structure:**
```
textbooks/
├── english/
│   ├── grade1/
│   ├── grade2/
│   └── grade3/
└── gujarati/
    ├── grade1/
    ├── grade2/
    └── grade3/
```

**Run the batch processor:**
```bash
python vectordb_guj_batch.py
```

Select option:
- **Option 1**: Use predefined list (edit `TEXTBOOKS` array in the script)
- **Option 2**: Auto-discover all PDFs in the textbooks directory
- **Option 3**: Process a single file

---

##  Running the Application

### **Start Backend Server**
```bash
# From project root (with virtual environment activated)
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### **Start Frontend Development Server**
```bash
# From my-app directory
cd my-app
npm run dev
```

Frontend will be available at: `http://localhost:5173`

### **Access the Application**
Open your browser and navigate to `http://localhost:5173`

---

##  Usage Guide

### **Basic Workflow**

1. **Select Avatar**: Choose male or female teacher avatar
2. **Choose Grade**: Select grade (1, 2, or 3)
3. **Select Subject**: Pick subject (English, Maths, EVS, Gujarati)
4. **Choose Medium**: Select language (English or Gujarati)
5. **Ask Questions**: 
   - Type your question in the input box, OR
   - Click the microphone button and speak
6. **Upload Materials** (Optional): Upload PDFs, images, or documents for additional context
7. **Get Answers**: The AI teacher will respond with voice and text

### **Voice Commands**
- Click 🎤 to start voice input
- Speak clearly in your selected language
- The system will automatically transcribe and process your question

### **File Upload**
Supported formats:
- PDF documents
- Images (PNG, JPG, JPEG, BMP, TIFF)
- DOCX files
- TXT files

---

##  Project Structure

```
project-root/
├── backend.py                      # FastAPI server
├── groq-rag.py                     # English RAG testing script
├── groq-rag-guj.py                 # Gujarati RAG testing script
├── vectordb_guj_batch.py           # Batch database builder
├── vectordb.py                     # Database utilities
├── clear_guj_collection.py         # Database cleanup script
├── testing-guj-ocr.py              # OCR testing script
├── API_KEY.TXT                     # Groq API key (gitignored)
├── .gitignore                      # Git ignore rules
│
├── my-app/                         # React frontend
│   ├── public/
│   │   ├── models/
│   │   │   ├── teacher_female.glb  # Female avatar
│   │   │   └── teacher_male.glb    # Male avatar
│   │   └── animations/
│   │       ├── Idle_Standing_female.fbx
│   │       ├── Talking_Standing_female.fbx
│   │       ├── Idle_Standing_male.fbx
│   │       └── Talking_Standing_male.fbx
│   ├── src/
│   │   ├── components/
│   │   │   ├── AvatarScene.jsx
│   │   │   ├── TeacherAvatar.jsx
│   │   │   ├── Avatar_Female.jsx
│   │   │   ├── Avatar_Male.jsx
│   │   │   └── AvatarSelection.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── textbooks/                      # Source textbooks (gitignored)
│   ├── english/
│   │   ├── grade1/
│   │   ├── grade2/
│   │   └── grade3/
│   └── gujarati/
│       ├── grade1/
│       ├── grade2/
│       └── grade3/
│
└── vector_db/                      # ChromaDB storage (gitignored)
    ├── grade1_english_db/
    ├── grade1_maths_db/
    ├── grade3_gujarati_evs_db/
    └── ...
```

---

##  How It Works

### **Architecture Overview**

```
User Query → Speech Recognition → FastAPI Backend
                                        ↓
                            Language Detection
                                        ↓
                    ┌───────────────────┴───────────────────┐
                    ↓                                       ↓
            Load Textbook DB                    Process Uploaded File
                    ↓                                       ↓
            Vector Similarity Search            Create Ephemeral DB
                    ↓                                       ↓
            Retrieve Relevant Chunks            Query Uploaded Content
                    └───────────────────┬───────────────────┘
                                        ↓
                            Merge Context
                                        ↓
                    Groq LLM (llama-3.3-70b-versatile)
                                        ↓
                            Generated Answer
                                        ↓
                    Text-to-Speech Synthesis
                                        ↓
                    Avatar Animation + Audio Playback
```

### **RAG Pipeline**

1. **Document Ingestion**:
   - PDFs converted to images (400 DPI)
   - OCR extraction with Tesseract (Gujarati + English)
   - Text chunked into 500-character segments with 50-char overlap (backend) or 400-char with 50-char overlap (batch processor)

2. **Embedding Generation**:
   - English: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
   - Gujarati: `intfloat/multilingual-e5-base` (768 dimensions)
   - Stored in ChromaDB with metadata (grade, subject, page, language)

3. **Query Processing**:
   - User query embedded using same model
   - Cosine similarity search in vector database
   - Top-K chunks retrieved (K=3-5)
   - Distance threshold filtering (< 1.5 for Gujarati)

4. **Answer Generation**:
   - Context + query sent to Groq LLM
   - System prompt ensures curriculum-aligned responses
   - Temperature=0 for factual accuracy
   - Language-specific prompts for English vs Gujarati

5. **Multimodal Output**:
   - Text displayed in chat interface
   - Speech synthesis with language-specific voices
   - Avatar lip-sync animation triggered during speech

---

## 🎓 Educational Impact

### **Alignment with SDG 4: Quality Education**

This project addresses multiple UN Sustainable Development Goal 4 targets:

- **Target 4.1**: Free, equitable primary education for all
- **Target 4.4**: Relevant skills for employment (digital literacy)
- **Target 4.5**: Eliminate gender disparities (inclusive avatars)
- **Target 4.6**: Literacy and numeracy (foundational subjects)
- **Target 4.a**: Inclusive learning environments (voice accessibility)

### **Research Contributions**

1. **Multilingual NLP**: Practical implementation of RAG for low-resource Indian languages (Gujarati)
2. **Curriculum Alignment**: Grounding LLM responses in official NCERT and GSEB textbooks
3. **Accessible EdTech**: Voice-first interface for low-literacy contexts
4. **Cultural Responsiveness**: Regional language support and culturally appropriate avatars
5. **OCR Quality Enhancement**: Image preprocessing pipeline for better Gujarati text recognition

---

## 📊 Performance Metrics

- **Model Loading**: ~2-3s (first load, then cached)
- **Query Response Time**: ~1-3s (depends on Groq API latency)
- **Animation Switching**: <500ms (smooth transitions)
- **Voice Synthesis**: Real-time (browser native)
- **OCR Processing**: ~5-10s per page at 400 DPI
- **Database Query**: <100ms (vector similarity search)

---

## 📄 License

This project is licensed under the MIT License.

---

## Acknowledgments

- **Groq** - For providing fast LLM inference API
- **HuggingFace** - For open-source embedding models
- **Mixamo** - For free animation library
- **Ready Player Me** - For avatar creation tools
- **Tesseract OCR** - For multilingual text recognition
- **NCERT & GSEB** - For educational textbook content
- **LangChain** - For RAG framework
- **ChromaDB** - For vector database

---

## Contact

**Project Maintainer**: Roshni  
**GitHub**: [@roshni257](https://github.com/roshni257)  
**Repository**: [AI-Powered-Virtual-Teacher-for-Primary-Education](https://github.com/roshni257/AI-Powered-Virtual-Teacher-for-Primary-Education)

---

**Made with ❤️ for Quality Education (SDG 4)**


