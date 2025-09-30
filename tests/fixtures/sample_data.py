"""
Sample data for testing various components.

This module provides mock data for testing different data sources,
API responses, and content processing scenarios.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any

# Sample Reddit data
SAMPLE_REDDIT_POSTS = [
    {
        "id": "abc123",
        "title": "Breakthrough in Quantum Computing: New Algorithm Achieves Quantum Advantage",
        "selftext": "Researchers at MIT have developed a new quantum algorithm that demonstrates clear quantum advantage over classical computers for optimization problems...",
        "url": "https://reddit.com/r/technology/comments/abc123",
        "score": 1250,
        "num_comments": 89,
        "created_utc": (datetime.now() - timedelta(hours=2)).timestamp(),
        "subreddit": "technology",
        "author": "quantum_researcher",
    },
    {
        "id": "def456",
        "title": "SpaceX Successfully Launches Mars Mission with New Raptor Engines",
        "selftext": "SpaceX has successfully launched their latest Mars mission using the new Raptor 3.0 engines, marking a significant milestone...",
        "url": "https://reddit.com/r/SpaceX/comments/def456",
        "score": 2100,
        "num_comments": 156,
        "created_utc": (datetime.now() - timedelta(hours=5)).timestamp(),
        "subreddit": "SpaceX",
        "author": "space_enthusiast",
    },
    {
        "id": "ghi789",
        "title": "Climate Change: New Carbon Capture Technology Shows Promise",
        "selftext": "A new direct air capture technology developed by Climeworks has achieved record efficiency rates...",
        "url": "https://reddit.com/r/climate/comments/ghi789",
        "score": 850,
        "num_comments": 67,
        "created_utc": (datetime.now() - timedelta(hours=8)).timestamp(),
        "subreddit": "climate",
        "author": "climate_scientist",
    },
]

# Sample YouTube data
SAMPLE_YOUTUBE_VIDEOS = [
    {
        "video_id": "dQw4w9WgXcQ",
        "title": "The Future of AI: GPT-5 and Beyond",
        "description": "In this video, we explore the latest developments in AI and what GPT-5 might bring...",
        "channel_title": "AI Explained",
        "duration": "PT15M30S",  # ISO 8601 duration format
        "view_count": 125000,
        "published_at": (datetime.now() - timedelta(days=2)).isoformat(),
        "transcript": [
            {
                "text": "Welcome to AI Explained. Today we're discussing the future of AI...",
                "start": 0.0,
            },
            {
                "text": "GPT-5 is expected to bring revolutionary changes...",
                "start": 15.5,
            },
            {"text": "The implications for society are profound...", "start": 45.2},
        ],
    },
    {
        "video_id": "abc123def",
        "title": "Mars Colonization: Engineering Challenges",
        "description": "Exploring the technical challenges of establishing a permanent human presence on Mars...",
        "channel_title": "Space Engineering",
        "duration": "PT28M45S",
        "view_count": 89000,
        "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
        "transcript": [
            {
                "text": "Mars colonization presents unique engineering challenges...",
                "start": 0.0,
            },
            {"text": "The atmosphere is less than 1% of Earth's...", "start": 30.0},
            {"text": "Radiation shielding is a critical concern...", "start": 120.5},
        ],
    },
]

# Sample ArXiv papers
SAMPLE_ARXIV_PAPERS = [
    {
        "id": "2024.01234",
        "title": "Attention Is All You Need: A Comprehensive Review of Transformer Architectures",
        "authors": ["John Smith", "Jane Doe", "Bob Wilson"],
        "abstract": "This paper provides a comprehensive review of transformer architectures and their applications in natural language processing...",
        "published": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "updated": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "categories": ["cs.AI", "cs.LG"],
        "pdf_url": "https://arxiv.org/pdf/2024.01234.pdf",
        "entry_id": "http://arxiv.org/abs/2024.01234v1",
    },
    {
        "id": "2024.05678",
        "title": "Quantum Machine Learning: Bridging Quantum Computing and AI",
        "authors": ["Alice Johnson", "Charlie Brown"],
        "abstract": "We present a novel approach to quantum machine learning that leverages quantum superposition...",
        "published": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "updated": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "categories": ["quant-ph", "cs.LG"],
        "pdf_url": "https://arxiv.org/pdf/2024.05678.pdf",
        "entry_id": "http://arxiv.org/abs/2024.05678v1",
    },
]

# Sample news articles
SAMPLE_NEWS_ARTICLES = [
    {
        "title": "Tech Giants Announce Joint AI Safety Initiative",
        "url": "https://example.com/news/ai-safety-initiative",
        "source": "Tech News Daily",
        "published_at": (datetime.now() - timedelta(hours=6)).isoformat(),
        "content": "Major technology companies including Google, Microsoft, and OpenAI have announced a joint initiative to develop AI safety standards...",
        "summary": "Tech companies collaborate on AI safety standards to ensure responsible development.",
        "author": "Sarah Tech Reporter",
    },
    {
        "title": "Breakthrough in Fusion Energy: ITER Achieves Record Temperature",
        "url": "https://example.com/news/fusion-breakthrough",
        "source": "Science Today",
        "published_at": (datetime.now() - timedelta(hours=12)).isoformat(),
        "content": "The International Thermonuclear Experimental Reactor (ITER) has achieved a record-breaking plasma temperature of 100 million degrees Celsius...",
        "summary": "ITER fusion reactor reaches milestone temperature, bringing clean energy closer to reality.",
        "author": "Dr. Energy Physicist",
    },
]

# Sample API responses for mocking
MOCK_OPENAI_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": "This is a mock response from OpenAI's API for testing purposes. The content would normally contain AI-generated text based on the input prompt."
            }
        }
    ],
    "usage": {"prompt_tokens": 50, "completion_tokens": 100, "total_tokens": 150},
}

MOCK_REDDIT_API_RESPONSE = {
    "data": {"children": [{"data": post} for post in SAMPLE_REDDIT_POSTS]}
}

MOCK_YOUTUBE_API_RESPONSE = {
    "items": [
        {
            "id": {"videoId": video["video_id"]},
            "snippet": {
                "title": video["title"],
                "description": video["description"],
                "channelTitle": video["channel_title"],
                "publishedAt": video["published_at"],
            },
            "statistics": {"viewCount": str(video["view_count"])},
            "contentDetails": {"duration": video["duration"]},
        }
        for video in SAMPLE_YOUTUBE_VIDEOS
    ]
}

MOCK_ARXIV_RESPONSE = {"entries": SAMPLE_ARXIV_PAPERS}

# Error scenarios for testing
ERROR_SCENARIOS = {
    "network_error": {"status_code": 500, "error": "Internal Server Error"},
    "rate_limit_error": {"status_code": 429, "error": "Rate limit exceeded"},
    "authentication_error": {"status_code": 401, "error": "Unauthorized"},
    "not_found_error": {"status_code": 404, "error": "Not Found"},
}

# Test content for processing
SAMPLE_PROCESSED_CONTENT = {
    "stories": [
        {
            "title": "AI Breakthrough in Quantum Computing",
            "summary": "Researchers achieve quantum advantage with new algorithm",
            "source": "reddit",
            "url": "https://reddit.com/r/technology/comments/abc123",
            "score": 1250,
            "timestamp": datetime.now().isoformat(),
            "topics": ["artificial intelligence", "quantum computing"],
        },
        {
            "title": "SpaceX Mars Mission Success",
            "summary": "New Raptor engines power successful Mars launch",
            "source": "reddit",
            "url": "https://reddit.com/r/SpaceX/comments/def456",
            "score": 2100,
            "timestamp": datetime.now().isoformat(),
            "topics": ["space exploration", "technology"],
        },
    ],
    "metadata": {
        "total_stories": 2,
        "sources": ["reddit"],
        "generation_time": datetime.now().isoformat(),
        "topics_covered": [
            "artificial intelligence",
            "quantum computing",
            "space exploration",
            "technology",
        ],
    },
}
