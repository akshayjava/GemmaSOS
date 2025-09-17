"""
Web App Integration Example
Flask web application with integrated crisis response system
"""

from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime
import sys
import os

# Add parent directory to path to import GemmaSOS components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crisis_detector import CrisisDetector
from response_generator import CrisisResponseGenerator
from safety_system import SafetySystem

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

class WebAppWithCrisisSupport:
    def __init__(self):
        """Initialize the web app with crisis support"""
        self.crisis_detector = CrisisDetector()
        self.response_generator = CrisisResponseGenerator()
        self.safety_system = SafetySystem()
        self.conversation_history = {}
    
    def process_message(self, user_id, message):
        """Process user message with crisis detection"""
        try:
            # Validate input
            validation = self.safety_system.validate_input(text=message)
            if not validation["is_safe"]:
                return {
                    "error": "Content cannot be processed safely",
                    "recommendations": validation.get("recommendations", [])
                }
            
            # Detect crisis
            crisis_result = self.crisis_detector.detect_crisis_from_text(message)
            
            # Store in conversation history
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            self.conversation_history[user_id].append({
                "timestamp": datetime.now().isoformat(),
                "user_message": message,
                "crisis_detected": crisis_result["crisis_detected"],
                "confidence": crisis_result["confidence"]
            })
            
            if crisis_result["crisis_detected"]:
                # Generate crisis response
                response = self.response_generator.generate_response(
                    crisis_type=crisis_result.get("primary_category"),
                    user_message=message,
                    confidence=crisis_result["combined_confidence"],
                    immediate_risk=crisis_result["immediate_risk"]
                )
                
                return {
                    "crisis_detected": True,
                    "response": response["response"],
                    "resources": response["resources"],
                    "safety_plan": response.get("safety_plan"),
                    "confidence": crisis_result["combined_confidence"],
                    "risk_level": self.safety_system.assess_risk_level(crisis_result)
                }
            else:
                # Handle normal message
                return {
                    "crisis_detected": False,
                    "response": f"Thanks for your message: {message}",
                    "confidence": 0.0
                }
                
        except Exception as e:
            return {
                "error": f"Processing failed: {str(e)}",
                "crisis_detected": False
            }
    
    def get_conversation_history(self, user_id):
        """Get conversation history for a user"""
        return self.conversation_history.get(user_id, [])
    
    def clear_conversation(self, user_id):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        return True

# Initialize the app
crisis_app = WebAppWithCrisisSupport()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def handle_message():
    """Handle incoming messages"""
    data = request.json
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get or create user session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    
    # Process message
    result = crisis_app.process_message(user_id, message)
    
    return jsonify(result)

@app.route('/api/history')
def get_history():
    """Get conversation history"""
    if 'user_id' not in session:
        return jsonify([])
    
    user_id = session['user_id']
    history = crisis_app.get_conversation_history(user_id)
    return jsonify(history)

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    if 'user_id' not in session:
        return jsonify({"success": False})
    
    user_id = session['user_id']
    success = crisis_app.clear_conversation(user_id)
    return jsonify({"success": success})

@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        "status": "running",
        "privacy": "on_device_only",
        "model_loaded": True,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
