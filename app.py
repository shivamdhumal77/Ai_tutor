from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from services.ai_agent import (
    MultiGradeLessonSynthesizer,
    VoiceAssistant,
    AdaptiveContentAgent,
    CulturalContextAgent,
    DoubtResolutionAgent,
    AssessmentGeneratorAgent,
    PeerTeachingAgent,
    ParentEngagementAgent,
    ResourcePlannerAgent,
    MultiCalendarAgent,
    DoubtResolutionRAGAgent
)
from utils.helpers import format_response
from services.assessment_resource_agent import store_resource, get_resources

app = Flask(__name__)

# --- Assessment Resource Filters Endpoint (for dropdowns) ---
@app.route('/feature/assessment/get_resource_filters', methods=['GET'])
def get_resource_filters():
    meta = get_resources()
    grades = sorted(set(entry['grade'] for entry in meta if entry.get('grade')))
    subjects = sorted(set(entry['subject'] for entry in meta if entry.get('subject')))
    return jsonify({'success': True, 'grades': grades, 'subjects': subjects})

# --- Doubt Resolution RAG Agent (PDF/Image chat) ---
import tempfile
def register_doubt_rag_endpoints(app):
    doubt_rag_agent = DoubtResolutionRAGAgent()
    @app.route('/feature/doubt_resolution_pdf', methods=['POST'])
    def upload_pdf():
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'error': 'No PDF uploaded.'}), 400
        file = request.files['pdf']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'File must be a PDF.'}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            try:
                doubt_rag_agent.load_pdf(tmp.name)
            except Exception as e:
                os.unlink(tmp.name)
                return jsonify({'success': False, 'error': str(e)}), 500
            os.unlink(tmp.name)
        return jsonify({'success': True})
    @app.route('/feature/doubt_resolution_image', methods=['POST'])
    def upload_image():
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image uploaded.'}), 400
        file = request.files['image']
        if not (file.filename.lower().endswith('.png') or file.filename.lower().endswith('.jpg') or file.filename.lower().endswith('.jpeg')):
            return jsonify({'success': False, 'error': 'File must be an image.'}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            file.save(tmp.name)
            try:
                doubt_rag_agent.load_image(tmp.name)
            except Exception as e:
                os.unlink(tmp.name)
                return jsonify({'success': False, 'error': str(e)}), 500
            os.unlink(tmp.name)
        return jsonify({'success': True})
    @app.route('/feature/doubt_resolution_chat', methods=['POST'])
    def doubt_resolution_chat():
        data = request.get_json(force=True, silent=True)
        question = data.get('question', '')
        if not question:
            return jsonify({'response': 'Please enter a question.'})
        try:
            answer = doubt_rag_agent.answer(question)
            return jsonify({'response': answer})
        except Exception as e:
            return jsonify({'response': f'Error: {str(e)}'})

register_doubt_rag_endpoints(app)

# --- Assessment Resource Endpoints (Notes/Flashcards) ---
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'uploads')

@app.route('/feature/assessment/upload_resource', methods=['POST'])
def upload_assessment_resource():
    file = request.files.get('file')
    resource_type = request.form.get('resource_type')
    grade = request.form.get('grade')
    subject = request.form.get('subject')
    topic = request.form.get('topic')
    if not file or not resource_type or not grade or not subject or not topic:
        return jsonify({'success': False, 'error': 'Missing required fields.'}), 400
    try:
        entry = store_resource(file, resource_type, grade, subject, topic)
        return jsonify({'success': True, 'entry': entry})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Retrieve resources (list)
@app.route('/feature/assessment/get_resources', methods=['GET'])
def get_assessment_resources():
    resource_type = request.args.get('resource_type')
    grade = request.args.get('grade')
    subject = request.args.get('subject')
    topic = request.args.get('topic')
    results = get_resources(resource_type, grade, subject, topic)
    return jsonify({'success': True, 'results': results})

# Serve uploaded files
@app.route('/uploads/<resource_type>/<filename>')
def serve_uploaded_resource(resource_type, filename):
    if resource_type not in ['notes', 'flashcards']:
        return 'Invalid resource type', 404
    directory = os.path.join(UPLOADS_DIR, resource_type)
    return send_from_directory(directory, filename)

