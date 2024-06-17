from typing import List

from openai import OpenAI


class LLMSearch:
    def __init__(self):
        """
        Initializes the LLMSearch with the messages.
        args:
            messages: A list of messages.
        """

    def optimize_query(self, query: str) -> str:
        """
        Optimizes the given query to improve the performance of the similary search algorithm.
        """
        # Create an instance of the OpenAI class
        client = OpenAI()

        # Create a prompt
        prompt = self.__get_llm_optimizer_configuration()

        # Create a completion with GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
        )

        return response.choices[0].message.content

    def create_response(self, query: str, results: dict) -> str:
        """
        Creates a response with GPT-4o to the given query using the search results.
        """
        # Transform the search results into a formatted string
        results = "\n".join(
            [
                f"{i+1}. {result.page_content} ({result.metadata['bucket_name']}/{result.metadata['object_name']})"
                for i, result in enumerate(results)
            ]
        )

        # Create an instance of the OpenAI class
        client = OpenAI()

        # Create a prompt
        prompt = self.__get_llm_search_configuration()

        # Create a completion with GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "system", "content": f"Results: {results}"},
                {"role": "user", "content": query},
            ],
        )

        return response.choices[0].message.content

    @staticmethod
    def __get_llm_search_configuration():
        """
        Sets the LLM configuration.
        """
        rules = """
            You are a assistant that helps users find information in a document database. A user asks you a query, and you need to provide the answer based on the search results. Here is the query and the search results:
            You must only answer the query related to the search results.
            You can otmize the query to get better results.
            If the query is not related to the search results, you can respond with "The query is not related to the search results."
            You must only answer the query asked. Do not provide any additional information.
            If you do not know the answer, you can respond with "I could not find the answer."
            If you need more information, you can ask for it.
            Respond in the language of the original query.
            """
        
        return rules

    @staticmethod
    def __get_llm_optimizer_configuration():
        """
        Sets the LLM configuration.
        """
        rules = """
            You are a query optimizer. You have to optimize the given query to improve the performance of the similary search algorithm.
            Exemple: 
            Query: "What is my commition in a sale of 1000$?"
            Optimized Query: "What is the porcentage of my commition in a sale?"
            Write the optimized query in the language of the original query.
            Only return the optimized query.
            """

        return rules
