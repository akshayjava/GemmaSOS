"""
GemmaSOS Demo App - Interactive Crisis Response Testing
A simplified demo to showcase Gemma on-device crisis response capabilities
"""

import gradio as gr
import torch
import logging
import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GemmaSOSDemo:
    """
    Demo application for testing Gemma on-device crisis response
    """
    
    def __init__(self):
        """Initialize the demo application"""
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_loaded = False
        
        # Demo scenarios for testing
        self.demo_scenarios = self._load_demo_scenarios()
        
        # Crisis detection using Gemma safety features (simplified for demo)
        self.safety_categories = {
            "self_harm": "Content expressing intent to harm oneself",
            "violence": "Content expressing intent to harm others", 
            "harassment": "Content that is abusive or threatening",
            "dangerous_content": "Content promoting dangerous activities"
        }
        
        # Crisis resources
        self.crisis_resources = {
            "general": [
                {"name": "National Suicide Prevention Lifeline", "number": "988"},
                {"name": "Crisis Text Line", "text": "Text HOME to 741741"},
                {"name": "Emergency Services", "number": "911"}
            ],
            "self_harm": [
                {"name": "Self-Injury Outreach & Support", "website": "sioutreach.org"}
            ],
            "suicide": [
                {"name": "National Suicide Prevention Lifeline", "number": "988"}
            ],
            "violence": [
                {"name": "National Domestic Violence Hotline", "number": "1-800-799-7233"}
            ],
            "abuse": [
                {"name": "National Domestic Violence Hotline", "number": "1-800-799-7233"}
            ],
            "overdose": [
                {"name": "National Poison Control Center", "number": "1-800-222-1222"}
            ]
        }
    
    def _load_demo_scenarios(self) -> List[Dict[str, Any]]:
        """Load demo scenarios for testing"""
        return [
            {
                "id": "scenario_1",
                "name": "General Sadness",
                "description": "Someone feeling down but not in crisis",
                "text": "I'm feeling really sad today. Nothing seems to be going right.",
                "expected_crisis": False,
                "category": "general"
            },
            {
                "id": "scenario_2", 
                "name": "Self-Harm Crisis",
                "description": "Someone expressing self-harm thoughts",
                "text": "I want to cut myself tonight. I can't take this pain anymore.",
                "expected_crisis": True,
                "category": "self_harm"
            },
            {
                "id": "scenario_3",
                "name": "Suicidal Ideation",
                "description": "Someone expressing suicidal thoughts",
                "text": "I don't want to live anymore. Everyone would be better off without me.",
                "expected_crisis": True,
                "category": "suicide"
            },
            {
                "id": "scenario_4",
                "name": "Violence Threat",
                "description": "Someone threatening violence",
                "text": "I'm going to hurt someone who deserves it. They'll pay for what they did.",
                "expected_crisis": True,
                "category": "violence"
            },
            {
                "id": "scenario_5",
                "name": "Abuse Situation",
                "description": "Someone reporting abuse",
                "text": "He hits me every day and I'm scared. I don't know what to do.",
                "expected_crisis": True,
                "category": "abuse"
            },
            {
                "id": "scenario_6",
                "name": "Overdose Situation",
                "description": "Someone reporting overdose",
                "text": "I took too many pills and I feel really sick. I think I need help.",
                "expected_crisis": True,
                "category": "overdose"
            }
        ]
    
    def load_gemma_model(self) -> str:
        """Load the Gemma model for demo purposes"""
        try:
            if self.model_loaded:
                return "✅ Model already loaded!"
            
            logger.info("Loading Gemma model for demo...")
            
            # For demo purposes, we'll simulate model loading
            # In a real implementation, this would load the actual Gemma model
            self.model_loaded = True
            
            return f"✅ Gemma model loaded successfully on {self.device}!\n\n" \
                   "Note: This is a demo simulation. In the full system, this would load the actual Gemma-2B model."
                   
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return f"❌ Error loading model: {str(e)}"
    
    def detect_crisis_simple(self, text: str) -> Dict[str, Any]:
        """
        Simple crisis detection using Gemma safety features for demo purposes
        
        Args:
            text: Input text to analyze
            
        Returns:
            Crisis detection results
        """
        if not text or not text.strip():
            return {
                "crisis_detected": False,
                "categories": [],
                "confidence": 0.0,
                "message": "No text provided for analysis."
            }
        
        # Simulate Gemma safety analysis
        safety_analysis = self._simulate_gemma_safety_analysis(text)
        
        # Map safety categories to crisis categories
        detected_crises = []
        max_confidence = 0.0
        
        for safety_category, safety_data in safety_analysis.items():
            if safety_data.get("detected", False) and safety_data.get("confidence", 0) > 0.3:
                # Map to crisis category
                crisis_category = self._map_safety_to_crisis(safety_category)
                if crisis_category:
                    detected_crises.append({
                        "category": crisis_category,
                        "confidence": safety_data["confidence"],
                        "safety_category": safety_category,
                        "severity": safety_data.get("severity", "medium"),
                        "reasoning": safety_data.get("reasoning", "")
                    })
                    max_confidence = max(max_confidence, safety_data["confidence"])
        
        return {
            "crisis_detected": len(detected_crises) > 0,
            "categories": detected_crises,
            "confidence": max_confidence,
            "safety_analysis": safety_analysis,
            "immediate_risk": any(cat.get("severity") == "high" for cat in detected_crises),
            "message": f"Safety analysis complete. Found {len(detected_crises)} crisis indicators."
        }
    
    def _simulate_gemma_safety_analysis(self, text: str) -> Dict[str, Any]:
        """Simulate Gemma safety analysis for demo"""
        text_lower = text.lower()
        
        # Simulate safety analysis for each category
        safety_analysis = {}
        
        # Self-harm analysis
        self_harm_indicators = ["hurt myself", "cut myself", "kill myself", "end it all", "not worth living", "suicide"]
        self_harm_detected = any(indicator in text_lower for indicator in self_harm_indicators)
        safety_analysis["self_harm"] = {
            "detected": self_harm_detected,
            "confidence": 0.8 if self_harm_detected else 0.1,
            "severity": "high" if self_harm_detected else "low",
            "reasoning": "Self-harm indicators detected" if self_harm_detected else "No self-harm indicators"
        }
        
        # Violence analysis
        violence_indicators = ["hurt someone", "attack", "fight", "violence", "threaten", "revenge"]
        violence_detected = any(indicator in text_lower for indicator in violence_indicators)
        safety_analysis["violence"] = {
            "detected": violence_detected,
            "confidence": 0.7 if violence_detected else 0.1,
            "severity": "medium" if violence_detected else "low",
            "reasoning": "Violence indicators detected" if violence_detected else "No violence indicators"
        }
        
        # Harassment analysis
        harassment_indicators = ["abuse", "hit me", "scared", "threaten", "intimidate", "unsafe"]
        harassment_detected = any(indicator in text_lower for indicator in harassment_indicators)
        safety_analysis["harassment"] = {
            "detected": harassment_detected,
            "confidence": 0.8 if harassment_detected else 0.1,
            "severity": "high" if harassment_detected else "low",
            "reasoning": "Harassment indicators detected" if harassment_detected else "No harassment indicators"
        }
        
        # Dangerous content analysis
        dangerous_indicators = ["overdose", "too many pills", "drugs", "poison", "unconscious", "sick"]
        dangerous_detected = any(indicator in text_lower for indicator in dangerous_indicators)
        safety_analysis["dangerous_content"] = {
            "detected": dangerous_detected,
            "confidence": 0.9 if dangerous_detected else 0.1,
            "severity": "high" if dangerous_detected else "low",
            "reasoning": "Dangerous content indicators detected" if dangerous_detected else "No dangerous content indicators"
        }
        
        return safety_analysis
    
    def _map_safety_to_crisis(self, safety_category: str) -> str:
        """Map safety category to crisis category"""
        mapping = {
            "self_harm": "self_harm",
            "violence": "violence",
            "harassment": "abuse", 
            "dangerous_content": "overdose"
        }
        return mapping.get(safety_category, "general")
    
    def generate_response(self, crisis_result: Dict[str, Any], user_text: str) -> str:
        """Generate empathetic response based on safety-aware crisis detection"""
        if not crisis_result["crisis_detected"]:
            return self._generate_general_response()
        
        # Get primary crisis category
        primary_category = crisis_result["categories"][0]["category"] if crisis_result["categories"] else "general"
        immediate_risk = crisis_result.get("immediate_risk", False)
        safety_analysis = crisis_result.get("safety_analysis", {})
        
        # Generate response based on category
        response_templates = {
            "self_harm": {
                "immediate": "I can hear that you're in a lot of pain right now. You don't have to go through this alone. Your life has value, even when it doesn't feel that way.",
                "supportive": "It takes courage to reach out when you're struggling. I'm glad you did. You're not alone in this."
            },
            "suicide": {
                "immediate": "I'm very concerned about you right now. Your life matters, and I want to help you stay safe. Please know that you don't have to face this alone.",
                "supportive": "Thank you for sharing this with me. It takes incredible strength to be so honest. I'm here with you."
            },
            "violence": {
                "immediate": "I'm concerned about your safety. Violence is never the answer, and there are better ways to handle this situation.",
                "supportive": "It's okay to feel angry, but we need to find safe ways to express these feelings."
            },
            "abuse": {
                "immediate": "I'm so sorry this is happening to you. You don't deserve to be treated this way. Your safety is the most important thing right now.",
                "supportive": "It took courage to share this with me. You're not to blame for what happened. You deserve to be treated with respect."
            },
            "overdose": {
                "immediate": "I'm very concerned about your safety right now. If you've already taken something, please call emergency services immediately.",
                "supportive": "I'm glad you're reaching out. You don't have to face this alone. There are people who care about you."
            }
        }
        
        response_type = "immediate" if immediate_risk else "supportive"
        base_response = response_templates.get(primary_category, {}).get(response_type, 
            "I'm here to listen and support you. You don't have to face this alone.")
        
        # Add resources
        resources = self.crisis_resources.get(primary_category, self.crisis_resources["general"])
        resource_text = "\n\n**Resources that might help:**\n"
        for resource in resources[:3]:  # Show top 3 resources
            if resource.get("number"):
                resource_text += f"• {resource['name']}: {resource['number']}\n"
            elif resource.get("text"):
                resource_text += f"• {resource['name']}: {resource['text']}\n"
            elif resource.get("website"):
                resource_text += f"• {resource['name']}: {resource['website']}\n"
        
        # Add emergency notice if immediate risk
        if immediate_risk:
            emergency_notice = "\n\n🚨 **If you're in immediate danger, please call 911 or 988 right now.**"
        else:
            emergency_notice = ""
        
        return f"{base_response}{resource_text}{emergency_notice}"
    
    def _generate_general_response(self) -> str:
        """Generate general supportive response for non-crisis situations"""
        return """No crisis indicators detected. This appears to be a general message. 

If you're experiencing distress or need someone to talk to, please don't hesitate to reach out for support. Your feelings are valid and important.

**General Resources:**
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Emergency Services: 911"""
    
    def load_demo_scenario(self, scenario_id: str) -> str:
        """Load a demo scenario for testing"""
        scenario = next((s for s in self.demo_scenarios if s["id"] == scenario_id), None)
        if scenario:
            return scenario["text"]
        return "Scenario not found."
    
    def get_demo_scenarios(self) -> List[Dict[str, str]]:
        """Get list of available demo scenarios"""
        return [
            {"id": scenario["id"], "name": scenario["name"], "description": scenario["description"]}
            for scenario in self.demo_scenarios
        ]

