import os
import dotenv
from fastapi import FastAPI

from src.modules.scan_file import lambda_handler as scan_file
from src.modules.document_search import lambda_handler as document_search

dotenv.load_dotenv()

app = FastAPI()

BUCKET_NAME = os.environ.get("BUCKET_NAME")




if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
