from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from PIL import Image
import io
import fitz  # PyMuPDF for PDF text extraction

# -------------------------------
# App setup
# -------------------------------
app = FastAPI(title="InsightAR Backend")

# Allow frontend (Next.js) to access backend
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# AI Models
# -------------------------------

# Image Captioning Model
model = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

# Document Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Question Answering Model (for text-based PDFs)
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# -------------------------------
# API Endpoints
# -------------------------------

@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    """
    Accepts an image file and returns a caption.
    """
    image = Image.open(io.BytesIO(await file.read()))
    result = model(image)
    caption = result[0]["generated_text"]
    return {"caption": caption}


@app.post("/analyze-doc/")
async def analyze_doc(file: UploadFile = File(...)):
    """
    Accepts a PDF document and returns a concise summary.
    """
    # Read uploaded PDF into memory
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Extract text from all pages
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()

    # Truncate long text (models have token limits)
    text = text[:4000]

    # Summarize the extracted text
    summary = summarizer(
        text,
        max_length=200,
        min_length=50,
        do_sample=False
    )[0]["summary_text"]

    return {"summary": summary}


@app.post("/ask-doc/")
async def ask_doc(file: UploadFile = File(...), question: str = Form(...)):
    """
    Accepts a PDF and a question, extracts text, and answers based on document content.
    """
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Extract text from all pages
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()

    # Truncate to stay within token limits
    text = text[:4000]

    # Get the answer using the QA model
    answer = qa_model(question=question, context=text)

    return {
        "question": question,
        "answer": answer["answer"],
        "confidence": round(answer["score"], 3)
    }
