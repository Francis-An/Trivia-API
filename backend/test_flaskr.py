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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','$Kwaku4671','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # New question
    new_question = {
        'question' : 'Who is the best player?',
        'answer' : 'Ronaldo',
        'category' : 6,
        'difficulty' : 3
    }

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
 
    # Test case behaviours for trivia API

    #Test case method to test the behaviour of get all catagories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


    
    # Test case method to test the behaviour of getting questions of category and paginated in 10
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    # Test case method to get the pagination of questions
    def test_questions_pagination(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])


    #Test case method to get invalid pagination
    def test_404_invalid_pagination(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    #Test case method to test the deletion of question with the given id
    def test_delete_question(self):
        res = self.client().delete('/questions/41')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['id'],41)

    #Test case method to test the error when the id does not exist
    def test_400_bad_request(self):
        res = self.client().delete('/questions/41')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Bad request')

    
    # Test case method to test the adding of new question
    def test_add_question(self):
        res = self.client().post('/questions', json = self.new_question)
        data = json.loads(res.data)

        new_question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['created'], new_question.id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    # Test case method to handle not allowed error when add a question
    def test_405_method_used_to_add_question_not_allowed(self):
        res = self.client().post('/questions/3', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')


    # Test case method to test the behaviour of searching a question
    def test_search_question(self):
        res = self.client().post('/questions', json={'search' : 'player'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #Test case method to test the search of question that doesn't exit in the database
    def test_search_question_not_exist(self):
        res = self.client().post('/questions', json={'search' : '##dljdhesl'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    #Test case method to test how to get questions based on categor
    def test_questions_in_specific_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('total_questions')
        self.assertTrue(len(data['questions']))


    #Test case method to test the quize game play
    def test_get_question_for_quiz(self):
        res = self.client().post('/quizzes', 
        json={'previous_questions': [], 
              'quiz_category': {'type':'Science', 'id':2}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


    #Test case method to test the quize game play failed
    def test_400_quiz_game_play_failed(self):
        res = self.client().post('/quizzes', json={'previous_questions':[],
                'quiz_category':{'type':'Science','id':'100'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        # self.assertEqual(data['message'], 'Method not allowed')

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()