# --- Doubt Resolution RAG Agent (PDF/Image chat) ---
import tempfile, os

def register_doubt_rag_endpoints(app):
    doubt_rag_agent = DoubtResolutionRAGAgent()

    @app.route('/feature/doubt_resolution_pdf', methods=['POST'])
    def upload_pdf():
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'error': 'No PDF uploaded.'}), 400
        file = request.files['pdf']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'File must be a PDF.'}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            try:
                doubt_rag_agent.load_pdf(tmp.name)
            except Exception as e:
                os.unlink(tmp.name)
                return jsonify({'success': False, 'error': str(e)}), 500
            os.unlink(tmp.name)
        return jsonify({'success': True})

    @app.route('/feature/doubt_resolution_image', methods=['POST'])
    def upload_image():
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image uploaded.'}), 400
        file = request.files['image']
        if not (file.filename.lower().endswith('.png') or file.filename.lower().endswith('.jpg') or file.filename.lower().endswith('.jpeg')):
            return jsonify({'success': False, 'error': 'File must be an image.'}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            file.save(tmp.name)
            try:
                doubt_rag_agent.load_image(tmp.name)
            except Exception as e:
                os.unlink(tmp.name)
                return jsonify({'success': False, 'error': str(e)}), 500
            os.unlink(tmp.name)
        return jsonify({'success': True})

    @app.route('/feature/doubt_resolution_chat', methods=['POST'])
    def doubt_resolution_chat():
        data = request.get_json(force=True, silent=True)
        question = data.get('question', '')
        if not question:
            return jsonify({'response': 'Please enter a question.'})
        try:
            answer = doubt_rag_agent.answer(question)
            return jsonify({'response': answer})
        except Exception as e:
            return jsonify({'response': f'Error: {str(e)}'})


from utils.helpers import format_response

app = Flask(__name__)
register_doubt_rag_endpoints(app)

# --- Assessment Resource Endpoints (Notes/Flashcards) ---
import os
from services.assessment_resource_agent import store_resource, get_resources
from flask import send_from_directory
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'uploads')

@app.route('/feature/assessment/upload_resource', methods=['POST'])
def upload_assessment_resource():
    file = request.files.get('file')
    resource_type = request.form.get('resource_type')
    grade = request.form.get('grade')
    subject = request.form.get('subject')
    topic = request.form.get('topic')
    if not file or not resource_type or not grade or not subject or not topic:
        return jsonify({'success': False, 'error': 'Missing required fields.'}), 400
    try:
        entry = store_resource(file, resource_type, grade, subject, topic)
        return jsonify({'success': True, 'entry': entry})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Retrieve resources (list)
@app.route('/feature/assessment/get_resources', methods=['GET'])
def get_assessment_resources():
    resource_type = request.args.get('resource_type')
    grade = request.args.get('grade')
    subject = request.args.get('subject')
    topic = request.args.get('topic')
    results = get_resources(resource_type, grade, subject, topic)
    return jsonify({'success': True, 'results': results})

# Serve uploaded files
@app.route('/uploads/<resource_type>/<filename>')
def serve_uploaded_resource(resource_type, filename):
    if resource_type not in ['notes', 'flashcards']:
        return 'Invalid resource type', 404
    directory = os.path.join(UPLOADS_DIR, resource_type)
    return send_from_directory(directory, filename)
    MultiGradeLessonSynthesizer,
    VoiceAssistant,
    AdaptiveContentAgent,
    CulturalContextAgent,
    DoubtResolutionAgent,
    AssessmentGeneratorAgent,
    PeerTeachingAgent,
    ParentEngagementAgent,
    ResourcePlannerAgent,
    MultiCalendarAgent,
    DoubtResolutionRAGAgent


# --- Doubt Resolution RAG Agent (PDF/Image chat) ---
import tempfile, os

