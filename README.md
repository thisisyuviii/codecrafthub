# CodeCraftHub 🚀

Welcome to **CodeCraftHub**, a simple, personalized learning platform designed for developers to track courses they want to learn. 

This project is specifically designed for beginners who are learning **REST APIs** and **Backend Development** for the first time. It uses **Python** with the lightweight **Flask** framework, and stores course data in a plain text file (`courses.json`) without requiring any complex database setup.

---

## 📖 What is a REST API? (A Quick Primer for Beginners)

A **REST API** (Representational State Transfer Application Programming Interface) allows two software systems to communicate over the web using standard **HTTP (Hypertext Transfer Protocol)**. 

When you use a REST API, you perform actions using **HTTP Methods** (also called verbs):
1. **GET**: Retrieve information (like reading a course).
2. **POST**: Create new information (like adding a course).
3. **PUT**: Update existing information (like marking a course as "Completed").
4. **DELETE**: Remove information (like deleting a course).

Every API request you send receives an **HTTP Status Code** telling you what happened:
* `200 OK`: Request succeeded.
* `201 Created`: Successfully created a new resource.
* `400 Bad Request`: The request had invalid data or was missing fields.
* `404 Not Found`: The resource you requested does not exist.
* `500 Internal Server Error`: Something went wrong on the server.

---

## ✨ Features

* **Complete CRUD REST API**: Create, Read, Update, and Delete courses.
* **No Database Required**: All data is stored in a clean, human-readable local `courses.json` file.
* **Auto-generated Fields**: Handles unique IDs and ISO 8601 timestamps (`created_at`) automatically.
* **Data Validation**: Enforces required fields, target date formatting (`YYYY-MM-DD`), and course status values (`Not Started`, `In Progress`, `Completed`).
* **Visual Frontend Dashboard**: Comes with a premium, responsive dark mode single-page dashboard built using Glassmorphic design principles to test and use your API instantly.

---

## 📁 Project Structure

```text
codecrafthub/
│
├── app.py              # The main Flask application (contains routes and logic)
├── requirements.txt    # Lists Python packages our project depends on (Flask)
├── courses.json        # Your local database file (automatically created at startup)
└── templates/
    └── index.html      # Frontend HTML/CSS/JS dashboard that interacts with the API
```

---

## 🛠️ Step-by-Step Installation Instructions

Follow these steps to set up the project on your computer:

### Step 1: Open a Terminal
Open your preferred terminal app (Command Prompt, PowerShell, Git Bash, or the VS Code terminal) and navigate to the directory where this project is saved:
```bash
cd path/to/codecrafthub
```

### Step 2: Set Up a Virtual Environment (Recommended)
A virtual environment keeps the project's dependencies isolated from the rest of your computer.
* **On Windows**:
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **On macOS/Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
*(Once activated, you will see `(.venv)` displayed at the start of your terminal line.)*

### Step 3: Install Dependencies
Install the required Flask framework using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

---

## ⚡ How to Run the Application

Start the Flask development server:
```bash
python app.py
```

If successful, you will see output like this in your terminal:
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Now, open your web browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

You will be greeted by the **CodeCraftHub Dashboard**!

---

## 🛣️ API Endpoints Documentation

All API responses are formatted in **JSON (JavaScript Object Notation)**.

### 1. Retrieve All Courses
* **Endpoint:** `GET /api/courses`
* **Description:** Returns an array of all courses currently saved.
* **Expected Response (`200 OK`):**
  ```json
  [
      {
          "id": 1,
          "name": "Learn Flask REST APIs",
          "description": "Master HTTP methods and JSON routing basics.",
          "target_date": "2026-08-30",
          "status": "In Progress",
          "created_at": "2026-07-08T18:30:15Z"
      }
  ]
  ```

### 2. Retrieve a Specific Course
* **Endpoint:** `GET /api/courses/<id>`
* **Description:** Retrieves details of a single course by its unique ID.
* **Expected Response (`200 OK`):**
  ```json
  {
      "id": 1,
      "name": "Learn Flask REST APIs",
      "description": "Master HTTP methods and JSON routing basics.",
      "target_date": "2026-08-30",
      "status": "In Progress",
      "created_at": "2026-07-08T18:30:15Z"
  }
  ```

### 3. Add a New Course
* **Endpoint:** `POST /api/courses`
* **Description:** Creates a new course. The `id` and `created_at` fields are generated automatically.
* **Example JSON Request Body:**
  ```json
  {
      "name": "Master Git & GitHub",
      "description": "Learn how to collaborate using Git branch structures.",
      "target_date": "2026-09-15",
      "status": "Not Started"
  }
  ```
