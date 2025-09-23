# GemmaSOS - On-Device Crisis Response and Intervention System

A privacy-focused, on-device crisis intervention system using Google's Gemma model with built-in safety features to detect crisis situations and provide empathetic support and resources.

## 🔒 Privacy & Security

- **100% On-Device Processing**: All analysis happens locally on your device
- **No Data Transmission**: Nothing is sent to external servers
- **Temporary Storage Only**: No permanent storage of user content
- **Automatic Cleanup**: Data is automatically cleaned up after sessions

## 🚨 Crisis Detection Capabilities

The system uses Gemma's built-in safety features to detect and respond to:

- **Self-Harm Content**: Detects expressions of self-injury, suicide ideation, or self-destructive behavior
- **Violence Threats**: Identifies threats of violence toward self or others
- **Harassment/Abuse**: Recognizes abusive, threatening, or intimidating content
- **Dangerous Content**: Detects content promoting dangerous activities or substance abuse

### Safety Analysis Features
- **Context-Aware Detection**: Uses advanced language understanding instead of simple keyword matching
- **Severity Assessment**: Provides detailed severity levels (low, medium, high)
- **Reasoning Transparency**: Explains why content was flagged as harmful
- **Confidence Scoring**: Provides reliability metrics for each detection

## 🛠️ Features

### Safety-Based Detection
- **Gemma Safety Analysis**: Leverages Google's advanced safety content moderation
- **Context-Aware Processing**: Understands nuanced language and context
- **Multimodal Support**: Analyzes both text and images using safety features
- **Real-Time Assessment**: Provides immediate safety evaluation

### Empathetic Response Generation
- **Safety-Aware Responses**: Generates responses based on detailed safety analysis
- **Trauma-Informed**: Uses evidence-based crisis intervention techniques
- **Personalized Responses**: Creates contextually appropriate responses with safety context
- **Resource Integration**: Provides relevant helpline and support resources

### Safety Measures
- **Content Filtering**: Blocks harmful or triggering content
- **Risk Assessment**: Evaluates crisis severity levels
- **Safety Planning**: Provides immediate safety recommendations
- **Emergency Resources**: Quick access to crisis hotlines and emergency services

## 📋 Requirements

- Python 3.8 or higher
- 4GB+ RAM (8GB recommended)
- GPU support recommended but not required
- Internet connection for initial model download

## 🚀 Quick Start

### Option 1: Demo (Recommended for Testing)
Test the safety-based approach without full installation:

```bash
# Run the demo application
python demo_app.py

# Access the demo interface
# Open your browser to http://localhost:7861
```

### Option 2: Full Installation
Install the complete system with Gemma safety features:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd GemmaSOS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the safety approach**:
   ```bash
   python test_safety_approach.py
   ```

4. **Run the main application**:
   ```bash
   python main_app.py
   ```

5. **Access the interface**:
   Open your browser to `http://localhost:7860`

## 🧪 Demo Application

### Quick Demo (No Full Installation Required)

Test the system's capabilities without installing the full Gemma model:

1. **Run the demo**:
   ```bash
   python run_demo.py
   ```

2. **Access the demo**:
   Open your browser to `http://localhost:7861`

3. **Test scenarios**:
   - Load predefined crisis scenarios
   - Test custom text input
   - See crisis detection in action
   - Review generated responses

### Demo Features

- **Safety Analysis Testing**: Test Gemma's safety features with sample scenarios
- **Crisis Detection Simulation**: See how safety categories map to crisis types
- **Safety-Aware Response Generation**: View empathetic responses with safety context
- **Resource Matching**: See how appropriate resources are provided
- **Privacy Demonstration**: Understand on-device processing

### Demo Scenarios

The demo includes 12 test scenarios covering:
- **Crisis Situations**: Self-harm, suicide, violence, abuse, overdose
- **Subtle Indicators**: Less obvious crisis situations
- **Non-Crisis**: General stress and relationship issues

See `DEMO_GUIDE.md` for detailed testing instructions.

## 🔌 Integration Guide

### Quick Integration

The GemmaSOS system is designed for easy integration into existing applications. Choose your integration method:

#### **1. Direct Integration (Recommended)**
```python
from crisis_detector import CrisisDetector
from response_generator import CrisisResponseGenerator
from safety_system import SafetySystem

# Initialize components
crisis_detector = CrisisDetector()
response_generator = CrisisResponseGenerator()
safety_system = SafetySystem()

# Process user input
def handle_user_message(text):
    # Validate input
    validation = safety_system.validate_input(text=text)
    if not validation["is_safe"]:
        return "Content cannot be processed safely."
    
    # Detect crisis using safety analysis
    crisis_result = crisis_detector.detect_crisis_from_text(text)
    
    if crisis_result["crisis_detected"]:
        # Generate safety-aware crisis response
        response = response_generator.generate_response(
            crisis_type=crisis_result.get("primary_category"),
            user_message=text,
            confidence=crisis_result["combined_confidence"],
            immediate_risk=crisis_result["immediate_risk"],
            safety_analysis=crisis_result.get("safety_analysis")
        )
        return response["response"]
    else:
        return "No crisis detected. Normal processing continues."
```

