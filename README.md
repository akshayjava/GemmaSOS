# GemmaSOS - On-Device Crisis Response and Intervention System

A privacy-focused, on-device crisis intervention system using Google's Gemma lightweight model to detect crisis situations and provide empathetic support and resources.

## 🔒 Privacy & Security

- **100% On-Device Processing**: All analysis happens locally on your device
- **No Data Transmission**: Nothing is sent to external servers
- **Temporary Storage Only**: No permanent storage of user content
- **Automatic Cleanup**: Data is automatically cleaned up after sessions

## 🚨 Crisis Detection Capabilities

The system can detect and respond to:

- **Self-Harm**: Cutting, burning, self-injury behaviors
- **Suicide Risk**: Suicidal thoughts, plans, or ideation
- **Violence**: Threats of violence toward self or others
- **Abuse**: Physical, emotional, or sexual abuse situations
- **Overdose**: Drug overdose or poisoning situations

## 🛠️ Features

### Multimodal Detection
- **Text Analysis**: Detects crisis indicators in written messages
- **Image Analysis**: Analyzes images for potential crisis indicators
- **Combined Processing**: Integrates both text and image analysis

### Empathetic Response Generation
- **Trauma-Informed**: Uses evidence-based crisis intervention techniques
- **Personalized Responses**: Generates contextually appropriate responses
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

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd GemmaSOS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main_app.py
   ```

4. **Access the interface**:
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

- **Interactive Testing**: Test crisis detection with sample scenarios
- **Model Simulation**: See how Gemma model analysis works
- **Response Generation**: View empathetic response generation
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
    
    # Detect crisis
    crisis_result = crisis_detector.detect_crisis_from_text(text)
    
    if crisis_result["crisis_detected"]:
        # Generate crisis response
        response = response_generator.generate_response(
            crisis_type=crisis_result.get("primary_category"),
            user_message=text,
            confidence=crisis_result["combined_confidence"],
            immediate_risk=crisis_result["immediate_risk"]
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
The system uses Google's Gemma-2B model by default. You can modify the model in the configuration:

```python
# In crisis_detector.py and response_generator.py
model_name = "google/gemma-2b-it"  # Change this if needed
```

### Safety Thresholds
Adjust crisis detection sensitivity in `safety_system.py`:

```python
self.safety_thresholds = {
    "immediate_risk": 0.8,
    "high_risk": 0.6,
    "medium_risk": 0.4,
    "low_risk": 0.2
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
- **Green Status**: No crisis detected
- **Yellow Status**: Low to medium risk detected
- **Red Status**: High risk or immediate danger detected

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
   - Multimodal crisis detection
   - Keyword-based analysis
   - Gemma model integration

2. **CrisisResponseGenerator** (`response_generator.py`)
   - Empathetic response generation
   - Resource database management
   - Safety planning

3. **SafetySystem** (`safety_system.py`)
   - Privacy protection
   - Content filtering
   - Risk assessment

4. **MainApp** (`main_app.py`)
   - User interface
   - Component integration
   - Session management

### Data Flow

```
User Input → Safety Validation → Crisis Detection → Response Generation → User Interface
     ↓              ↓                    ↓                    ↓
Privacy Check → Content Filter → Risk Assessment → Resource Matching
```

## 🔍 Crisis Detection Methods

### Text Analysis
- **Keyword Matching**: Identifies crisis-related terms
- **Context Analysis**: Uses Gemma model for deeper understanding
- **Severity Assessment**: Evaluates immediacy and risk level

### Image Analysis
- **Color Analysis**: Detects potential blood or injury indicators
- **Edge Detection**: Identifies sharp objects or tools
- **Pattern Recognition**: Analyzes visual crisis indicators

### Combined Analysis
- **Multimodal Fusion**: Integrates text and image analysis
- **Confidence Scoring**: Provides reliability metrics
- **Risk Prioritization**: Determines appropriate response level

## 🛡️ Safety Features

### Content Filtering
- Blocks harmful instructional content
- Filters triggering material
- Prevents dangerous advice

### Privacy Protection
- No data logging
- Temporary processing only
- Automatic cleanup
- No external transmission

### Risk Management
- Immediate risk detection
- Escalation procedures
- Emergency resource access
- Safety planning

## 📊 Performance

### System Requirements
- **Minimum**: 4GB RAM, CPU-only processing
- **Recommended**: 8GB RAM, GPU acceleration
- **Model Size**: ~5GB for Gemma-2B
- **Processing Time**: 1-3 seconds per analysis

### Optimization
- Model quantization for faster inference
- Batch processing for multiple inputs
- Memory management for long sessions
- Automatic cleanup of temporary data

## 🧪 Testing

### Crisis Scenarios
The system has been tested with various crisis scenarios:

- Self-harm indicators
- Suicidal ideation
- Violence threats
- Abuse situations
- Overdose scenarios

### Safety Testing
- Content filtering effectiveness
- Privacy protection verification
- Response appropriateness
- Resource accuracy

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
