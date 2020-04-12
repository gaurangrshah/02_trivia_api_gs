# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

# API

This API is currently under development and can be run locally via:

```shell
curl http://127.0.0.1:5000/<endpoint>
```



## Endpoints

---

### GET /categories

**General**:

- Returns a list of strings representing all available category types

> #### Statuses:
>
> | Status | Message            | Reason                               |
> | ------ | ------------------ | ------------------------------------ |
> | 200    | Success            | if categories are found              |
> | 405    | Method Not Allowed | if incorrect request.method provided |
> | 422    | Not processable    | for any other errors                 |

### Sample:

```json
["Science", "Art", "Geography", "History", "Entertainment", "Sports"]
```

---



### GET /questions

**General**:

- Returns paginated list of dictionaries representing questions, based on category provided.
- if a category is provided, it is used to find the `category_id`, else defaults to `1`

> #### Statuses:
>
> | Status | Message         | Reason                                                |
> | ------ | --------------- | ----------------------------------------------------- |
> | 200    | Success         | if questions are found                                |
> | 405    | Not allowed     | if incorrect request.method provided                  |
> | 404    | Not found       | if category_id is invalid or if max questions reached |
> | 422    | Not processable | for all other errors                                  |



### Sample:

```json
{"categories: ["Science","Art","Geography","History","Entertainment","Sports"],
 "current_category":"Science",
 "questions":[{
 "answer":"Alexander Fleming",
 "category":1,
 "difficulty":3,
 "id":21,
 "question":
 "Who discovered penicillin?"
},{
  "answer":"Blood",
  "category":1,
  "difficulty":4,
  "id":22,
  "question":"Hematology is a branch of medicine involving the study of what?"
}],
"total_questions":3
}
```

---



### DELETE /questions/<int: question_id>

**General**:

- Returns status of 200 if question is successfully deleted
- takes one argument, which is an `int` that represents the `question_id`

> #### Statuses:
>
> | Status | Message         | Reason                                                       |
> | ------ | --------------- | ------------------------------------------------------------ |
> | 200    | Success         | if question is deleted successfully                          |
> | 405    | Not allowed     | if incorrect request.method provided or if invalid question_id |
> | 404    | Not found       | if question_id not found                                     |
> | 422    | Not processable | for all other errors                                         |

### Sample:

```json
{"status":200,"success":true}
```

---



### POST /questions

**General**:

- Returns status of 200 if successful and status 404 if question already exists, or status 422 for all other errors

- requires an object with the following shape: 

  - ```
    {'question': str, 'answer': string, difficult: int, `category`: int}
    ```

    

> #### Statuses:
>
> | Status | Message         | Reason                               |
> | ------ | --------------- | ------------------------------------ |
> | 200    | Success         | if question is added successfully    |
> | 405    | Not allowed     | if incorrect request.method provided |
> | 404    | Not found       | if question already exists           |
> | 422    | Not processable | for all other errors                 |

### Sample:

```json
{"status":200,"success":true}
```

---



### POST /questions/search

**General**:

- Returns a list of paginated objects representing all questions that include the provided `search_term`
- takes a single argument, which is a `string` that represents a `search_term`

> #### Statuses:
>
> | Status | Message         | Reason                           |
> | ------ | --------------- | -------------------------------- |
> | 200    | Success         | if `search_term` has any matches |
> | 405    | Not allowed     | if incorrect request.method      |
> | 422    | Not processable | for all other errors             |

### Sample:

```json
{
  "questions":[{
    "answer":"Alexander Fleming",
    "category":1,
    "difficulty":3,
    "id":21,"question":
    "Who discovered penicillin?"
  }],
  "total_questions":1
}
```

---



### GET /questions/<int: category_id>/questions

**General**:

- Returns list of questions based on provided category_id
- requires an `int` representing the `category_id`

> #### Statuses:
>
> | Status | Message         | Reason                                                 |
> | ------ | --------------- | ------------------------------------------------------ |
> | 200    | Success         | if successfully found questions matching `category_id` |
> | 405    | Not allowed     | if incorrect request.method provided                   |
> | 422    | Not processable | for all other errors                                   |
>
> 

### Sample:

```json
{"categories":["Science","Art","Geography","History","Entertainment","Sports"],
 "current_category":{
   "id":4,
   "type":"History"
 },
 "questions": [{
   "answer":"George Washington Carver",
   "category":4,
   "difficulty":2,
   "id":12,
   "question":"Who invented Peanut Butter?"
 },{
   "answer":"Scarab",
   "category":4,
   "difficulty":4,
   "id":23,
   "question":"Which dung beetle was worshipped by the ancient Egyptians?"
 }],
 "total_questions":2
}
```

---



### POST /quizzes

**General**:

- Returns a single random question from paginated list of all available questions pertaining to current category
- requires one argument, which is an `int` representing the `category_id`

> #### Statuses:
>
> | Status | Message         | Reason                                                 |
> | ------ | --------------- | ------------------------------------------------------ |
> | 200    | Success         | if question is added successfully                      |
> | 405    | Not allowed     | if incorrect request.method provided                   |
> | 422    | Not processable | for all other errors                                   |
> | 500    | Server error    | occurs when the next question in list cannot be loaded |

### Sample:

```json
{"question":{
  "answer":"Alexander Fleming",
  "category":1,
  "difficulty":3,
  "id":21,
  "question":"Who discovered penicillin?"
}}
```

---





## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

> - **NOTE**:  Please be sure to drop the db and create a new db as per the instructions above, between each test run, you may need to stop and start the postgres service if you see any errors
>
> ```shell
> brew services stop postgresql
> ```
>
> ```shell
> brew services start postgresql
> ```
>
> if the above method does not work, you can try:
>
> ```shell
> pg_ctl -D /usr/local/var/postgres stop
> ```
>
> ```shell
> pg_ctl -D /usr/local/var/postgres start
> ```



