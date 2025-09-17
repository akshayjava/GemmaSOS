"""
Empathetic Response Generator for Crisis Intervention
Generates trauma-informed, supportive responses using Gemma model
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, List, Optional, Tuple
import logging
import json
import random

logger = logging.getLogger(__name__)

class CrisisResponseGenerator:
    """
    Generates empathetic, trauma-informed responses for crisis situations
    """
    
    def __init__(self, model_name: str = "google/gemma-2b-it"):
        """
        Initialize the response generator
        
        Args:
            model_name: Hugging Face model identifier for Gemma
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model and tokenizer
        self._load_model()
        
        # Response templates for different crisis types
        self.response_templates = {
            "self_harm": {
                "immediate": [
                    "I can hear that you're in a lot of pain right now. You don't have to go through this alone.",
                    "I'm really concerned about you. Your life has value, even when it doesn't feel that way.",
                    "I want you to know that what you're feeling right now is valid, and there are people who care about you."
                ],
                "supportive": [
                    "It takes courage to reach out when you're struggling. I'm glad you did.",
                    "You're not alone in this. Many people have felt this way and found ways to cope.",
                    "Your feelings are important, and so are you."
                ]
            },
            "suicide": {
                "immediate": [
                    "I'm very concerned about you right now. Your life matters, and I want to help you stay safe.",
                    "I can hear how much pain you're in. Please know that you don't have to face this alone.",
                    "I care about you, and I want to make sure you're safe. Can we talk about what's happening?"
                ],
                "supportive": [
                    "Thank you for sharing this with me. It takes incredible strength to be so honest.",
                    "I'm here with you. You don't have to carry this burden alone.",
                    "Your life has meaning, even when it's hard to see right now."
                ]
            },
            "violence": {
                "immediate": [
                    "I'm concerned about your safety. Violence is never the answer, and there are better ways to handle this.",
                    "I can hear that you're very angry right now. Let's talk about what's really bothering you.",
                    "I want to help you find a safer way to express these feelings."
                ],
                "supportive": [
                    "It's okay to feel angry, but we need to find safe ways to express it.",
                    "I'm here to listen and help you work through these feelings.",
                    "There are people who can help you resolve this situation safely."
                ]
            },
            "abuse": {
                "immediate": [
                    "I'm so sorry this is happening to you. You don't deserve to be treated this way.",
                    "Your safety is the most important thing right now. You're not alone.",
                    "I believe you, and I want to help you get to safety."
                ],
                "supportive": [
                    "It took courage to share this with me. You're not to blame for what happened.",
                    "You deserve to be treated with respect and kindness.",
                    "I'm here to support you in whatever way you need."
                ]
            },
            "overdose": {
                "immediate": [
                    "I'm very concerned about your safety right now. Please don't take any more.",
                    "Your life is valuable, and I want to help you stay safe.",
                    "If you've already taken something, please call emergency services immediately."
                ],
                "supportive": [
                    "I'm glad you're reaching out. You don't have to face this alone.",
                    "There are people who care about you and want to help you through this.",
                    "Recovery is possible, and you deserve support."
                ]
            }
        }
        
        # Crisis resource database
        self.crisis_resources = self._load_crisis_resources()
    
    def _load_model(self):
        """Load the Gemma model for response generation"""
        try:
            logger.info(f"Loading response model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
                
            logger.info("Response model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading response model: {e}")
            raise
    
    def _load_crisis_resources(self) -> Dict[str, List[Dict]]:
        """Load comprehensive crisis resources and helplines"""
        return {
            "general": [
                {
                    "name": "National Suicide Prevention Lifeline",
                    "number": "988",
                    "text": "Text HOME to 741741",
                    "description": "24/7 crisis support for suicide prevention",
                    "available": "24/7"
                },
                {
                    "name": "Crisis Text Line",
                    "number": "Text HOME to 741741",
                    "description": "Free, 24/7 crisis support via text",
                    "available": "24/7"
                }
            ],
            "self_harm": [
                {
                    "name": "Self-Injury Outreach & Support",
                    "website": "sioutreach.org",
                    "description": "Resources and support for self-injury recovery"
                },
                {
                    "name": "To Write Love on Her Arms",
                    "website": "twloha.com",
                    "description": "Hope and help for people struggling with depression, addiction, self-injury, and suicide"
                }
            ],
            "suicide": [
                {
                    "name": "National Suicide Prevention Lifeline",
                    "number": "988",
                    "text": "Text HOME to 741741",
                    "description": "24/7 crisis support for suicide prevention",
                    "available": "24/7"
                },
                {
                    "name": "American Foundation for Suicide Prevention",
                    "website": "afsp.org",
                    "description": "Resources, support groups, and prevention programs"
                }
            ],
            "violence": [
                {
                    "name": "National Domestic Violence Hotline",
                    "number": "1-800-799-7233",
                    "text": "Text START to 88788",
                    "description": "24/7 support for domestic violence",
                    "available": "24/7"
                },
                {
                    "name": "National Sexual Assault Hotline",
                    "number": "1-800-656-4673",
                    "description": "24/7 support for sexual assault survivors",
                    "available": "24/7"
                }
            ],
            "abuse": [
                {
                    "name": "National Domestic Violence Hotline",
                    "number": "1-800-799-7233",
                    "text": "Text START to 88788",
                    "description": "24/7 support for domestic violence",
                    "available": "24/7"
                },
                {
                    "name": "Childhelp National Child Abuse Hotline",
                    "number": "1-800-4-A-CHILD (1-800-422-4453)",
                    "description": "24/7 support for child abuse",
                    "available": "24/7"
                }
            ],
            "overdose": [
                {
                    "name": "SAMHSA National Helpline",
                    "number": "1-800-662-4357",
                    "description": "24/7 treatment referral and information service",
                    "available": "24/7"
                },
                {
                    "name": "National Poison Control Center",
                    "number": "1-800-222-1222",
                    "description": "24/7 poison emergency support",
                    "available": "24/7"
                }
            ]
        }
    
    def generate_response(self, 
                         crisis_type: str, 
                         user_message: str, 
                         confidence: float,
                         immediate_risk: bool = False) -> Dict[str, any]:
        """
        Generate an empathetic response for a crisis situation
        
        Args:
            crisis_type: Type of crisis detected
            user_message: User's original message
            confidence: Confidence level of crisis detection
            immediate_risk: Whether there's immediate risk
            
        Returns:
            Dictionary containing response and resources
        """
        try:
            # Select appropriate response template
            response_type = "immediate" if immediate_risk or confidence > 0.7 else "supportive"
            
            if crisis_type in self.response_templates:
                base_response = random.choice(self.response_templates[crisis_type][response_type])
            else:
                base_response = "I'm here to listen and support you. You don't have to face this alone."
            
            # Generate personalized response using Gemma
            personalized_response = self._generate_personalized_response(
                user_message, base_response, crisis_type, immediate_risk
            )
            
            # Get relevant resources
            resources = self._get_relevant_resources(crisis_type, immediate_risk)
            
            # Create safety plan if needed
            safety_plan = self._create_safety_plan(crisis_type, immediate_risk) if immediate_risk else None
            
            return {
                "response": personalized_response,
                "resources": resources,
                "safety_plan": safety_plan,
                "immediate_risk": immediate_risk,
                "crisis_type": crisis_type,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_fallback_response(crisis_type, immediate_risk)
    
    def _generate_personalized_response(self, 
                                      user_message: str, 
                                      base_response: str,
                                      crisis_type: str,
                                      immediate_risk: bool) -> str:
        """
        Use Gemma model to generate a personalized response
        
        Args:
            user_message: User's original message
            base_response: Base response template
            crisis_type: Type of crisis
            immediate_risk: Whether there's immediate risk
            
        Returns:
            Personalized response text
        """
        try:
            # Create a prompt for response generation
            risk_level = "immediate crisis" if immediate_risk else "crisis situation"
            
            prompt = f"""<start_of_turn>user
You are a compassionate crisis counselor. Generate a supportive, empathetic response for someone in a {risk_level} related to {crisis_type}.

Guidelines:
- Be warm, non-judgmental, and validating
- Acknowledge their pain without minimizing it
- Offer hope and support
- Keep response under 150 words
- Use "I" statements to show care
- Avoid giving medical advice

User's message: "{user_message}"
Base response: "{base_response}"

Generate a personalized, empathetic response:
<end_of_turn>
<start_of_turn>model"""

            # Tokenize and generate
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the model's response
            if "<start_of_turn>model" in response:
                model_response = response.split("<start_of_turn>model")[-1].strip()
            else:
                model_response = response
            
            # Clean up the response
            model_response = model_response.replace("<end_of_turn>", "").strip()
            
            # Fallback to base response if model response is too short or inappropriate
            if len(model_response) < 20 or any(word in model_response.lower() for word in ["sorry", "can't help", "unable"]):
                return base_response
            
            return model_response
            
        except Exception as e:
            logger.error(f"Error in personalized response generation: {e}")
            return base_response
    
    def _get_relevant_resources(self, crisis_type: str, immediate_risk: bool) -> List[Dict]:
        """
        Get relevant crisis resources based on crisis type
        
        Args:
            crisis_type: Type of crisis
            immediate_risk: Whether there's immediate risk
            
        Returns:
            List of relevant resources
        """
        resources = []
        
        # Always include general crisis resources
        resources.extend(self.crisis_resources["general"])
        
        # Add specific resources for the crisis type
        if crisis_type in self.crisis_resources:
            resources.extend(self.crisis_resources[crisis_type])
        
        # Prioritize immediate resources if there's immediate risk
        if immediate_risk:
            resources = [r for r in resources if r.get("available") == "24/7"]
        
        return resources[:5]  # Limit to 5 resources
    
    def _create_safety_plan(self, crisis_type: str, immediate_risk: bool) -> Dict[str, any]:
        """
        Create a safety plan for immediate risk situations
        
        Args:
            crisis_type: Type of crisis
            immediate_risk: Whether there's immediate risk
            
        Returns:
            Safety plan dictionary
        """
        if not immediate_risk:
            return None
        
        safety_plan = {
            "immediate_actions": [
                "Call 911 or go to the nearest emergency room if you're in immediate danger",
                "Remove any means of self-harm from your immediate environment",
                "Stay with a trusted person or in a public place",
                "Call a crisis hotline: 988 (Suicide & Crisis Lifeline)"
            ],
            "coping_strategies": [
                "Practice deep breathing exercises",
                "Use grounding techniques (5-4-3-2-1 method)",
                "Reach out to a trusted friend or family member",
                "Engage in a calming activity you enjoy"
            ],
            "warning_signs": [
                "Feeling hopeless or worthless",
                "Having thoughts of self-harm or suicide",
                "Feeling isolated or alone",
                "Changes in sleep or appetite"
            ],
            "emergency_contacts": [
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "Emergency Services: 911"
            ]
        }
        
        return safety_plan
    
    def _get_fallback_response(self, crisis_type: str, immediate_risk: bool) -> Dict[str, any]:
        """
        Get a fallback response if generation fails
        
        Args:
            crisis_type: Type of crisis
            immediate_risk: Whether there's immediate risk
            
        Returns:
            Fallback response dictionary
        """
        if immediate_risk:
            response = "I'm very concerned about your safety right now. Please call 988 (Suicide & Crisis Lifeline) or 911 immediately. You don't have to face this alone."
        else:
            response = "I'm here to listen and support you. You don't have to face this alone. Please consider reaching out to a crisis hotline or mental health professional."
        
        return {
            "response": response,
            "resources": self.crisis_resources["general"][:3],
            "safety_plan": self._create_safety_plan(crisis_type, immediate_risk) if immediate_risk else None,
            "immediate_risk": immediate_risk,
            "crisis_type": crisis_type,
            "confidence": 0.5
        }

# Example usage
if __name__ == "__main__":
    generator = CrisisResponseGenerator()
    
    # Test response generation
    response = generator.generate_response(
        crisis_type="suicide",
        user_message="I don't want to live anymore",
        confidence=0.8,
        immediate_risk=True
    )
    
    print("Generated Response:")
    print(json.dumps(response, indent=2))
