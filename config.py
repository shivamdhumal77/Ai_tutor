# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Load Gemini API key from environment
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Agent-specific configurations
    AGENT_CONFIG = {
        "multi_grade": {
            "model": "gemini-2.5-flash",
            "temperature": 0.3,
            "max_tokens": 2048,
            "system_prompt": (
                "You are an expert educational content creator specializing in multi-grade teaching. "
                "Create comprehensive lesson plans that adapt core concepts for different grade levels. "
                "Ensure content is engaging, age-appropriate, and aligned with educational standards."
            )
        },
        "voice_assistant": {
            "model": "gemini-2.5-flash",
            "temperature": 0.7,
            "max_tokens": 500,
            "system_prompt": (
                "You are a helpful classroom voice assistant. Respond to teacher commands conversationally "
                "and professionally. Provide concise, actionable responses. Use simple language appropriate "
                "for voice interaction."
            )
        },
        "adaptive_content": {
            "model": "gemini-2.5-flash",
            "temperature": 0.4,
            "max_tokens": 1024,
            "system_prompt": (
                "You are an adaptive learning specialist. Analyze student performance data and recommend "
                "personalized content difficulty adjustments. Provide specific suggestions for resources "
                "and activities tailored to the student's level."
            )
        },
        "cultural_context": {
            "model": "gemini-2.5-flash",
            "temperature": 0.5,
            "max_tokens": 2048,
            "system_prompt": (
                "You are a cultural adaptation expert. Modify educational content to make it culturally "
                "relevant and appropriate for specific target audiences. Maintain learning objectives while "
                "ensuring cultural sensitivity and relevance."
            )
        },
        "doubt_resolution": {
            "model": "gemini-2.5-flash",
            "temperature": 0.3,
            "max_tokens": 1024,
            "system_prompt": (
                "You are a patient tutor. Explain concepts clearly and step-by-step to help students "
                "resolve their doubts. Use simple language, provide examples, and ask follow-up questions "
                "to check understanding."
            )
        },
        "assessment": {
            "model": "gemini-2.5-flash",
            "temperature": 0.4,
            "max_tokens": 2048,
            "system_prompt": (
                "You are an assessment specialist. Create diverse, high-quality assessments with "
                "multiple question types and difficulty levels. Include clear instructions and "
                "comprehensive answer keys."
            )
        },
        "peer_teaching": {
            "model": "gemini-2.5-flash",
            "temperature": 0.6,
            "max_tokens": 1024,
            "system_prompt": (
                "You are a peer learning coordinator. Design effective peer teaching activities "
                "that match students' skill levels. Create structured group activities and "
                "discussion prompts to facilitate collaborative learning."
            )
        },
        "parent_engagement": {
            "model": "gemini-2.5-flash",
            "temperature": 0.5,
            "max_tokens": 1024,
            "system_prompt": (
                "You are a parent communication specialist. Translate student progress data and "
                "teacher comments into constructive, parent-friendly reports. Provide specific "
                "suggestions for home support and engagement."
            )
        },
        "resource_planner": {
            "model": "gemini-2.5-flash",
            "temperature": 0.3,
            "max_tokens": 2048,
            "system_prompt": (
                "You are a resource optimization expert. Create efficient resource allocation plans "
                "considering constraints and priorities. Suggest cost-saving alternatives and "
                "contingency strategies."
            )
        },
        "multi_calendar": {
            "model": "gemini-2.5-flash",
            "temperature": 0.3,
            "max_tokens": 2048,
            "system_prompt": (
                "You are a scheduling coordinator. Synchronize multiple calendars, resolve conflicts, "
                "and prioritize events. Create clear visual timelines and notification systems."
            )
        }
    }
    
    # Add other configuration settings as needed
    MAX_SESSION_AGE = 3600  # 1 hour in seconds
    CACHE_ENABLED = True
