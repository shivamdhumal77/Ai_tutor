
// GeminiClient: Handles all 10 AI Tutor features via Flask endpoints
class GeminiClient {
    constructor() {
        this.baseUrl = '/feature';
    }

    // Generic request method for any feature
    async requestFeature(featureKey, data) {
        const response = await fetch(`${this.baseUrl}/${featureKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return response.json();
    }

    // 1. Multi-Grade Lesson Synthesizer
    async multiGradeLesson(topic, grade_levels) {
        return this.requestFeature('multi_grade', { topic, grade_levels });
    }

    // 2. Voice-Powered Classroom Assistant
    async voiceAssistant(transcript) {
        return this.requestFeature('voice_assistant', { transcript });
    }

    // 3. Adaptive Content Difficulty Branching
    async adaptiveContent(content, performance_data) {
        return this.requestFeature('adaptive_content', { content, performance_data });
    }

    // 4. Cultural Context Integration Engine
    async culturalContext(content, cultural_background) {
        return this.requestFeature('cultural_context', { content, cultural_background });
    }

    // 5. Instant Doubt Resolution System
    async doubtResolution(question, subject) {
        return this.requestFeature('doubt_resolution', { question, subject });
    }

    // 6. Smart Assessment Generator
    async assessment(topic, difficulty, question_types) {
        return this.requestFeature('assessment', { topic, difficulty, question_types });
    }

    // 7. Peer Teaching Orchestrator
    async peerTeaching(topic, student_profiles) {
        return this.requestFeature('peer_teaching', { topic, student_profiles });
    }

    // 8. Parent-Community Engagement Portal
    async parentEngagement(student_progress, upcoming_events) {
        return this.requestFeature('parent_engagement', { student_progress, upcoming_events });
    }

    // 9. Resource Optimization Planner
    async resourcePlanner(budget, constraints, requirements) {
        return this.requestFeature('resource_planner', { budget, constraints, requirements });
    }

    // 10. Smart Multi-Calendar / Scheduler
    async multiCalendar(events, constraints) {
        return this.requestFeature('multi_calendar', { events, constraints });
    }
}

// Make available globally
window.geminiClient = new GeminiClient();