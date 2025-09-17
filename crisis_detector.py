"""
Crisis Detection System using Google's Gemma Model
Detects various crisis situations from multimodal input (text, images)
"""

import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor
from PIL import Image
import cv2
import re
from typing import Dict, List, Tuple, Optional, Union
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrisisDetector:
    """
    On-device crisis detection system using Gemma model
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
        
        # Crisis categories and their keywords from config
        self.crisis_categories = {}
        for category, keywords in Config.CRISIS_KEYWORDS.items():
            self.crisis_categories[category] = {
                "keywords": keywords,
                "severity_keywords": Config.SEVERITY_KEYWORDS.get(category, [])
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
        Detect crisis situations from text input
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing crisis detection results
        """
        if not text or not text.strip():
            return {"crisis_detected": False, "categories": [], "confidence": 0.0}
        
        text_lower = text.lower()
        detected_crises = []
        max_confidence = 0.0
        
        # Check each crisis category
        for category, config in self.crisis_categories.items():
            keyword_matches = sum(1 for keyword in config["keywords"] 
                                if keyword in text_lower)
            severity_matches = sum(1 for keyword in config["severity_keywords"] 
                                 if keyword in text_lower)
            
            # Calculate confidence based on keyword matches
            total_keywords = len(config["keywords"])
            confidence = (keyword_matches / total_keywords) * 0.7 + (severity_matches * 0.3)
            
            if confidence > 0.1:  # Threshold for detection
                detected_crises.append({
                    "category": category,
                    "confidence": min(confidence, 1.0),
                    "keyword_matches": keyword_matches,
                    "severity_indicators": severity_matches
                })
                max_confidence = max(max_confidence, confidence)
        
        # Use Gemma model for additional analysis if crisis detected
        if detected_crises:
            gemma_analysis = self._analyze_with_gemma(text)
            max_confidence = max(max_confidence, gemma_analysis.get("confidence", 0.0))
        
        return {
            "crisis_detected": len(detected_crises) > 0,
            "categories": detected_crises,
            "confidence": max_confidence,
            "gemma_analysis": gemma_analysis if detected_crises else None
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
    
    def _analyze_with_gemma(self, text: str) -> Dict[str, any]:
        """
        Use Gemma model for additional crisis analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            Analysis results from Gemma model
        """
        try:
            # Create a prompt for crisis analysis
            prompt = f"""<start_of_turn>user
Analyze the following text for crisis indicators. Respond with a JSON object containing:
- crisis_level: "low", "medium", "high", or "none"
- concern_areas: list of concerning topics
- immediate_risk: true/false
- recommended_action: brief recommendation

Text: "{text}"
<end_of_turn>
<start_of_turn>model"""

            # Tokenize and generate
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.3,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the model's response
            if "<start_of_turn>model" in response:
                model_response = response.split("<start_of_turn>model")[-1].strip()
            else:
                model_response = response
            
            # Parse response (basic parsing)
            crisis_level = "none"
            immediate_risk = False
            
            if "high" in model_response.lower():
                crisis_level = "high"
                immediate_risk = True
            elif "medium" in model_response.lower():
                crisis_level = "medium"
            elif "low" in model_response.lower():
                crisis_level = "low"
            
            return {
                "crisis_level": crisis_level,
                "immediate_risk": immediate_risk,
                "raw_response": model_response,
                "confidence": 0.8 if immediate_risk else 0.5
            }
            
        except Exception as e:
            logger.error(f"Error in Gemma analysis: {e}")
            return {
                "crisis_level": "none",
                "immediate_risk": False,
                "raw_response": "",
                "confidence": 0.0
            }
    
    def detect_multimodal_crisis(self, text: str = None, image: Union[str, Image.Image] = None) -> Dict[str, any]:
        """
        Detect crisis situations from multimodal input
        
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
        
        # Check for immediate risk
        if results["text_analysis"] and results["text_analysis"].get("gemma_analysis"):
            results["immediate_risk"] = results["text_analysis"]["gemma_analysis"].get("immediate_risk", False)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Initialize the crisis detector
    detector = CrisisDetector()
    
    # Test with sample text
    test_text = "I'm thinking about hurting myself tonight"
    results = detector.detect_crisis_from_text(test_text)
    print(f"Crisis detection results: {results}")
