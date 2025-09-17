# GemmaSOS Integration Guide

This comprehensive guide shows you how to integrate the GemmaSOS crisis response system into your applications.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Integration Methods](#integration-methods)
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install torch transformers gradio pillow opencv-python numpy
```

### 2. Basic Integration

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

## 🔌 Integration Methods

### Method 1: Direct Integration (Recommended)

**Best for**: Custom applications, full control needed

**Pros**:
- Complete control over processing
- No external dependencies
- Full privacy protection
- Customizable responses

**Cons**:
- Requires more setup
- Need to handle model loading
- More complex implementation

**Example**: See `examples/web_app/` for a complete Flask application.

### Method 2: API Integration

**Best for**: Microservices, multiple client applications

**Pros**:
- Easy to integrate
- Language agnostic
- Centralized processing
- Easy to scale

**Cons**:
- Network dependency
- Requires API server
- Potential latency

**Example**: See `examples/api_server/` for a complete REST API.

### Method 3: SDK Integration

**Best for**: Mobile applications, third-party integrations

**Pros**:
- Easy to use
- Platform-specific optimizations
- Built-in UI components
- Documentation included

**Cons**:
- Platform-specific
- Less customization
- Additional dependencies

**Example**: See `examples/mobile_app/` for iOS SDK integration.

## 📱 Platform-Specific Guides

### Web Applications

#### React Integration

```javascript
import React, { useState } from 'react';

function CrisisAwareChat() {
    const [message, setMessage] = useState('');
    const [crisisResult, setCrisisResult] = useState(null);
    
    const analyzeMessage = async (text) => {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const result = await response.json();
        setCrisisResult(result);
        
        if (result.crisis_detected) {
            showCrisisModal(result.response, result.resources);
        }
    };
    
    return (
        <div>
            <input 
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && analyzeMessage(message)}
            />
            <button onClick={() => analyzeMessage(message)}>Send</button>
            
            {crisisResult?.crisis_detected && (
                <CrisisResponseModal 
                    response={crisisResult.response}
                    resources={crisisResult.resources}
                />
            )}
        </div>
    );
}
```

#### Vue.js Integration

```vue
<template>
  <div class="crisis-chat">
    <input 
      v-model="message" 
      @keyup.enter="analyzeMessage"
      placeholder="Type your message..."
    />
    <button @click="analyzeMessage">Analyze</button>
    
    <div v-if="crisisResult?.crisis_detected" class="crisis-alert">
      <h3>Crisis Support</h3>
      <p>{{ crisisResult.response }}</p>
      <div class="resources">
        <h4>Resources:</h4>
        <ul>
          <li v-for="resource in crisisResult.resources" :key="resource.name">
            {{ resource.name }}: {{ resource.number }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
      crisisResult: null
    }
  },
  methods: {
    async analyzeMessage() {
      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: this.message })
        });
        
        this.crisisResult = await response.json();
      } catch (error) {
        console.error('Analysis failed:', error);
      }
    }
  }
}
</script>
```

### Mobile Applications

#### React Native Integration

```javascript
import React, { useState } from 'react';
import { Alert, TextInput, Button, View, Text } from 'react-native';

