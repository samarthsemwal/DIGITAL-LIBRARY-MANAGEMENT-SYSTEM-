from flask import Blueprint, jsonify, request

# Define chatbot blueprint
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

# 🧠 Simple rule-based chatbot (AI Assistant)
responses = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! Ask me about books, borrowing, or fines.",
    "borrow": "To borrow a book, go to Dashboard and click 'Borrow'.",
    "return": "To return a book, go to 'My Books' and click 'Return'.",
    "fine": "A fine of ₹5 per day applies after the due date.",
    "admin": "The admin can view all borrow logs and manage books.",
    "available": "You can check available books in your dashboard.",
    "hours": "The library is open 9 AM to 5 PM, Monday to Saturday.",
    "author": "You can search books by author in the dashboard search bar.",
    "category": "Books are divided into categories like Fiction, Science, etc.",
    "email": "We send email alerts for due dates and important notices.",
    "reset": "If you forgot your password, please contact admin for reset.",
    "help": "You can ask me about library hours, fines, or borrowing process.",
    "default": "I'm not sure about that. Try asking about borrowing, returning, or fines."
}


@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    """Handles chatbot queries."""
    data = request.get_json()
    user_message = data.get('message', '').lower()

    response = None
    for key, reply in responses.items():
        if key in user_message:
            response = reply
            break

    if not response:
        response = responses["default"]

    return jsonify({"reply": response})
