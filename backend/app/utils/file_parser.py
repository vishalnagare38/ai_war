from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile
from pypdf import PdfReader


async def extract_transcript_text(file: UploadFile) -> str:
    filename = file.filename or ""
    ext = Path(filename).suffix.lower()

    content = await file.read()

    if ext == ".txt" or file.content_type in {"text/plain", "text/txt"}:
        try:
            text = content.decode("utf-8", errors="ignore").strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Could not read TXT file.")
        if not text:
            raise HTTPException(status_code=400, detail="TXT file is empty.")
        return text

    if ext == ".pdf" or file.content_type == "application/pdf":
        try:
            reader = PdfReader(BytesIO(content))
            pages_text = []
            for page in reader.pages:
                pages_text.append(page.extract_text() or "")
            text = "\n".join(pages_text).strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Could not read PDF file.")

        if not text:
            raise HTTPException(status_code=400, detail="No extractable text found in PDF.")
        return text

    raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")