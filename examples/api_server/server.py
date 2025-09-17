"""
API Server Integration Example
RESTful API server with integrated crisis response system
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
import sys
import os
import logging

# Add parent directory to path to import GemmaSOS components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crisis_detector import CrisisDetector
from response_generator import CrisisResponseGenerator
from safety_system import SafetySystem

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

class CrisisAPIServer:
    def __init__(self):
        """Initialize the API server with crisis support"""
        self.crisis_detector = CrisisDetector()
        self.response_generator = CrisisResponseGenerator()
        self.safety_system = SafetySystem()
        self.active_sessions = {}
        self.analytics = {
            "total_requests": 0,
            "crisis_detections": 0,
            "false_positives": 0,
            "response_times": []
        }
    
    def process_text(self, text, session_id=None):
        """Process text input for crisis detection"""
        start_time = datetime.now()
        
        try:
            # Validate input
            validation = self.safety_system.validate_input(text=text)
            if not validation["is_safe"]:
                return {
                    "success": False,
                    "error": "Content cannot be processed safely",
                    "recommendations": validation.get("recommendations", [])
                }
            
            # Detect crisis
            crisis_result = self.crisis_detector.detect_crisis_from_text(text)
            
            # Update analytics
            self.analytics["total_requests"] += 1
            if crisis_result["crisis_detected"]:
                self.analytics["crisis_detections"] += 1
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()
            self.analytics["response_times"].append(response_time)
            
            # Keep only last 100 response times
            if len(self.analytics["response_times"]) > 100:
                self.analytics["response_times"] = self.analytics["response_times"][-100:]
            
            if crisis_result["crisis_detected"]:
                # Generate crisis response
                response = self.response_generator.generate_response(
                    crisis_type=crisis_result.get("primary_category"),
                    user_message=text,
                    confidence=crisis_result["combined_confidence"],
                    immediate_risk=crisis_result["immediate_risk"]
                )
                
                # Store session data if provided
                if session_id:
                    self._store_session_data(session_id, text, crisis_result, response)
                
                return {
                    "success": True,
                    "crisis_detected": True,
                    "crisis_type": crisis_result.get("primary_category"),
                    "confidence": crisis_result["combined_confidence"],
                    "immediate_risk": crisis_result["immediate_risk"],
                    "response": response["response"],
                    "resources": response["resources"],
                    "safety_plan": response.get("safety_plan"),
                    "risk_level": self.safety_system.assess_risk_level(crisis_result),
                    "response_time": response_time
                }
            else:
                return {
                    "success": True,
                    "crisis_detected": False,
                    "confidence": crisis_result["confidence"],
                    "message": "No crisis indicators detected",
                    "response_time": response_time
                }
                
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            return {
                "success": False,
                "error": f"Processing failed: {str(e)}"
            }
    
    def process_image(self, image_path, session_id=None):
        """Process image input for crisis detection"""
        start_time = datetime.now()
        
        try:
            # Validate input
            validation = self.safety_system.validate_input(image_path=image_path)
            if not validation["is_safe"]:
                return {
                    "success": False,
                    "error": "Image cannot be processed safely",
                    "recommendations": validation.get("recommendations", [])
                }
            
            # Detect crisis
            crisis_result = self.crisis_detector.detect_crisis_from_image(image_path)
            
            # Update analytics
            self.analytics["total_requests"] += 1
            if crisis_result["crisis_detected"]:
                self.analytics["crisis_detections"] += 1
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()
            self.analytics["response_times"].append(response_time)
            
            return {
                "success": True,
                "crisis_detected": crisis_result["crisis_detected"],
                "indicators": crisis_result.get("indicators", []),
                "confidence": crisis_result["confidence"],
                "response_time": response_time
            }
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return {
                "success": False,
                "error": f"Image processing failed: {str(e)}"
            }
    
    def process_multimodal(self, text=None, image_path=None, session_id=None):
        """Process multimodal input for crisis detection"""
        start_time = datetime.now()
        
        try:
            # Validate input
            validation = self.safety_system.validate_input(text=text, image_path=image_path)
            if not validation["is_safe"]:
                return {
                    "success": False,
                    "error": "Content cannot be processed safely",
                    "recommendations": validation.get("recommendations", [])
                }
            
            # Detect crisis
            crisis_result = self.crisis_detector.detect_multimodal_crisis(text=text, image=image_path)
            
            # Update analytics
            self.analytics["total_requests"] += 1
            if crisis_result["crisis_detected"]:
                self.analytics["crisis_detections"] += 1
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()
            self.analytics["response_times"].append(response_time)
            
            if crisis_result["crisis_detected"]:
                # Generate crisis response
                response = self.response_generator.generate_response(
                    crisis_type=crisis_result.get("primary_category"),
                    user_message=text or "",
                    confidence=crisis_result["combined_confidence"],
                    immediate_risk=crisis_result["immediate_risk"]
                )
                
                # Store session data if provided
                if session_id:
                    self._store_session_data(session_id, text, crisis_result, response)
                
                return {
                    "success": True,
                    "crisis_detected": True,
                    "crisis_type": crisis_result.get("primary_category"),
                    "confidence": crisis_result["combined_confidence"],
                    "immediate_risk": crisis_result["immediate_risk"],
                    "text_analysis": crisis_result.get("text_analysis"),
                    "image_analysis": crisis_result.get("image_analysis"),
                    "response": response["response"],
                    "resources": response["resources"],
                    "safety_plan": response.get("safety_plan"),
                    "risk_level": self.safety_system.assess_risk_level(crisis_result),
                    "response_time": response_time
                }
            else:
                return {
                    "success": True,
                    "crisis_detected": False,
                    "confidence": crisis_result["combined_confidence"],
                    "message": "No crisis indicators detected",
                    "response_time": response_time
                }
                
        except Exception as e:
            logger.error(f"Error processing multimodal input: {e}")
            return {
                "success": False,
                "error": f"Processing failed: {str(e)}"
            }
    
    def _store_session_data(self, session_id, text, crisis_result, response):
        """Store session data for analytics"""
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {
                "created_at": datetime.now(),
                "interactions": []
            }
        
        self.active_sessions[session_id]["interactions"].append({
            "timestamp": datetime.now().isoformat(),
            "text_length": len(text) if text else 0,
            "crisis_detected": crisis_result["crisis_detected"],
            "confidence": crisis_result["combined_confidence"],
            "crisis_type": crisis_result.get("primary_category")
        })
    
    def get_analytics(self):
        """Get privacy-safe analytics"""
        avg_response_time = 0
        if self.analytics["response_times"]:
            avg_response_time = sum(self.analytics["response_times"]) / len(self.analytics["response_times"])
        
        return {
            "total_requests": self.analytics["total_requests"],
            "crisis_detections": self.analytics["crisis_detections"],
            "false_positives": self.analytics["false_positives"],
            "average_response_time": round(avg_response_time, 3),
            "active_sessions": len(self.active_sessions),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_session_data(self, session_id):
        """Get session data"""
        return self.active_sessions.get(session_id, {})
    
    def cleanup_old_sessions(self, max_age_hours=24):
        """Clean up old sessions"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        sessions_to_remove = [
            sid for sid, data in self.active_sessions.items()
            if data["created_at"] < cutoff_time
        ]
        
        for sid in sessions_to_remove:
            del self.active_sessions[sid]
        
        return len(sessions_to_remove)

