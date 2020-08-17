import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    @app.route('/categories')
    def get_categories():
        data = Category.query.all()
        dictCategories = {}
        for category in data:
            dictCategories[category.id] = category.type
        return jsonify({
            'categories': dictCategories,
            'success': True
        }), 200

    @app.route('/questions')
    def get_questions():
        page = int(request.args.get('page', 1))
        data = Question.query.all()
        res = list(map(lambda e: e.format(), data))

        catData = Category.query.all()
        dictCategories = {}
        for category in catData:
            dictCategories[category.id] = category.type
        return jsonify({
            'questions': res[(page - 1) * QUESTIONS_PER_PAGE:page * QUESTIONS_PER_PAGE],
            'success': True,
            'total_questions': len(res),
            'categories': dictCategories,
            'current_category': 0
        }), 200

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter_by(id=id).first()
        try:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question.id
            }), 200
        except BaseException:
            print(sys.exc_info())
            return jsonify({
                'success': False
            }), 422

    @app.route('/questions', methods=['POST'])
    def post_question():
        data = request.get_json()
        response = None
        if data.get('searchTerm') is not None:
            response = search_question(data)
        else:
            response = create_question(data)
        return response

    def create_question(data):
        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        difficulty = data.get('difficulty')
        if question is None or answer is None or category is None or difficulty is None:
            abort(400)
        try:
            q = Question(question, answer, category, difficulty)
            q.insert()
            return jsonify({
                'success': True,
                'question_id': q.id
            }), 201
        except BaseException:
            print(sys.exc_info())
            return jsonify({
                'success': False
            }), 400

    def search_question(data):
        search_term = data.get('searchTerm')
        if search_term is None:
            abort(400)
        try:
            questions = Question.query.filter(
                Question.question.ilike(
                    '%{}%'.format(search_term))).all()
            questions = list(map(lambda e: e.format(), questions))
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': 0
            }), 200
        except BaseException:
            return jsonify({
                'success': False
            }), 400

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            questions = list(map(lambda e: e.format(), questions))
            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': len(questions),
                'current_category': category_id
            }), 200
        except BaseException:
            return jsonify({
                'success': False
            }), 422

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        data = request.get_json()
        prev_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category', 0)
        try:
            query = Question.query.filter(Question.id.notin_(prev_questions))
            if quiz_category.get('id') is not 0:
                query = query.filter(
                    Question.category == quiz_category.get('id'))
            res = query.all()
            if(len(res) == 0):  # Less than 5 questions on category
                return jsonify({
                    'success': True
                }), 200
            idx = random.randint(0, len(res) - 1)
            question = res[idx].format()
            return jsonify({
                'success': True,
                'question': question
            }), 200
        except BaseException:
            print(sys.exc_info())
            return jsonify({
                'success': False,
                'message': "Not able to get a new quiz question"
            }), 400

    @app.errorhandler(400)
    def handle_request_error(e):
        return jsonify({
            'success': False,
            'message': "Request error!"
        }), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({
            'success': False,
            'message': "This resource was not found"
        }), 404

    @app.errorhandler(422)
    def handle_unprocessable(e):
        return jsonify({
            'success': False,
            'message': "Unable to proccess this request"
        }), 422

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({
            'success': False,
            'message': "Internal error!"
        }), 500

    return app
