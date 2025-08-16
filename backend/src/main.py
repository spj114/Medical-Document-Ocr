from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from extractor import extract
import uuid
from dotenv import load_dotenv

load_dotenv()

poppler_path = os.getenv("POPPLER_PATH")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

@app.post('/extract_from_doc')
def extract_from_doc(file_format: str = Form(...), file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        return {'error': 'Only PDF files are supported'}
    
    contents = file.file.read()
    file.file.close()
    
    saved_path = 'uploads/' + str(uuid.uuid4()) + '.pdf'

    try:
        with open(saved_path, 'wb') as f:
            f.write(contents)
        
        data = extract(saved_path, file_format, poppler_path)
        
        if not data or all(not v for v in data.values()):
            data = {'error': 'No data could be extracted from the document. Please ensure the document is clear and in the expected format.'}
            
    except FileNotFoundError as e:
        data = {'error': f'File processing error: {str(e)}'}
    except Exception as e:
        data = {'error': f'Extraction failed: {str(e)}'}
    finally:
        if os.path.exists(saved_path):
            os.remove(saved_path)

    return data

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)