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
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        sampleQuestion = Question("DeletethisQuestion", "Answer", "2", 10)
        sampleQuestion.insert()
    
    def tearDown(self):
        """Executed after reach test"""
        questions = Question.query.filter(Question.question == "DeletethisQuestion").all()
        for q in questions:
            q.delete()
        pass

    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success', False))

    def test_get_categories(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success', False))

    def test_delete_question(self):
        question = Question.query.filter(Question.question == "DeletethisQuestion").first()
        res = self.client().delete('/questions/{}'.format(question.id))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data.get('deleted'), question.id)
    
    def test_post_question(self):
        res = self.client().post('/questions', json={"question":"A", "answer":"B", "category":2, "difficulty":1})
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data.get('success'), True)
        self.assertIsNotNone(data.get('question_id'))

    def test_search_question(self):
        searchTerm = "Delete"
        res = self.client().post('/questions', json={"searchTerm": searchTerm})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('total_questions') > 0)
        questions = list(data.get('questions'))
        for question in questions:
            self.assertTrue(searchTerm.lower() in question.get('question').lower())
    
    def test_search_nonexisting(self):
        searchTerm = "This certainly doesnt exist on my db"
        res = self.client().post('/questions', json={"searchTerm": searchTerm})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('total_questions') == 0)
    
    def test_search_category_questions(self):
        res = self.client().get('/categories/2/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('total_questions') > 0)

    def test_quiz(self):
        res = self.client().post('/quizzes', json={"previous_questions": [], "quiz_category": {"id": "2"}})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('question'))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()