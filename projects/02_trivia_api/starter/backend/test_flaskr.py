import os
import unittest
import json
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
import functools
import pdb
import traceback


def debug_on(*exceptions):
    if not exceptions:
        exceptions = (AssertionError, )
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions:
                info = sys.exc_info()
                traceback.print_exception(*info) 
                pdb.post_mortem(info[2])
        return wrapper
    return decorator


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    QUESTIONS_PER_PAGE = 10

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = Question('WHats Down?', 'Nothings Down :p', '4', '4')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass
        # self.db.session.remove()
        # self.db.drop_all()

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['count'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)

    def test_get_questions_on_page2(self):
        params = {'page': 2}
        res = self.client().get('/questions', query_string=params)
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertEqual(data['success'], True)

    def test_searching_question(self):
        params = { 'searchTerm': 'Test' }
        response = self.client().post('/questions', data=json.dumps(params), content_type='application/json')
        # data = json.loads(response.decode('utf-8'))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['questions'])

    def test_adding_search_question(self):
        params = { 'searchTerm': 'Lead Brown Tester' }
        response = self.client().post('/questions', data=json.dumps(params), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data['questions'])

    def test_add_question(self):
        content = {
            'question': self.new_question.question,
            'answer': self.new_question.answer,
            'difficulty': self.new_question.difficulty,
            'category': self.new_question.category
        }
        response = self.client().post('/questions', json=content, content_type='application/json')
        question = Question.query.filter(Question.question == self.new_question.question).one_or_none()
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_get_question_by_category(self):
        category_id = '2'
        endpoint = f'categories/{category_id}/questions'
        response = self.client().get(endpoint)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])

    def test_get_question_by_category_404(self):
        category_id = '7'
        endpoint = f'categories/{category_id}/questions'
        response = self.client().get(endpoint)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_delete_question(self):
        question_id = '28'
        response = self.client().delete(f'/delete/{question_id}')
        data = json.loads(response.data)
        question = Question.query.get(question_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], question_id)
        self.assertEqual(question, None)

    def test_quizzes_with_quiz_category(self):
        headers = {
            'Content-Type': 'application/json'
        }
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Science',
                'id': 1
            }
        }
        response = self.client().post('/quizzes', json=post_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])
    
    def test_quizzes_without_quiz_category(self):
        headers = {
            'Content-Type': 'application/json'
        }
        content = {
            'previous_questions': [],
            'quiz_category': {
                'type': ' ',
                'id': 0
            }
        }
        response = self.client().post('/quizzes', json=content, headers=headers)
        print(f'Response :: {response}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])


if __name__ == "__main__":
    unittest.main()
