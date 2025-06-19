from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re
import textwrap
import time
import requests
from urllib.parse import quote
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure Gemini API with your key
API_KEY = "AIzaSyDYe2eqkYl2ZzKkpm7NBT7DT6ivxib37PA"
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# YouTube API Configuration (Get your own API key from Google Cloud Console)
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"  # Replace with your YouTube API key
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def get_simplified_explanation(topic):
    """Get a detailed teacher-like explanation for any subject"""
    conversation = [
        {
            "role": "user",
            "parts": [
                "ROLE: You are a master teacher with 25 years of experience across all subjects.",
                "TASK: Create a comprehensive lesson on: " + topic,
                "",
                "LESSON STRUCTURE:",
                "1. INTRODUCTION: Start with an intriguing hook that relates to everyday life",
                "2. CORE CONCEPT: Explain the fundamental principles in simple terms",
                "3. KEY POINTS: Break down into 3-5 main ideas with clear examples",
                "4. REAL-WORLD APPLICATIONS: Show how this is used in practical situations",
                "5. COMMON MISCONCEPTIONS: Address 2-3 frequent misunderstandings",
                "6. LEARNING TIPS: Provide effective study strategies",
                "7. SUMMARY: Recap the most important takeaways",
                "",
                "TEACHING STYLE:",
                "- Use warm, encouraging, and patient tone",
                "- Employ relatable analogies and metaphors",
                "- Include interactive elements like rhetorical questions",
                "- Minimum 800 words, maximum 1500 words",
                "- Avoid jargon without explanation",
                "- Use section headings with Markdown formatting",
                "- Be inclusive and supportive to all learners",
                "",
                "TOPIC: " + topic,
                "",
                "If you cannot provide a substantive lesson, respond with: 'TOPIC_TOO_COMPLEX'",
                "Otherwise, provide the complete lesson."
            ]
        }
    ]
    
    for attempt in range(3):
        try:
            response = model.generate_content(conversation)
            text = response.text
            
            if "fascinating process" in text.lower() or "transform inputs" in text.lower():
                raise ValueError("Generic response detected")
                
            if len(text) < 500:
                raise ValueError("Response too short")
                
            return text
            
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            time.sleep(2 ** attempt)
    
    fallback = f"""
    I apologize - our AI teacher is having difficulty preparing a lesson on '{topic}'. 
    This could be because the topic is very specialized or complex.
    
    Please try one of these options:
    1. Rephrase your topic to be more specific
    2. Break it down into smaller subtopics
    3. Try a different subject area
    
    For example:
    Instead of "Physics", try "Newton's Laws of Motion"
    Instead of "Biology", try "Photosynthesis process"
    """
    return fallback

def get_word_meaning(word):
    """Get word meaning using Gemini API"""
    try:
        prompt = f"""
        Define the word '{word}' in a clear, educational manner.
        
        Provide:
        1. Definition (simple and clear)
        2. Part of speech
        3. Example sentence
        4. Etymology (if interesting)
        5. Synonyms (2-3)
        
        Format as JSON with keys: definition, part_of_speech, example, etymology, synonyms
        """
        
        response = model.generate_content(prompt)
        # Extract JSON from response
        text = response.text
        
        # Try to parse as JSON, fallback to simple definition
        try:
            return json.loads(text)
        except:
            return {
                "definition": text,
                "part_of_speech": "N/A",
                "example": "N/A",
                "etymology": "N/A",
                "synonyms": []
            }
    except Exception as e:
        return {
            "definition": f"Unable to fetch definition for '{word}'",
            "part_of_speech": "N/A",
            "example": "N/A",
            "etymology": "N/A",
            "synonyms": []
        }

