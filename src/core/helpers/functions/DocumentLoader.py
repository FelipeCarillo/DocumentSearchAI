import os
import uuid
import boto3
import botocore
from typing import List
from datetime import datetime
from tempfile import NamedTemporaryFile

from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PDFMinerLoader

from src.core.helpers.exeptions.exceptions import (
    InvalidFileFormat,
    S3Exeption,
    S3ObjectNotFound,
)


class DocumentLoader:
    def __init__(
        self,
        bucket_name: str,
        object_name: str,
        aws_region: str,
    ):
        """
        Initializes the DocumentLoader with the bucket name and object name.
        args:
            bucket_name: The name of the S3 bucket.
            object_name: The name of the S3 object.
            aws_region: The AWS region.
        """

        self.bucket_name = bucket_name
        self.object_name = object_name
        self.aws_region = aws_region

        boto3.setup_default_session(region_name=aws_region)

        s3 = boto3.client("s3")
        if os.environ.get("STAGE") == "dev":
            s3 = boto3.client(
                "s3",
                endpoint_url="http://localhost:9000",
                aws_access_key_id=os.environ.get("MINIO_ACCESS_KEY"),
                aws_secret_access_key=os.environ.get("MINIO_SECRET_KEY"),
            )
        self.s3 = s3

    def load(self):
        """
        Loads the text from the input document and returns the text.
        """
        if self.object_name.endswith(".pdf"):
            return self.__load_from_pdf()
        elif self.object_name.endswith(".txt"):
            return self.__load_from_text()
        elif (
            self.object_name.endswith(".jpg")
            or self.object_name.endswith(".jpeg")
            or self.object_name.endswith(".png")
        ):
            return self.__load_from_image()
        else:
            raise InvalidFileFormat(self.object_name.split(".")[-1])

    def __load_from_text(self) -> List[Document]:
        """
        Loads the text from the input document and returns the text in a structured format.
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=self.object_name)
            text = response["Body"].read().decode("utf-8")

            loader = TextLoader(text)
            docs = loader.load()

            for doc in docs:
                doc.metadata = {
                    "id": uuid.uuid4().hex,
                    "bucket_name": self.bucket_name,
                    "object_name": self.object_name,
                    "timestamp": datetime.now().isoformat(),
                }

            return self.__split_documents(docs)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise S3ObjectNotFound(e.response["Error"]["Message"])
            else:
                raise S3Exeption(e.response["Error"]["Message"])

    def __load_from_pdf(self) -> List[Document]:
        """
        Loads the text from the input PDF document and returns the text in a structured format.
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=self.object_name)
            file = response["Body"].read()

            with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file)
                temp_file_path = temp_file.name

            try:
                loader = PDFMinerLoader(temp_file_path)
                docs = loader.load()

                for doc in docs:
                    doc.metadata = {
                        "id": uuid.uuid4().hex,
                        "bucket_name": self.bucket_name,
                        "object_name": self.object_name,
                        "timestamp": datetime.now().isoformat(),
                    }

                return self.__split_documents(docs)

            finally:
                os.remove(temp_file_path)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise S3ObjectNotFound(e.response["Error"]["Message"])
            else:
                raise S3Exeption(e.response["Error"]["Message"])

    def __load_from_image(self) -> List[Document]:
        """
        Loads the text from the input image document and returns the text in a structured format.
        """
        try:
            textract = boto3.client("textract")
            if os.environ.get("STAGE") == "dev":
                textract = boto3.client(
                    "textract",
                    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                )

            # Get the image from the S3 bucket
            document_bytes = self.s3.get_object(
                Bucket=self.bucket_name, Key=self.object_name
            )["Body"].read()

            # Detect the text in the image
            response = textract.detect_document_text(Bytes=document_bytes)

            text_extracted = ""
            for item in response["Blocks"]:
                if item["BlockType"] == "LINE":
                    text_extracted += item["Text"] + "\n"

            with NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_file.write(text_extracted.encode("utf-8"))
                temp_file_path = temp_file.name

            loader = TextLoader(temp_file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata = {
                    "id": uuid.uuid4().hex,
                    "bucket_name": self.bucket_name,
                    "object_name": self.object_name,
                    "timestamp": datetime.now().isoformat(),
                }

            return self.__split_documents(docs)

        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidS3ObjectException":
                raise Exception(
                    "The S3 object is invalid or does not exist: "
                    + e.response["Error"]["Message"]
                )
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                raise Exception(
                    "The parameters are invalid: " + e.response["Error"]["Message"]
                )
            elif e.response["Error"]["Code"] == "UnsupportedDocumentException":
                raise Exception(
                    "The document is not supported: " + e.response["Error"]["Message"]
                )
            elif e.response["Error"]["Code"] == "DocumentTooLargeException":
                raise Exception(
                    "The document is too large: " + e.response["Error"]["Message"]
                )
            else:
                raise Exception("An error occurred: " + e.response["Error"]["Message"])

    @staticmethod
    def __split_documents(docs: List[Document]) -> List[Document]:
        """
        Splits the documents into chunks of 500 characters with an overlap of 0 characters.
        args:
            docs: A list of Documents.
        """
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        chunks = text_splitter.split_documents(docs)

        return chunks
