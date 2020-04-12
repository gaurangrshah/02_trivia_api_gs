import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'bunty@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.example_question = {
            'question': 'Where in the world is Carment Sandiego?',
            'answer': 'California',
            'difficulty': 1,
            'category': 1
        }

        self.wrong_question = {
            'question': 'Will this work?',
            'answer': 'This should not work',
            'category': 9,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])

    def test_get_questions_with_invalid_category(self):
        res = self.client().get('/questions?category=100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not processable')

    # def test_create_question(self):
    #     res = self.client().post('/questions', json=self.example_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     # print('complete')

    # def test_create_duplicate_question(self):
    #     res = self.client().post('/question', json=self.example_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Not found')

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/47')  # update value after first run
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_delete_question_with_invalid_id(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not allowed')

    def test_delete_question_with_no_id(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not allowed')

    def test_create_question_with_invalid_args(self):
        res = self.client().post('/question', json=self.wrong_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')

    def test_search_questions(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'the'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue((data['total_questions']))

    def test_search_questions_with_no_term(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Not processable')

    def test_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue((data['total_questions']))
        self.assertTrue(data['categories'])
        self.assertTrue((data['current_category']))

    def test_questions_with_invalid_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Not processable')

    def test_start_quiz(self):
        res = self.client().post(
            '/quizzes', json={'previous_questions': [], 'quiz_category': {'id': 1}, })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_404_not_found(self):
        res = self.client().delete('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_405_not_allowed(self):
        res = self.client().get('/questions/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not allowed')

    def test_422_not_processable(self):
        res = self.client().post('/questions', json=self.wrong_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not processable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