const CrisisAwareApp = () => {
  const [message, setMessage] = useState('');
  const [crisisResult, setCrisisResult] = useState(null);
  
  const analyzeMessage = async (text) => {
    try {
      const response = await fetch('http://your-api-server.com/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      
      const result = await response.json();
      setCrisisResult(result);
      
      if (result.crisis_detected) {
        Alert.alert(
          'Crisis Detected',
          result.response,
          [
            { text: 'Get Help', onPress: () => openCrisisResources(result.resources) },
            { text: 'OK', style: 'default' }
          ]
        );
      }
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };
  
  return (
    <View>
      <TextInput
        value={message}
        onChangeText={setMessage}
        placeholder="Type your message..."
      />
      <Button title="Analyze" onPress={() => analyzeMessage(message)} />
      
      {crisisResult?.crisis_detected && (
        <View style={styles.crisisAlert}>
          <Text style={styles.crisisText}>{crisisResult.response}</Text>
        </View>
      )}
    </View>
  );
};
```

#### Flutter Integration

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CrisisAwareApp extends StatefulWidget {
  @override
  _CrisisAwareAppState createState() => _CrisisAwareAppState();
}

class _CrisisAwareAppState extends State<CrisisAwareApp> {
  final TextEditingController _messageController = TextEditingController();
  Map<String, dynamic>? _crisisResult;
  
  Future<void> _analyzeMessage(String text) async {
    try {
      final response = await http.post(
        Uri.parse('http://your-api-server.com/analyze'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'text': text}),
      );
      
      if (response.statusCode == 200) {
        setState(() {
          _crisisResult = json.decode(response.body);
        });
        
        if (_crisisResult!['crisis_detected']) {
          _showCrisisDialog();
        }
      }
    } catch (e) {
      print('Analysis failed: $e');
    }
  }
  
  void _showCrisisDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Crisis Support'),
          content: Text(_crisisResult!['response']),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: Text('OK'),
            ),
          ],
        );
      },
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Crisis Aware App')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _messageController,
              decoration: InputDecoration(
                hintText: 'Type your message...',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => _analyzeMessage(_messageController.text),
              child: Text('Analyze'),
            ),
            if (_crisisResult != null && _crisisResult!['crisis_detected'])
              Container(
                margin: EdgeInsets.only(top: 16),
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.shade100,
                  border: Border.all(color: Colors.red),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _crisisResult!['response'],
                  style: TextStyle(color: Colors.red.shade800),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
```

### Desktop Applications

#### Electron Integration

```javascript
const { ipcRenderer } = require('electron');
const { CrisisDetector } = require('./crisis-detector');

class CrisisAwareApp {
  constructor() {
    this.crisisDetector = new CrisisDetector();
    this.setupEventListeners();
  }
  
  setupEventListeners() {
    document.getElementById('sendButton').addEventListener('click', () => {
      this.analyzeMessage();
    });
    
    document.getElementById('messageInput').addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.analyzeMessage();
      }
    });
  }
  
  async analyzeMessage() {
    const message = document.getElementById('messageInput').value;
    
    if (!message.trim()) return;
    
    try {
      const result = await this.crisisDetector.analyzeText(message);
      
      if (result.crisis_detected) {
        this.showCrisisResponse(result);
      } else {
        this.showNormalResponse(result);
      }
    } catch (error) {
      console.error('Analysis failed:', error);
      this.showError('Analysis failed. Please try again.');
    }
  }
  
  showCrisisResponse(result) {
    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = `
      <div class="crisis-alert">
        <h3>Crisis Support</h3>
        <p>${result.response}</p>
        <div class="resources">
          <h4>Resources:</h4>
          <ul>
            ${result.resources.map(r => `<li>${r.name}: ${r.number || r.website}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
    responseDiv.className = 'crisis-response';
  }
  
  showNormalResponse(result) {
    const responseDiv = document.getElementById('response');
    responseDiv.innerHTML = `<p>${result.response}</p>`;
    responseDiv.className = 'normal-response';
  }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new CrisisAwareApp();
});
```

## ⚙️ Configuration

### Environment Variables

```bash
# Model configuration
export GEMMA_SOS_MODEL="google/gemma-2b-it"
export GEMMA_SOS_CACHE_DIR="/path/to/model/cache"
export GEMMA_SOS_DEVICE="cuda"  # or "cpu"

# Safety thresholds
export GEMMA_SOS_IMMEDIATE_RISK_THRESHOLD="0.8"
export GEMMA_SOS_HIGH_RISK_THRESHOLD="0.6"
export GEMMA_SOS_MEDIUM_RISK_THRESHOLD="0.4"
export GEMMA_SOS_LOW_RISK_THRESHOLD="0.2"

# Privacy settings
export GEMMA_SOS_DATA_RETENTION_HOURS="0"
export GEMMA_SOS_AUTO_CLEANUP_INTERVAL="3600"
export GEMMA_SOS_MAX_LOG_ENTRIES="100"
```

### Configuration File

```python
# config.py
class Config:
    # Model settings
    MODEL_NAME = "google/gemma-2b-it"
    MODEL_CACHE_DIR = "~/.cache/huggingface/transformers"
    MODEL_PRECISION = "float16"  # or "float32"
    
    # Safety thresholds
    SAFETY_THRESHOLDS = {
        "immediate_risk": 0.8,
        "high_risk": 0.6,
        "medium_risk": 0.4,
        "low_risk": 0.2
    }
    
    # Privacy settings
    PRIVACY_CONFIG = {
        "data_retention_hours": 0,
        "max_session_duration_hours": 8,
        "auto_cleanup_interval_hours": 1,
        "max_log_entries": 100
    }
    
    # Custom crisis keywords
    CUSTOM_CRISIS_KEYWORDS = {
        "your_app_specific": [
            "app_specific_keyword1",
            "app_specific_keyword2"
        ]
    }
    
    # Custom response templates
    CUSTOM_RESPONSES = {
        "your_app_specific": {
            "immediate": "Your app-specific crisis response...",
            "supportive": "Your app-specific supportive response..."
        }
    }
```

## 🧪 Testing

### Unit Tests

```python
import unittest
from crisis_detector import CrisisDetector

class TestCrisisIntegration(unittest.TestCase):
    def setUp(self):
        self.detector = CrisisDetector()
    
    def test_self_harm_detection(self):
        result = self.detector.detect_crisis_from_text("I want to hurt myself")
        self.assertTrue(result["crisis_detected"])
        self.assertEqual(result["categories"][0]["category"], "self_harm")
    
    def test_suicide_detection(self):
        result = self.detector.detect_crisis_from_text("I don't want to live anymore")
        self.assertTrue(result["crisis_detected"])
        self.assertEqual(result["categories"][0]["category"], "suicide")
    
    def test_no_crisis_detection(self):
        result = self.detector.detect_crisis_from_text("Hello, how are you?")
        self.assertFalse(result["crisis_detected"])
    
    def test_confidence_scores(self):
        result = self.detector.detect_crisis_from_text("I want to cut myself tonight")
        self.assertGreater(result["confidence"], 0.5)
        self.assertLessEqual(result["confidence"], 1.0)
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
    assert response["immediate_risk"] == False
```

### Performance Tests

```python
import time
import statistics

def test_performance():
    detector = CrisisDetector()
    test_messages = [
        "I want to hurt myself",
        "I don't want to live anymore",
        "Hello, how are you?",
        "I'm feeling really sad today"
    ]
    
    response_times = []
    
    for message in test_messages:
        start_time = time.time()
        result = detector.detect_crisis_from_text(message)
        end_time = time.time()
        
        response_times.append(end_time - start_time)
    
    avg_response_time = statistics.mean(response_times)
    max_response_time = max(response_times)
    
    print(f"Average response time: {avg_response_time:.3f}s")
    print(f"Maximum response time: {max_response_time:.3f}s")
    
    # Assert performance requirements
    assert avg_response_time < 3.0, "Average response time too slow"
    assert max_response_time < 5.0, "Maximum response time too slow"
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV GEMMA_SOS_MODEL="google/gemma-2b-it"
ENV GEMMA_SOS_DEVICE="cpu"

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  crisis-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GEMMA_SOS_MODEL=google/gemma-2b-it
      - GEMMA_SOS_DEVICE=cpu
    volumes:
      - ./models:/app/models
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - crisis-api
    restart: unless-stopped
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crisis-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crisis-api
  template:
    metadata:
      labels:
        app: crisis-api
    spec:
      containers:
      - name: crisis-api
        image: your-registry/crisis-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: GEMMA_SOS_MODEL
          value: "google/gemma-2b-it"
        - name: GEMMA_SOS_DEVICE
          value: "cpu"
        resources:
          requests:
            memory: "4Gi"
            cpu: "1000m"
          limits:
            memory: "8Gi"
            cpu: "2000m"
---
apiVersion: v1
kind: Service
metadata:
  name: crisis-api-service
spec:
  selector:
    app: crisis-api
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Model Loading Fails

**Problem**: Model fails to load or takes too long

**Solutions**:
```python
# Check available memory
import psutil
print(f"Available memory: {psutil.virtual_memory().available / (1024**3):.1f} GB")

# Try loading with CPU only
detector = CrisisDetector(device="cpu")

# Use model quantization
detector = CrisisDetector(quantized=True)
```

#### 2. Low Detection Accuracy

**Problem**: Crisis detection is not accurate enough

**Solutions**:
```python
# Adjust sensitivity thresholds
from config import Config
Config.SAFETY_THRESHOLDS["low_risk"] = 0.1  # More sensitive

# Add custom keywords
Config.CUSTOM_CRISIS_KEYWORDS["your_app"] = ["custom_keyword1", "custom_keyword2"]

# Retrain with your data
detector.retrain_with_custom_data(your_training_data)
```

#### 3. Memory Issues

**Problem**: Application runs out of memory

**Solutions**:
```python
# Enable model cleanup
safety_system.cleanup_session_data()
safety_system.cleanup()

# Use model quantization
detector = CrisisDetector(quantized=True)

# Implement memory monitoring
import psutil
if psutil.virtual_memory().percent > 80:
    safety_system.cleanup()
```

#### 4. Slow Response Times

**Problem**: Analysis takes too long

**Solutions**:
```python
# Use GPU acceleration
detector = CrisisDetector(device="cuda")

# Enable model caching
detector.enable_caching()

# Use batch processing
results = detector.batch_analyze(messages)
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging
detector = CrisisDetector()
detector.debug_mode = True

# Enable detailed logging
detector.enable_detailed_logging()
```

### Performance Monitoring

```python
import time
import psutil

class PerformanceMonitor:
    def __init__(self):
        self.start_time = None
        self.memory_usage = []
    
    def start_monitoring(self):
        self.start_time = time.time()
    
    def end_monitoring(self):
        if self.start_time:
            duration = time.time() - self.start_time
            memory = psutil.virtual_memory().percent
            self.memory_usage.append(memory)
            
            print(f"Processing time: {duration:.3f}s")
            print(f"Memory usage: {memory:.1f}%")
            
            if memory > 90:
                print("WARNING: High memory usage detected")
```

## 📞 Support

### Getting Help

1. **Documentation**: Check the main README.md and API_DOCUMENTATION.md
2. **Examples**: Review the examples in the `examples/` directory
3. **Issues**: Create an issue in the repository
4. **Community**: Join the community forum

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Remember**: This system is designed to provide support and resources, but it is not a replacement for professional mental health care or emergency services. If you or someone you know is in immediate danger, please call 911 or your local emergency services immediately.
