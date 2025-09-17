# GemmaSOS Integration Examples

This directory contains complete integration examples showing how to integrate the GemmaSOS crisis response system into various types of applications.

## 📁 Directory Structure

```
examples/
├── web_app/           # Flask web application
├── mobile_app/        # Mobile app integrations
├── api_server/        # REST API server
├── chatbot/           # Discord bot integration
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Choose Your Integration Type

- **Web App**: For web-based applications (React, Vue, Angular, etc.)
- **Mobile App**: For iOS and Android applications
- **API Server**: For microservices and API-based integrations
- **Chatbot**: For Discord, Slack, or other chat platforms

### 2. Navigate to Your Example

```bash
cd examples/your_chosen_example
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Copy GemmaSOS Components

```bash
cp ../../crisis_detector.py .
cp ../../response_generator.py .
cp ../../safety_system.py .
cp ../../config.py .
```

### 5. Run the Example

```bash
python app.py  # or the appropriate run command
```

## 📱 Web App Integration

**Location**: `examples/web_app/`

**Description**: Complete Flask web application with integrated crisis detection.

**Features**:
- Real-time crisis detection
- Empathetic response generation
- Resource recommendations
- Session management
- Privacy protection

**Files**:
- `app.py` - Main Flask application
- `templates/index.html` - Web interface
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation

**Usage**:
```bash
cd examples/web_app
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## 📱 Mobile App Integration

**Location**: `examples/mobile_app/`

**Description**: iOS SDK and example application for mobile crisis detection.

**Features**:
- Native iOS SDK
- Crisis detection and response
- Resource integration
- Privacy protection
- Emergency contact integration

**Files**:
- `ios/CrisisResponseSDK.swift` - iOS SDK
- `ios/ViewController.swift` - Example app
- `android/` - Android integration (coming soon)

**Usage**:
1. Open the iOS project in Xcode
2. Install the SDK
3. Run the example app

## 🌐 API Server Integration

**Location**: `examples/api_server/`

**Description**: RESTful API server for crisis detection and response.

**Features**:
- RESTful API endpoints
- Text and image analysis
- Multimodal processing
- Session management
- Analytics and monitoring

**Files**:
- `server.py` - Main API server
- `client_example.py` - Python client example
- `requirements.txt` - Dependencies
- `README.md` - API documentation

**Usage**:
```bash
cd examples/api_server
pip install -r requirements.txt
python server.py
# API available at http://localhost:5000
```

**API Endpoints**:
- `POST /api/analyze/text` - Analyze text
- `POST /api/analyze/image` - Analyze image
- `POST /api/analyze/multimodal` - Analyze multimodal input
- `GET /api/session/<id>` - Get session data
- `GET /api/analytics` - Get analytics
- `GET /api/resources` - Get crisis resources

## 🤖 Chatbot Integration

**Location**: `examples/chatbot/`

**Description**: Discord bot with integrated crisis detection.

**Features**:
- Discord bot integration
- Real-time crisis detection
- Empathetic responses
- Resource recommendations
- Admin commands

**Files**:
- `chatbot.py` - Main Discord bot
- `requirements.txt` - Dependencies
- `README.md` - Bot documentation

**Usage**:
```bash
cd examples/chatbot
pip install -r requirements.txt
export DISCORD_BOT_TOKEN=your_bot_token
python chatbot.py
```

## 🔧 Configuration

### Environment Variables

All examples support the following environment variables:

```bash
# Model configuration
export GEMMA_SOS_MODEL="google/gemma-2b-it"
export GEMMA_SOS_DEVICE="cuda"  # or "cpu"
export GEMMA_SOS_CACHE_DIR="/path/to/cache"

# Safety thresholds
export GEMMA_SOS_IMMEDIATE_RISK_THRESHOLD="0.8"
export GEMMA_SOS_HIGH_RISK_THRESHOLD="0.6"
export GEMMA_SOS_MEDIUM_RISK_THRESHOLD="0.4"
export GEMMA_SOS_LOW_RISK_THRESHOLD="0.2"

# Privacy settings
export GEMMA_SOS_DATA_RETENTION_HOURS="0"
export GEMMA_SOS_AUTO_CLEANUP_INTERVAL="3600"
```

### Custom Configuration

Each example includes a `config.py` file that you can modify:

```python
# Customize crisis detection
CUSTOM_CRISIS_KEYWORDS = {
    "your_app_specific": [
        "custom_keyword1",
        "custom_keyword2"
    ]
}

