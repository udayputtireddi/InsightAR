# InsightAR

InsightAR is a multimodal AI assistant that understands **images, PDF documents and multi-model tools**.  
It lets you:

- 🖼 Upload an image and get a **rich, BLIP-2-powered caption**
- 📄 Upload a PDF and get an **intelligent summary** using **Long-T5**
- ❓ Ask **natural language questions** about your PDF with **RAG + DeBERTa v3 QA**

---

## Tech Stack

**Frontend**
- Next.js 16 (App Router)
- React, TypeScript
- Tailwind CSS
- Axios for API calls


**Backend**
- FastAPI (Python)
- Uvicorn
- PyMuPDF (`fitz`) for PDF text extraction

**AI / ML**
- `Salesforce/blip2-flan-t5-xl` for image captioning
- `google/long-t5-tglobal-base` for long-document summarization
- `deepset/deberta-v3-large-squad2` for question answering
- `sentence-transformers/all-MiniLM-L6-v2` for embeddings & RAG-style retrieval

---

## Features

### 🖼 Image Analyzer
- Upload an image (JPEG/PNG)
- BLIP-2 generates a detailed caption
- Runs on Apple MPS (if available) or CPU

### 📄 Document Analyzer
- Upload a PDF document
- Extracts text from each page using PyMuPDF
- Long-T5 generates a concise, readable summary

### ❓ Ask Questions About a PDF (RAG)
- Splits the document into semantic chunks
- Uses MiniLM embeddings to find the most relevant chunks
- Runs DeBERTa v3 QA over those chunks for accurate answers

---

✨ Vision Tools
  - Image Captioning
  - Image Understanding
  - OCR Extraction

📄 Document Tools
  - Summarization
  - PDF Q&A
  - Extract Structured Data

📦 Multi-modal Tools
  - Image + PDF QA
  - Vision+Text Analysis