#### **2. API Integration**
```python
import requests

def analyze_crisis(text):
    response = requests.post('http://localhost:5000/analyze', 
                           json={'text': text})
    return response.json()
```

#### **3. Mobile SDK Integration**
```swift
// iOS Swift
let sdk = CrisisResponseSDK()
let result = sdk.analyzeText(userInput)
if result.isCrisis {
    showCrisisResponse(result.response)
}
```

### Integration Examples

See the `examples/` directory for complete integration examples:
- **Web App Integration** (`examples/web_app/`)
- **Mobile App Integration** (`examples/mobile_app/`)
- **API Server Integration** (`examples/api_server/`)
- **Chat Bot Integration** (`examples/chatbot/`)

### API Documentation

Complete API documentation is available in `API_DOCUMENTATION.md`.

## 🔧 Configuration

### Model Selection
The system uses Google's Gemma-2B model with built-in safety features by default. You can modify the model in the configuration:

```python
# In crisis_detector.py and response_generator.py
model_name = "google/gemma-2b-it"  # Change this if needed
```

### Safety Configuration
Configure Gemma safety analysis parameters in `config.py`:

```python
SAFETY_ANALYSIS_CONFIG = {
    "confidence_threshold": 0.3,
    "high_severity_threshold": 0.7,
    "immediate_risk_indicators": ["high", "immediate", "urgent"],
    "response_temperature": 0.6,
    "max_safety_tokens": 300
}
```

### Safety Categories
The system analyzes content across these safety categories:

```python
GEMMA_SAFETY_CATEGORIES = {
    "self_harm": "Content expressing intent to harm oneself",
    "violence": "Content expressing intent to harm others", 
    "harassment": "Content that is abusive or threatening",
    "dangerous_content": "Content promoting dangerous activities"
}
```

## 📱 Usage

### Text Input
1. Type your message in the text box
2. Click "Send" or press Enter
3. The system will analyze for crisis indicators
4. Receive empathetic response and resources

### Image Input
1. Upload an image using the image input
2. The system will analyze for visual crisis indicators
3. Receive appropriate response and resources

### Crisis Detection
- **Green Status**: No safety concerns detected
- **Yellow Status**: Low to medium safety risk detected
- **Red Status**: High safety risk or immediate danger detected

## 🆘 Emergency Resources

### Immediate Help
- **911**: Emergency Services
- **988**: Suicide & Crisis Lifeline
- **Text HOME to 741741**: Crisis Text Line

### 24/7 Support
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **National Domestic Violence Hotline**: 1-800-799-7233
- **National Sexual Assault Hotline**: 1-800-656-4673

## 🏗️ Architecture

### Components

1. **CrisisDetector** (`crisis_detector.py`)
   - Safety-based crisis detection using Gemma's built-in features
   - Context-aware analysis with severity assessment
   - Multimodal safety evaluation

2. **CrisisResponseGenerator** (`response_generator.py`)
   - Safety-aware empathetic response generation
   - Resource database management
   - Safety planning with detailed analysis context

3. **SafetySystem** (`safety_system.py`)
   - Privacy protection and content filtering
   - Safety analysis integration
   - Risk assessment based on Gemma safety features

4. **MainApp** (`main_app.py`)
   - User interface with safety analysis display
   - Component integration
   - Session management

### Data Flow

```
User Input → Safety Validation → Gemma Safety Analysis → Crisis Detection → Safety-Aware Response → User Interface
     ↓              ↓                    ↓                    ↓                    ↓
Privacy Check → Content Filter → Safety Categories → Severity Assessment → Resource Matching
```

## 🔍 Safety-Based Detection Methods

### Gemma Safety Analysis
- **Context-Aware Detection**: Uses advanced language understanding instead of keyword matching
- **Safety Categories**: Analyzes content across self-harm, violence, harassment, and dangerous content
- **Severity Assessment**: Provides detailed severity levels (low, medium, high) with reasoning
- **Confidence Scoring**: Offers reliability metrics for each safety category

### Text Analysis
- **Safety Content Moderation**: Leverages Gemma's built-in safety features
- **Structured Analysis**: Uses JSON-formatted safety analysis with detailed reasoning
- **Real-Time Processing**: Provides immediate safety evaluation
- **Fallback Parsing**: Handles edge cases when structured analysis fails

### Image Analysis
- **Visual Safety Analysis**: Extends safety features to image content
- **Color Analysis**: Detects potential blood or injury indicators
- **Edge Detection**: Identifies sharp objects or tools
- **Pattern Recognition**: Analyzes visual crisis indicators

