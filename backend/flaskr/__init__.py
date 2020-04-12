import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(reqest, items):
    '''
    Returns a list with paginated items
    Args:
        request: object
        items: list
    Returns:
        available_items: an indexed list of paginated items
    '''
    # get page number from request params:
    page = request.args.get('page', 1, type=int)
    # set starting index (account for 0 index)
    start = (page - 1) * QUESTIONS_PER_PAGE
    # set ending index
    end = start + QUESTIONS_PER_PAGE

    # format
    available_items = [item.format() for item in items]

    return available_items[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    db = SQLAlchemy()

    # ✅ @TODO: Delete the sample route after completing the TODOs
    # ✅ @TODO: Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ✅ @TODO: Use the after_request decorator to set Access-Control-Allow

    @app.after_request  # adds headers to the response
    def after_request(response):
        # allows authorization from headers
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization, true', )

        # specifies which methods are allowed
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response  # sets the response that is sent back to the client
    '''
    ✅ @TODO: Create an endpoint to handle GET requestsfor all available categories.

    Returns: list of all available categories
    '''
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            if not request.method == 'GET':
                abort(405)
            # grab categories list
            all_categories = Category.query.order_by(Category.id).all()
            # return list of strings / type = category name
            categories = [category.type
                          for category in all_categories]
            return jsonify({
                'status_code': 200,
                'success': True,
                'categories': categories,
            })
        except:
            abort(422)

    '''
    ✅ @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    Returns paginated list of question, based on category provided.
    Args:
        category: int
    Returns:
        questions: list of paginated questions
        total_questions: int of number of items in questions
        current_category: str representing the current category
        categories: list of all categories
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():

        if not request.method == 'GET':
            abort(405)
        try:
            # get category by id or set default to 1
            curr_category_id = request.args.get('category', 1, type=int)
            paginated_questions = []
            if curr_category_id:
                curr_category = Category.query.filter(
                    Category.id == curr_category_id).one_or_none()

                if curr_category is None:
                    abort(404)

                questions = Question.query.order_by('id').filter(
                    Question.category == curr_category_id
                ).all()
                paginated_questions = paginate(request, questions)
            else:
                questions = Question.query.all()
                paginated_questions = paginate(request, questions)

            ordered_categories = Category.query.order_by('id').all()
            categories_list = [category.type
                               for category in ordered_categories]

            if len(categories_list) == 0 | len(questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'status_code': 200,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': curr_category.type,
                'categories': categories_list,
            })
        except Exception as e:
            print('⁉️', e)
            abort(422)

    '''
    ✅ @TODO:
    Create an endpoint to DELETE question using a question ID.

    Returns status of 200 if question is successfully deleted
    Args:
        question_id: int representing the id of the question to be deleted
    Returns:
        status: 200
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        if not request.method == 'DELETE':
            abort(405)

        try:
            question = db.session.query(Question).filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            if question:
                db.session.delete(question)
                db.session.commit()

                return jsonify({
                    'status': 200,
                    'success': True
                })
            else:
                return jsonify({
                    'status': 405,
                    'message': 'Not Allowed'
                })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    '''
    ✅ @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    Returns status of 200 if successful and status 404 if question already exists, or status 422 for all other errors
    Args:
        question: str representing the question property
        answer: str representing the answer property
        difficulty: int representing the difficult property
        category: int representing the category property
    Returns:
        status: 200 - when successful
        status: 404 - if item already exists
        status: 422 - for all other errors
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        if not request.method == 'POST':
            abort(405)

        try:
            data = request.get_json()
            question = Question(
                question=str(data['question']),
                answer=str(data['answer']),
                difficulty=int(data['difficulty']),
                category=int(data['category']),
            )

            db_match = db.session.query(Question).filter_by(
                question=question.question).one_or_none()

            if db_match is None:
                db.session.add(question)
                db.session.commit()
                return jsonify({
                    'success': True,
                    'status': 200
                })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close

    '''
    ✅ @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    Returns a list of paginated objects representing all questiones that include the provided search term
    Args:
        search_term: str representing a term to match to all available questions
    Returns:

    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        if not request.method == 'POST':
            abort(405)

        data = request.get_json()
        search_term = data.get('searchTerm')

        if not search_term:
            abort(422)

        try:
            questions = Question.query.filter(
                Question.question.ilike('%{}%'.format(search_term))).all()

            if not questions:
                abort(422)

            paginated_questions = paginate(request, questions)

            return jsonify({
                'success': True,
                'status': 200,
                'questions': paginated_questions,
                'total_questions':  len(paginated_questions)
            })
        except:
            abort(422)

    '''
    ✅ @TODO:
    Create a GET endpoint to get questions based on category.

    Returns list of questions based on provided category_id
    Args:
        category_id: int representing the id of the category to get questions for
    Returns:
        questions: list of objects representing paginated_questions
        total_questions: int representing count of questions
        categories: list of strings representing all category types
        current_category: string representing current category
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_categories(category_id):

        if not request.method == 'GET':
            abort(405)

        try:
            curr_category_id = category_id + 1

            curr_category = Category.query.filter(
                Category.id == curr_category_id).one_or_none()

            all_categories = Category.query.all()
            questions = Question.query.filter(
                Question.category == curr_category_id).all()

            paginated_questions = paginate(request, questions)

            return jsonify({
                "success": True,
                "status": 200,
                "questions": paginated_questions,
                "total_questions": len(paginated_questions),
                "categories": [category.type for category in all_categories],
                "current_category": curr_category.format(),
            })
        except:
            abort(422)

    '''
    ✅ @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    Returns a single random question from paginated list of all available questions pertaining to current category
    Args:
        category_id: int representing selected category
    Returns:
        question: string representing current question for quiz game
    '''
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():

        if not request.method == 'POST':
            abort(405)

        data = request.get_json()
        category_id = int(data['quiz_category']['id']) + 1
        if not category_id:
            abort(422)
        try:

            category = Category.query.get(category_id)
            previous_questions = data["previous_questions"]
            if not category == None:
                if "previous_questions" in data and len(previous_questions) > 0:
                    questions = Question.query.filter(Question.id.notin_(
                        previous_questions), Question.category == category.id).all()
                else:
                    questions = Question.query.filter(
                        Question.category == category.id).all()
            else:
                if "previous_questions" in data and len(previous_questions) > 0:
                    questions = Question.query.filter(
                        Question.id.notin_(previous_questions)).all()
                else:
                    questions = Question.query.all()
            max = len(questions) - 1
            if max > 0:
                question = questions[random.randint(0, max)].format()
            else:
                question = False
            return jsonify({
                'status': 200,
                "success": True,
                "question": question
            })
        except:
            abort(500, 'An error occured while trying to load the next question')

    # ✅ @TODO: Create error handlers for all expected errors including 404 and 422.
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'success': False,
            'message': 'Not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(e):
        return jsonify({
            'success': False,
            'message': 'Not allowed'
        }), 405

    @app.errorhandler(422)
    def not_processable(e):
        return jsonify({
            'success': False,
            'message': 'Not processable'
        }), 422

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

    return app
