"""
Safety and Privacy System for Crisis Intervention
Ensures on-device processing, data privacy, and safety measures
"""

import os
import hashlib
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import tempfile
import shutil

logger = logging.getLogger(__name__)

class SafetySystem:
    """
    Handles safety measures, privacy protection, and on-device processing
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the safety system
        
        Args:
            data_dir: Directory for temporary data storage (optional)
        """
        self.data_dir = data_dir or tempfile.mkdtemp(prefix="gemma_sos_")
        self.session_data = {}
        self.safety_logs = []
        
        # Ensure data directory exists and is secure
        os.makedirs(self.data_dir, mode=0o700, exist_ok=True)
        
        # Content filtering rules
        self.content_filters = self._initialize_content_filters()
        
        # Safety thresholds
        self.safety_thresholds = {
            "immediate_risk": 0.8,
            "high_risk": 0.6,
            "medium_risk": 0.4,
            "low_risk": 0.2
        }
        
        logger.info(f"Safety system initialized with data directory: {self.data_dir}")
    
    def _initialize_content_filters(self) -> Dict[str, List[str]]:
        """Initialize content filtering rules for safety"""
        return {
            "harmful_content": [
                "detailed methods", "step by step", "how to", "instructions",
                "tutorial", "guide", "detailed", "specific", "exact"
            ],
            "triggering_content": [
                "graphic", "explicit", "detailed description", "gory",
                "disturbing", "traumatic", "triggering"
            ],
            "dangerous_advice": [
                "ignore professional help", "don't tell anyone", "keep it secret",
                "you're alone", "no one cares", "give up"
            ]
        }
    
    def validate_input(self, text: str = None, image_path: str = None) -> Dict[str, Any]:
        """
        Validate input for safety and appropriateness
        
        Args:
            text: Text input to validate
            image_path: Path to image file to validate
            
        Returns:
            Validation results with safety recommendations
        """
        validation_result = {
            "is_safe": True,
            "warnings": [],
            "blocked_content": [],
            "recommendations": []
        }
        
        # Validate text input
        if text:
            text_validation = self._validate_text_content(text)
            validation_result["warnings"].extend(text_validation["warnings"])
            validation_result["blocked_content"].extend(text_validation["blocked_content"])
            
            if not text_validation["is_safe"]:
                validation_result["is_safe"] = False
        
        # Validate image input
        if image_path and os.path.exists(image_path):
            image_validation = self._validate_image_content(image_path)
            validation_result["warnings"].extend(image_validation["warnings"])
            validation_result["blocked_content"].extend(image_validation["blocked_content"])
            
            if not image_validation["is_safe"]:
                validation_result["is_safe"] = False
        
        # Generate safety recommendations
        validation_result["recommendations"] = self._generate_safety_recommendations(validation_result)
        
        return validation_result
    
    def _validate_text_content(self, text: str) -> Dict[str, Any]:
        """Validate text content for safety"""
        result = {
            "is_safe": True,
            "warnings": [],
            "blocked_content": []
        }
        
        text_lower = text.lower()
        
        # Check for harmful content
        for category, patterns in self.content_filters.items():
            for pattern in patterns:
                if pattern in text_lower:
                    if category == "harmful_content":
                        result["is_safe"] = False
                        result["blocked_content"].append(f"Potentially harmful content detected: {pattern}")
                    elif category == "triggering_content":
                        result["warnings"].append(f"Potentially triggering content: {pattern}")
                    elif category == "dangerous_advice":
                        result["is_safe"] = False
                        result["blocked_content"].append(f"Dangerous advice detected: {pattern}")
        
        # Check for crisis content that needs immediate attention
        crisis_indicators = [
            "right now", "tonight", "today", "immediately", "asap",
            "can't take it", "end it all", "final", "last time"
        ]
        
        for indicator in crisis_indicators:
            if indicator in text_lower:
                result["warnings"].append(f"Immediate crisis indicator: {indicator}")
        
        return result
    
    def _validate_image_content(self, image_path: str) -> Dict[str, Any]:
        """Validate image content for safety"""
        result = {
            "is_safe": True,
            "warnings": [],
            "blocked_content": []
        }
        
        try:
            # Basic file validation
            if not os.path.exists(image_path):
                result["is_safe"] = False
                result["blocked_content"].append("Image file not found")
                return result
            
            # Check file size (limit to 10MB)
            file_size = os.path.getsize(image_path)
            if file_size > 10 * 1024 * 1024:  # 10MB
                result["warnings"].append("Image file is very large")
            
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            file_ext = os.path.splitext(image_path)[1].lower()
            if file_ext not in allowed_extensions:
                result["is_safe"] = False
                result["blocked_content"].append(f"Unsupported file format: {file_ext}")
            
            # Additional image content validation could be added here
            # For now, we'll do basic validation
            
        except Exception as e:
            logger.error(f"Error validating image: {e}")
            result["is_safe"] = False
            result["blocked_content"].append(f"Error processing image: {str(e)}")
        
        return result
    
    def _generate_safety_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Generate safety recommendations based on validation results"""
        recommendations = []
        
        if validation_result["blocked_content"]:
            recommendations.append("Content has been blocked for safety reasons")
            recommendations.append("Please rephrase your message to avoid harmful content")
        
        if validation_result["warnings"]:
            recommendations.append("Please be mindful of potentially triggering content")
            recommendations.append("Consider reaching out to a mental health professional")
        
        if not validation_result["is_safe"]:
            recommendations.append("This content cannot be processed safely")
            recommendations.append("Please contact a crisis hotline for immediate support")
        
        return recommendations
    
    def ensure_privacy(self, data: Any, session_id: str = None) -> str:
        """
        Ensure data privacy by processing on-device only
        
        Args:
            data: Data to process
            session_id: Optional session identifier
            
        Returns:
            Processed data identifier (no actual data stored)
        """
        # Generate a unique identifier for the data
        data_id = hashlib.sha256(str(data).encode()).hexdigest()[:16]
        
        # Store minimal metadata only (no actual content)
        if session_id:
            if session_id not in self.session_data:
                self.session_data[session_id] = {
                    "created_at": datetime.now(),
                    "data_ids": [],
                    "last_activity": datetime.now()
                }
            
            self.session_data[session_id]["data_ids"].append(data_id)
            self.session_data[session_id]["last_activity"] = datetime.now()
        
        # Log the processing (without storing actual content)
        self._log_processing(data_id, "data_processed")
        
        return data_id
    
    def _log_processing(self, data_id: str, action: str):
        """Log processing activities for safety monitoring"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "data_id": data_id,
            "action": action,
            "session_active": len(self.session_data)
        }
        
        self.safety_logs.append(log_entry)
        
        # Keep only last 100 log entries
        if len(self.safety_logs) > 100:
            self.safety_logs = self.safety_logs[-100:]
    
    def assess_risk_level(self, crisis_detection_result: Dict[str, Any]) -> str:
        """
        Assess risk level based on crisis detection results using Gemma safety analysis
        
        Args:
            crisis_detection_result: Results from crisis detection
            
        Returns:
            Risk level: 'immediate', 'high', 'medium', 'low', or 'none'
        """
        confidence = crisis_detection_result.get("confidence", 0.0)
        immediate_risk = crisis_detection_result.get("immediate_risk", False)
        safety_analysis = crisis_detection_result.get("safety_analysis", {})
        
        # Check for high severity in safety analysis
        high_severity_detected = False
        if safety_analysis:
            for category, data in safety_analysis.items():
                if data.get("detected", False) and data.get("severity") == "high":
                    high_severity_detected = True
                    break
        
        if immediate_risk or confidence >= self.safety_thresholds["immediate_risk"] or high_severity_detected:
            return "immediate"
        elif confidence >= self.safety_thresholds["high_risk"]:
            return "high"
        elif confidence >= self.safety_thresholds["medium_risk"]:
            return "medium"
        elif confidence >= self.safety_thresholds["low_risk"]:
            return "low"
        else:
            return "none"
    
    def get_safety_actions(self, risk_level: str) -> List[Dict[str, str]]:
        """
        Get recommended safety actions based on risk level
        
        Args:
            risk_level: Assessed risk level
            
        Returns:
            List of recommended safety actions
        """
        safety_actions = {
            "immediate": [
                {
                    "action": "call_emergency",
                    "description": "Call 911 or emergency services immediately",
                    "priority": "critical"
                },
                {
                    "action": "call_crisis_hotline",
                    "description": "Call 988 (Suicide & Crisis Lifeline)",
                    "priority": "critical"
                },
                {
                    "action": "remove_means",
                    "description": "Remove any means of self-harm from immediate environment",
                    "priority": "high"
                }
            ],
            "high": [
                {
                    "action": "call_crisis_hotline",
                    "description": "Call 988 (Suicide & Crisis Lifeline)",
                    "priority": "high"
                },
                {
                    "action": "contact_trusted_person",
                    "description": "Reach out to a trusted friend or family member",
                    "priority": "high"
                },
                {
                    "action": "seek_professional_help",
                    "description": "Contact a mental health professional",
                    "priority": "medium"
                }
            ],
            "medium": [
                {
                    "action": "contact_trusted_person",
                    "description": "Reach out to a trusted friend or family member",
                    "priority": "medium"
                },
                {
                    "action": "use_coping_strategies",
                    "description": "Practice coping strategies and self-care",
                    "priority": "medium"
                },
                {
                    "action": "consider_professional_help",
                    "description": "Consider reaching out to a mental health professional",
                    "priority": "low"
                }
            ],
            "low": [
                {
                    "action": "use_coping_strategies",
                    "description": "Practice coping strategies and self-care",
                    "priority": "low"
                },
                {
                    "action": "monitor_symptoms",
                    "description": "Monitor your mental health and seek help if needed",
                    "priority": "low"
                }
            ],
            "none": [
                {
                    "action": "general_wellness",
                    "description": "Continue practicing good mental health habits",
                    "priority": "low"
                }
            ]
        }
        
        return safety_actions.get(risk_level, safety_actions["none"])
    
    def cleanup_session_data(self, session_id: str = None, max_age_hours: int = 24):
        """
        Clean up old session data to maintain privacy
        
        Args:
            session_id: Specific session to clean up (optional)
            max_age_hours: Maximum age of data to keep in hours
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        if session_id:
            if session_id in self.session_data:
                if self.session_data[session_id]["created_at"] < cutoff_time:
                    del self.session_data[session_id]
                    logger.info(f"Cleaned up session data for: {session_id}")
        else:
            # Clean up all old sessions
            sessions_to_remove = [
                sid for sid, data in self.session_data.items()
                if data["created_at"] < cutoff_time
            ]
            
            for sid in sessions_to_remove:
                del self.session_data[sid]
            
            if sessions_to_remove:
                logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
    
    def get_privacy_summary(self) -> Dict[str, Any]:
        """
        Get a summary of privacy measures in place
        
        Returns:
            Privacy summary dictionary
        """
        return {
            "data_processing": "on_device_only",
            "data_storage": "temporary_metadata_only",
            "data_transmission": "none",
            "active_sessions": len(self.session_data),
            "safety_logs_count": len(self.safety_logs),
            "data_directory": self.data_dir,
            "privacy_measures": [
                "No data sent to external servers",
                "No permanent storage of user content",
                "Temporary data automatically cleaned up",
                "All processing happens on device",
                "No tracking or analytics"
            ]
        }
    
    def cleanup(self):
        """Clean up all temporary data and resources"""
        try:
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
                logger.info("Cleaned up temporary data directory")
            
            self.session_data.clear()
            self.safety_logs.clear()
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# Example usage
if __name__ == "__main__":
    safety = SafetySystem()
    
    # Test input validation
    validation = safety.validate_input(text="I'm feeling really down today")
    print("Validation result:", validation)
    
    # Test risk assessment
    crisis_result = {"confidence": 0.7, "immediate_risk": False}
    risk_level = safety.assess_risk_level(crisis_result)
    print("Risk level:", risk_level)
    
    # Get safety actions
    actions = safety.get_safety_actions(risk_level)
    print("Safety actions:", actions)
    
    # Cleanup
    safety.cleanup()
