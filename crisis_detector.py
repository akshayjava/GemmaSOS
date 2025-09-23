"""
Crisis Detection System using Google's Gemma Model Safety Features
Detects various crisis situations using Gemma's built-in safety capabilities
"""

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor
from PIL import Image
import cv2
import re
import json
from typing import Dict, List, Tuple, Optional, Union
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrisisDetector:
    """
    On-device crisis detection system using Gemma model safety features
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the crisis detector with Gemma model
        
        Args:
            model_name: Hugging Face model identifier for Gemma
        """
        self.model_name = model_name or Config.MODEL_NAME
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Crisis categories mapped to Gemma safety categories
        self.crisis_mapping = {
            "self_harm": "self_harm",
            "suicide": "self_harm", 
            "violence": "violence",
            "abuse": "harassment",
            "overdose": "dangerous_content"
        }
        
        # Initialize model and tokenizer
        self._load_model()
        
    def _load_model(self):
        """Load the Gemma model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
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
                
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def detect_crisis_from_text(self, text: str) -> Dict[str, any]:
        """
        Detect crisis situations from text input using Gemma's safety features
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing crisis detection results
        """
        if not text or not text.strip():
            return {"crisis_detected": False, "categories": [], "confidence": 0.0}
        
        # Use Gemma's safety analysis
        safety_analysis = self._analyze_with_gemma_safety(text)
        
        # Map Gemma safety categories to crisis categories
        detected_crises = []
        max_confidence = 0.0
        
        for safety_category, safety_data in safety_analysis.items():
            if safety_data.get("detected", False) and safety_data.get("confidence", 0) > 0.3:
                # Map to our crisis categories
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
            "immediate_risk": any(cat.get("severity") == "high" for cat in detected_crises)
        }
    
    def detect_crisis_from_image(self, image: Union[str, Image.Image]) -> Dict[str, any]:
        """
        Detect crisis situations from image input
        
        Args:
            image: Image path or PIL Image object
            
        Returns:
            Dictionary containing crisis detection results
        """
        try:
            if isinstance(image, str):
                image = Image.open(image)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Basic image analysis for crisis indicators
            crisis_indicators = self._analyze_image_content(image)
            
            return {
                "crisis_detected": len(crisis_indicators) > 0,
                "indicators": crisis_indicators,
                "confidence": max([indicator["confidence"] for indicator in crisis_indicators], default=0.0)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {"crisis_detected": False, "indicators": [], "confidence": 0.0}
    
    def _analyze_image_content(self, image: Image.Image) -> List[Dict]:
        """
        Analyze image content for crisis indicators
        
        Args:
            image: PIL Image object
            
        Returns:
            List of detected crisis indicators
        """
        indicators = []
        
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Check for blood/red colors (potential self-harm)
        red_pixels = np.sum((img_array[:, :, 0] > 150) & 
                          (img_array[:, :, 1] < 100) & 
                          (img_array[:, :, 2] < 100))
        total_pixels = img_array.shape[0] * img_array.shape[1]
        red_ratio = red_pixels / total_pixels
        
        if red_ratio > 0.05:  # 5% threshold
            indicators.append({
                "type": "potential_blood",
                "confidence": min(red_ratio * 2, 1.0),
                "description": "High concentration of red pixels detected"
            })
        
        # Check for sharp objects (basic edge detection)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_ratio = np.sum(edges > 0) / total_pixels
        
        if edge_ratio > 0.1:  # High edge density might indicate sharp objects
            indicators.append({
                "type": "potential_sharp_objects",
                "confidence": min(edge_ratio, 1.0),
                "description": "High edge density detected, possible sharp objects"
            })
        
        return indicators
    
    def _analyze_with_gemma_safety(self, text: str) -> Dict[str, any]:
        """
        Use Gemma model for safety analysis using structured safety prompts
        
        Args:
            text: Text to analyze
            
        Returns:
            Safety analysis results from Gemma model
        """
        try:
            # Create a structured safety analysis prompt
            prompt = f"""<start_of_turn>user
You are a safety content moderation expert. Analyze the following text for harmful content across these categories:

1. Self-harm: Content expressing intent to harm oneself, including suicide ideation, self-injury, or self-destructive behavior
2. Violence: Content expressing intent to harm others, threats of violence, or promoting violence
3. Harassment: Content that is abusive, threatening, or intended to intimidate or harm others
4. Dangerous content: Content that promotes dangerous activities, substance abuse, or harmful behaviors

For each category, determine:
- detected: true/false
- confidence: 0.0-1.0
- severity: "low", "medium", "high"
- reasoning: brief explanation

Respond with a JSON object containing these categories.