def get_youtube_videos(topic, max_results=5):
    """Get YouTube videos related to the topic"""
    try:
        params = {
            'part': 'snippet',
            'q': f"{topic} educational tutorial",
            'type': 'video',
            'maxResults': max_results,
            'order': 'relevance',
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(YOUTUBE_API_URL, params=params)
        data = response.json()
        
        videos = []
        if 'items' in data:
            for item in data['items']:
                video = {
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'][:150] + '...',
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'channel': item['snippet']['channelTitle'],
                    'published': item['snippet']['publishedAt']
                }
                videos.append(video)
        
        return videos
    except Exception as e:
        print(f"YouTube API error: {e}")
        return []

def get_article_suggestions(topic):
    """Generate article suggestions using AI"""
    try:
        prompt = f"""
        Suggest 5 high-quality educational articles or resources about '{topic}'.
        
        For each suggestion, provide:
        1. Title (make it educational and engaging)
        2. Description (2-3 sentences about what the article covers)
        3. Suggested source type (Academic paper, Educational website, Encyclopedia, etc.)
        
        Format as JSON array with objects containing: title, description, source_type
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        try:
            return json.loads(text)
        except:
            # Fallback suggestions
            return [
                {
                    "title": f"Introduction to {topic}",
                    "description": f"A comprehensive overview of {topic} covering basic concepts and principles.",
                    "source_type": "Educational Website"
                },
                {
                    "title": f"Advanced {topic} Concepts",
                    "description": f"Deep dive into complex aspects of {topic} with detailed explanations.",
                    "source_type": "Academic Resource"
                }
            ]
    except Exception as e:
        return []

def generate_quiz(topic):
    """Generate a quiz based on the topic"""
    try:
        prompt = f"""
        Create a 5-question multiple choice quiz about '{topic}'.
        
        For each question:
        1. Question text
        2. Four options (A, B, C, D)
        3. Correct answer (letter)
        4. Brief explanation of the correct answer
        
        Make questions educational and varying in difficulty.
        Format as JSON array with objects containing: question, options, correct_answer, explanation
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        try:
            return json.loads(text)
        except:
            return []
    except Exception as e:
        return []

def get_related_topics(topic):
    """Get related topics for further learning"""
    try:
        prompt = f"""
        Suggest 6 related topics to '{topic}' that a student might want to learn next.
        
        Include both:
        - Prerequisite topics (if any)
        - Advanced topics to explore next
        
        Format as JSON array of strings, each being a topic name.
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        try:
            return json.loads(text)
        except:
            return [f"Introduction to {topic}", f"Advanced {topic}", f"{topic} Applications"]
    except Exception as e:
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain_topic():
    topic = request.form['topic'].strip()
    
    if not topic:
        return jsonify({'error': 'Please enter a topic'})
    
    try:
        # Get explanation from Gemini
        explanation = get_simplified_explanation(topic)
        
        # Get additional resources
        youtube_videos = get_youtube_videos(topic)
        article_suggestions = get_article_suggestions(topic)
        related_topics = get_related_topics(topic)
        
        return jsonify({
            'topic': topic,
            'explanation': explanation,
            'youtube_videos': youtube_videos,
            'articles': article_suggestions,
            'related_topics': related_topics
        })
    except Exception as e:
        return jsonify({'error': f"System error: {str(e)}"})

@app.route('/define', methods=['POST'])
def define_word():
    word = request.form['word'].strip()
    
    if not word:
        return jsonify({'error': 'Please enter a word'})
    
    try:
        definition = get_word_meaning(word)
        return jsonify(definition)
    except Exception as e:
        return jsonify({'error': f"Error getting definition: {str(e)}"})

@app.route('/quiz', methods=['POST'])
def generate_topic_quiz():
    topic = request.form['topic'].strip()
    
    if not topic:
        return jsonify({'error': 'Please enter a topic'})
    
    try:
        quiz_questions = generate_quiz(topic)
        return jsonify({'quiz': quiz_questions})
    except Exception as e:
        return jsonify({'error': f"Error generating quiz: {str(e)}"})

@app.route('/voice-settings', methods=['POST'])
def save_voice_settings():
    """Save user voice preferences"""
    data = request.get_json()
    # In a real app, you'd save this to a database
    # For now, just return success
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5001)