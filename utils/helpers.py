
# utils/helpers.py
import json
import re
from datetime import datetime

def format_response(agent_name, response_text):
    """
    Format Gemini response based on agent type for HTML display.
    Add more agent-specific formatting as needed.
    """
    formatting_rules = {
        "multi_grade": lambda t: "<div class='lesson-plan'>{}</div>".format(_htmlify_json(t)),
        "doubt_resolution": lambda t: "<div class='explanation'>{}</div>".format(t.replace('\n', '<br>')),
        "assessment": lambda t: "<div class='assessment'>{}</div>".format(_htmlify_json(t)),
        "parent_engagement": lambda t: "<div class='parent-update'>{}</div>".format(t.replace('\n', '<br>')),
        "resource_planner": lambda t: "<div class='resource-plan'>{}</div>".format(_htmlify_json(t)),
        "default": lambda t: t.replace('\n', '<br>')
    }
    return formatting_rules.get(agent_name, formatting_rules["default"])(response_text)

def _htmlify_json(text):
    """Try to pretty-print JSON as HTML, fallback to <pre>text</pre>"""
    try:
        obj = extract_json(text)
        if isinstance(obj, dict) or isinstance(obj, list):
            return f"<pre>{json.dumps(obj, indent=2, ensure_ascii=False)}</pre>"
        return str(obj)
    except Exception:
        return f"<pre>{text}</pre>"

def extract_json(response_text):
    """
    Extract JSON from Gemini response when structured output is requested.
    Handles markdown code blocks, plain JSON, and fallback.
    """
    try:
        # Handle JSON wrapped in markdown code blocks
        json_match = re.search(r'```json\s*([\s\S]+?)\s*```', response_text, re.IGNORECASE)
        if json_match:
            return json.loads(json_match.group(1))
        # Handle plain JSON output
        return json.loads(response_text)
    except (json.JSONDecodeError, TypeError, ValueError):
        # Fallback to error message
        return {
            "error": "Failed to parse JSON response",
            "raw_response": response_text
        }

def get_current_academic_period():
    """
    Determine current academic period based on date.
    Returns: 'Fall YYYY', 'Spring YYYY', or 'Summer YYYY'
    """
    now = datetime.now()
    month = now.month
    if 8 <= month <= 12:
        return f"Fall {now.year}"
    elif 1 <= month <= 5:
        return f"Spring {now.year}"
    else:
        return f"Summer {now.year}"