Text to analyze: "{text}"
<end_of_turn>
<start_of_turn>model"""

            # Tokenize and generate
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=300,
                    temperature=0.1,  # Low temperature for consistent safety analysis
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
            
            # Parse JSON response
            try:
                # Try to extract JSON from the response
                json_start = model_response.find('{')
                json_end = model_response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = model_response[json_start:json_end]
                    safety_data = json.loads(json_str)
                else:
                    # Fallback parsing if JSON extraction fails
                    safety_data = self._parse_safety_response_fallback(model_response)
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                safety_data = self._parse_safety_response_fallback(model_response)
            
            return safety_data
            
        except Exception as e:
            logger.error(f"Error in Gemma safety analysis: {e}")
            return {
                "self_harm": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Analysis failed"},
                "violence": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Analysis failed"},
                "harassment": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Analysis failed"},
                "dangerous_content": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Analysis failed"}
            }
    
    def _parse_safety_response_fallback(self, response: str) -> Dict[str, any]:
        """Fallback parser for safety response when JSON parsing fails"""
        response_lower = response.lower()
        
        # Default safety categories
        safety_data = {
            "self_harm": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Fallback analysis"},
            "violence": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Fallback analysis"},
            "harassment": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Fallback analysis"},
            "dangerous_content": {"detected": False, "confidence": 0.0, "severity": "low", "reasoning": "Fallback analysis"}
        }
        
        # Simple keyword-based fallback analysis
        self_harm_indicators = ["self-harm", "suicide", "kill myself", "hurt myself", "cut myself"]
        violence_indicators = ["violence", "hurt someone", "attack", "fight", "threaten"]
        harassment_indicators = ["harassment", "abuse", "threaten", "intimidate", "bully"]
        dangerous_indicators = ["dangerous", "overdose", "drugs", "poison", "harmful"]
        
        # Check for self-harm
        if any(indicator in response_lower for indicator in self_harm_indicators):
            safety_data["self_harm"] = {"detected": True, "confidence": 0.7, "severity": "high", "reasoning": "Self-harm indicators detected"}
        
        # Check for violence
        if any(indicator in response_lower for indicator in violence_indicators):
            safety_data["violence"] = {"detected": True, "confidence": 0.6, "severity": "medium", "reasoning": "Violence indicators detected"}
        
        # Check for harassment
        if any(indicator in response_lower for indicator in harassment_indicators):
            safety_data["harassment"] = {"detected": True, "confidence": 0.6, "severity": "medium", "reasoning": "Harassment indicators detected"}
        
        # Check for dangerous content
        if any(indicator in response_lower for indicator in dangerous_indicators):
            safety_data["dangerous_content"] = {"detected": True, "confidence": 0.6, "severity": "medium", "reasoning": "Dangerous content indicators detected"}
        
        return safety_data
    
    def _map_safety_to_crisis(self, safety_category: str) -> Optional[str]:
        """Map Gemma safety categories to crisis categories"""
        mapping = {
            "self_harm": "self_harm",
            "violence": "violence", 
            "harassment": "abuse",
            "dangerous_content": "overdose"
        }
        return mapping.get(safety_category)
    
    def detect_multimodal_crisis(self, text: str = None, image: Union[str, Image.Image] = None) -> Dict[str, any]:
        """
        Detect crisis situations from multimodal input using Gemma safety features
        
        Args:
            text: Text input (optional)
            image: Image input (optional)
            
        Returns:
            Combined crisis detection results
        """
        results = {
            "crisis_detected": False,
            "text_analysis": None,
            "image_analysis": None,
            "combined_confidence": 0.0,
            "primary_category": None,
            "immediate_risk": False
        }
        
        # Analyze text if provided
        if text:
            text_results = self.detect_crisis_from_text(text)
            results["text_analysis"] = text_results
            
            if text_results["crisis_detected"]:
                results["crisis_detected"] = True
                results["combined_confidence"] = max(results["combined_confidence"], text_results["confidence"])
                
                # Determine primary category
                if text_results["categories"]:
                    primary = max(text_results["categories"], key=lambda x: x["confidence"])
                    results["primary_category"] = primary["category"]
        
        # Analyze image if provided
        if image:
            image_results = self.detect_crisis_from_image(image)
            results["image_analysis"] = image_results
            
            if image_results["crisis_detected"]:
                results["crisis_detected"] = True
                results["combined_confidence"] = max(results["combined_confidence"], image_results["confidence"])
        
        # Check for immediate risk from text analysis
        if results["text_analysis"]:
            results["immediate_risk"] = results["text_analysis"].get("immediate_risk", False)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Initialize the crisis detector
    detector = CrisisDetector()
    
    # Test with sample text
    test_text = "I'm thinking about hurting myself tonight"
    results = detector.detect_crisis_from_text(test_text)
    print(f"Crisis detection results: {results}")
