"""
Sample configuration data for testing.

This module provides various configuration scenarios for testing
different aspects of the configuration parser and validation.
"""

from typing import Dict, Any

# Valid configuration samples
VALID_MINIMAL_CONFIG = {
    "interests": ["artificial intelligence"]
}

VALID_FULL_CONFIG = {
    "interests": [
        "artificial intelligence",
        "machine learning",
        "geopolitics",
        "biotechnology",
        "climate change",
        "space exploration",
        "cybersecurity"
    ],
    "newsletter": {
        "tone": "witty",
        "include_opinions": True,
        "frequency": "weekly",
        "max_stories": 10
    },
    "content": {
        "include_academic": True,
        "include_reddit": True,
        "include_youtube": True,
        "include_news": True,
        "reddit": {
            "min_upvotes": 100,
            "max_age_hours": 48
        },
        "youtube": {
            "min_views": 10000,
            "max_duration_minutes": 60
        }
    },
    "output": {
        "format": "markdown",
        "include_sources": True,
        "include_summary_stats": True
    }
}

VALID_ALTERNATIVE_CONFIG = {
    "interests": [
        "quantum computing",
        "renewable energy",
        "space technology"
    ],
    "newsletter": {
        "tone": "professional",
        "include_opinions": False,
        "frequency": "daily",
        "max_stories": 5
    },
    "content": {
        "include_academic": False,
        "include_reddit": False,
        "include_youtube": True,
        "include_news": True,
        "reddit": {
            "min_upvotes": 50,
            "max_age_hours": 24
        },
        "youtube": {
            "min_views": 5000,
            "max_duration_minutes": 30
        }
    },
    "output": {
        "format": "html",
        "include_sources": False,
        "include_summary_stats": False
    }
}

# Invalid configuration samples for testing validation
INVALID_EMPTY_INTERESTS = {
    "interests": []
}

INVALID_MISSING_INTERESTS = {
    "newsletter": {
        "tone": "witty"
    }
}

INVALID_TONE = {
    "interests": ["ai"],
    "newsletter": {
        "tone": "invalid_tone"
    }
}

INVALID_FREQUENCY = {
    "interests": ["ai"],
    "newsletter": {
        "frequency": "monthly"
    }
}

INVALID_FORMAT = {
    "interests": ["ai"],
    "output": {
        "format": "docx"
    }
}

INVALID_NEGATIVE_VALUES = {
    "interests": ["ai"],
    "newsletter": {
        "max_stories": -5
    },
    "content": {
        "reddit": {
            "min_upvotes": -10,
            "max_age_hours": -24
        },
        "youtube": {
            "min_views": -1000,
            "max_duration_minutes": -30
        }
    }
}

INVALID_ZERO_VALUES = {
    "interests": ["ai"],
    "newsletter": {
        "max_stories": 0
    },
    "content": {
        "reddit": {
            "max_age_hours": 0
        },
        "youtube": {
            "max_duration_minutes": 0
        }
    }
}

INVALID_ALL_SOURCES_DISABLED = {
    "interests": ["ai"],
    "content": {
        "include_academic": False,
        "include_reddit": False,
        "include_youtube": False,
        "include_news": False
    }
}

INVALID_EXTRA_FIELDS = {
    "interests": ["ai"],
    "newsletter": {
        "tone": "witty",
        "extra_field": "not_allowed"
    },
    "unknown_section": {
        "some_field": "value"
    }
}

# Edge cases
DUPLICATE_INTERESTS = {
    "interests": [
        "AI",
        "ai",
        "Artificial Intelligence",
        "artificial intelligence",
        "Machine Learning",
        "machine learning",
        "ML"
    ]
}

WHITESPACE_INTERESTS = {
    "interests": [
        "  artificial intelligence  ",
        "\tmachine learning\t",
        "\ndeep learning\n",
        "  robotics"
    ]
}

BOUNDARY_VALUES = {
    "interests": ["ai"],
    "newsletter": {
        "max_stories": 50  # Maximum allowed
    },
    "content": {
        "reddit": {
            "min_upvotes": 0,  # Minimum allowed
            "max_age_hours": 1  # Minimum allowed
        },
        "youtube": {
            "min_views": 0,  # Minimum allowed  
            "max_duration_minutes": 1  # Minimum allowed
        }
    }
}

# Configuration variants for different use cases
ACADEMIC_FOCUSED_CONFIG = {
    "interests": [
        "machine learning research",
        "computer science",
        "academic publications"
    ],
    "newsletter": {
        "tone": "academic",
        "include_opinions": False,
        "frequency": "weekly",
        "max_stories": 15
    },
    "content": {
        "include_academic": True,
        "include_reddit": False,
        "include_youtube": False,
        "include_news": False
    }
}

SOCIAL_FOCUSED_CONFIG = {
    "interests": [
        "tech trends",
        "startup news",
        "social media"
    ],
    "newsletter": {
        "tone": "casual",
        "include_opinions": True,
        "frequency": "daily",
        "max_stories": 20
    },
    "content": {
        "include_academic": False,
        "include_reddit": True,
        "include_youtube": True,
        "include_news": True,
        "reddit": {
            "min_upvotes": 500,
            "max_age_hours": 12
        },
        "youtube": {
            "min_views": 50000,
            "max_duration_minutes": 15
        }
    }
}
