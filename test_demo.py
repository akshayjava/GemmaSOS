#!/usr/bin/env python3
"""
Test script for GemmaSOS Demo
Tests the demo application functionality
"""

import sys
import os
import json
import logging

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from demo_app import GemmaSOSDemo

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_demo_functionality():
    """Test the demo application functionality"""
    logger.info("Testing GemmaSOS Demo functionality...")
    
    # Initialize demo
    demo = GemmaSOSDemo()
    
    # Test scenarios
    test_scenarios = [
        {
            "text": "I'm feeling really sad today",
            "expected_crisis": False,
            "description": "General sadness - no crisis"
        },
        {
            "text": "I want to hurt myself tonight",
            "expected_crisis": True,
            "description": "Self-harm crisis"
        },
        {
            "text": "I don't want to live anymore",
            "expected_crisis": True,
            "description": "Suicidal ideation"
        },
        {
            "text": "I'm going to hurt someone",
            "expected_crisis": True,
            "description": "Violence threat"
        },
        {
            "text": "He hits me every day",
            "expected_crisis": True,
            "description": "Abuse situation"
        },
        {
            "text": "I took too many pills",
            "expected_crisis": True,
            "description": "Overdose situation"
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(test_scenarios):
        logger.info(f"Testing scenario {i+1}: {scenario['description']}")
        
        try:
            # Test crisis detection
            crisis_result = demo.detect_crisis_simple(scenario["text"])
            
            # Test response generation
            response = demo.generate_response(crisis_result, scenario["text"])
            
            # Check if crisis detection matches expectation
            crisis_detected = crisis_result["crisis_detected"]
            expected_crisis = scenario["expected_crisis"]
            
            test_result = {
                "scenario": i + 1,
                "description": scenario["description"],
                "text": scenario["text"],
                "crisis_detected": crisis_detected,
                "expected_crisis": expected_crisis,
                "passed": crisis_detected == expected_crisis,
                "confidence": crisis_result["confidence"],
                "response_length": len(response),
                "has_resources": "Resources" in response
            }
            
            results.append(test_result)
            
            status = "PASS" if test_result["passed"] else "FAIL"
            logger.info(f"  Result: {status} - Crisis detected: {crisis_detected}, Expected: {expected_crisis}")
            
        except Exception as e:
            logger.error(f"  Error in scenario {i+1}: {e}")
            results.append({
                "scenario": i + 1,
                "description": scenario["description"],
                "error": str(e),
                "passed": False
            })
    
    # Test demo scenarios loading
    logger.info("Testing demo scenarios loading...")
    try:
        scenarios = demo.get_demo_scenarios()
        logger.info(f"  Loaded {len(scenarios)} demo scenarios")
        
        # Test loading a specific scenario
        if scenarios:
            first_scenario = scenarios[0]
            scenario_text = demo.load_demo_scenario(first_scenario["id"])
            logger.info(f"  Loaded scenario text: {scenario_text[:50]}...")
        
    except Exception as e:
        logger.error(f"  Error loading demo scenarios: {e}")
    
    # Test model loading simulation
    logger.info("Testing model loading simulation...")
    try:
        model_status = demo.load_gemma_model()
        logger.info(f"  Model loading result: {model_status[:100]}...")
    except Exception as e:
        logger.error(f"  Error in model loading: {e}")
    
    # Calculate results
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result.get("passed", False))
    
    logger.info("\n" + "="*50)
    logger.info("DEMO TEST RESULTS")
    logger.info("="*50)
    logger.info(f"Total tests: {total_tests}")
    logger.info(f"Passed tests: {passed_tests}")
    logger.info(f"Failed tests: {total_tests - passed_tests}")
    
    if passed_tests == total_tests:
        logger.info("🎉 ALL DEMO TESTS PASSED!")
        return True
    else:
        logger.warning(f"⚠️ {total_tests - passed_tests} tests failed.")
        return False

def main():
    """Main test function"""
    logger.info("Starting GemmaSOS Demo tests...")
    
    success = test_demo_functionality()
    
    if success:
        print("\n✅ Demo tests passed! The demo is ready to use.")
        print("\nTo run the demo:")
        print("  python run_demo.py")
        print("\nThen open your browser to: http://localhost:7861")
        sys.exit(0)
    else:
        print("\n❌ Some demo tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
