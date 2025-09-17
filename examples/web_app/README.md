# Web App Integration Example

This example demonstrates how to integrate GemmaSOS crisis detection into a Flask web application.

## Features

- **Real-time Crisis Detection**: Detects crisis situations in user messages
- **Empathetic Responses**: Provides supportive responses for crisis situations
- **Resource Integration**: Shows relevant crisis resources and helplines
- **Privacy Protection**: All processing happens on-device
- **Session Management**: Maintains conversation history per user
- **Safety Planning**: Provides immediate safety actions for high-risk situations

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy GemmaSOS components**:
   ```bash
   cp ../../crisis_detector.py .
   cp ../../response_generator.py .
   cp ../../safety_system.py .
   cp ../../config.py .
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser**:
   Navigate to `http://localhost:5000`

## Usage

### Basic Chat
- Type messages in the input field
- Press Enter or click Send to send messages
- The system will analyze each message for crisis indicators

### Crisis Detection
- When crisis indicators are detected, the system will:
  - Show a crisis response with empathetic language
  - Display relevant resources and helplines
  - Provide safety planning information
  - Change the UI to indicate crisis mode

### Normal Messages
- Non-crisis messages receive normal responses
- The system continues regular chat functionality

## API Endpoints

### POST /api/message
Send a message for analysis.

**Request:**
```json
{
    "message": "I want to hurt myself"
}
```

**Response:**
```json
{
    "crisis_detected": true,
    "response": "I can hear that you're in a lot of pain...",
    "resources": [
        {
            "name": "National Suicide Prevention Lifeline",
            "number": "988"
        }
    ],
    "safety_plan": {
        "immediate_actions": ["Call 911 if in immediate danger"]
    },
    "confidence": 0.8,
    "risk_level": "high"
}
```

### GET /api/history
Get conversation history for the current session.

**Response:**
```json
[
    {
        "timestamp": "2024-01-01T12:00:00",
        "user_message": "Hello",
        "crisis_detected": false,
        "confidence": 0.0
    }
]
```

### POST /api/clear
Clear conversation history for the current session.

**Response:**
```json
{
    "success": true
}
```

### GET /api/status
Get system status.

**Response:**
```json
{
    "status": "running",
    "privacy": "on_device_only",
    "model_loaded": true,
    "timestamp": "2024-01-01T12:00:00"
}
```

## Customization

### Modify Crisis Detection
Edit the crisis detection logic in `app.py`:

```python
def process_message(self, user_id, message):
    # Add custom validation
    if self.custom_validation(message):
        return {"error": "Custom validation failed"}
    
    # Continue with crisis detection...
```

### Customize Responses
Modify response generation:

```python
if crisis_result["crisis_detected"]:
    # Add custom response logic
    response = self.response_generator.generate_response(...)
    
    # Add custom resources
    response["resources"].extend(self.get_custom_resources())
    
    return response
```

### UI Customization
Modify `templates/index.html` to match your app's design:

```css
.crisis-message {
    background-color: #your-crisis-color;
    border-left: 4px solid #your-border-color;
}
```

## Security Considerations

### Session Management
- Uses Flask sessions for user identification
- Sessions are stored server-side
- Consider using secure session cookies in production

### Input Validation
- All input is validated through the safety system
- Unsafe content is blocked before processing
- No user content is permanently stored

### Privacy Protection
- All crisis detection happens on-device
- No data is sent to external servers
- Conversation history is stored in memory only

## Production Deployment

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export MODEL_CACHE_DIR=/path/to/model/cache
```

### Database Integration
For persistent conversation history:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    message = db.Column(db.Text, nullable=False)
    crisis_detected = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

### Load Balancing
For multiple instances:

```python
from flask_session import Session

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
Session(app)
```

## Testing

### Unit Tests
```python
import unittest
from app import crisis_app

class TestCrisisIntegration(unittest.TestCase):
    def test_crisis_detection(self):
        result = crisis_app.process_message("test_user", "I want to hurt myself")
        self.assertTrue(result["crisis_detected"])
    
    def test_normal_message(self):
        result = crisis_app.process_message("test_user", "Hello")
        self.assertFalse(result["crisis_detected"])
```

### Integration Tests
```python
def test_api_endpoints():
    with app.test_client() as client:
        # Test message endpoint
        response = client.post('/api/message', 
                             json={'message': 'I want to hurt myself'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['crisis_detected'] == True
```

## Troubleshooting

### Common Issues

1. **Model Loading Fails**
   - Check available memory (minimum 4GB)
   - Verify model files are downloaded
   - Try loading with CPU only

2. **Slow Response Times**
   - Enable model caching
   - Use model quantization
   - Consider using GPU acceleration

3. **Memory Issues**
   - Implement conversation cleanup
   - Use database for persistent storage
   - Monitor memory usage

### Debug Mode
```python
app.config['DEBUG'] = True
app.config['TESTING'] = True
```

## Support

For issues with this integration example:
- Check the main GemmaSOS documentation
- Review the API documentation
- Contact the development team
