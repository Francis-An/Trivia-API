# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

### API Reference

### Getting started
	Base URL: Currently, this app can only runs locally and is not hosted as a based URL. The backend
	app is hosted at the default, http://127.0.0.1:5000/ which is set as a proxy in the frontend 
	configuration.
	Authentication: This application does not yet require authentication or an API key.
### Errors
	Errors are presented as the following JSON object:
  ```json
	{
		"success" : False,
		"error" : 405,
		"message" : "Method not allowed"
	}
  ```

	The API will return four request error types when request fail
		400 Bad request           || request sent by client has a malformed syntax.

		422 Unprocessable         || indicates that the server understands the content type of the request entity, and the syntax of the request entity is correct, but it was unable to process the contained instructions.

		404 Resource not found    || ndicates that the server cannot find the requested resource.

		405 Method not allowed    || indicates that the server knows the request method, but the target resource doesn't support this method.

### Resource endpoint Library
  GET '/categories'
		General:
			List of categories object, success, and values are returned. 
			Sample curl http://127.0.0.1:500/categories

      ```json
      {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
        "success": true
      }
      ```

	GET '/questions'
		General:
			List of questions objects, categories object, success value, current_category, and total number of questions are returned. 
			Results are paginated in groups of ten as well. Include an argument asking for the page number to begin with 1.
			Sample curl http://127.0.0.1:500/questions

      ```json
        {
            "categories": {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports"
            },
            "current_category": "http://127.0.0.1:5000/questions?page=2",
            "questions": [
                {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                },
                {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 4,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
                },
                {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
                },
                
            ],
            "success": true,
            "total_questions": 23
            }
        
      ```
        

  GET '/categories/{category_id}/questions'
		General:
      Returns objects of questions of a specific category, success value, current_category, and total number of questions in that category are returned. 

      Sample curl http://127.0.0.1:500/categories/6/questions

      ```json
        {
                "category_id": 6,
                "category_type": "Sports",
                "questions": [
                    {
                    "answer": "Brazil",
                    "category": 6,
                    "difficulty": 3,
                    "id": 10,
                    "question": "Which is the only team to play in every soccer World Cup tournament?"
                    },
                    {
                    "answer": "Uruguay",
                    "category": 6,
                    "difficulty": 4,
                    "id": 11,
                    "question": "Which country won the first ever soccer World Cup in 1930?"
                    },
                    {
                    "answer": "Man United",
                    "category": 6,
                    "difficulty": 4,
                    "id": 66,
                    "question": "Which team do Ronald plays?"
                    },
                    {
                    "answer": "Real Madrid",
                    "category": 6,
                    "difficulty": 3,
                    "id": 67,
                    "question": "Which tearm won the champions league in 2022"
                    },
                    {
                    "answer": "Messi",
                    "category": 6,
                    "difficulty": 3,
                    "id": 68,
                    "question": "Who is the best prayer?"
                    }
                ],
                "success": true,
                "total_questions": 7
            }
        
      ```
      
        
      
	POST '/questions'
		General:
			Use the submitted question, answer, category, and difficulty to create a new question. Updates the front end by returning the ID of the newly generated question, the question, the total number of questions, a success value, and a list of questions and it's paginated by 10 based on the current page number.

			Sample  curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"What work do Ronaldo do?", "answer":"Played football","category":"6", "difficulty":"3"}'

      ```json
			{
                  "categories": {
                    "1": "Science",
                    "2": "Art",
                    "3": "Geography",
                    "4": "History",
                    "5": "Entertainment",
                    "6": "Sports"
                    },
                    "created": 72,
                    "currentCategory": "http://127.0.0.1:5000/questions?page=1",
                    "question": "What work do Ronaldo do?",
                    "questions": [
                        {
                        "answer": "Man United",
                        "category": 6,
                        "difficulty": 4,
                        "id": 66,
                        "question": "Which team do Ronald plays?"
                        },
                        {
                        "answer": "Real Madrid",
                        "category": 6,
                        "difficulty": 3,
                        "id": 67,
                        "question": "Which tearm won the champions league in 2022"
                        },
                        {
                        "answer": "Messi",
                        "category": 6,
                        "difficulty": 3,
                        "id": 68,
                        "question": "Who is the best prayer?"
                        },
                        {
                        "answer": "Played football",
                        "category": 6,
                        "difficulty": 3,
                        "id": 72,
                        "question": "What work do Ronaldo do?"
                        }
                    ],
                    "success": true,
                    "total_questions": 24
            }
      ```


	DELETE '/questions/{question_id}'
		General:
			if it exists, deletes the question with the specified id. Returns the success value, the total number of questions left, and the ID of the deleted book.
			curl -X DELETE  http://127.0.0.1:500/questions/71 

      ```json
        {
          "id": 71,
          "success": true,
          "total_questions": 23
        }
      ```

	POST '/questions/search'
		General:
      search is a string argument we pass in the parameter to search for questions. Returns objects of any questions for whom the search term is a substring of the question passed in the parameter paginated by ten, success value, total questions of the results, and the current_category.

      Sample  curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}' 

      ```json
        "current_category": "http://127.0.0.1:5000/questions?page=1",
        {
          "questions": [
            {
              "answer": "Maya Angelou",
              "category": 4,
              "difficulty": 2,
              "id": 5,
              "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
              "answer": "Edward Scissorhands",
              "category": 5,
              "difficulty": 3,
              "id": 6,
              "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }
          ],
          "success": true,
          "total_question": 2
        }

      ```

    GET '/quizzes'
        General
            The guiz game play will give users random set of questions to at a time without repeating the previous questions. 
            'quiz_category' : Is a dictionary that contian the category id.
            'previous_questions' : A list that will contain the IDs of the previous questions.
            This endpoint returns a question object, success value, and total number of questions in the current category.

            Sample  curl http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"id":"2"}}'

            ```json
                {
                  "question": {
                      "answer": "Escher",
                      "category": 2,
                      "difficulty": 1,
                      "id": 16,
                      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
                  },
                  "success": true,
                  "total_questions": 4
                }

            ```

           


### Authors
	Yours truly, Annor Francis Yeboah - Udacity FullStack Nanodegree Student.

### Acknowledgements
	Many thanks to Udacity's fantastic staff and all of the aspiring full-stack superstars students!



## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
