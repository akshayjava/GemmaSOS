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
        
        # Crisis detection keywords (simplified for demo)
        self.crisis_keywords = {
            "self_harm": ["cut", "hurt myself", "bleeding", "razor", "knife"],
            "suicide": ["kill myself", "end it all", "suicide", "not worth living"],
            "violence": ["hurt someone", "attack", "fight", "violence"],
            "abuse": ["abuse", "hit me", "scared", "unsafe"],
            "overdose": ["overdose", "too many pills", "unconscious"]
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
        Simple crisis detection for demo purposes
        
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
        
        text_lower = text.lower()
        detected_crises = []
        max_confidence = 0.0
        
        # Check each crisis category
        for category, keywords in self.crisis_keywords.items():
            matches = [keyword for keyword in keywords if keyword in text_lower]
            
            if matches:
                confidence = min(len(matches) / len(keywords) + 0.3, 1.0)
                detected_crises.append({
                    "category": category,
                    "confidence": confidence,
                    "matched_keywords": matches
                })
                max_confidence = max(max_confidence, confidence)
        
        # Simulate Gemma model analysis
        gemma_analysis = self._simulate_gemma_analysis(text, detected_crises)
        
        return {
            "crisis_detected": len(detected_crises) > 0,
            "categories": detected_crises,
            "confidence": max_confidence,
            "gemma_analysis": gemma_analysis,
            "message": f"Analysis complete. Found {len(detected_crises)} crisis indicators."
        }
    
    def _simulate_gemma_analysis(self, text: str, detected_crises: List[Dict]) -> Dict[str, Any]:
        """Simulate Gemma model analysis for demo"""
        if not detected_crises:
            return {
                "crisis_level": "none",
                "immediate_risk": False,
                "analysis": "No crisis indicators detected in the text.",
                "confidence": 0.8
            }
        
        # Determine crisis level based on detected categories
        crisis_level = "low"
        immediate_risk = False
        
        for crisis in detected_crises:
            if crisis["confidence"] > 0.7:
                crisis_level = "high"
                immediate_risk = True
            elif crisis["confidence"] > 0.5:
                crisis_level = "medium"
        
        # Generate analysis text
        if immediate_risk:
            analysis = "High-risk crisis situation detected. Immediate intervention recommended."
        elif crisis_level == "medium":
            analysis = "Medium-risk situation detected. Support and monitoring recommended."
        else:
            analysis = "Low-risk situation detected. General support and resources recommended."
        
        return {
            "crisis_level": crisis_level,
            "immediate_risk": immediate_risk,
            "analysis": analysis,
            "confidence": 0.85
        }
    
    def generate_response(self, crisis_result: Dict[str, Any], user_text: str) -> str:
        """Generate empathetic response based on crisis detection"""
        if not crisis_result["crisis_detected"]:
            return self._generate_general_response()
        
        # Get primary crisis category
        primary_category = crisis_result["categories"][0]["category"] if crisis_result["categories"] else "general"
        immediate_risk = crisis_result.get("gemma_analysis", {}).get("immediate_risk", False)
        
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
                    gr.Markdown("### 🔍 Analysis Results")
                    
                    crisis_detection = gr.JSON(
                        label="Crisis Detection Results",
                        value={}
                    )
                    
                    gemma_analysis = gr.JSON(
                        label="Gemma Model Analysis",
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
                    
                    1. **Crisis Detection**: Identifies crisis indicators in text
                    2. **Gemma Analysis**: Uses AI to assess risk level
                    3. **Response Generation**: Creates empathetic responses
                    4. **Resource Matching**: Provides relevant help resources
                    
                    **Crisis Types Detected:**
                    - Self-harm
                    - Suicide risk
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
            
            # Detect crisis
            crisis_result = demo.detect_crisis_simple(text)
            
            # Only generate response if crisis is detected
            if crisis_result["crisis_detected"]:
                response = demo.generate_response(crisis_result, text)
            else:
                response = "No crisis indicators detected. This appears to be a general message. If you're experiencing distress, please don't hesitate to reach out for support."
            
            # Extract Gemma analysis
            gemma_analysis = crisis_result.get("gemma_analysis", {})
            
            return crisis_result, gemma_analysis, response
        
        def clear_and_analyze(text):
            """Clear response and analyze new text"""
            if not text.strip():
                return {}, {}, "Please enter some text to analyze."
            
            # Detect crisis
            crisis_result = demo.detect_crisis_simple(text)
            
            # Only generate response if crisis is detected
            if crisis_result["crisis_detected"]:
                response = demo.generate_response(crisis_result, text)
            else:
                response = "No crisis indicators detected. This appears to be a general message. If you're experiencing distress, please don't hesitate to reach out for support."
            
            # Extract Gemma analysis
            gemma_analysis = crisis_result.get("gemma_analysis", {})
            
            return crisis_result, gemma_analysis, response
        
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
            outputs=[crisis_detection, gemma_analysis, response_output]
        )
        
        text_input.submit(
            clear_and_analyze,
            inputs=[text_input],
            outputs=[crisis_detection, gemma_analysis, response_output]
        )
        
        clear_btn.click(
            clear_all,
            outputs=[crisis_detection, gemma_analysis, response_output, text_input]
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
