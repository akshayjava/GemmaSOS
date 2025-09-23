"""
GemmaSOS - On-Device Crisis Response and Intervention System
Main application integrating all components
"""

import gradio as gr
import logging
import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import os
import tempfile

from crisis_detector import CrisisDetector
from response_generator import CrisisResponseGenerator
from safety_system import SafetySystem

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GemmaSOSApp:
    """
    Main application class for the crisis intervention system
    """
    
    def __init__(self):
        """Initialize the application with all components"""
        self.session_id = str(uuid.uuid4())
        logger.info(f"Initializing GemmaSOS app with session: {self.session_id}")
        
        # Initialize components
        try:
            self.crisis_detector = CrisisDetector()
            self.response_generator = CrisisResponseGenerator()
            self.safety_system = SafetySystem()
            logger.info("All components initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            raise
        
        # Application state
        self.conversation_history = []
        self.current_crisis_state = None
        
    def process_input(self, 
                     text_input: str = None, 
                     image_input = None,
                     history: List = None) -> Tuple[str, List, Dict]:
        """
        Process user input and generate appropriate response
        
        Args:
            text_input: Text input from user
            image_input: Image input from user
            history: Conversation history
            
        Returns:
            Tuple of (response_text, updated_history, crisis_info)
        """
        try:
            # Validate input for safety
            validation_result = self.safety_system.validate_input(
                text=text_input, 
                image_path=image_input
            )
            
            if not validation_result["is_safe"]:
                return self._handle_unsafe_input(validation_result), history or [], {}
            
            # Detect crisis situations
            crisis_result = self.crisis_detector.detect_multimodal_crisis(
                text=text_input,
                image=image_input
            )
            
            # Assess risk level
            risk_level = self.safety_system.assess_risk_level(crisis_result)
            
            # Generate appropriate response
            if crisis_result["crisis_detected"]:
                response = self.response_generator.generate_response(
                    crisis_type=crisis_result.get("primary_category", "general"),
                    user_message=text_input or "",
                    confidence=crisis_result["combined_confidence"],
                    immediate_risk=crisis_result["immediate_risk"],
                    safety_analysis=crisis_result.get("safety_analysis")
                )
                
                # Get safety actions
                safety_actions = self.safety_system.get_safety_actions(risk_level)
                response["safety_actions"] = safety_actions
                
                # Update crisis state
                self.current_crisis_state = {
                    "risk_level": risk_level,
                    "crisis_type": crisis_result.get("primary_category"),
                    "confidence": crisis_result["combined_confidence"],
                    "timestamp": datetime.now().isoformat()
                }
                
            else:
                # No crisis detected - provide general supportive response
                response = self._generate_general_response(text_input)
                self.current_crisis_state = None
            
            # Format response for display
            response_text = self._format_response(response, risk_level)
            
            # Update conversation history
            updated_history = history or []
            if text_input:
                updated_history.append([text_input, response_text])
            
            # Log the interaction (privacy-safe)
            self._log_interaction(text_input, crisis_result, risk_level)
            
            return response_text, updated_history, self.current_crisis_state or {}
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return self._handle_error(e), history or [], {}
    
    def _handle_unsafe_input(self, validation_result: Dict) -> str:
        """Handle unsafe input with appropriate response"""
        return f"""⚠️ **Safety Notice**

I cannot process this content safely. {validation_result.get('recommendations', ['Please rephrase your message.'])[0]}

If you're in immediate danger, please:
- Call 911 or emergency services
- Call 988 (Suicide & Crisis Lifeline)
- Go to your nearest emergency room

I'm here to help when you're ready to share in a safe way."""
    
    def _generate_general_response(self, text_input: str) -> Dict:
        """Generate a general supportive response when no crisis is detected"""
        return {
            "response": "Thank you for sharing that with me. I'm here to listen and support you. If you ever need to talk about something more serious, I'm here for that too.",
            "resources": self.response_generator.crisis_resources["general"][:2],
            "safety_plan": None,
            "immediate_risk": False,
            "crisis_type": "general",
            "confidence": 0.0
        }
    
    def _format_response(self, response: Dict, risk_level: str) -> str:
        """Format the response for display in the UI"""
        formatted_response = f"**{response['response']}**\n\n"
        
        # Add resources if available
        if response.get("resources"):
            formatted_response += "**Resources that might help:**\n"
            for resource in response["resources"]:
                if resource.get("number"):
                    formatted_response += f"• {resource['name']}: {resource['number']}\n"
                elif resource.get("website"):
                    formatted_response += f"• {resource['name']}: {resource['website']}\n"
                else:
                    formatted_response += f"• {resource['name']}\n"
            formatted_response += "\n"
        
        # Add safety actions if high risk
        if risk_level in ["immediate", "high"] and response.get("safety_actions"):
            formatted_response += "**Important Safety Steps:**\n"
            for action in response["safety_actions"][:3]:  # Show top 3 actions
                formatted_response += f"• {action['description']}\n"
            formatted_response += "\n"
        
        # Add safety plan if available
        if response.get("safety_plan"):
            safety_plan = response["safety_plan"]
            formatted_response += "**Safety Plan:**\n"
            if safety_plan.get("immediate_actions"):
                formatted_response += "Immediate actions:\n"
                for action in safety_plan["immediate_actions"][:3]:
                    formatted_response += f"• {action}\n"
            formatted_response += "\n"
        
        # Add privacy notice
        formatted_response += "🔒 **Privacy Notice:** All processing happens on your device. Nothing is sent to external servers."
        
        return formatted_response
    
    def _handle_error(self, error: Exception) -> str:
        """Handle errors gracefully"""
        return f"""I'm sorry, I encountered an error while processing your message. 

Please try again, or if you're in immediate danger:
- Call 911 or emergency services
- Call 988 (Suicide & Crisis Lifeline)

Error: {str(error)}"""
    
    def _log_interaction(self, text_input: str, crisis_result: Dict, risk_level: str):
        """Log interaction for safety monitoring (privacy-safe)"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "crisis_detected": crisis_result["crisis_detected"],
            "risk_level": risk_level,
            "confidence": crisis_result.get("combined_confidence", 0.0),
            "text_length": len(text_input) if text_input else 0
        }
        
        # Store minimal metadata only
        self.safety_system._log_processing(
            hashlib.sha256(str(log_entry).encode()).hexdigest()[:16],
            "interaction_logged"
        )
    
    def get_crisis_status(self) -> Dict:
        """Get current crisis status for monitoring"""
        if self.current_crisis_state:
            return {
                "status": "crisis_detected",
                "risk_level": self.current_crisis_state["risk_level"],
                "crisis_type": self.current_crisis_state["crisis_type"],
                "confidence": self.current_crisis_state["confidence"],
                "timestamp": self.current_crisis_state["timestamp"]
            }
        else:
            return {"status": "no_crisis_detected"}
    
    def get_privacy_info(self) -> Dict:
        """Get privacy information"""
        return self.safety_system.get_privacy_summary()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.safety_system.cleanup()
            logger.info("Application cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def create_interface():
    """Create the Gradio interface"""
    app = GemmaSOSApp()
    
    # Custom CSS for better styling
    css = """
    .crisis-alert {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 10px;
        margin: 10px 0;
    }
    .privacy-notice {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 10px;
        margin: 10px 0;
    }
    .resource-box {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    """
    
    with gr.Blocks(css=css, title="GemmaSOS - Crisis Support") as interface:
        gr.Markdown("""
        # 🔒 GemmaSOS - On-Device Crisis Support
        
        **Your privacy is protected** - Everything processes on your device. Nothing is sent to external servers.
        
        This system can help detect crisis situations and provide supportive resources. If you're in immediate danger, please call 911 or 988.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Main chat interface
                chatbot = gr.Chatbot(
                    label="Crisis Support Chat",
                    height=400,
                    show_label=True
                )
                
                with gr.Row():
                    text_input = gr.Textbox(
                        placeholder="Share what's on your mind...",
                        label="Message",
                        lines=3
                    )
                    send_btn = gr.Button("Send", variant="primary")
                
                # Image input
                image_input = gr.Image(
                    label="Upload Image (Optional)",
                    type="filepath",
                    height=200
                )
                
                # Clear button
                clear_btn = gr.Button("Clear Conversation", variant="secondary")
            
            with gr.Column(scale=1):
                # Crisis status
                crisis_status = gr.JSON(
                    label="Crisis Status",
                    value=app.get_crisis_status()
                )
                
                # Privacy info
                privacy_info = gr.JSON(
                    label="Privacy Information",
                    value=app.get_privacy_info()
                )
                
                # Emergency resources
                gr.Markdown("""
                ### 🚨 Emergency Resources
                
                **Immediate Help:**
                - 911 (Emergency Services)
                - 988 (Suicide & Crisis Lifeline)
                - Text HOME to 741741 (Crisis Text Line)
                
                **24/7 Support:**
                - National Suicide Prevention Lifeline: 988
                - Crisis Text Line: Text HOME to 741741
                - National Domestic Violence Hotline: 1-800-799-7233
                """)
        
        # Event handlers
        def process_message(text, image, history):
            if not text and not image:
                return history, {}, "Please enter a message or upload an image."
            
            response, updated_history, crisis_info = app.process_input(
                text_input=text,
                image_input=image,
                history=history
            )
            
            return updated_history, crisis_info, ""
        
        def clear_conversation():
            app.conversation_history = []
            app.current_crisis_state = None
            return [], {}, ""
        
        # Connect events
        send_btn.click(
            process_message,
            inputs=[text_input, image_input, chatbot],
            outputs=[chatbot, crisis_status, text_input]
        )
        
        text_input.submit(
            process_message,
            inputs=[text_input, image_input, chatbot],
            outputs=[chatbot, crisis_status, text_input]
        )
        
        clear_btn.click(
            clear_conversation,
            outputs=[chatbot, crisis_status, text_input]
        )
        
        # Update crisis status periodically
        def update_status():
            return app.get_crisis_status()
        
        crisis_status.change(
            update_status,
            outputs=[crisis_status]
        )
    
    return interface, app

def main():
    """Main function to run the application"""
    try:
        interface, app = create_interface()
        
        # Launch the interface
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        if 'app' in locals():
            app.cleanup()

if __name__ == "__main__":
    main()
