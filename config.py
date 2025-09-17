"""
Configuration file for GemmaSOS Crisis Intervention System
"""

import os
from typing import Dict, List, Any

class Config:
    """Configuration settings for the crisis intervention system"""
    
    # Model Configuration
    MODEL_NAME = "google/gemma-2b-it"
    MODEL_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "transformers")
    
    # Safety Thresholds
    SAFETY_THRESHOLDS = {
        "immediate_risk": 0.8,
        "high_risk": 0.6,
        "medium_risk": 0.4,
        "low_risk": 0.2
    }
    
    # Crisis Detection Keywords
    CRISIS_KEYWORDS = {
        "self_harm": [
            "cut", "cutting", "self harm", "self-harm", "hurt myself", 
            "bleeding", "wound", "scar", "razor", "knife", "sharp",
            "burn", "burning", "hit myself", "punch myself"
        ],
        "suicide": [
            "kill myself", "end it all", "not worth living", "better off dead",
            "suicide", "take my life", "end my life", "jump", "overdose",
            "hang myself", "shoot myself", "no point", "hopeless"
        ],
        "violence": [
            "hurt someone", "kill someone", "attack", "fight", "violence",
            "beat up", "punch", "hit", "stab", "shoot", "threaten",
            "revenge", "payback", "destroy", "harm"
        ],
        "abuse": [
            "abuse", "abused", "hit me", "hurt me", "beat me", "violence",
            "threaten", "scared", "afraid", "unsafe", "hurt", "pain",
            "control", "manipulate", "force", "coerce"
        ],
        "overdose": [
            "overdose", "too much", "pills", "drugs", "medication",
            "poison", "sick", "nausea", "dizzy", "unconscious",
            "emergency", "hospital", "ambulance"
        ]
    }
    
    # Severity Keywords
    SEVERITY_KEYWORDS = {
        "self_harm": ["bleeding", "hospital", "emergency", "serious"],
        "suicide": ["plan", "method", "tonight", "today", "now"],
        "violence": ["gun", "weapon", "tonight", "today", "plan"],
        "abuse": ["emergency", "police", "help", "danger", "now"],
        "overdose": ["unconscious", "emergency", "hospital", "ambulance", "now"]
    }
    
    # Content Filtering Rules
    CONTENT_FILTERS = {
        "harmful_content": [
            "detailed methods", "step by step", "how to", "instructions",
            "tutorial", "guide", "detailed", "specific", "exact"
        ],
        "triggering_content": [
            "graphic", "explicit", "detailed description", "gory",
            "disturbing", "traumatic", "triggering"
        ],
        "dangerous_advice": [
            "ignore professional help", "don't tell anyone", "keep it secret",
            "you're alone", "no one cares", "give up"
        ]
    }
    
    # Crisis Resources
    CRISIS_RESOURCES = {
        "general": [
            {
                "name": "National Suicide Prevention Lifeline",
                "number": "988",
                "text": "Text HOME to 741741",
                "description": "24/7 crisis support for suicide prevention",
                "available": "24/7"
            },
            {
                "name": "Crisis Text Line",
                "number": "Text HOME to 741741",
                "description": "Free, 24/7 crisis support via text",
                "available": "24/7"
            }
        ],
        "self_harm": [
            {
                "name": "Self-Injury Outreach & Support",
                "website": "sioutreach.org",
                "description": "Resources and support for self-injury recovery"
            },
            {
                "name": "To Write Love on Her Arms",
                "website": "twloha.com",
                "description": "Hope and help for people struggling with depression, addiction, self-injury, and suicide"
            }
        ],
        "suicide": [
            {
                "name": "National Suicide Prevention Lifeline",
                "number": "988",
                "text": "Text HOME to 741741",
                "description": "24/7 crisis support for suicide prevention",
                "available": "24/7"
            },
            {
                "name": "American Foundation for Suicide Prevention",
                "website": "afsp.org",
                "description": "Resources, support groups, and prevention programs"
            }
        ],
        "violence": [
            {
                "name": "National Domestic Violence Hotline",
                "number": "1-800-799-7233",
                "text": "Text START to 88788",
                "description": "24/7 support for domestic violence",
                "available": "24/7"
            },
            {
                "name": "National Sexual Assault Hotline",
                "number": "1-800-656-4673",
                "description": "24/7 support for sexual assault survivors",
                "available": "24/7"
            }
        ],
        "abuse": [
            {
                "name": "National Domestic Violence Hotline",
                "number": "1-800-799-7233",
                "text": "Text START to 88788",
                "description": "24/7 support for domestic violence",
                "available": "24/7"
            },
            {
                "name": "Childhelp National Child Abuse Hotline",
                "number": "1-800-4-A-CHILD (1-800-422-4453)",
                "description": "24/7 support for child abuse",
                "available": "24/7"
            }
        ],
        "overdose": [
            {
                "name": "SAMHSA National Helpline",
                "number": "1-800-662-4357",
                "description": "24/7 treatment referral and information service",
                "available": "24/7"
            },
            {
                "name": "National Poison Control Center",
                "number": "1-800-222-1222",
                "description": "24/7 poison emergency support",
                "available": "24/7"
            }
        ]
    }
    
    # Response Templates
    RESPONSE_TEMPLATES = {
        "self_harm": {
            "immediate": [
                "I can hear that you're in a lot of pain right now. You don't have to go through this alone.",
                "I'm really concerned about you. Your life has value, even when it doesn't feel that way.",
                "I want you to know that what you're feeling right now is valid, and there are people who care about you."
            ],
            "supportive": [
                "It takes courage to reach out when you're struggling. I'm glad you did.",
                "You're not alone in this. Many people have felt this way and found ways to cope.",
                "Your feelings are important, and so are you."
            ]
        },
        "suicide": {
            "immediate": [
                "I'm very concerned about you right now. Your life matters, and I want to help you stay safe.",
                "I can hear how much pain you're in. Please know that you don't have to face this alone.",
                "I care about you, and I want to make sure you're safe. Can we talk about what's happening?"
            ],
            "supportive": [
                "Thank you for sharing this with me. It takes incredible strength to be so honest.",
                "I'm here with you. You don't have to carry this burden alone.",
                "Your life has meaning, even when it's hard to see right now."
            ]
        },
        "violence": {
            "immediate": [
                "I'm concerned about your safety. Violence is never the answer, and there are better ways to handle this.",
                "I can hear that you're very angry right now. Let's talk about what's really bothering you.",
                "I want to help you find a safer way to express these feelings."
            ],
            "supportive": [
                "It's okay to feel angry, but we need to find safe ways to express it.",
                "I'm here to listen and help you work through these feelings.",
                "There are people who can help you resolve this situation safely."
            ]
        },
        "abuse": {
            "immediate": [
                "I'm so sorry this is happening to you. You don't deserve to be treated this way.",
                "Your safety is the most important thing right now. You're not alone.",
                "I believe you, and I want to help you get to safety."
            ],
            "supportive": [
                "It took courage to share this with me. You're not to blame for what happened.",
                "You deserve to be treated with respect and kindness.",
                "I'm here to support you in whatever way you need."
            ]
        },
        "overdose": {
            "immediate": [
                "I'm very concerned about your safety right now. Please don't take any more.",
                "Your life is valuable, and I want to help you stay safe.",
                "If you've already taken something, please call emergency services immediately."
            ],
            "supportive": [
                "I'm glad you're reaching out. You don't have to face this alone.",
                "There are people who care about you and want to help you through this.",
                "Recovery is possible, and you deserve support."
            ]
        }
    }
    
    # UI Configuration
    UI_CONFIG = {
        "title": "GemmaSOS - Crisis Support",
        "description": "Your privacy is protected - Everything processes on your device. Nothing is sent to external servers.",
        "server_name": "0.0.0.0",
        "server_port": 7860,
        "share": False,
        "show_error": True
    }
    
    # Logging Configuration
    LOGGING_CONFIG = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/gemma_sos.log"
    }
    
    # Privacy Configuration
    PRIVACY_CONFIG = {
        "data_retention_hours": 24,
        "max_session_duration_hours": 8,
        "auto_cleanup_interval_hours": 1,
        "max_log_entries": 100
    }
    
    # Image Processing Configuration
    IMAGE_CONFIG = {
        "max_file_size_mb": 10,
        "allowed_formats": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        "max_dimensions": (2048, 2048)
    }
    
    # Model Processing Configuration
    MODEL_CONFIG = {
        "max_tokens": 512,
        "temperature": 0.7,
        "max_new_tokens": 200,
        "do_sample": True
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary"""
        return {
            "model_name": cls.MODEL_NAME,
            "safety_thresholds": cls.SAFETY_THRESHOLDS,
            "crisis_keywords": cls.CRISIS_KEYWORDS,
            "severity_keywords": cls.SEVERITY_KEYWORDS,
            "content_filters": cls.CONTENT_FILTERS,
            "crisis_resources": cls.CRISIS_RESOURCES,
            "response_templates": cls.RESPONSE_TEMPLATES,
            "ui_config": cls.UI_CONFIG,
            "logging_config": cls.LOGGING_CONFIG,
            "privacy_config": cls.PRIVACY_CONFIG,
            "image_config": cls.IMAGE_CONFIG,
            "model_config": cls.MODEL_CONFIG
        }
    
    @classmethod
    def update_config(cls, **kwargs):
        """Update configuration values"""
        for key, value in kwargs.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

# Environment-specific overrides
if os.getenv("GEMMA_SOS_DEBUG"):
    Config.LOGGING_CONFIG["level"] = "DEBUG"

if os.getenv("GEMMA_SOS_PORT"):
    Config.UI_CONFIG["server_port"] = int(os.getenv("GEMMA_SOS_PORT"))

if os.getenv("GEMMA_SOS_MODEL"):
    Config.MODEL_NAME = os.getenv("GEMMA_SOS_MODEL")