* **Expected Response (`201 Created`):**
  ```json
  {
      "id": 2,
      "name": "Master Git & GitHub",
      "description": "Learn how to collaborate using Git branch structures.",
      "target_date": "2026-09-15",
      "status": "Not Started",
      "created_at": "2026-07-08T18:32:00Z"
  }
  ```

### 4. Update an Existing Course
* **Endpoint:** `PUT /api/courses/<id>`
* **Description:** Updates specific details of a course. Send only the fields you want to update.
* **Example JSON Request Body:**
  ```json
  {
      "status": "Completed",
      "target_date": "2026-09-10"
  }
  ```
* **Expected Response (`200 OK`):**
  ```json
  {
      "id": 2,
      "name": "Master Git & GitHub",
      "description": "Learn how to collaborate using Git branch structures.",
      "target_date": "2026-09-10",
      "status": "Completed",
      "created_at": "2026-07-08T18:32:00Z"
  }
  ```

### 5. Delete a Course
* **Endpoint:** `DELETE /api/courses/<id>`
* **Description:** Permanently deletes a course.
* **Expected Response (`200 OK`):**
  ```json
  {
      "message": "Course with ID 2 deleted successfully."
  }
  ```

---

## 🧪 Testing the API Using curl

Open a new terminal window to run these tests while your Flask app is running.

> [!IMPORTANT]
> **Windows PowerShell Users:** 
> 1. By default, `curl` in PowerShell is an alias for the native command `Invoke-WebRequest`, which does not accept `-X` or `-d` parameters. To run curl, you must use **`curl.exe`** instead.
> 2. The backslash (`\`) is not used for line continuation in PowerShell. Use the **backtick (`` ` ``)** instead, or run the command on a single line.
> 3. Single quotes are treated differently; you should escape double quotes inside your JSON body.


### Test Case 1: Create a Course (POST)
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
     -H "Content-Type: application/json" \
     -d "{\"name\": \"Learn Docker Basics\", \"description\": \"Understand container virtualization.\", \"target_date\": \"2026-10-01\", \"status\": \"Not Started\"}"
```

### Test Case 2: Update Course Status (PUT)
```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
     -H "Content-Type: application/json" \
     -d "{\"status\": \"In Progress\"}"
```

### Test Case 3: Error Test - Missing Fields (POST)
*Should fail because description is missing.*
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
     -H "Content-Type: application/json" \
     -d "{\"name\": \"Incomplete Course\", \"target_date\": \"2026-10-01\", \"status\": \"Not Started\"}"
```
*Expected Error response:* `{"error": "Missing required fields: description"}`

### Test Case 4: Error Test - Invalid Status (POST)
*Should fail because 'Finished' is not a valid status option.*
```bash
curl -X POST http://127.0.0.1:5000/api/courses \
     -H "Content-Type: application/json" \
     -d "{\"name\": \"Docker Basics\", \"description\": \"Containers\", \"target_date\": \"2026-10-01\", \"status\": \"Finished\"}"
```
*Expected Error response:* `{"error": "Invalid status: 'Finished'. Must be one of: Not Started, In Progress, Completed"}`

---

## 🔍 Troubleshooting Common Issues

### 1. `Address already in use` or `Port 5000 is occupied`
This happens when another service or previous Flask instance is already running on port 5000.
* **Solution**: You can change the port in [app.py](file:///e:/CODES/codecrafthub/app.py) on line 214:
  ```python
  app.run(debug=True, port=5001)  # Change 5000 to 5001 or any free port
  ```

### 2. `JSONDecodeError` or server crash on startup
This happens if the `courses.json` database file gets corrupted or holds invalid JSON content.
* **Solution**: Simply delete the `courses.json` file. The server will recreate a fresh, empty database containing `[]` automatically when it starts.

### 3. Command `pip` or `python` not found
This occurs when Python is not added to your system's PATH environment variables.
* **Solution**: On Windows, check "Add Python to PATH" when installing Python. Otherwise, try using `py` or `python3` instead of `python` in your terminal commands.

### 4. `ModuleNotFoundError: No module named 'flask'`
This means Flask was installed in a environment that is not currently active.
* **Solution**: Make sure you have activated your virtual environment (Step 2 of installation) before running `pip install` and starting the app.
