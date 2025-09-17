"""
API Client Example
Demonstrates how to use the Crisis API Server
"""

import requests
import json
import time
import uuid

class CrisisAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        """Initialize the API client"""
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
    
    def health_check(self):
        """Check if the API server is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_text(self, text):
        """Analyze text for crisis indicators"""
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze/text",
                json={
                    "text": text,
                    "session_id": self.session_id
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_image(self, image_path):
        """Analyze image for crisis indicators"""
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze/image",
                json={
                    "image_path": image_path,
                    "session_id": self.session_id
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_multimodal(self, text=None, image_path=None):
        """Analyze multimodal input for crisis indicators"""
        try:
            response = requests.post(
                f"{self.base_url}/api/analyze/multimodal",
                json={
                    "text": text,
                    "image_path": image_path,
                    "session_id": self.session_id
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_session_data(self):
        """Get session data"""
        try:
            response = requests.get(f"{self.base_url}/api/session/{self.session_id}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_analytics(self):
        """Get analytics data"""
        try:
            response = requests.get(f"{self.base_url}/api/analytics")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_resources(self, crisis_type="general"):
        """Get crisis resources"""
        try:
            response = requests.get(f"{self.base_url}/api/resources?type={crisis_type}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def main():
    """Main function to demonstrate API usage"""
    print("🔒 Crisis API Client Example")
    print("=" * 40)
    
    # Initialize client
    client = CrisisAPIClient()
    
    # Check server health
    print("\n1. Checking server health...")
    health = client.health_check()
    if "error" in health:
        print(f"❌ Server not available: {health['error']}")
        print("Make sure to start the server with: python server.py")
        return
    else:
        print(f"✅ Server is healthy: {health['status']}")
    
    # Test text analysis
    print("\n2. Testing text analysis...")
    test_messages = [
        "Hello, how are you?",
        "I want to hurt myself tonight",
        "I'm feeling really sad today",
        "I don't want to live anymore"
    ]
    
    for message in test_messages:
        print(f"\nMessage: '{message}'")
        result = client.analyze_text(message)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            if result["success"]:
                if result["crisis_detected"]:
                    print(f"🚨 Crisis detected: {result['crisis_type']}")
                    print(f"   Confidence: {result['confidence']:.2f}")
                    print(f"   Risk level: {result['risk_level']}")
                    print(f"   Response: {result['response'][:100]}...")
                    if result.get("resources"):
                        print(f"   Resources: {len(result['resources'])} available")
                else:
                    print(f"✅ No crisis detected (confidence: {result['confidence']:.2f})")
                print(f"   Response time: {result.get('response_time', 0):.3f}s")
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    # Test multimodal analysis
    print("\n3. Testing multimodal analysis...")
    multimodal_result = client.analyze_multimodal(
        text="I'm thinking about hurting myself",
        image_path=None  # No image for this example
    )
    
    if "error" in multimodal_result:
        print(f"❌ Multimodal analysis error: {multimodal_result['error']}")
    else:
        print(f"✅ Multimodal analysis completed")
        if multimodal_result["crisis_detected"]:
            print(f"   Crisis type: {multimodal_result['crisis_type']}")
            print(f"   Confidence: {multimodal_result['confidence']:.2f}")
    
    # Get session data
    print("\n4. Getting session data...")
    session_data = client.get_session_data()
    if "error" in session_data:
        print(f"❌ Error getting session data: {session_data['error']}")
    else:
        print(f"✅ Session data retrieved")
        print(f"   Interactions: {len(session_data.get('interactions', []))}")
        print(f"   Created at: {session_data.get('created_at', 'Unknown')}")
    
    # Get analytics
    print("\n5. Getting analytics...")
    analytics = client.get_analytics()
    if "error" in analytics:
        print(f"❌ Error getting analytics: {analytics['error']}")
    else:
        print(f"✅ Analytics retrieved")
        print(f"   Total requests: {analytics['total_requests']}")
        print(f"   Crisis detections: {analytics['crisis_detections']}")
        print(f"   Average response time: {analytics['average_response_time']:.3f}s")
        print(f"   Active sessions: {analytics['active_sessions']}")
    
    # Get resources
    print("\n6. Getting crisis resources...")
    resources = client.get_resources("self_harm")
    if "error" in resources:
        print(f"❌ Error getting resources: {resources['error']}")
    else:
        print(f"✅ Resources retrieved for {resources['crisis_type']}")
        for resource in resources['resources']:
            print(f"   - {resource['name']}")
            if resource.get('number'):
                print(f"     Phone: {resource['number']}")
            if resource.get('website'):
                print(f"     Website: {resource['website']}")
    
    print("\n" + "=" * 40)
    print("✅ API client example completed!")

if __name__ == "__main__":
    main()
