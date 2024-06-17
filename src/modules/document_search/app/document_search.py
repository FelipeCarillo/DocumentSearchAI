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

        # Get the Elasticsearch index name from the environment variables
        es_index_name = os.environ.get("ES_INDEX_NAME")

        # Create an instance of the DocumentStore class
        document_store = DocumentStore(es_index_name=es_index_name)

        # Search the Elasticsearch database for the query
        search_results = document_store.search_vector_store(query)

        # Create an instance of the LLMSearch class
        llm = LLMSearch()

        # Create a response with GPT-4o to the given query using the search results
        response = llm.create_response(query, search_results)

        return OK("Success", response).to_dict()

    except Exception as e:
        print(f"Error: {e}")
        return InternalServerError("Error", str(e)).to_dict()