def register_doubt_rag_endpoints(app):
    doubt_rag_agent = DoubtResolutionRAGAgent()

    @app.route('/feature/doubt_resolution_pdf', methods=['POST'])
    def upload_pdf():
        if 'pdf' not in request.files:
            return jsonify({'success': False, 'error': 'No PDF uploaded.'}), 400
        file = request.files['pdf']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'File must be a PDF.'}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            try:
                doubt_rag_agent.load_pdf(tmp.name)
            except Exception as e:
                os.unlink(tmp.name)
                return jsonify({'success': False, 'error': str(e)}), 500
            os.unlink(tmp.name)
        return jsonify({'success': True})

    @app.route('/feature/doubt_resolution_image', methods=['POST'])
    def upload_image():
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image uploaded.'}), 400
        file = request.files['image']
        if not (file.filename.lower().endswith('.png') or file.filename.lower().endswith('.jpg') or file.filename.lower().endswith('.jpeg')):
            return jsonify({'success': False, 'error': 'File must be an image.'}), 400
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            file.save(tmp.name)
            try:
                doubt_rag_agent.load_image(tmp.name)
            except Exception as e:
                os.unlink(tmp.name)
                return jsonify({'success': False, 'error': str(e)}), 500
            os.unlink(tmp.name)
        return jsonify({'success': True})

    @app.route('/feature/doubt_resolution_chat', methods=['POST'])
    def doubt_resolution_chat():
        data = request.get_json(force=True, silent=True)
        question = data.get('question', '')
        if not question:
            return jsonify({'response': 'Please enter a question.'})
        try:
            answer = doubt_rag_agent.answer(question)
            return jsonify({'response': answer})
        except Exception as e:
            return jsonify({'response': f'Error: {str(e)}'})


from utils.helpers import format_response

app = Flask(__name__)
register_doubt_rag_endpoints(app)

# Feature registry: maps feature keys to agent instances and handler lambdas
FEATURES = {
    "multi_grade": {
        "name": "Intelligent Multi-Grade Lesson Synthesizer",
        "agent": MultiGradeLessonSynthesizer(),
        "handler": lambda agent, data: agent.create_lesson(data['topic'], data['grade_levels'])
    },
    "voice_assistant": {
        "name": "Voice-Powered Classroom Assistant",
        "agent": VoiceAssistant(),
        "handler": lambda agent, data: agent.process_voice_command(data['transcript'])
    },
    "adaptive_content": {
        "name": "Adaptive Content Difficulty Branching",
        "agent": AdaptiveContentAgent(),
        "handler": lambda agent, data: agent.adjust_difficulty(data['content'], data['performance_data'])
    },
    "cultural_context": {
        "name": "Cultural Context Integration Engine",
        "agent": CulturalContextAgent(),
        "handler": lambda agent, data: agent.add_context(data['content'], data['cultural_background'])
    },
    "doubt_resolution": {
        "name": "Instant Doubt Resolution System",
        "agent": DoubtResolutionAgent(),
        "handler": lambda agent, data: agent.resolve_query(data['question'], data['subject'])
    },
    "assessment": {
        "name": "Smart Assessment Generator",
        "agent": AssessmentGeneratorAgent(),
        "handler": lambda agent, data: agent.generate_assessment(data['topic'], data['difficulty'], data['question_types'])
    },
    "peer_teaching": {
        "name": "Peer Teaching Orchestrator",
        "agent": PeerTeachingAgent(),
        "handler": lambda agent, data: agent.create_activity(data['topic'], data['student_profiles'])
    },
    "parent_engagement": {
        "name": "Parent-Community Engagement Portal",
        "agent": ParentEngagementAgent(),
        "handler": lambda agent, data: agent.generate_update(data['student_progress'], data['upcoming_events'])
    },
    "resource_planner": {
        "name": "Resource Optimization Planner",
        "agent": ResourcePlannerAgent(),
        "handler": lambda agent, data: agent.optimize_resources(data['budget'], data['constraints'], data['requirements'])
    },
    "multi_calendar": {
        "name": "Smart Multi-Calendar / Scheduler",
        "agent": MultiCalendarAgent(),
        "handler": lambda agent, data: agent.schedule_events(data['events'], data['constraints'])
    }
}

@app.route('/')
def index():
    # Pass feature list to template for dynamic UI
    return render_template('index.html', features=[{"key": k, "name": v["name"]} for k, v in FEATURES.items()])

