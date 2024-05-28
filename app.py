from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import openai
import faiss
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Set your OpenAI API key
openai.api_key = 'sk-proj-bpkAPRdrpN4Qn3aAfVIqT3BlbkFJU7V78e3kNGCFDeC0L4sq'

documents = []

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_reader = fitz.open(stream=file.file.read(), filetype="pdf")
        text = ""
        for page_num in range(pdf_reader.page_count):
            page = pdf_reader.load_page(page_num)
            text += page.get_text()

        documents.append(text)
        return {"message": "PDF content extracted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryModel(BaseModel):
    query: str

@app.post("/query_pdf/")
async def query_pdf(query: QueryModel):
    try:
        context = " ".join(documents)
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Context: {context}\n\nQuestion: {query.query}\nAnswer:",
            max_tokens=150
        )
        return JSONResponse(content={"answer": response.choices[0].text.strip()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
