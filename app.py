import os
import json
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing) manually to allow the frontend
# to communicate with the API when served from a different port (e.g., Live Server).
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
    return response



# Define the path to the JSON file where course data will be stored.
# This places courses.json in the same directory as app.py.
DATA_FILE = os.path.join(os.path.dirname(__file__), 'courses.json')

def init_db():
    """
    Ensures that the courses.json file exists and is initialized with an empty JSON array [].
    This fulfills the requirement to automatically create the file if it doesn't exist.
    """
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)
        except IOError as e:
            print(f"Error: Could not initialize database file at {DATA_FILE}. Details: {e}")

# Initialize the JSON database file upon application startup
init_db()

def load_courses():
    """
    Retrieves course data from the JSON file.
    Returns a list of course dictionaries.
    """
    # Double-check existence (e.g., if deleted during runtime)
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: The file {DATA_FILE} contains invalid JSON. Details: {e}")
        return []
    except IOError as e:
        print(f"IO Error: Could not read file {DATA_FILE}. Details: {e}")
        return []

def save_courses(courses):
    """
    Writes the list of courses back to the JSON file with pretty printing.
    Returns True if successful, False otherwise.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            # indent=4 writes formatted JSON that is easy for humans to read
            json.dump(courses, f, indent=4)
        return True
    except IOError as e:
        print(f"IO Error: Could not write to file {DATA_FILE}. Details: {e}")
        return False

def validate_date(date_string):
    """
    Validates if a given date string matches the YYYY-MM-DD format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Handler for CORS Preflight OPTIONS requests
@app.route('/api/courses', methods=['OPTIONS'])
@app.route('/api/courses/<int:course_id>', methods=['OPTIONS'])
def handle_options(course_id=None):
    return '', 204

# ==========================================
# FRONTEND ROUTE
# ==========================================
@app.route('/')
def index():
    """
    Serves the user interface dashboard.
    """
    return render_template('index.html')

# ==========================================
# REST API ENDPOINTS
# ==========================================

# 1. GET /api/courses - Get all courses
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    courses = load_courses()
    return jsonify(courses), 200

# 2. GET /api/courses/<id> - Get a specific course by ID
@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    courses = load_courses()
    
    # Search for the course with the matching ID
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course is None:
        return jsonify({"error": f"Course with ID {course_id} not found."}), 404
        
    return jsonify(course), 200

# 3. POST /api/courses - Add a new course
@app.route('/api/courses', methods=['POST'])
def create_course():
    # Parse incoming JSON payload
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid request body. Expected JSON data."}), 400
        
    # --- Validation: Missing Required Fields ---
    required_fields = ['name', 'description', 'target_date', 'status']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
    name = data.get('name').strip()
    description = data.get('description').strip()
    target_date = data.get('target_date').strip()
    status = data.get('status').strip()
    
    # Ensure fields are not just empty spaces
    if not name:
        return jsonify({"error": "Course 'name' cannot be empty."}), 400
    if not description:
        return jsonify({"error": "Course 'description' cannot be empty."}), 400
    if not target_date:
        return jsonify({"error": "Course 'target_date' cannot be empty."}), 400
    if not status:
        return jsonify({"error": "Course 'status' cannot be empty."}), 400
        
    # --- Validation: Target Date Format (YYYY-MM-DD) ---
    if not validate_date(target_date):
        return jsonify({"error": f"Invalid 'target_date' format: '{target_date}'. Must be YYYY-MM-DD."}), 400
        
    # --- Validation: Status Values ---
    valid_statuses = ["Not Started", "In Progress", "Completed"]
    if status not in valid_statuses:
        return jsonify({"error": f"Invalid status: '{status}'. Must be one of: {', '.join(valid_statuses)}"}), 400
        
    # Load current list of courses
    courses = load_courses()
    
    # --- Auto-generate Unique ID ---
    # Find the maximum existing ID and add 1. If the list is empty, start from 1.
    next_id = max([c['id'] for c in courses], default=0) + 1
    
    # --- Auto-generate Created At Timestamp ---
    # Format as ISO 8601 UTC timestamp: YYYY-MM-DDTHH:MM:SSZ
    created_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Build new course record
    new_course = {
        "id": next_id,
        "name": name,
        "description": description,
        "target_date": target_date,
        "status": status,
        "created_at": created_at
    }
    
    # Save back to file
    courses.append(new_course)
    if save_courses(courses):
        return jsonify(new_course), 201
    else:
        return jsonify({"error": "Internal Server Error: Failed to save course data."}), 500

# 4. PUT /api/courses/<id> - Update a course
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body. Expected JSON data."}), 400
        
    courses = load_courses()
    
    # Find the course to update
    course = next((c for c in courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({"error": f"Course with ID {course_id} not found."}), 404
        
    # --- Update & Validate Fields ---
    if 'name' in data:
        name = data['name'].strip()
        if not name:
            return jsonify({"error": "Course 'name' cannot be empty."}), 400
        course['name'] = name
        
    if 'description' in data:
        description = data['description'].strip()
        if not description:
            return jsonify({"error": "Course 'description' cannot be empty."}), 400
        course['description'] = description
        
    if 'target_date' in data:
        target_date = data['target_date'].strip()
        if not target_date:
            return jsonify({"error": "Course 'target_date' cannot be empty."}), 400
        if not validate_date(target_date):
            return jsonify({"error": f"Invalid 'target_date' format: '{target_date}'. Must be YYYY-MM-DD."}), 400
        course['target_date'] = target_date
        
    if 'status' in data:
        status = data['status'].strip()
        if not status:
            return jsonify({"error": "Course 'status' cannot be empty."}), 400
        valid_statuses = ["Not Started", "In Progress", "Completed"]
        if status not in valid_statuses:
            return jsonify({"error": f"Invalid status: '{status}'. Must be one of: {', '.join(valid_statuses)}"}), 400
        course['status'] = status
        
    # Save changes to the JSON file
    if save_courses(courses):
        return jsonify(course), 200
    else:
        return jsonify({"error": "Internal Server Error: Failed to save updated course data."}), 500

# 5. DELETE /api/courses/<id> - Delete a course
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = load_courses()
    
    # Verify course exists
    course = next((c for c in courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({"error": f"Course with ID {course_id} not found."}), 404
        
    # Create a new list excluding the course with the matching ID
    updated_courses = [c for c in courses if c['id'] != course_id]
    
    if save_courses(updated_courses):
        return jsonify({"message": f"Course with ID {course_id} deleted successfully."}), 200
    else:
        return jsonify({"error": "Internal Server Error: Failed to delete course."}), 500

if __name__ == '__main__':
    print("- CodeCraftHub API is starting...")
    data_path = os.path.abspath(DATA_FILE).replace('\\', '/')
    print(f"- Data will be stored in: `{data_path}`")
    print("- API will be available at: `http://localhost:5000`")
    # Start the Flask development server on port 5000 in debug mode.
    # Debug mode enables auto-reloading when code changes are detected.
    app.run(debug=True, port=5000)

