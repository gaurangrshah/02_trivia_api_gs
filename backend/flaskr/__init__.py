import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(reqest, items):
    # get page number from request params:
    page = request.args.get('page', 1, type=int)
    # set starting index (account for 0 index)
    start = (page - 1) * QUESTIONS_PER_PAGE
    # set ending index
    end = start + QUESTIONS_PER_PAGE

    # format
    available_items = [item.format() for item in items]

    # print('🚧', available_items[start:end])
    return available_items[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    db = SQLAlchemy()

    # @TODO: Delete the sample route after completing the TODOs ⁉️
    # ✅ @TODO: Set up CORS. Allow '*' for origins.
    CORS(app)

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

    # ✅ @TODO: Create an endpoint to handle GET requestsfor all available categories.
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
                'success': True,
                'categories': categories,
                'status_code': 200
            })
        except:
            abort(422)

    '''
    ✅ @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():

        if not request.method == 'GET':
            abort(405)

        try:
            # get category id or set default to 1
            curr_category_id = request.args.get('category', 1, type=int)
            paginated_questions = []
            if curr_category_id:
                # Query for current category by curr_category_id
                curr_category = Category.query.filter(
                    Category.id == curr_category_id).one_or_none()

                if curr_category is None:
                    # if current category does not exist, abort
                    abort(404)

                questions = Question.query.order_by('id').filter(
                    Question.category == curr_category_id
                ).all()
                paginated_questions = paginate(request, questions)
            else:
                # if curr_category exists query for related questions:
                questions = Question.query.all()
                paginated_questions = paginate(request, questions)

            # query for all categtories, and convert to ordered list of strings:
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

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        if not request.method == 'DELETE':
            abort(405)
        if not question_id:
            abort(400)

        try:
            question = db.session.query(Question).filter(
                Question.id == question_id).first()
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
            print('‼️ failed delete',)
            db.session.rollback()
            abort(400)
        finally:
            db.session.close()

    '''
    ✅ @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        if not request.method == 'POST':
            abort(405)

        try:
            data = request.get_json()
            question = Question(
                question=data['question'],
                answer=data['answer'],
                difficulty=data['difficulty'],
                category=data['category'],
            )

            if not question.question and question.answer and question.difficulty and question.category:
                print('cannot create, missing field')
                abort(422)

            db_match = db.session.query(Question).filter_by(
                question=question.question).one_or_none()

            print(db_match)
            if db_match is None:
                print('adding...')
                db.session.add(question)
                db.session.commit()
                return jsonify({
                    'success': True,
                    'status': 200
                })
            else:
                print('setting fail, found db match')
                return jsonify({
                    'success': False,
                    'status': 404,
                    'message': 'Not found'
                })
        except:
            print('testing abort')
            db.session.rollback()
            abort(422)
        finally:
            db.session.close

    '''
    ✅ @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions', methods=['POST'])
    def search_questions():
        if not request.method == 'POST':
            abort(404)
        try:
            data = request.get_json()
            search_term = data.get('searchTerm')
            questions = Question.query.filter(
                Question.question.ilike('%{}%'.format(search_term))).all()

            paginated_questions = paginate(request, questions)

            return jsonify({
                'success': True,
                'status': 200,
                'questions': paginated_questions,
            })
        except:
            print('aborting search')
            abort(422)

    '''
    ✅ @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_categories(category_id):

        if not request.method == 'GET':
            abort(405)

        try:
            curr_category_id = category_id + 1

            curr_category = Category.query.filter(
                Category.id == curr_category_id).one_or_none()
            print(curr_category)

            all_categories = Category.query.all()
            questions = Question.query.filter(
                Question.category == curr_category_id).all()

            paginated_questions = paginate(request, questions)
            print('getting question by category', type(paginated_questions))

            return jsonify({
                "success": True,
                "status": 200,
                "questions": paginated_questions,
                "totalQuestions": len(paginated_questions),
                "categories": [category.type for category in all_categories],
                "currentCategory": curr_category.format(),
            })
        except:
            abort(422)

    '''
    🚧 @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():

        if not request.method == 'POST':
            abort(405)

        try:
            data = request.get_json()

            category_id = int(data['quiz_category']['id'])
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
                "success": True,
                "question": question
            })
        except:
            abort(500, "An error occured while trying to load the next question")

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
        print(e)
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
