import os
import jwt
import dotenv
import base64
from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware

from src.modules.scan_file.app.scan_file import lambda_handler as scan_file
from src.modules.list_files.app.list_files import lambda_handler as list_files
from src.modules.delete_file.app.delete_file import lambda_handler as delete_file
from src.modules.upload_file.app.upload_file import lambda_handler as upload_file
from src.modules.document_search.app.document_search import (
    lambda_handler as document_search,
)

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")
Authorization = ""


def set_authorization():
    global Authorization
    jwt_secret = os.environ.get("JWT_SECRET")
    Authorization = jwt.encode({"user": "user"}, jwt_secret, algorithm="HS256")


def create_event(body={}, params={}, object: str = ""):
    global Authorization
    if not Authorization:
        set_authorization()
    return {
        "body": body,
        "queryStringParameters": params,
        "Records": [
            {"s3": {"bucket": {"name": AWS_BUCKET_NAME}, "object": {"key": object}}}
        ],
        "headers": {"Authorization": Authorization},
    }


def create_response(response):
    content = response["body"]
    status_code = response["statusCode"]
    return Response(
        content=content, status_code=status_code, media_type="application/json"
    )


@app.get("/list-files")
def list_files_route():
    event = create_event()
    response = list_files(event, None)
    return create_response(response)


@app.delete("/delete-file")
def delete_file_route(file_name: str):
    event = create_event(params={"file_name": file_name})
    response = delete_file(event, None)
    return create_response(response)


@app.post(
    "/upload-file-docs",
    description="Upload a file to the S3 bucket and scan it. This function is for FastAPI docs.",
)
def upload_file_docs_route(file: UploadFile = File(...)):
    file_base64 = base64.b64encode(file.file.read()).decode("utf-8")

    event = create_event(
        body={
            "file_name": file.filename,
            "file_body": file_base64,
            "content_type": file.content_type,
        },
    )
    response = upload_file(event, None)
    try:
        scan_file(create_event(object=str(file.filename)), None)
    finally:
        return create_response(response)


@app.post("/upload-file")
def upload_file_route(file: dict):
    event = create_event(
        body={
            "file_name": file.get("file_name"),
            "file_body": file.get("file_body"),
            "content_type": file.get("content_type"),
        }
    )
    response = upload_file(event, None)
    try:
        scan_file(create_event(object=file.get("file_name")), None)
    finally:
        return create_response(response)


@app.get("/document-search")
def document_search_route(query: str, object_name: str):
    event = create_event(params={"query": query, "object_name": object_name})
    response = document_search(event, None)
    return create_response(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
