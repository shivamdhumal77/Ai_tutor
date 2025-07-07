from services.gemini_service import GeminiService
import json

class BaseAgent:
    def __init__(self, model_name=None):
        # Always use the latest model from config or env
        import os
        model_name = model_name or os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
        self.gemini = GeminiService(model_name)

    def generate_response(self, prompt):
        return self.gemini.generate_content(prompt)

    def safe_json(self, response):
        try:
            return json.loads(response)
        except Exception:
            return {"raw_response": response}

# 11. Doubt Resolution with PDF/Image (LangChain + RAG)
class DoubtResolutionRAGAgent(BaseAgent):
    def __init__(self, model_name=None):
        super().__init__(model_name)
        # Lazy import to avoid errors if not installed
        try:
            from langchain_community.document_loaders import PyPDFLoader
            from langchain_community.document_loaders import UnstructuredImageLoader
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            from langchain.chains import RetrievalQA
            self.PyPDFLoader = PyPDFLoader
            self.UnstructuredImageLoader = UnstructuredImageLoader
            self.RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter
            self.HuggingFaceEmbeddings = HuggingFaceEmbeddings
            self.FAISS = FAISS
            self.RetrievalQA = RetrievalQA
        except ImportError:
            raise ImportError("Please install langchain, faiss-cpu, and unstructured[local-inference,pdf] for PDF/image RAG support.")
        self.vectorstore = None
        self.qa_chain = None

    def load_pdf(self, pdf_path):
        # Load and embed PDF
        loader = self.PyPDFLoader(pdf_path)
        docs = loader.load()
        splitter = self.RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        splits = splitter.split_documents(docs)
        embeddings = self.HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = self.FAISS.from_documents(splits, embeddings)
        self.qa_chain = self.RetrievalQA.from_chain_type(
            llm=self.gemini,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever()
        )

    def load_image(self, image_path):
        # Load and embed image (OCR)
        loader = self.UnstructuredImageLoader(image_path)
        docs = loader.load()
        splitter = self.RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        splits = splitter.split_documents(docs)
        embeddings = self.HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = self.FAISS.from_documents(splits, embeddings)
        self.qa_chain = self.RetrievalQA.from_chain_type(
            llm=self.gemini,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever()
        )

    def answer(self, question):
        if not self.qa_chain:
            return "Please upload a PDF or image first."
        result = self.qa_chain({"query": question})
        return result["result"] if "result" in result else str(result)
from services.gemini_service import GeminiService
import json

class BaseAgent:
    def __init__(self, model_name=None):
        # Always use the latest model from config or env
        import os
        model_name = model_name or os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
        self.gemini = GeminiService(model_name)

    def generate_response(self, prompt):
        return self.gemini.generate_content(prompt)

    def safe_json(self, response):
        try:
            return json.loads(response)
        except Exception:
            return {"raw_response": response}

# 1. Multi-Grade Lesson Synthesizer
class MultiGradeLessonSynthesizer(BaseAgent):
    def create_lesson(self, topic, grade_levels):
        prompt = (
            f"Create a multi-grade lesson plan for '{topic}' for grades {grade_levels}. "
            "Return JSON: objectives, activities, assessments for each grade."
        )
        return self.safe_json(self.generate_response(prompt))

# 2. Voice-Powered Classroom Assistant
class VoiceAssistant(BaseAgent):
    def process_voice_command(self, transcript, session_id=None):
        # Use Gemini to classify the intent and act accordingly (MLP-style prompt chaining)
        prompt = (
            f"You are an AI teaching assistant. Analyze the following user message and classify its intent as one of: greeting, reminder, explanation, confusion, or general. "
            f"Then, based on the intent, do the following:\n"
            f"- If greeting: reply with a warm greeting.\n"
            f"- If reminder: extract the topic and date/time, and say you will schedule it.\n"
            f"- If explanation: provide a clear, concise explanation of the topic.\n"
            f"- If confusion: suggest helpful YouTube and article links for the topic.\n"
            f"- If general: answer as a helpful classroom assistant.\n"
            f"Return a JSON object with keys: intent, response_text, [topic, date] if relevant.\n"
            f"User message: {transcript}"
        )
        raw = self.generate_response(prompt)
        # If the model returns a code block or stringified JSON, parse it robustly
        import re, json
        if isinstance(raw, str) and raw.strip().startswith('```json'):
            raw = re.sub(r'^```json[\s\n]*', '', raw.strip())
            raw = re.sub(r'```$', '', raw.strip())
        try:
            result = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            result = {'response_text': str(raw)}
        return result.get('response_text', str(result))

# 3. Adaptive Content Difficulty Branching
class AdaptiveContentAgent(BaseAgent):
    def adjust_difficulty(self, content, performance_data):
        prompt = (
            f"Adapt content for student performance.\n"
            f"Content: {content}\nPerformance: {performance_data}\n"
            "Return JSON: simplified, standard, advanced."
        )
        return self.safe_json(self.generate_response(prompt))

# 4. Cultural Context Integration Engine
class CulturalContextAgent(BaseAgent):
    def add_context(self, content, cultural_background):
        prompt = (
            f"Make this content culturally relevant for {cultural_background}: {content}\n"
            "Keep objectives, add relevant examples. Return improved content."
        )
        return self.generate_response(prompt)

# 5. Instant Doubt Resolution System
class DoubtResolutionAgent(BaseAgent):
    def resolve_query(self, question, subject):
        prompt = (
            f"Answer this {subject} question: '{question}'. "
            "Step-by-step, address misconceptions. Return answer."
        )
        return self.generate_response(prompt)

# 6. Smart Assessment Generator
class AssessmentGeneratorAgent(BaseAgent):
    def generate_assessment(self, topic, difficulty, question_types):
        prompt = (
            f"Create a {difficulty} assessment on '{topic}' with types {question_types}. "
            "Return JSON: mcq, short_answer, essay, answer_keys, rubrics."
        )
        return self.safe_json(self.generate_response(prompt))

# 7. Peer Teaching Orchestrator
class PeerTeachingAgent(BaseAgent):
    def create_activity(self, topic, student_profiles):
        prompt = (
            f"Peer teaching for '{topic}' with profiles {student_profiles}. "
            "Return JSON: roles, prompts, collaboration."
        )
        return self.safe_json(self.generate_response(prompt))

# 8. Parent-Community Engagement Portal
class ParentEngagementAgent(BaseAgent):
    def generate_update(self, student_progress, upcoming_events):
        prompt = (
            f"Parent update. Progress: {student_progress}. Events: {upcoming_events}. "
            "Write 3 positive, constructive paragraphs with emojis."
        )
        return self.generate_response(prompt)

# 9. Resource Optimization Planner
class ResourcePlannerAgent(BaseAgent):
    def optimize_resources(self, budget, constraints, requirements):
        prompt = (
            f"Optimize resources. Budget: {budget}, Constraints: {constraints}, "
            f"Requirements: {requirements}. Return JSON: purchase_list, alternatives."
        )
        return self.safe_json(self.generate_response(prompt))

# 10. Smart Multi-Calendar / Scheduler
class MultiCalendarAgent(BaseAgent):
    def schedule_events(self, events, constraints):
        prompt = (
            f"Schedule events: {events} with constraints: {constraints}. "
            "Return iCal format, color-coded."
        )
        return self.generate_response(prompt)