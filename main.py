import os
import vertexai

from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    GenerationConfig,
    Part,
    Tool,
)

from utils import (
    get_book_id_by_title,
    get_books_for_author,
    get_num_in_stock_for_book,
)


vertexai.init(project=os.environ["GOOGLE_PROJECT_ID"], location="us-central1")

GET_BOOK_BY_AUTHOR = "get_books_for_author"
GET_BOOK_ID_BY_TITLE = "get_book_id_by_title"
GET_NUM_IN_STOCK_FOR_BOOK = "get_num_in_stock_for_book"

# Specify a function declaration and parameters for an API request
get_authors_for_book_func = FunctionDeclaration(
    name=GET_BOOK_BY_AUTHOR,
    description="Get a list of book names for an author.",
    parameters={
        "type": "object",
        "properties": {
            "first_name": {
                "type": "string",
                "description": "The first name of the author",
            },
            "last_name": {
                "type": "string",
                "description": "The last name of the author",
            },
        },
    },
)

get_book_id_by_title_func = FunctionDeclaration(
    name=GET_BOOK_ID_BY_TITLE,
    description="Get a unique id for a book title or name. Takes a single name or title and returns an integer which is the id.",
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The title or name of the book.",
            },
        },
    },
)

get_num_in_stock_for_book_func = FunctionDeclaration(
    name=GET_NUM_IN_STOCK_FOR_BOOK,
    description="Retrieve how many books are in stock or available.",
    parameters={
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "The name or title for the book which stock should be requested..",
            },
        },
    },
)


# Define a tool that includes the above function
tools = Tool(
    function_declarations=[
        get_authors_for_book_func,
        get_book_id_by_title_func,
        get_num_in_stock_for_book_func,
    ],
)

# Initialize Gemini model
model = GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=GenerationConfig(temperature=0),
    tools=[tools],
)

# Start a chat session
chat_session = model.start_chat()


def send_message(message: str):

    response_1 = chat_session.send_message(message)
    function_calls = response_1.candidates[0].function_calls

    api_responses = []
    if function_calls:
        api_responses = []
        for func in function_calls:
            if func.name == GET_BOOK_BY_AUTHOR:
                api_responses.append(
                    {
                        "name": func.name,
                        "content": get_books_for_author(
                            first_name=func.args["first_name"],
                            last_name=func.args["last_name"],
                        ),
                    }
                )
            elif func.name == GET_BOOK_ID_BY_TITLE:
                api_responses.append(
                    {
                        "name": func.name,
                        "content": get_book_id_by_title(
                            title=func.args["title"],
                        ),
                    }
                )
            elif func.name == GET_NUM_IN_STOCK_FOR_BOOK:
                api_responses.append(
                    {
                        "name": func.name,
                        "content": get_num_in_stock_for_book(
                            title=func.args["title"],
                        ),
                    }
                )

        # Return the API response to Gemini
        for api_response in api_responses:
            name = api_response.pop("name")
            response = chat_session.send_message(
                [
                    Part.from_function_response(
                        name=name,
                        response=api_response,
                    )
                ]
            )
            try:
                print(response.text)
            except ValueError:
                print("no output")


while True:
    m = input()
    send_message(m)

# Which books are written by Guenther Hendriks?
# How many copies of the first of those books are available?
# What are the ids of those books?
