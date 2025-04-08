from flask import render_template, request, jsonify
from gemini_api import get_gemini_response

def setup_routes(app):
    # Main index route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Simple chatbot response
    @app.route('/simple_chat', methods=['POST'])
    def simple_chat():
        user_message = request.json['message']
        response = f"Simple Bot says: {user_message}"  # Simple echo response
        return jsonify({'response': response})

    # Route for advanced chatbot page
    @app.route('/advanced_chat')
    def advanced_chat():
        return render_template('advanced_chatbot.html')

    # API route for advanced chatbot using Gemini API
    @app.route('/gemini_chat', methods=['POST'])
    def gemini_chat():
        user_message = request.json['message']
        response_text = get_gemini_response(user_message)
        return jsonify({'response': response_text})
