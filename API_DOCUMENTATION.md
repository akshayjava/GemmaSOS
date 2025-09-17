# GemmaSOS API Documentation

## Overview

The GemmaSOS API provides on-device crisis detection and response generation capabilities. All processing happens locally on your device, ensuring complete privacy and security.

## Core Components

### 1. CrisisDetector

Detects crisis situations from text and image input using Google's Gemma model.

#### Methods

##### `detect_crisis_from_text(text: str) -> Dict[str, Any]`

Detects crisis situations from text input.

**Parameters:**
- `text` (str): Input text to analyze

**Returns:**
```python
{
    "crisis_detected": bool,
    "categories": List[Dict],
    "confidence": float,
    "gemma_analysis": Dict
}
```

**Example:**
```python
from crisis_detector import CrisisDetector

detector = CrisisDetector()
result = detector.detect_crisis_from_text("I want to hurt myself")

print(result["crisis_detected"])  # True
print(result["categories"])       # [{"category": "self_harm", "confidence": 0.8}]
```

##### `detect_crisis_from_image(image: Union[str, Image.Image]) -> Dict[str, Any]`

Detects crisis situations from image input.

**Parameters:**
- `image` (str or PIL.Image): Image path or PIL Image object

**Returns:**
```python
{
    "crisis_detected": bool,
    "indicators": List[Dict],
    "confidence": float
}
```

##### `detect_multimodal_crisis(text: str = None, image: Union[str, Image.Image] = None) -> Dict[str, Any]`

Detects crisis situations from multimodal input.

**Parameters:**
- `text` (str, optional): Text input
- `image` (str or PIL.Image, optional): Image input

**Returns:**
```python
{
    "crisis_detected": bool,
    "text_analysis": Dict,
    "image_analysis": Dict,
    "combined_confidence": float,
    "primary_category": str,
    "immediate_risk": bool
}
```

### 2. CrisisResponseGenerator

Generates empathetic, trauma-informed responses for crisis situations.

#### Methods

##### `generate_response(crisis_type: str, user_message: str, confidence: float, immediate_risk: bool = False) -> Dict[str, Any]`

Generates an empathetic response for a crisis situation.

**Parameters:**
- `crisis_type` (str): Type of crisis detected
- `user_message` (str): User's original message
- `confidence` (float): Confidence level of crisis detection
- `immediate_risk` (bool): Whether there's immediate risk

**Returns:**
```python
{
    "response": str,
    "resources": List[Dict],
    "safety_plan": Dict,
    "immediate_risk": bool,
    "crisis_type": str,
    "confidence": float
}
```

**Example:**
```python
from response_generator import CrisisResponseGenerator

generator = CrisisResponseGenerator()
response = generator.generate_response(
    crisis_type="self_harm",
    user_message="I want to cut myself",
    confidence=0.8,
    immediate_risk=True
)

print(response["response"])  # Empathetic response text
print(response["resources"]) # List of crisis resources
```

### 3. SafetySystem

Handles safety measures, privacy protection, and content filtering.

#### Methods

##### `validate_input(text: str = None, image_path: str = None) -> Dict[str, Any]`

Validates input for safety and appropriateness.

**Parameters:**
- `text` (str, optional): Text input to validate
- `image_path` (str, optional): Path to image file to validate

**Returns:**
```python
{
    "is_safe": bool,
    "warnings": List[str],
    "blocked_content": List[str],
    "recommendations": List[str]
}
```

##### `assess_risk_level(crisis_detection_result: Dict[str, Any]) -> str`

Assesses risk level based on crisis detection results.

**Parameters:**
- `crisis_detection_result` (Dict): Results from crisis detection

**Returns:**
- `str`: Risk level ('immediate', 'high', 'medium', 'low', or 'none')

##### `get_safety_actions(risk_level: str) -> List[Dict[str, str]]`

Gets recommended safety actions based on risk level.

**Parameters:**
- `risk_level` (str): Assessed risk level

**Returns:**
```python
[
    {
        "action": str,
        "description": str,
        "priority": str
    }
]
```

## Crisis Types

The system detects the following crisis types:

### 1. Self-Harm
- **Keywords**: cut, cutting, self harm, hurt myself, bleeding, razor, knife
- **Severity Indicators**: bleeding, hospital, emergency, serious

### 2. Suicide
- **Keywords**: kill myself, end it all, suicide, take my life, not worth living
- **Severity Indicators**: plan, method, tonight, today, now

### 3. Violence
- **Keywords**: hurt someone, attack, fight, violence, threaten
- **Severity Indicators**: gun, weapon, tonight, today, plan

### 4. Abuse
- **Keywords**: abuse, hit me, scared, unsafe, control, manipulate
- **Severity Indicators**: emergency, police, help, danger, now

### 5. Overdose
- **Keywords**: overdose, too many pills, unconscious, sick, poison
- **Severity Indicators**: unconscious, emergency, hospital, ambulance, now

## Response Templates

### Crisis Response Structure