@app.route('/feature/<feature_key>', methods=['GET', 'POST'])
def feature_page(feature_key):
    feature = FEATURES.get(feature_key)
    if not feature:
        return jsonify({"error": "Invalid feature"}), 404


    if request.method == 'POST':
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"error": "I'm sorry, I couldn't understand your request. Could you please try again?"}), 400
        try:
            response = feature["handler"](feature["agent"], data)
            # Feature 1: After assessment, call AdaptiveContentAgent for personalized content
            if feature_key == 'assessment' and isinstance(response, dict):
                topic = data.get('topic', '')
                performance_data = response.get('answer_keys') or response.get('rubrics') or {}
                from services.ai_agent import AdaptiveContentAgent, PeerTeachingAgent
                adaptive_agent = AdaptiveContentAgent()
                adapted = adaptive_agent.adjust_difficulty(topic, performance_data)
                # Feature 3: If assessment is poor, suggest peer teaching
                peer_teaching = None
                perf_str = str(performance_data).lower()
                if not performance_data or 'poor' in perf_str or 'low' in perf_str or 'struggle' in perf_str:
                    peer_agent = PeerTeachingAgent()
                    student_profiles = ["Student A", "Student B"]
                    peer_teaching = peer_agent.create_activity(topic, student_profiles)
                return jsonify({
                    "assessment": response,
                    "adaptive_content": adapted,
                    "peer_teaching": peer_teaching
                })

            # Feature 4: Voice Assistant as Universal Orchestrator
            if feature_key == 'voice_assistant' and isinstance(response, dict):
                import re
                orchestration = None
                # Quiz creation and scheduling
                quiz_match = re.search(r'(create|make|generate) (a )?(quiz|assessment|test|questions?) (for|on|about) ([\w\s]+?)( and )?schedule (it|this)? (for|on|at|in) ([\w\s]+)', data.get('transcript', ''), re.IGNORECASE)
                if quiz_match:
                    topic = quiz_match.group(5).strip()
                    schedule_time = quiz_match.group(9).strip()
                    from services.ai_agent import AssessmentGeneratorAgent, MultiCalendarAgent
                    assessment_agent = AssessmentGeneratorAgent()
                    assessment = assessment_agent.generate_assessment(topic, 'medium', ['mcq', 'short_answer'])
                    calendar_agent = MultiCalendarAgent()
                    event = {"title": f"Quiz: {topic}", "date": schedule_time}
                    cal_result = calendar_agent.schedule_events([event], constraints=None)
                    orchestration = {
                        "assessment": assessment,
                        "calendar": cal_result,
                        "response_text": f"Quiz for '{topic}' created and scheduled for {schedule_time}."
                    }
                # Add more orchestration patterns as needed
                if orchestration:
                    response.update({"orchestration": orchestration})
                # Return the updated response
                formatted = format_response(feature_key, response) if isinstance(response, str) else response
                answer = None
                if isinstance(formatted, dict) and 'response_text' in formatted:
                    answer = formatted['response_text']
                elif isinstance(formatted, dict) and 'raw_response' in formatted:
                    import json
                    try:
                        raw = formatted['raw_response']
                        if raw.strip().startswith('```json'):
                            raw = raw.strip().lstrip('```json').rstrip('```').strip()
                        data_json = json.loads(raw)
                        answer = data_json.get('response_text', str(formatted))
                    except Exception:
                        answer = str(formatted)
                else:
                    answer = str(formatted)
                return jsonify({"response": answer, "orchestration": orchestration})
            # ...existing code for all other features...
            formatted = format_response(feature_key, response) if isinstance(response, str) else response
            answer = None
            if isinstance(formatted, dict) and 'response_text' in formatted:
                answer = formatted['response_text']
            elif isinstance(formatted, dict) and 'raw_response' in formatted:
                import json
                try:
                    raw = formatted['raw_response']
                    if raw.strip().startswith('```json'):
                        raw = raw.strip().lstrip('```json').rstrip('```').strip()
                    data_json = json.loads(raw)
                    answer = data_json.get('response_text', str(formatted))
                except Exception:
                    answer = str(formatted)
            else:
                answer = str(formatted)
            return jsonify({"response": answer})
        except Exception as e:
            return jsonify({"error": "Oops! Something went wrong. Please try again or ask another way. (Error: {} )".format(str(e))}), 500

    # GET: Render feature-specific page (optional: create templates/features/<feature_key>.html)
    return render_template(f'features/{feature_key}.html', feature_name=feature["name"])

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Run on all interfaces for local network access
    app.run(host="0.0.0.0", port=5000, debug=True)