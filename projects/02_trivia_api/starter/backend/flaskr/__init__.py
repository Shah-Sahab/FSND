import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS(app, resource={ r'/api/*': { 'origins': '*' } })
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    return response

  """
  Create an endpoint to handle GET requests 
  for all available categories.
  """
  @app.route('/categories', methods=['GET'])
  # @cross_origin()
  def get_all_categories():
    # selection =  Category.query.with_entities(Category.type).all()
    selection =  Category.query.all()

    if selection is None:
      abort(404)
    # categories = [category.format() for category in selection]
    categories = { category.id: category.type for category in selection }
    response = jsonify({
      'success': True,
      'count': len(categories),
      'categories': categories
    })
    return response


  '''
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
    page = request.args.get('page', 1, type=int)
    # Return all the Questions
    selection = Question.query.all()
    # Pagination - Define Start
    start = (page - 1) * QUESTIONS_PER_PAGE
    # Pagination - Define End.
    end = start + QUESTIONS_PER_PAGE
    # Format all the questions.
    formatted_questions = [question.format() for question in selection]
    # Jsonify the response. Add Success, questions, totalQuestions, categories. Current Category will be empty as of this moment.
    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'totalQuestions': len(formatted_questions[start:end]),
      # 'categories': [{category.id: category.type} for category in Category.query.all()],
      # 'categories': [category.format() for category in Category.query.all()],
      'categories': [category for category in Category.query.with_entities(Category.type).all()],
      'currentCategory': ' '
    })


  """
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """
  '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_or_search_question():
    # This method completes two purposes. Looks for the searchTerm 
    # and see if the search already exist. If not add the question 
    # to the Questions Model in DB.
    search_term = request.json.get('searchTerm')
    # print(f'Search Term: {search_term}')
    if search_term:
      print(f'My Search Term => {search_term}')
      questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
      return jsonify({
        'questions': [question.format() for question in questions],
        'totalQuestions': len(questions),
        'currentCategory': ''
      })
  
    print(f'No Search Term')
    # Get all parameters.
    question = request.json.get('question')
    answer = request.json.get('answer')
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')
    # If no params exist, abort(404) Not found.
    if not (question and answer and category and difficulty):
        return abort(400, 'Required question object keys missing from request body')
    
    # Else create a new question
    new_question = Question(question, answer, category, difficulty)
    new_question.insert()

    # Print Statement
    print(f' Question: {question}, answer: {answer}, difficulty: {difficulty}, category: {category} ')

    # Jsonify the response
    return jsonify({
      'question': new_question.format()
    })
    

  """
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """
  @app.route('/delete/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)
      # db.session.delete(question)
      question.delete()
      db.session.commit()
    except:
      print(sys.exc_info())
      db.session.rollback()
    finally:
      db.session.close()

  

  """
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """
  @app.route('/categories/<int:category_id>/questions')
  def get_question_by_category(category_id):
    """ 
    For some reason instead of sending an ID from frontend we receive an index. 
    index starts at 0 while the id starts at 1. adding +1 to any index creates the actual category.
    """
    actual_category_id = category_id + 1
    selection = Question.query.filter(Question.category == actual_category_id).all()
    print(f'questions => {selection}')
    if not (selection):
      abort(404)

    filtered_questions = [question.format() for question in selection]
    category = Category.query.get(actual_category_id)  
    return jsonify({
      'questions': filtered_questions,
      'totalQuestions': Question.query.count(),
      'currentCategory': category.type
    })


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

  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    previous_questions = request.json.get('previous_questions')
    quiz_category = request.json.get('quiz_category')
    print(f'questions => {previous_questions}, quiz_category=> {quiz_category}')
    # Selection changes based on what category has been selected.
    selection = None
    # Get everything if All is selected in UI
    if quiz_category.get('id') == 0:
      selection = Question.query.all()  
    else: # else just pick the questions from the given category.
      selection = Question.query.filter(Question.category == quiz_category.get('id')).all()
    questions = [sq.format() for sq in selection]
    rand = generate_random(len(questions))
    random_selected_question = questions[rand]
    print(f'Random Selected Question => {random_selected_question}')
    while previous_questions and random_selected_question in previous_questions:
      rand = generate_random(len(questions))
      # If questions[rand] matches the above criteria,
      # break loop, return the randomly selected question.
      if questions[rand] not in previous_questions:
        random_selected_question = questions[rand]
        break
      else:
        continue
      
    return jsonify({
      'previousQuestions': previous_questions,
      'question': random_selected_question
    })
    

  def generate_random(limiters_length):
    return random.randint(0, limiters_length - 1)

  """
  Create error handlers for all expected errors 
  including 404 and 422. 
  """
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Unprocessable Entity'
    }), 422
  
  return app

    