```python
{
    "response": "Empathetic response text",
    "resources": [
        {
            "name": "Resource Name",
            "number": "Phone Number",
            "website": "Website URL",
            "description": "Resource Description"
        }
    ],
    "safety_plan": {
        "immediate_actions": ["Action 1", "Action 2"],
        "coping_strategies": ["Strategy 1", "Strategy 2"],
        "warning_signs": ["Sign 1", "Sign 2"],
        "emergency_contacts": ["Contact 1", "Contact 2"]
    }
}
```

## Crisis Resources

### General Resources
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

### Specialized Resources
- **Self-Harm**: Self-Injury Outreach & Support (sioutreach.org)
- **Suicide**: American Foundation for Suicide Prevention (afsp.org)
- **Violence**: National Domestic Violence Hotline (1-800-799-7233)
- **Abuse**: Childhelp National Child Abuse Hotline (1-800-4-A-CHILD)
- **Overdose**: SAMHSA National Helpline (1-800-662-4357)

## Error Handling

### Common Exceptions

#### `ModelLoadError`
Raised when the Gemma model fails to load.

```python
try:
    detector = CrisisDetector()
except ModelLoadError as e:
    print(f"Failed to load model: {e}")
```

#### `ValidationError`
Raised when input validation fails.

```python
try:
    validation = safety_system.validate_input(text=text)
    if not validation["is_safe"]:
        raise ValidationError("Unsafe content detected")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

#### `ProcessingError`
Raised when crisis detection or response generation fails.

```python
try:
    result = detector.detect_crisis_from_text(text)
except ProcessingError as e:
    print(f"Processing failed: {e}")
```

## Configuration

### Model Configuration

```python
# config.py
MODEL_NAME = "google/gemma-2b-it"
MODEL_CACHE_DIR = "~/.cache/huggingface/transformers"
MODEL_PRECISION = "float16"  # or "float32"
```

### Safety Thresholds

```python
SAFETY_THRESHOLDS = {
    "immediate_risk": 0.8,
    "high_risk": 0.6,
    "medium_risk": 0.4,
    "low_risk": 0.2
}
```

### Privacy Settings

```python
PRIVACY_CONFIG = {
    "data_retention_hours": 0,  # Immediate cleanup
    "max_session_duration_hours": 8,
    "auto_cleanup_interval_hours": 1,
    "max_log_entries": 100
}
```

## Performance Considerations

### Memory Usage
- **Minimum**: 4GB RAM
- **Recommended**: 8GB RAM
- **Model Size**: ~5GB for Gemma-2B

### Processing Time
- **Text Analysis**: 1-3 seconds
- **Image Analysis**: 2-5 seconds
- **Response Generation**: 1-2 seconds

### Optimization Tips
1. Use model quantization for faster inference
2. Enable model caching for repeated use
3. Set appropriate memory limits
4. Use batch processing for multiple inputs

## Privacy and Security

### On-Device Processing
- All analysis happens locally
- No data sent to external servers
- Complete privacy protection

### Data Handling
- Temporary processing only
- Automatic cleanup after sessions
- No permanent storage of user content

### Content Filtering
- Blocks harmful instructional content
- Filters triggering material
- Prevents dangerous advice

## Testing

### Unit Tests

```python
import unittest
from crisis_detector import CrisisDetector

class TestCrisisDetection(unittest.TestCase):
    def setUp(self):
        self.detector = CrisisDetector()
    
    def test_self_harm_detection(self):
        result = self.detector.detect_crisis_from_text("I want to cut myself")
        self.assertTrue(result["crisis_detected"])
        self.assertEqual(result["categories"][0]["category"], "self_harm")
    
    def test_no_crisis_detection(self):
        result = self.detector.detect_crisis_from_text("Hello, how are you?")
        self.assertFalse(result["crisis_detected"])
```

### Integration Tests

```python
def test_end_to_end_flow():
    detector = CrisisDetector()
    generator = CrisisResponseGenerator()
    
    # Test crisis detection and response
    crisis_result = detector.detect_crisis_from_text("I want to hurt myself")
    assert crisis_result["crisis_detected"]
    
    response = generator.generate_response(
        crisis_type=crisis_result["categories"][0]["category"],
        user_message="I want to hurt myself",
        confidence=crisis_result["confidence"]
    )
    assert "crisis" in response["response"].lower()
    assert len(response["resources"]) > 0
```

## Troubleshooting

### Common Issues

#### Model Loading Fails
```python
# Check available memory
import psutil
print(f"Available memory: {psutil.virtual_memory().available / (1024**3):.1f} GB")

# Try loading with CPU only
detector = CrisisDetector(device="cpu")
```

#### Low Detection Accuracy
```python
# Adjust sensitivity thresholds
from config import Config
Config.SAFETY_THRESHOLDS["low_risk"] = 0.1  # More sensitive
```

#### Memory Issues
```python
# Enable model cleanup
safety_system.cleanup_session_data()
safety_system.cleanup()
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging
detector = CrisisDetector()
detector.debug_mode = True
```

## Support

For technical support or questions about the API:
- Check the main README.md file
- Review the integration examples in `examples/`
- Contact the development team

## License

This API is licensed under the MIT License. See the LICENSE file for details.
