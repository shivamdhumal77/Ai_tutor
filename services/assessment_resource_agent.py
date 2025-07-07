import os
from werkzeug.utils import secure_filename
from flask import current_app
import json

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
NOTES_DIR = os.path.join(RESOURCE_DIR, 'notes')
FLASHCARDS_DIR = os.path.join(RESOURCE_DIR, 'flashcards')
META_FILE = os.path.join(RESOURCE_DIR, 'resource_meta.json')

# Ensure directories exist
os.makedirs(NOTES_DIR, exist_ok=True)
os.makedirs(FLASHCARDS_DIR, exist_ok=True)

# Helper to load/save metadata

def load_metadata():
    if not os.path.exists(META_FILE):
        return []
    with open(META_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_metadata(meta):
    with open(META_FILE, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

# Store resource (note or flashcard)
def store_resource(file, resource_type, grade, subject, topic):
    filename = secure_filename(file.filename)
    if resource_type == 'note':
        save_dir = NOTES_DIR
    elif resource_type == 'flashcard':
        save_dir = FLASHCARDS_DIR
    else:
        raise ValueError('Invalid resource type')
    filepath = os.path.join(save_dir, filename)
    file.save(filepath)
    meta = load_metadata()
    entry = {
        'type': resource_type,
        'grade': grade,
        'subject': subject,
        'topic': topic,
        'filename': filename
    }
    meta.append(entry)
    save_metadata(meta)
    return entry

# Retrieve resources by filters
def get_resources(resource_type=None, grade=None, subject=None, topic=None):
    meta = load_metadata()
    results = []
    for entry in meta:
        if resource_type and entry['type'] != resource_type:
            continue
        if grade and entry['grade'] != grade:
            continue
        if subject and entry['subject'] != subject:
            continue
        if topic and entry['topic'] != topic:
            continue
        results.append(entry)
    return results