# Customize responses
CUSTOM_RESPONSES = {
    "your_app_specific": {
        "immediate": "Your custom crisis response...",
        "supportive": "Your custom supportive response..."
    }
}
```

## 🧪 Testing

### Unit Tests

Each example includes unit tests:

```bash
# Run tests for web app
cd examples/web_app
python -m pytest tests/

# Run tests for API server
cd examples/api_server
python -m pytest tests/

# Run tests for chatbot
cd examples/chatbot
python -m pytest tests/
```

### Integration Tests

Test the complete integration:

```bash
# Test web app integration
cd examples/web_app
python test_integration.py

# Test API server integration
cd examples/api_server
python test_integration.py

# Test chatbot integration
cd examples/chatbot
python test_integration.py
```

### Performance Tests

Test performance and scalability:

```bash
# Test web app performance
cd examples/web_app
python test_performance.py

# Test API server performance
cd examples/api_server
python test_performance.py
```

## 🚀 Deployment

### Docker Deployment

Each example includes Docker configuration:

```bash
# Build and run web app
cd examples/web_app
docker build -t crisis-web-app .
docker run -p 5000:5000 crisis-web-app

# Build and run API server
cd examples/api_server
docker build -t crisis-api-server .
docker run -p 5000:5000 crisis-api-server
```

### Production Deployment

For production deployment:

1. **Use a production WSGI server** (e.g., Gunicorn for Python)
2. **Set up reverse proxy** (e.g., Nginx)
3. **Configure SSL/TLS** for secure communication
4. **Set up monitoring** and logging
5. **Configure backup** and recovery

### Cloud Deployment

Examples are compatible with:
- **AWS**: EC2, ECS, Lambda
- **Google Cloud**: Compute Engine, Cloud Run
- **Azure**: Virtual Machines, Container Instances
- **Heroku**: Direct deployment
- **DigitalOcean**: Droplets, App Platform

## 🔒 Security Considerations

### Privacy Protection

All examples implement:
- **On-device processing**: No data sent to external servers
- **Temporary storage**: No permanent storage of user content
- **Automatic cleanup**: Data cleaned up after sessions
- **Content filtering**: Unsafe content blocked

### Security Best Practices

1. **Input validation**: All input is validated before processing
2. **Rate limiting**: Prevent abuse of the system
3. **Authentication**: Secure API endpoints
4. **HTTPS**: Encrypt all communication
5. **Logging**: Privacy-safe logging only

## 📊 Monitoring and Analytics

### Built-in Analytics

Each example includes privacy-safe analytics:

```python
# Get analytics data
analytics = crisis_system.get_analytics()
print(f"Total requests: {analytics['total_requests']}")
print(f"Crisis detections: {analytics['crisis_detections']}")
print(f"Average response time: {analytics['avg_response_time']:.3f}s")
```

### Custom Metrics

Add your own metrics:

```python
# Custom metrics
class CustomMetrics:
    def __init__(self):
        self.custom_events = []
    
    def track_event(self, event_name, data):
        self.custom_events.append({
            "event": event_name,
            "data": data,
            "timestamp": datetime.now()
        })
```

## 🆘 Crisis Resources

All examples include comprehensive crisis resources:

### Emergency Resources
- **911**: Emergency Services
- **988**: Suicide & Crisis Lifeline
- **Text HOME to 741741**: Crisis Text Line

### Specialized Resources
- **Self-Harm**: Self-Injury Outreach & Support
- **Suicide**: American Foundation for Suicide Prevention
- **Violence**: National Domestic Violence Hotline
- **Abuse**: Childhelp National Child Abuse Hotline
- **Overdose**: SAMHSA National Helpline

## 🤝 Contributing

### Adding New Examples

1. Create a new directory under `examples/`
2. Include a `README.md` with documentation
3. Add a `requirements.txt` with dependencies
4. Include example code and configuration
5. Add tests and documentation

### Example Structure

```
examples/your_example/
├── README.md          # Documentation
├── requirements.txt   # Dependencies
├── app.py            # Main application
├── config.py         # Configuration
├── tests/            # Test files
└── docker/           # Docker files
```

## 📞 Support

### Getting Help

1. **Documentation**: Check the main README.md and API_DOCUMENTATION.md
2. **Examples**: Review the examples in this directory
3. **Issues**: Create an issue in the repository
4. **Community**: Join the community forum

### Common Issues

1. **Model Loading**: Check available memory and dependencies
2. **Performance**: Use GPU acceleration and model quantization
3. **Memory**: Implement cleanup and monitoring
4. **Integration**: Check API endpoints and authentication

## 📄 License

All examples are licensed under the MIT License. See the LICENSE file for details.

---

**Remember**: These examples are for demonstration purposes. In production, ensure you have proper security, monitoring, and crisis response procedures in place.
