import os
from typing import List

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore


class DocumentStore:
    def __init__(self, es_index_name: str):
        """
        Initializes the DocumentStore with the Elasticsearch index name.
        args:
            es_index_name: The name of the Elasticsearch index.
        """
        self.es_index_name = es_index_name
        self.es_cloud_id = os.environ.get("ES_CLOUD_ID")
        self.es_api_key = os.environ.get("ES_API_KEY")
        self.es_url = (
            f"http://localhost:{os.environ.get('ES_PORT', '9200')}"
            if os.environ.get("STAGE") == "dev"
            else None
        )

    def store(self, documents: List[Document]):
        """
        Stores the documents in the Elasticsearch database.
        args:
            documents: A list of Documents.
        """
        try:
            # Create an instance of the OpenAIEmbeddings class
            embedding = OpenAIEmbeddings()

            # Store the documents in the Elasticsearch database
            if self.es_url:
                ElasticsearchStore.from_documents(
                    documents=documents,
                    es_url=self.es_url,
                    index_name=self.es_index_name,
                    embedding=embedding,
                )
            else:
                ElasticsearchStore.from_documents(
                    documents=documents,
                    es_cloud_id=self.es_cloud_id,
                    es_api_key=self.es_api_key,
                    index_name=self.es_index_name,
                    embedding=embedding,
                )

        except Exception as e:
            raise e

    def search_vector_store(self, query: str) -> List[Document]:
        """
        Searches the vector store for the given query and returns the search results.
        """
        try:
            embedding = OpenAIEmbeddings()
            db = None

            if self.es_url:
                db = ElasticsearchStore(
                    es_url=self.es_url,
                    index_name=self.es_index_name,
                    embedding=embedding,
                )
            else:
                db = ElasticsearchStore(
                    es_cloud_id=self.es_cloud_id,
                    es_api_key=self.es_api_key,
                    index_name=self.es_index_name,
                    embedding=embedding,
                )

            # Search the vector store for the given query
            results = db.similarity_search(query)

            return results

        except Exception as e:
            raise e

    def delete(self):
        """
        Deletes the index from the Elasticsearch database.
        args:
            document_id: The ID of the document to be deleted.
        """
        try:

            # Delete the document from the Elasticsearch database
            if self.es_url:
                ElasticsearchStore(
                    es_url=self.es_url,
                    index_name=self.es_index_name,
                ).delete(
                    ids=[self.es_index_name],
                    index_name=self.es_index_name,
                )
            else:
                ElasticsearchStore(
                    es_cloud_id=self.es_cloud_id,
                    es_api_key=self.es_api_key,
                    index_name=self.es_index_name,
                ).delete(
                    ids=[self.es_index_name],
                    index_name=self.es_index_name,
                )

        except Exception as e:
            raise e
