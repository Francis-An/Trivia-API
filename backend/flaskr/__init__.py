import os
from tkinter.font import ROMAN
from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from pagination import category_history,question_pagination
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Controll-Allowed-Headers','Authorization')
        response.headers.add('Access-Controll-Allowed-Methods','GET,POST,PATCH,DELETE,OPTIONS')
        return response

    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            return jsonify({
                'success' : True,
                'categories' : {category.id: category.type for category in categories}
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    # Method for category history
    def next_page(current_paginate):
        remaining_questions = len(current_paginate) % QUESTIONS_PER_PAGE
        next_page = category_history(request,len(current_paginate),remaining_questions)
        return next_page

    # End poine to get all questions
    @app.route('/questions')
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()

            # Paginate question per page
            current_paginate = question_pagination(request,selection)
            if len(current_paginate) == 0:
                abort(404)

            # category history
            category_history = next_page(current_paginate)

            return jsonify({
                'success' : True,
                'questions' : current_paginate,
                'total_questions' : len(selection),
                'categories' : {category.id: category.type for category in categories},
                'current_category' : category_history
            })
        except:
            abort(404)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            else:
                question.delete()
                questions_left = Question.query.all()
                return jsonify({
                    'success' : True,
                    'id' : question_id,
                    'total_questions' : len(questions_left)
                })
        except:
            abort(400)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    # Adding new question
    @app.route('/questions', methods=['POST'])
    def add_questions():
        body = request.get_json()
        try:
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_category = body.get('category')
            new_difficulty = body.get('difficulty')

            add_new = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty

            )

            add_new.insert()

            selection = Question.query.order_by(Question.id).all()
            # Page pagination when done done add
            current_paginate = question_pagination(request,selection)

            categories = Category.query.order_by(Category.id).all()
            # Category history
            category_history = next_page(current_paginate)

            return jsonify({
                'success' : True,
                'created' : add_new.id,
                'question' : add_new.question,
                'questions' : current_paginate,
                'total_questions' : len(selection),
                'categories' : {category.id: category.type for category in categories},
                'currentCategory' : category_history
            })
        except:
            abort(405)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # Search question
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        try:
            search_term = body.get('searchTerm')
            if search_term is not None:
                if search_term == '':
                    return jsonify({
                        'message' : 'You did not type anythin'
                    })
                else:
                    results = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
                    # current_paginate = question_pagination(request, results)
                    current_paginate = [search.format() for search in results]

                    # Category history
                    category_history = next_page(current_paginate)

                    questions = Question.query.order_by(Question.id).all()
                    # categories = Category.query.order_by(Category.id).all()
                    return jsonify({
                        'success' : True,
                        'questions' : current_paginate,
                        'total_question' : len(current_paginate),
                        'current_category' : category_history
                    })
        except:
            abort(404)

    

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # Getting all question in a specific category
    @app.route('/categories/<int:category_id>/questions')
    def get_specific_category_questions(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                abort(404)
            else:
                category_questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
                category_questions_paginate = question_pagination(request, category_questions)

                # current category history
                # current_category = next_page(category_questions_paginate)

                return jsonify({
                    'success' : True,
                    'questions' : category_questions_paginate,
                    'total_questions' : len(category_questions),
                    'category_id' : category.id,
                    'category_type' : category.type
                })
        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    # Method to filter question for the quize
    def quiz_filtered(previous_question, quiz_category):
        category = Category.query.filter(Category.id == quiz_category).first()
        if category is None:
            abort(404)
        else:
            trivia_questions = Question.query.filter(Question.id.notin_(previous_question),
            Question.category == quiz_category).all()
            return trivia_questions


    #Post to get questions to play the quiz
    @app.route('/quizzes', methods=['POST'])
    def get_questions_to_play_quiz():
        body = request.get_json()
        try:
            previous_question = body.get('previous_questions')
            quiz_category = body.get('quiz_category')['id']

            # array variable to contain all trivia question
            questions = []
            if quiz_category != 0:
               
                questions = quiz_filtered(previous_question, quiz_category)
                randomly_selected_question = None
            else:
                questions = Question.query.filter(Question.id.not_in(previous_question)).all()
            if len(questions)  >= 1:
                # Get random question for the quiz
                random_quiz = random.randrange(0, len(questions))
                randomly_selected_question = questions[random_quiz].format()
            return jsonify({
                'success' : True,
                'question' : randomly_selected_question,
                'total_questions' : len(questions)
            })
        except:
            abort(400)

    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    # Error handler for 404
    @app.errorhandler(404)
    def resource_not_found(error):
        return (jsonify({
            'success' : False,
            'error' : 404,
            'message' : 'Resource not found'
        }), 404)

    # Error handler for 400
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            'success' : False,
            'error' : 400,
            'message' : 'Bad request'
        }),400)

    #Error handler for 405
    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({
            'success' : False,
            'error' : 405,
            'message' : 'Method not allowed'
        }), 405)

    
    #Error handler for 422
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            'success' : False,
            'error' : 422,
            'message' : 'Unprocessable'
        }))

    return app