### Combined Analysis
- **Multimodal Safety Fusion**: Integrates text and image safety analysis
- **Crisis Category Mapping**: Maps safety categories to specific crisis types
- **Risk Prioritization**: Determines appropriate response level based on safety severity

## 🛡️ Safety Features

### Gemma Safety Integration
- **Built-in Safety Analysis**: Leverages Google's advanced content moderation
- **Context-Aware Detection**: Understands nuanced language and context
- **Structured Safety Assessment**: Provides detailed reasoning for safety decisions
- **Real-Time Processing**: Immediate safety evaluation with confidence scoring

### Content Filtering
- **Safety-Based Filtering**: Uses Gemma's safety categories for content assessment
- **Harmful Content Detection**: Identifies and blocks dangerous instructional content
- **Triggering Material Filtering**: Prevents exposure to potentially harmful content
- **Dangerous Advice Prevention**: Blocks content that could lead to harm

### Privacy Protection
- **100% On-Device Processing**: All safety analysis happens locally
- **No Data Logging**: No storage of user content or safety analysis
- **Temporary Processing Only**: Data is processed and immediately discarded
- **No External Transmission**: Nothing is sent to external servers

### Risk Management
- **Severity-Based Risk Assessment**: Uses detailed safety severity levels
- **Immediate Risk Detection**: Identifies high-severity safety concerns
- **Escalation Procedures**: Appropriate response based on safety analysis
- **Emergency Resource Access**: Quick access to crisis hotlines and emergency services

## ✨ Benefits of Safety-Based Approach

### Enhanced Accuracy
- **Context Understanding**: Goes beyond keyword matching to understand full context
- **Nuanced Detection**: Recognizes subtle expressions of distress and crisis
- **Reduced False Positives**: Better accuracy in distinguishing crisis from non-crisis content
- **Severity Assessment**: Provides detailed severity levels for appropriate response

### Improved Response Quality
- **Safety-Aware Responses**: Generates responses based on detailed safety analysis
- **Contextual Appropriateness**: Responses are tailored to specific safety concerns
- **Better Resource Matching**: More accurate matching of resources to crisis types
- **Enhanced Empathy**: More sophisticated understanding leads to better empathetic responses

### Future-Proof Technology
- **Google's Ongoing Improvements**: Benefits from Google's continuous safety feature updates
- **Advanced AI Capabilities**: Leverages cutting-edge language understanding
- **Scalable Architecture**: Can easily integrate new safety categories as they become available
- **Research-Backed**: Based on Google's extensive safety research and development

## 📊 Performance

### System Requirements
- **Minimum**: 4GB RAM, CPU-only processing
- **Recommended**: 8GB RAM, GPU acceleration
- **Model Size**: ~5GB for Gemma-2B with safety features
- **Processing Time**: 1-3 seconds per safety analysis

### Optimization
- **Safety Analysis Optimization**: Efficient processing of Gemma's safety features
- **Model Quantization**: Faster inference while maintaining safety accuracy
- **Batch Processing**: Multiple safety analyses in parallel
- **Memory Management**: Efficient handling of safety analysis data

## 🧪 Testing

### Safety Analysis Testing
The system has been tested with various safety scenarios:

- **Self-Harm Content**: Expressions of self-injury and suicide ideation
- **Violence Threats**: Threats of violence toward self or others
- **Harassment/Abuse**: Abusive, threatening, or intimidating content
- **Dangerous Content**: Content promoting dangerous activities or substance abuse

### Safety Testing
- **Safety Analysis Accuracy**: Tests Gemma's safety feature effectiveness
- **Context Understanding**: Validates nuanced language comprehension
- **Severity Assessment**: Verifies appropriate severity level assignment
- **Response Quality**: Ensures safety-aware responses are appropriate
- **Privacy Protection**: Confirms on-device processing and data protection

### Test Scripts
- **`test_safety_approach.py`**: Comprehensive testing of safety-based detection
- **`test_inadequate_responses.py`**: Quality assessment of response generation
- **`test_system.py`**: Overall system functionality testing

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Guidelines
- Maintain privacy-first approach
- Ensure crisis response appropriateness
- Test with various scenarios
- Document all changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

**Important**: This system is designed to provide support and resources, but it is not a replacement for professional mental health care or emergency services. If you or someone you know is in immediate danger, please call 911 or your local emergency services immediately.

## 🆘 Crisis Support

If you're experiencing a mental health crisis:

1. **Immediate Danger**: Call 911
2. **Suicide Risk**: Call 988 (Suicide & Crisis Lifeline)
3. **General Crisis**: Text HOME to 741741
4. **Domestic Violence**: Call 1-800-799-7233

## 📞 Support

For technical support or questions about this system:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Remember**: Your mental health matters. You are not alone, and help is available.
