import os

from src.core.helpers.http.http import HTTPRequest, OK, InternalServerError
from src.core.helpers.functions.LLMSearch import LLMSearch
from src.core.helpers.functions.DocumentStore import DocumentStore


def lambda_handler(event, context):
    """
    This function is responsible for making search requests to the Elasticsearch database according to the query.
    """

    request = HTTPRequest(event)

    try:

        # Get the query from the request parameters
        query = request.parameters.get("query")
        object_name = request.parameters.get("object_name")

        es_index_name = f"{os.environ.get("AWS_BUCKET_NAME")}-{object_name}-index"

        # Create an instance of the DocumentStore class
        document_store = DocumentStore(es_index_name=es_index_name)

        # Search the Elasticsearch database for the query
        search_results = document_store.search_vector_store(query)

        # Create an instance of the LLMSearch class
        llm = LLMSearch()

        # Create a response with GPT-4o to the given query using the search results
        response = llm.create_response(query, search_results)

        data = {
            "llm_response": response,
            "search_results": search_results,
        }

        return OK("Success", data).to_dict()

    except Exception as e:
        print(f"Error: {e}")
        return InternalServerError("Error", str(e)).to_dict()