# Initialize the API server
api_server = CrisisAPIServer()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze text for crisis indicators"""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({
            "success": False,
            "error": "Text input required"
        }), 400
    
    text = data['text'].strip()
    session_id = data.get('session_id')
    
    if not text:
        return jsonify({
            "success": False,
            "error": "Text cannot be empty"
        }), 400
    
    result = api_server.process_text(text, session_id)
    return jsonify(result)

@app.route('/api/analyze/image', methods=['POST'])
def analyze_image():
    """Analyze image for crisis indicators"""
    data = request.json
    
    if not data or 'image_path' not in data:
        return jsonify({
            "success": False,
            "error": "Image path required"
        }), 400
    
    image_path = data['image_path']
    session_id = data.get('session_id')
    
    if not os.path.exists(image_path):
        return jsonify({
            "success": False,
            "error": "Image file not found"
        }), 400
    
    result = api_server.process_image(image_path, session_id)
    return jsonify(result)

@app.route('/api/analyze/multimodal', methods=['POST'])
def analyze_multimodal():
    """Analyze multimodal input for crisis indicators"""
    data = request.json
    
    if not data or ('text' not in data and 'image_path' not in data):
        return jsonify({
            "success": False,
            "error": "Text or image input required"
        }), 400
    
    text = data.get('text', '').strip()
    image_path = data.get('image_path')
    session_id = data.get('session_id')
    
    if not text and not image_path:
        return jsonify({
            "success": False,
            "error": "At least one input (text or image) required"
        }), 400
    
    result = api_server.process_multimodal(text, image_path, session_id)
    return jsonify(result)

@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session data"""
    session_data = api_server.get_session_data(session_id)
    return jsonify(session_data)

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get privacy-safe analytics"""
    analytics = api_server.get_analytics()
    return jsonify(analytics)

@app.route('/api/cleanup', methods=['POST'])
def cleanup_sessions():
    """Clean up old sessions"""
    data = request.json or {}
    max_age_hours = data.get('max_age_hours', 24)
    
    cleaned_count = api_server.cleanup_old_sessions(max_age_hours)
    
    return jsonify({
        "success": True,
        "cleaned_sessions": cleaned_count,
        "max_age_hours": max_age_hours
    })

@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get crisis resources"""
    crisis_type = request.args.get('type', 'general')
    
    resources = api_server.response_generator.crisis_resources.get(crisis_type, [])
    
    return jsonify({
        "crisis_type": crisis_type,
        "resources": resources
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    logger.info("Starting Crisis API Server...")
    logger.info("Available endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  POST /api/analyze/text - Analyze text")
    logger.info("  POST /api/analyze/image - Analyze image")
    logger.info("  POST /api/analyze/multimodal - Analyze multimodal input")
    logger.info("  GET  /api/session/<id> - Get session data")
    logger.info("  GET  /api/analytics - Get analytics")
    logger.info("  POST /api/cleanup - Clean up sessions")
    logger.info("  GET  /api/resources - Get crisis resources")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
