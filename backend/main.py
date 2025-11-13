from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
from PIL import Image
import io
import fitz  # PyMuPDF for PDF extraction
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration

# -------------------------------
# App setup
# -------------------------------
app = FastAPI(title="InsightAR Backend")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 🚀 BLIP-2 Image Captioning (FLAN-T5-XL – FAST)
# -------------------------------
device = "mps" if torch.backends.mps.is_available() else "cpu"

processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-flan-t5-xl",
    torch_dtype=torch.float16 if device != "cpu" else torch.float32,
)
model.to(device)


# -------------------------------
# PDF Summarizer (Bart CNN)
# -------------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# -------------------------------
# Document Question Answering
# -------------------------------
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

# -------------------------------
# 📸 Image Captioning Endpoint
# -------------------------------
@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    inputs = processor(
        image,
        return_tensors="pt"
    ).to(device, torch.float16 if device != "cpu" else torch.float32)

    generated_ids = model.generate(**inputs, max_length=50)
    caption = processor.decode(generated_ids[0], skip_special_tokens=True)

    return {"caption": caption}

# -------------------------------
# 📄 PDF Summarization Endpoint
# -------------------------------
@app.post("/analyze-doc/")
async def analyze_doc(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()

    text = text[:4000]

    summary = summarizer(
        text,
        max_length=200,
        min_length=50,
        do_sample=False
    )[0]["summary_text"]

    return {"summary": summary}

# -------------------------------
# 💬 PDF Q&A Endpoint
# -------------------------------
@app.post("/ask-doc/")
async def ask_doc(file: UploadFile = File(...), question: str = Form(...)):
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()

    text = text[:4000]

    answer = qa_model(question=question, context=text)

    return {
        "question": question,
        "answer": answer["answer"],
        "confidence": round(answer["score"], 3)
    }