def create_demo_interface():
    """Create the demo interface"""
    demo = GemmaSOSDemo()
    
    # Custom CSS for demo styling
    css = """
    .demo-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .crisis-alert {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .no-crisis {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .demo-section {
        background-color: #f5f5f5;
        padding: 20px;
        margin: 20px 0;
        border-radius: 8px;
    }
    .resource-box {
        background-color: #e3f2fd;
        border: 1px solid #2196f3;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    """
    
    with gr.Blocks(css=css, title="GemmaSOS Demo - Crisis Response Testing") as interface:
        gr.Markdown("""
        # 🔒 GemmaSOS Demo - On-Device Crisis Response Testing
        
        **Test Google's Gemma model for crisis detection and response generation**
        
        This demo showcases how the Gemma lightweight model can detect crisis situations and generate empathetic responses entirely on your device.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Model Loading Section
                with gr.Group():
                    gr.Markdown("### 🤖 Model Loading")
                    load_model_btn = gr.Button("Load Gemma Model", variant="primary", size="lg")
                    model_status = gr.Textbox(
                        label="Model Status",
                        value="Model not loaded. Click 'Load Gemma Model' to start.",
                        interactive=False,
                        lines=4
                    )
                
                # Text Input Section
                with gr.Group():
                    gr.Markdown("### 📝 Test Crisis Detection")
                    
                    # Demo scenarios dropdown
                    scenario_dropdown = gr.Dropdown(
                        choices=[(s["name"], s["id"]) for s in demo.get_demo_scenarios()],
                        label="Load Demo Scenario",
                        value=None
                    )
                    load_scenario_btn = gr.Button("Load Scenario", variant="secondary")
                    
                    # Text input
                    text_input = gr.Textbox(
                        label="Enter text to analyze",
                        placeholder="Type your message here or load a demo scenario...",
                        lines=4
                    )
                    
                    # Analysis buttons
                    with gr.Row():
                        analyze_btn = gr.Button("Analyze for Crisis", variant="primary")
                        clear_btn = gr.Button("Clear All", variant="secondary")
                
                # Results Section
                with gr.Group():
                    gr.Markdown("### 🔍 Safety Analysis Results")
                    
                    crisis_detection = gr.JSON(
                        label="Crisis Detection Results",
                        value={}
                    )
                    
                    safety_analysis = gr.JSON(
                        label="Gemma Safety Analysis",
                        value={}
                    )
                
                # Response Section
                with gr.Group():
                    gr.Markdown("### 💬 Generated Response")
                    
                    response_output = gr.Textbox(
                        label="Empathetic Response",
                        lines=8,
                        interactive=False
                    )
            
            with gr.Column(scale=1):
                # Demo Information
                with gr.Group():
                    gr.Markdown("### 📚 Demo Information")
                    
                    gr.Markdown("""
                    **What this demo shows:**
                    
                    1. **Safety Analysis**: Uses Gemma's built-in safety features
                    2. **Crisis Detection**: Maps safety categories to crisis types
                    3. **Response Generation**: Creates safety-aware empathetic responses
                    4. **Resource Matching**: Provides relevant help resources
                    
                    **Safety Categories Analyzed:**
                    - Self-harm content
                    - Violence threats
                    - Harassment/abuse
                    - Dangerous content
                    
                    **Crisis Types Mapped:**
                    - Self-harm & suicide risk
                    - Violence threats
                    - Abuse situations
                    - Overdose scenarios
                    """)
                
                # Privacy Notice
                with gr.Group():
                    gr.Markdown("### 🔒 Privacy & Security")
                    
                    gr.Markdown("""
                    **On-Device Processing:**
                    - All analysis happens locally
                    - No data sent to external servers
                    - Complete privacy protection
                    - Temporary processing only
                    """)
                
                # Emergency Resources
                with gr.Group():
                    gr.Markdown("### 🚨 Emergency Resources")
                    
                    gr.Markdown("""
                    **If you're in immediate danger:**
                    - Call 911
                    - Call 988 (Suicide & Crisis Lifeline)
                    - Text HOME to 741741
                    
                    **24/7 Support:**
                    - National Suicide Prevention Lifeline: 988
                    - Crisis Text Line: Text HOME to 741741
                    - National Domestic Violence Hotline: 1-800-799-7233
                    """)
        
        # Event handlers
        def load_model():
            return demo.load_gemma_model()
        
        def load_scenario(scenario_id):
            if scenario_id:
                return demo.load_demo_scenario(scenario_id)
            return ""
        
        def analyze_text(text):
            if not text.strip():
                return {}, {}, "Please enter some text to analyze."
            
            # Detect crisis using safety analysis
            crisis_result = demo.detect_crisis_simple(text)
            
            # Only generate response if crisis is detected
            if crisis_result["crisis_detected"]:
                response = demo.generate_response(crisis_result, text)
            else:
                response = "No crisis indicators detected. This appears to be a general message. If you're experiencing distress, please don't hesitate to reach out for support."
            
            # Extract safety analysis
            safety_analysis = crisis_result.get("safety_analysis", {})
            
            return crisis_result, safety_analysis, response
        
        def clear_and_analyze(text):
            """Clear response and analyze new text"""
            if not text.strip():
                return {}, {}, "Please enter some text to analyze."
            
            # Detect crisis using safety analysis
            crisis_result = demo.detect_crisis_simple(text)
            
            # Only generate response if crisis is detected
            if crisis_result["crisis_detected"]:
                response = demo.generate_response(crisis_result, text)
            else:
                response = "No crisis indicators detected. This appears to be a general message. If you're experiencing distress, please don't hesitate to reach out for support."
            
            # Extract safety analysis
            safety_analysis = crisis_result.get("safety_analysis", {})
            
            return crisis_result, safety_analysis, response
        
        def clear_all():
            """Clear all outputs"""
            return {}, {}, "", ""
        
        # Connect events
        load_model_btn.click(
            load_model,
            outputs=[model_status]
        )
        
        load_scenario_btn.click(
            load_scenario,
            inputs=[scenario_dropdown],
            outputs=[text_input]
        )
        
        analyze_btn.click(
            clear_and_analyze,
            inputs=[text_input],
            outputs=[crisis_detection, safety_analysis, response_output]
        )
        
        text_input.submit(
            clear_and_analyze,
            inputs=[text_input],
            outputs=[crisis_detection, safety_analysis, response_output]
        )
        
        clear_btn.click(
            clear_all,
            outputs=[crisis_detection, safety_analysis, response_output, text_input]
        )
    
    return interface

def main():
    """Main function to run the demo"""
    try:
        interface = create_demo_interface()
        
        # Launch the demo
        interface.launch(
            server_name="0.0.0.0",
            server_port=7861,  # Different port from main app
            share=False,
            show_error=True
        )
        
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo error: {e}")

if __name__ == "__main__":
    main()
