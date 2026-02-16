
import subprocess
import pyautogui
import time
from datetime import datetime

def ai_dj_mode_enhanced(command=""):
    try:
        if not command:
            return start_dj_session()
        
        command_lower = command.lower()
        if "party" in command_lower or "upbeat" in command_lower:
            return dj_party_mode()
        elif "chill" in command_lower or "relax" in command_lower:
            return dj_chill_mode()
        elif "focus" in command_lower or "work" in command_lower:
            return dj_focus_mode()
        elif "stop" in command_lower or "off" in command_lower:
            return stop_dj_session()
        else:
            return ai_music_selection(command)
    except Exception as e:
        return f"DJ mode error: {str(e)}"

def start_dj_session():
    try:
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 12:
            return dj_focus_mode()
        elif 13 <= current_hour <= 18:
            return dj_auto_mode()
        elif 19 <= current_hour <= 23:
            return dj_party_mode()
        else:
            return dj_chill_mode()
    except Exception as e:
        return f"DJ session error: {str(e)}"

def dj_party_mode():
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)  # Search box
        time.sleep(1)
        pyautogui.typewrite('party music mix 2024')
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)  # First video
        time.sleep(2)
        return "AI DJ: Party mode activated! Playing YouTube party mix"
    except Exception as e:
        return f"Party mode error: {str(e)}"

def dj_chill_mode():
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite('lofi hip hop study chill music')
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return "AI DJ: Chill mode activated! Playing YouTube lofi mix"
    except Exception as e:
        return f"Chill mode error: {str(e)}"

def dj_focus_mode():
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite('focus music instrumental ambient study')
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return "AI DJ: Focus mode activated! Playing YouTube focus music"
    except Exception as e:
        return f"Focus mode error: {str(e)}"

def dj_auto_mode():
    try:
        playlists = ['top hits 2024', 'pop music mix', 'rock classics', 'indie music', 'electronic dance']
        import random
        playlist = random.choice(playlists)
        
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite(playlist)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return f"AI DJ: Auto mode activated! Playing YouTube {playlist}"
    except Exception as e:
        return f"Auto mode error: {str(e)}"

def ai_music_selection(request):
    try:
        subprocess.run('start chrome https://www.youtube.com', shell=True)
        time.sleep(3)
        pyautogui.click(640, 100)
        time.sleep(1)
        pyautogui.typewrite(request[:50])
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.click(320, 300)
        time.sleep(2)
        return f"AI DJ: Playing YouTube {request}"
    except Exception as e:
        return f"Music selection error: {str(e)}"

def stop_dj_session():
    try:
        pyautogui.press('space')
        return "AI DJ: Session ended. Music paused."
    except Exception as e:
        return f"Stop DJ error: {str(e)}"
def try_all_ai_providers(prompt, system_prompt="", messages=None):
    """Try Groq -> Gemini -> Ollama in order"""
    
    # Try Groq first
    try:
        from engine.dual_ai import dual_ai
        if hasattr(dual_ai, 'groq_client'):
            response = dual_ai.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages or [{"role": "user", "content": prompt}],
                temperature=0.4
            )
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq failed: {e}")
    
    # Try Gemini second
    try:
        from engine.dual_ai import dual_ai
        if hasattr(dual_ai, 'gemini_model'):
            response = dual_ai.gemini_model.generate_content(prompt)
            return response.text.strip()
    except Exception as e:
        print(f"Gemini failed: {e}")
    
 
    # All failed
    return None
import threading
import time
import numpy as np

class AmbientAwareness:
    def __init__(self):
        self.active = False
        self.thread = None
        
    def start(self):
        """Start ambient sound detection"""
        if self.active:
            return "Ambient awareness already running"
        
        try:
            import pyaudio
            
            self.active = True
            
            def listen_background():
                try:
                    # Audio config
                    CHUNK = 1024
                    FORMAT = pyaudio.paInt16
                    CHANNELS = 1
                    RATE = 44100
                    THRESHOLD = 5  # Very low threshold for sensitive detection
                    
                    p = pyaudio.PyAudio()
                    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                                  input=True, frames_per_buffer=CHUNK)
                    
                    doorbell_count = 0
                    alarm_count = 0
                    crying_count = 0
                    
                    while self.active:
                        try:
                            data = stream.read(CHUNK, exception_on_overflow=False)
                            audio_data = np.frombuffer(data, dtype=np.int16)
                            # Fix volume calculation
                            mean_square = np.mean(audio_data.astype(np.float64)**2)
                            volume = np.sqrt(max(0, mean_square)) if mean_square > 0 else 0
                            
                            if volume > THRESHOLD:
                                high_freq = np.mean(np.abs(audio_data[audio_data > np.mean(audio_data)]))
                                
                                # Doorbell (short, high-pitched)
                                if high_freq > 50 and volume > 20:
                                    doorbell_count += 1
                                    if doorbell_count >= 3:
                                        self._alert("Doorbell detected! Someone is at the door.")
                                        doorbell_count = 0
                                        time.sleep(5)
                                
                                # Alarm (sustained loud)
                                elif volume > 30:
                                    alarm_count += 1
                                    if alarm_count >= 5:
                                        self._alert("Alarm detected! Please check for emergencies.")
                                        alarm_count = 0
                                        time.sleep(10)
                                
                                # Baby crying (variable pitch)
                                elif 20 < high_freq < 100 and volume > 15:
                                    crying_count += 1
                                    if crying_count >= 5:
                                        self._alert("Baby crying detected! The baby may need attention.")
                                        crying_count = 0
                                        time.sleep(15)
                                
                                # General sound detection
                                elif volume > 10:
                                    print(f"Sound: Vol={volume:.1f}, Freq={high_freq:.1f}")
                            
                            # Reset counters gradually
                            if volume < THRESHOLD:
                                doorbell_count = max(0, doorbell_count - 1)
                                alarm_count = max(0, alarm_count - 1)
                                crying_count = max(0, crying_count - 1)
                            
                            # Debug output for testing
                            if volume > 2:
                                print(f"Audio: {volume:.1f}", end=" ", flush=True)
                            
                            time.sleep(0.1)
                            
                        except Exception as e:
                            continue
                    
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    
                except Exception as e:
                    self.active = False
            
            self.thread = threading.Thread(target=listen_background, daemon=True)
            self.thread.start()
            
            return "Ambient awareness started - listening for doorbell, alarms, baby crying"
            
        except ImportError:
            return "PyAudio not installed. Run: pip install pyaudio numpy"
        except Exception as e:
            return f"Failed to start: {str(e)}"
    
    def stop(self):
        """Stop ambient detection"""
        self.active = False
        if self.thread:
            self.thread.join(timeout=2)
        return "Ambient awareness stopped"
    
    def status(self):
        """Get status"""
        return f"Ambient awareness: {'Active' if self.active else 'Inactive'}"
    
    def _alert(self, message):
        """Alert user"""
        print(f"🔊 AMBIENT ALERT: {message}")
        
        try:
            from engine.features import speak
            speak(message)
        except:
            pass

# Global instance
ambient_awareness = AmbientAwareness()
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class AutoCodeArchitect:
    def __init__(self):
        self.desktop_path = Path.home() / "Desktop"
    
    def detect_request_type(self, query: str) -> Dict:
        query_lower = query.lower()
        
        language = self._detect_language(query_lower)
        project_type = self._detect_project_type(query_lower)
        project_name = self._extract_project_name(query)
        
        return {
            'language': language,
            'project_type': project_type,
            'project_name': project_name,
            'original_query': query
        }
    
    def _detect_language(self, query: str) -> str:
        query_lower = query.lower()
        if any(word in query_lower for word in ['python', 'flask', 'django', 'fastapi']):
            return 'python'
        elif any(word in query_lower for word in ['javascript', 'js', 'node', 'react', 'vue', 'angular']):
            return 'javascript'
        elif any(word in query_lower for word in ['java', 'spring']):
            return 'java'
        elif any(word in query_lower for word in ['c#', 'csharp', '.net']):
            return 'csharp'
        elif any(word in query_lower for word in ['php', 'laravel']):
            return 'php'
        elif any(word in query_lower for word in ['html', 'css', 'static']):
            return 'html'
        else:
            return 'python'
    
    def _detect_project_type(self, query: str) -> str:
        query_lower = query.lower()
        if any(phrase in query_lower for phrase in ['only html', 'html and css', 'static', 'frontend only']):
            return 'static'
        elif any(word in query_lower for word in ['react', 'vue', 'angular']):
            return 'spa'
        elif any(word in query_lower for word in ['api', 'rest', 'microservice']):
            return 'api'
        elif any(word in query_lower for word in ['desktop', 'gui', 'tkinter', 'electron']):
            return 'desktop'
        elif any(word in query_lower for word in ['mobile', 'android', 'ios']):
            return 'mobile'
        else:
            return 'web'
    
    def _extract_project_name(self, query: str) -> str:
        # Extract everything after 'generate code' or similar commands
        patterns = [
            r'generate\s+code\s+(.+?)(?:\s+using|\s+with|\s+in|$)',
            r'create\s+(?:a\s+)?(.+?)(?:\s+using|\s+with|\s+in|$)',
            r'build\s+(?:a\s+)?(.+?)(?:\s+using|\s+with|\s+in|$)',
            r'make\s+(?:a\s+)?(.+?)(?:\s+using|\s+with|\s+in|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Clean up the name
                name = re.sub(r'\b(app|application|project|system)\b', '', name, flags=re.IGNORECASE).strip()
                # Convert to title case and remove spaces
                name = ''.join(word.capitalize() for word in name.split())
                if name and len(name) > 2:
                    return name[:20] + 'App'
        
        # If no pattern matches, use the whole query after 'generate code'
        if 'generate code' in query.lower():
            name = query.lower().replace('generate code', '').strip()
            name = ''.join(word.capitalize() for word in name.split())
            if name:
                return name[:20] + 'App'
        
        return 'JarvisProject'
    
    def generate_code(self, request_info: Dict) -> Dict:
        return self._generate_project(request_info)
    
    def _generate_project(self, request_info: Dict) -> Dict:
        language = request_info['language']
        project_type = request_info['project_type']
        project_name = request_info['project_name']
        
        files = self._generate_project_files(request_info)
        
        return {
            'type': 'project',
            'project_name': project_name,
            'files': files,
            'language': language,
            'project_type': project_type
        }
    
    def _generate_project_files(self, request_info: Dict) -> Dict:
        files = {}
        language = request_info['language']
        project_type = request_info['project_type']
        project_name = request_info['project_name']
        
        files['README.md'] = self._generate_readme(project_name, project_type, language)
        
        if project_type == 'static' or language == 'html':
            files['index.html'] = self._generate_static_html(project_name, request_info['original_query'])
            files['style.css'] = self._generate_static_css()
            files['script.js'] = self._generate_static_js(project_name)
        elif language == 'javascript':
            files['server.js'] = self._generate_main_code(request_info)
            files['package.json'] = self._generate_package_json(project_name)
            if project_type != 'api':
                files['public/index.html'] = self._generate_html_template(project_name, request_info['original_query'])
                files['public/style.css'] = self._generate_css_styles()
        elif language == 'java':
            files['Main.java'] = self._generate_main_code(request_info)
            files['pom.xml'] = self._generate_maven_pom(project_name)
        elif language == 'csharp':
            files['Program.cs'] = self._generate_main_code(request_info)
            files[f'{project_name}.csproj'] = self._generate_csproj(project_name)
        elif language == 'php':
            files['index.php'] = self._generate_main_code(request_info)
            files['composer.json'] = self._generate_composer_json(project_name)
        elif language == 'python':
            files['app.py'] = self._generate_main_code(request_info)
            files['requirements.txt'] = self._generate_requirements(project_type)
            if project_type == 'web':
                files['templates/index.html'] = self._generate_html_template(project_name, request_info['original_query'])
                files['static/style.css'] = self._generate_css_styles()
        else:
            files['app.py'] = self._generate_main_code(request_info)
        
        return files
    
    def _generate_main_code(self, request_info: Dict) -> str:
        language = request_info['language']
        project_type = request_info['project_type']
        project_name = request_info['project_name']
        query = request_info['original_query']
        
        if language == 'python':
            return self._generate_python_code(project_name, query, project_type)
        elif language == 'javascript':
            return self._generate_javascript_code(project_name, query, project_type)
        elif language == 'java':
            return self._generate_java_code(project_name, query, project_type)
        elif language == 'csharp':
            return self._generate_csharp_code(project_name, query, project_type)
        elif language == 'php':
            return self._generate_php_code(project_name, query, project_type)
        else:
            return self._generate_python_code(project_name, query, project_type)
    
    def _generate_python_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        return self._generate_advanced_python_app(project_name, query, project_type)
    
    def _python_flask_app(self, project_name: str, query: str = '') -> str:
        # Generate code based on project name/type
        query_and_name = (query + ' ' + project_name).lower()
        
        if 'calculator' in query_and_name:
            return '''from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']
        
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            result = num1 / num2 if num2 != 0 else "Cannot divide by zero"
        else:
            result = "Invalid operation"
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
'''
        elif 'library' in query.lower() and 'management' in query.lower():
            return '''from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = 'library_secret'

def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    # Create users table
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  role TEXT DEFAULT 'user',
                  name TEXT NOT NULL)""")
    
    # Create books table
    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  isbn TEXT UNIQUE,
                  category TEXT,
                  total_copies INTEGER DEFAULT 1,
                  available_copies INTEGER DEFAULT 1)""")
    
    # Create issued_books table
    c.execute("""CREATE TABLE IF NOT EXISTS issued_books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book_id INTEGER,
                  user_id INTEGER,
                  issue_date TEXT NOT NULL,
                  due_date TEXT NOT NULL,
                  return_date TEXT,
                  status TEXT DEFAULT 'issued')""")
    
    # Insert sample data
    c.execute("INSERT OR IGNORE INTO users (username, password, role, name) VALUES (?, ?, ?, ?)", 
              ('admin', 'admin123', 'admin', 'Administrator'))
    c.execute("INSERT OR IGNORE INTO users (username, password, role, name) VALUES (?, ?, ?, ?)", 
              ('user1', 'user123', 'user', 'John Doe'))
    c.execute("INSERT OR IGNORE INTO books (title, author, isbn, category, total_copies, available_copies) VALUES (?, ?, ?, ?, ?, ?)", 
              ('Python Programming', 'John Smith', '978-0123456789', 'Programming', 5, 5))
    
    conn.commit()
    conn.close()

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['role'] = user[3]
        return redirect('/dashboard')
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'title')
    query = 'SELECT * FROM books WHERE available_copies > 0'
    params = []
    if search:
        query += ' AND (title LIKE ? OR author LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    if sort_by in ['title', 'author', 'category']:
        query += f' ORDER BY {sort_by}'
    c.execute(query, params)
    books = c.fetchall()
    conn.close()
    return render_template('dashboard.html', books=books, search=search, sort_by=sort_by)

@app.route('/issue/<int:book_id>')
def issue_book(book_id):
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT available_copies FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    if book and book[0] > 0:
        issue_date = date.today().strftime('%Y-%m-%d')
        due_date = (date.today() + timedelta(days=14)).strftime('%Y-%m-%d')
        c.execute('INSERT INTO issued_books (book_id, user_id, issue_date, due_date) VALUES (?, ?, ?, ?)', 
                  (book_id, session['user_id'], issue_date, due_date))
        c.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id = ?', (book_id,))
        conn.commit()
    conn.close()
    return redirect('/dashboard')

@app.route('/return/<int:issue_id>')
def return_book(issue_id):
    if 'user_id' not in session:
        return redirect('/')
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT book_id FROM issued_books WHERE id = ? AND user_id = ?', (issue_id, session['user_id']))
    result = c.fetchone()
    if result:
        book_id = result[0]
        return_date = date.today().strftime('%Y-%m-%d')
        c.execute('UPDATE issued_books SET return_date = ?, status = "returned" WHERE id = ?', (return_date, issue_id))
        c.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id = ?', (book_id,))
        conn.commit()
    conn.close()
    return redirect('/dashboard')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
'''
        elif 'student' in query.lower() and 'management' in query.lower():
            return '''from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'student_secret'

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id TEXT UNIQUE,
                  name TEXT NOT NULL,
                  email TEXT,
                  course TEXT,
                  year INTEGER,
                  gpa REAL DEFAULT 0.0)""")
    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students ORDER BY name')
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (student_id, name, email, course, year, gpa) VALUES (?, ?, ?, ?, ?, ?)',
             (request.form['student_id'], request.form['name'], request.form['email'],
              request.form['course'], int(request.form['year']), float(request.form['gpa'])))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
'''
        elif 'todo' in query.lower():
            return '''from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  priority TEXT DEFAULT 'medium',
                  status TEXT DEFAULT 'pending',
                  created_date TEXT)""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY priority DESC')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title, description, priority, created_date) VALUES (?, ?, ?, ?)',
             (request.form['title'], request.form['description'], 
              request.form['priority'], datetime.now().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
'''
        else:
            # Generate advanced Flask app based on detailed user requirements
            return self._generate_advanced_flask_app(project_name, query)
    
    def _generate_html_template(self, project_name: str, query: str = '') -> str:
        if 'calculator' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Calculator App</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="calculator">
        <h1>Calculator</h1>
        <div class="display">
            <input type="text" id="result" readonly>
        </div>
        <div class="buttons">
            <button onclick="clearDisplay()">C</button>
            <button onclick="appendToDisplay('/')">/</button>
            <button onclick="appendToDisplay('*')">*</button>
            <button onclick="deleteLast()">←</button>
            
            <button onclick="appendToDisplay('7')">7</button>
            <button onclick="appendToDisplay('8')">8</button>
            <button onclick="appendToDisplay('9')">9</button>
            <button onclick="appendToDisplay('-')">-</button>
            
            <button onclick="appendToDisplay('4')">4</button>
            <button onclick="appendToDisplay('5')">5</button>
            <button onclick="appendToDisplay('6')">6</button>
            <button onclick="appendToDisplay('+')">+</button>
            
            <button onclick="appendToDisplay('1')">1</button>
            <button onclick="appendToDisplay('2')">2</button>
            <button onclick="appendToDisplay('3')">3</button>
            <button onclick="calculate()" rowspan="2">=</button>
            
            <button onclick="appendToDisplay('0')" colspan="2">0</button>
            <button onclick="appendToDisplay('.')">,</button>
        </div>
    </div>
    
    <script>
        let display = document.getElementById('result');
        
        function appendToDisplay(value) {
            display.value += value;
        }
        
        function clearDisplay() {
            display.value = '';
        }
        
        function deleteLast() {
            display.value = display.value.slice(0, -1);
        }
        
        function calculate() {
            try {
                display.value = eval(display.value);
            } catch (error) {
                display.value = 'Error';
            }
        }
    </script>
</body>
</html>'''
        elif 'library' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Library Management System</title>
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div class="login-container">
        <div class="login-card">
            <h1>Library Management System</h1>
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="btn-primary">Login</button>
            </form>
            <div class="demo-info">
                <p>Demo Accounts:</p>
                <p>Admin: admin / admin123</p>
                <p>User: user1 / user123</p>
            </div>
        </div>
    </div>
</body>
</html>'''
        elif 'student' in query.lower() and 'management' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Student Management System</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Student Management System</h1>
        
        <div class="add-student">
            <h2>Add New Student</h2>
            <form method="POST" action="/add">
                <input type="text" name="student_id" placeholder="Student ID" required>
                <input type="text" name="name" placeholder="Full Name" required>
                <input type="email" name="email" placeholder="Email">
                <input type="text" name="course" placeholder="Course" required>
                <input type="number" name="year" placeholder="Year" min="1" max="4" required>
                <input type="number" name="gpa" placeholder="GPA" step="0.01" min="0" max="4">
                <button type="submit">Add Student</button>
            </form>
        </div>
        
        <div class="students-list">
            <h2>Students List</h2>
            <table>
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Course</th>
                        <th>Year</th>
                        <th>GPA</th>
                    </tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student[1] }}</td>
                        <td>{{ student[2] }}</td>
                        <td>{{ student[3] }}</td>
                        <td>{{ student[4] }}</td>
                        <td>{{ student[5] }}</td>
                        <td>{{ student[6] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''
        elif 'todo' in query.lower():
            return '''<!DOCTYPE html>
<html>
<head>
    <title>Todo List Manager</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Todo List Manager</h1>
        
        <div class="add-task">
            <h2>Add New Task</h2>
            <form method="POST" action="/add">
                <input type="text" name="title" placeholder="Task Title" required>
                <textarea name="description" placeholder="Description"></textarea>
                <select name="priority">
                    <option value="low">Low Priority</option>
                    <option value="medium" selected>Medium Priority</option>
                    <option value="high">High Priority</option>
                </select>
                <button type="submit">Add Task</button>
            </form>
        </div>
        
        <div class="tasks-list">
            <h2>Tasks</h2>
            {% for task in tasks %}
            <div class="task priority-{{ task[3] }}">
                <h3>{{ task[1] }}</h3>
                <p>{{ task[2] }}</p>
                <span class="priority">{{ task[3].title() }} Priority</span>
                <span class="status">{{ task[4].title() }}</span>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>'''
        else:
            return f'''<!DOCTYPE html>
<html>
<head>
    <title>{{{{ app_name }}}}</title>
    <link rel="stylesheet" href="/static/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div class="container">
        <header>
            <h1>{{{{ app_name }}}}</h1>
            <p>Complete Management System</p>
        </header>
        
        <div class="add-section">
            <h2>Add New Item</h2>
            <form method="POST" action="/add" class="add-form">
                <input type="text" name="name" placeholder="Name" required>
                <textarea name="description" placeholder="Description"></textarea>
                <input type="text" name="category" placeholder="Category">
                <button type="submit" class="btn-primary">Add Item</button>
            </form>
        </div>
        
        <div class="items-section">
            <h2>Items List</h2>
            <div class="items-grid">
                {{% for item in items %}}
                <div class="item-card">
                    <h3>{{{{ item[1] }}}}</h3>
                    <p>{{{{ item[2] or 'No description' }}}}</p>
                    <div class="item-meta">
                        <span class="category">{{{{ item[3] }}}}</span>
                        <span class="date">{{{{ item[5] }}}}</span>
                    </div>
                    <div class="item-actions">
                        <a href="/delete/{{{{ item[0] }}}}" class="btn-delete" onclick="return confirm('Delete this item?')">Delete</a>
                    </div>
                </div>
                {{% endfor %}}
            </div>
            
            {{% if not items %}}
            <div class="empty-state">
                <p>No items found. Add your first item above!</p>
            </div>
            {{% endif %}}
        </div>
    </div>
    
    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('{{{{ app_name }}}} loaded successfully!');
        }});
    </script>
</body>
</html>'''
    
    def _generate_dashboard_template(self) -> str:
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Library Dashboard</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="dashboard">
        <div class="sidebar">
            <h2>Library System</h2>
            <nav>
                <a href="/dashboard">Books</a>
                <a href="/my-books">My Books</a>
                <a href="/logout">Logout</a>
            </nav>
        </div>
        <div class="main-content">
            <div class="search-bar">
                <form method="GET">
                    <input type="text" name="search" placeholder="Search books..." value="{{ search }}">
                    <select name="sort">
                        <option value="title" {% if sort_by == 'title' %}selected{% endif %}>Title</option>
                        <option value="author" {% if sort_by == 'author' %}selected{% endif %}>Author</option>
                        <option value="category" {% if sort_by == 'category' %}selected{% endif %}>Category</option>
                    </select>
                    <button type="submit">Search</button>
                </form>
            </div>
            <div class="books-grid">
                {% for book in books %}
                <div class="book-card">
                    <h3>{{ book[1] }}</h3>
                    <p>Author: {{ book[2] }}</p>
                    <p>Category: {{ book[4] }}</p>
                    <p>Available: {{ book[6] }}/{{ book[5] }}</p>
                    <a href="/issue/{{ book[0] }}" class="btn-issue">Issue Book</a>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    def _generate_css_styles(self) -> str:
        return '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
}

.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.login-card {
    background: white;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    width: 300px;
}

.login-card h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

.login-card input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.btn-primary {
    width: 100%;
    padding: 12px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.btn-primary:hover {
    background-color: #0056b3;
}

.demo-info {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 4px;
    font-size: 14px;
}

.dashboard {
    display: flex;
    height: 100vh;
}

.sidebar {
    width: 250px;
    background-color: #343a40;
    color: white;
    padding: 20px;
}

.sidebar h2 {
    margin-bottom: 30px;
}

.sidebar nav a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 10px 0;
    border-bottom: 1px solid #495057;
}

.sidebar nav a:hover {
    background-color: #495057;
    padding-left: 10px;
}

.main-content {
    flex: 1;
    padding: 20px;
}

.search-bar {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-bar form {
    display: flex;
    gap: 10px;
    align-items: center;
}

.search-bar input, .search-bar select {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.search-bar button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.books-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.book-card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-card h3 {
    margin-top: 0;
    color: #333;
}

.btn-issue {
    display: inline-block;
    padding: 8px 16px;
    background-color: #28a745;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    margin-top: 10px;
}

.btn-issue:hover {
    background-color: #218838;
}'''
    
    def _generate_readme(self, project_name: str, project_type: str, language: str) -> str:
        return f'''# {project_name}

Generated by Jarvis Auto Code Architect

## Description
A {project_type} application built with {language.title()}.

## Installation

### Requirements
- {language.title()} (latest version recommended)

### Setup
1. Clone or download this project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the main application:
```bash
python app.py
```

## Features
- Modern {project_type} interface
- Cross-platform compatibility
- Easy to extend and customize

## Generated by
Jarvis AI Assistant - Auto Code Architect
'''
    
    def _generate_static_html(self, project_name: str, query: str = '') -> str:
        """Generate advanced static HTML based on user requirements"""
        query_lower = query.lower()
        features = self._analyze_requirements(query_lower)
        
        # Determine project type
        if 'portfolio' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        elif 'ecommerce' in query_lower or 'shop' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        elif 'blog' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        elif 'landing' in query_lower:
            return self._generate_portfolio_html(project_name, features)
        else:
            return self._generate_portfolio_html(project_name, features)
    
    def _generate_portfolio_html(self, project_name: str, features: dict) -> str:
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <h2>Portfolio</h2>
            </div>
            <div class="nav-menu" id="nav-menu">
                <a href="#home" class="nav-link">Home</a>
                <a href="#about" class="nav-link">About</a>
                <a href="#skills" class="nav-link">Skills</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#contact" class="nav-link">Contact</a>
                {"<button class='theme-toggle' id='theme-toggle'><i class='fas fa-moon'></i></button>" if features['responsive'] else ""}
            </div>
            <div class="nav-toggle" id="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <h1 class="hero-title">Hi, I'm <span class="highlight">John Doe</span></h1>
                <p class="hero-subtitle">Full Stack Developer & UI/UX Designer</p>
                <p class="hero-description">I create amazing digital experiences that make people's lives easier.</p>
                <div class="hero-buttons">
                    <a href="#projects" class="btn btn-primary">View My Work</a>
                    <a href="#contact" class="btn btn-secondary">Get In Touch</a>
                </div>
            </div>
            <div class="hero-image">
                <div class="image-placeholder">
                    <i class="fas fa-user-circle"></i>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>I'm a passionate developer with 5+ years of experience creating web applications and user interfaces. I love turning complex problems into simple, beautiful designs.</p>
                    <div class="stats">
                        <div class="stat">
                            <h3>50+</h3>
                            <p>Projects Completed</p>
                        </div>
                        <div class="stat">
                            <h3>5+</h3>
                            <p>Years Experience</p>
                        </div>
                        <div class="stat">
                            <h3>100+</h3>
                            <p>Happy Clients</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Skills Section -->
    <section id="skills" class="skills">
        <div class="container">
            <h2 class="section-title">Skills & Technologies</h2>
            <div class="skills-grid">
                <div class="skill-card">
                    <i class="fab fa-html5"></i>
                    <h3>Frontend</h3>
                    <p>HTML5, CSS3, JavaScript, React, Vue.js</p>
                </div>
                <div class="skill-card">
                    <i class="fas fa-server"></i>
                    <h3>Backend</h3>
                    <p>Node.js, Python, PHP, Java, .NET</p>
                </div>
                <div class="skill-card">
                    <i class="fas fa-database"></i>
                    <h3>Database</h3>
                    <p>MySQL, PostgreSQL, MongoDB, SQLite</p>
                </div>
                <div class="skill-card">
                    <i class="fas fa-tools"></i>
                    <h3>Tools</h3>
                    <p>Git, Docker, AWS, Figma, Photoshop</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Projects Section -->
    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">Featured Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">
                        <div class="image-placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="project-overlay">
                            <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3>E-Commerce Platform</h3>
                        <p>Full-stack e-commerce solution with React and Node.js</p>
                        <div class="project-tech">
                            <span>React</span>
                            <span>Node.js</span>
                            <span>MongoDB</span>
                        </div>
                    </div>
                </div>
                
                <div class="project-card">
                    <div class="project-image">
                        <div class="image-placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="project-overlay">
                            <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3>Task Management App</h3>
                        <p>Collaborative task management with real-time updates</p>
                        <div class="project-tech">
                            <span>Vue.js</span>
                            <span>Firebase</span>
                            <span>CSS3</span>
                        </div>
                    </div>
                </div>
                
                <div class="project-card">
                    <div class="project-image">
                        <div class="image-placeholder">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="project-overlay">
                            <a href="#" class="project-link"><i class="fas fa-external-link-alt"></i></a>
                            <a href="#" class="project-link"><i class="fab fa-github"></i></a>
                        </div>
                    </div>
                    <div class="project-content">
                        <h3>Weather Dashboard</h3>
                        <p>Beautiful weather app with location-based forecasts</p>
                        <div class="project-tech">
                            <span>JavaScript</span>
                            <span>API</span>
                            <span>Chart.js</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <div>
                            <h3>Email</h3>
                            <p>john.doe@example.com</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <div>
                            <h3>Phone</h3>
                            <p>+1 (555) 123-4567</p>
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <div>
                            <h3>Location</h3>
                            <p>New York, NY</p>
                        </div>
                    </div>
                </div>
                
                <form class="contact-form" id="contact-form">
                    <div class="form-group">
                        <input type="text" id="name" name="name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" id="email" name="email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <input type="text" id="subject" name="subject" placeholder="Subject" required>
                    </div>
                    <div class="form-group">
                        <textarea id="message" name="message" placeholder="Your Message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2024 John Doe. All rights reserved.</p>
                <div class="social-links">
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                    <a href="#"><i class="fab fa-github"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
        </div>
    </footer>
        
        <div class="add-section">
            <h2>Add New Item</h2>
            <form id="addForm" class="add-form">
                <input type="text" id="itemName" placeholder="Item Name" required>
                <input type="text" id="itemCategory" placeholder="Category">
                <input type="number" id="itemQuantity" placeholder="Quantity" min="0">
                <input type="number" id="itemPrice" placeholder="Price" step="0.01" min="0">
                <textarea id="itemDescription" placeholder="Description"></textarea>
                <button type="submit" class="btn-primary">Add Item</button>
            </form>
        </div>
        
        <div class="items-section">
            <h2>Items List</h2>
            <div class="search-bar">
                <input type="text" id="searchInput" placeholder="Search items...">
                <select id="categoryFilter">
                    <option value="">All Categories</option>
                </select>
            </div>
            <div id="itemsList" class="items-grid">
                <!-- Items will be populated by JavaScript -->
            </div>
            <div id="emptyState" class="empty-state">
                <p>No items found. Add your first item above!</p>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _generate_static_css(self) -> str:
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 15px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    overflow: hidden;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 40px;
    text-align: center;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

.add-section {
    padding: 40px;
    background: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
}

.add-section h2 {
    margin-bottom: 20px;
    color: #333;
}

.add-form {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    align-items: end;
}

.add-form input,
.add-form textarea,
.add-form select {
    padding: 12px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s;
}

.add-form input:focus,
.add-form textarea:focus {
    outline: none;
    border-color: #667eea;
}

.add-form textarea {
    grid-column: 1 / -1;
    resize: vertical;
    min-height: 80px;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: transform 0.2s;
}

.btn-primary:hover {
    transform: translateY(-2px);
}

.items-section {
    padding: 40px;
}

.items-section h2 {
    margin-bottom: 20px;
    color: #333;
}

.search-bar {
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
}

.search-bar input,
.search-bar select {
    padding: 10px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 14px;
}

.search-bar input {
    flex: 1;
}

.items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.item-card {
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    padding: 20px;
    transition: all 0.3s;
    position: relative;
}

.item-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    border-color: #667eea;
}

.item-card h3 {
    color: #333;
    margin-bottom: 10px;
    font-size: 1.3rem;
}

.item-card p {
    color: #666;
    margin-bottom: 15px;
    line-height: 1.5;
}

.item-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.category {
    background: #667eea;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.quantity {
    background: #28a745;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.price {
    background: #ffc107;
    color: #333;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}

.item-actions {
    display: flex;
    gap: 10px;
}

.btn-delete {
    background: #dc3545;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    text-decoration: none;
    transition: background 0.2s;
}

.btn-delete:hover {
    background: #c82333;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #666;
    font-size: 1.1rem;
}

@media (max-width: 768px) {
    .add-form {
        grid-template-columns: 1fr;
    }
    
    .search-bar {
        flex-direction: column;
    }
    
    .items-grid {
        grid-template-columns: 1fr;
    }
}'''
    
    def _generate_javascript_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        return self._generate_advanced_javascript_app(project_name, query, project_type)
    
    def _generate_java_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        return self._generate_advanced_java_app(project_name, query, project_type)
    
    def _generate_spring_boot(self, project_name: str, query: str = '') -> str:
        class_name = project_name.replace('App', '').replace(' ', '')
        return f'''package com.jarvis.{class_name.lower()};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Service;
import java.util.*;
import java.time.LocalDateTime;

@SpringBootApplication
public class {class_name}Application {{
    public static void main(String[] args) {{
        SpringApplication.run({class_name}Application.class, args);
    }}
}}

@RestController
@RequestMapping("/api")
class {class_name}Controller {{
    private final {class_name}Service service;
    
    public {class_name}Controller({class_name}Service service) {{
        this.service = service;
    }}
    
    @GetMapping("/items")
    public List<Item> getAllItems() {{
        return service.getAllItems();
    }}
    
    @PostMapping("/items")
    public Item createItem(@RequestBody Item item) {{
        return service.createItem(item);
    }}
    
    @DeleteMapping("/items/{{id}}")
    public void deleteItem(@PathVariable Long id) {{
        service.deleteItem(id);
    }}
}}

@Service
class {class_name}Service {{
    private List<Item> items = new ArrayList<>();
    private Long nextId = 1L;
    
    public List<Item> getAllItems() {{
        return items;
    }}
    
    public Item createItem(Item item) {{
        item.setId(nextId++);
        item.setCreatedAt(LocalDateTime.now());
        items.add(item);
        return item;
    }}
    
    public void deleteItem(Long id) {{
        items.removeIf(item -> item.getId().equals(id));
    }}
}}

class Item {{
    private Long id;
    private String name;
    private String description;
    private String category;
    private LocalDateTime createdAt;
    
    // Constructors
    public Item() {{}}
    
    public Item(String name, String description, String category) {{
        this.name = name;
        this.description = description;
        this.category = category;
    }}
    
    // Getters and Setters
    public Long getId() {{ return id; }}
    public void setId(Long id) {{ this.id = id; }}
    
    public String getName() {{ return name; }}
    public void setName(String name) {{ this.name = name; }}
    
    public String getDescription() {{ return description; }}
    public void setDescription(String description) {{ this.description = description; }}
    
    public String getCategory() {{ return category; }}
    public void setCategory(String category) {{ this.category = category; }}
    
    public LocalDateTime getCreatedAt() {{ return createdAt; }}
    public void setCreatedAt(LocalDateTime createdAt) {{ this.createdAt = createdAt; }}
}}'''
    
    def _generate_advanced_flask_app(self, project_name: str, query: str = '') -> str:
        """Generate advanced Flask app based on user requirements"""
        query_lower = query.lower()
        
        # Analyze requirements
        has_auth = any(word in query_lower for word in ['login', 'register', 'user', 'auth', 'account'])
        has_charts = any(word in query_lower for word in ['chart', 'graph', 'visualization', 'analytics'])
        has_api = any(word in query_lower for word in ['api', 'rest', 'json'])
        has_file_upload = any(word in query_lower for word in ['upload', 'file', 'image'])
        has_email = any(word in query_lower for word in ['email', 'notification', 'mail'])
        has_search = any(word in query_lower for word in ['search', 'filter', 'find'])
        has_export = any(word in query_lower for word in ['export', 'pdf', 'csv', 'download'])
        
        # Determine database schema based on context
        if 'expense' in query_lower or 'finance' in query_lower:
            db_schema = self._get_expense_schema()
            routes = self._get_expense_routes()
        elif 'inventory' in query_lower or 'stock' in query_lower:
            db_schema = self._get_inventory_schema()
            routes = self._get_inventory_routes()
        elif 'student' in query_lower or 'school' in query_lower:
            db_schema = self._get_student_schema()
            routes = self._get_student_routes()
        elif 'employee' in query_lower or 'hr' in query_lower:
            db_schema = self._get_employee_schema()
            routes = self._get_employee_routes()
        else:
            db_schema = self._get_generic_schema()
            routes = self._get_generic_routes()
        
        # Generate imports based on features
        imports = ['from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session']
        imports.append('import sqlite3')
        imports.append('from datetime import datetime, date')
        imports.append('import os')
        
        if has_auth:
            imports.append('from werkzeug.security import generate_password_hash, check_password_hash')
        if has_file_upload:
            imports.append('from werkzeug.utils import secure_filename')
        if has_email:
            imports.append('from flask_mail import Mail, Message')
        if has_export:
            imports.append('import csv')
            imports.append('import io')
        
        app_name = project_name.replace('App', '').lower()
        
        return f'''{"; ".join(imports)}

app = Flask(__name__)
app.secret_key = '{app_name}_secret_key_change_in_production'

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

{"# Email configuration" if has_email else ""}
{"app.config['MAIL_SERVER'] = 'smtp.gmail.com'" if has_email else ""}
{"app.config['MAIL_PORT'] = 587" if has_email else ""}
{"app.config['MAIL_USE_TLS'] = True" if has_email else ""}
{"mail = Mail(app)" if has_email else ""}

def init_db():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
{db_schema}
    
    conn.commit()
    conn.close()

{routes}

{self._get_auth_routes() if has_auth else ""}

{self._get_api_routes(app_name) if has_api else ""}

{self._get_chart_routes() if has_charts else ""}

{self._get_export_routes(app_name) if has_export else ""}

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    init_db()
    app.run(debug=True)
'''
    
    def _get_expense_schema(self) -> str:
        return '''    # Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_date TEXT NOT NULL)""")
    
    # Categories table
    c.execute("""CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  type TEXT NOT NULL,
                  color TEXT DEFAULT '#007bff')""")
    
    # Transactions table
    c.execute("""CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  type TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category_id INTEGER,
                  description TEXT,
                  date TEXT NOT NULL,
                  created_date TEXT NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (category_id) REFERENCES categories (id))""")
    
    # Insert default categories
    categories = [
        ('Food & Dining', 'expense', '#ff6b6b'),
        ('Transportation', 'expense', '#4ecdc4'),
        ('Shopping', 'expense', '#45b7d1'),
        ('Entertainment', 'expense', '#96ceb4'),
        ('Bills & Utilities', 'expense', '#feca57'),
        ('Salary', 'income', '#48dbfb'),
        ('Freelance', 'income', '#0abde3'),
        ('Investment', 'income', '#006ba6')
    ]
    c.executemany('INSERT OR IGNORE INTO categories (name, type, color) VALUES (?, ?, ?)', categories)'''
    
    def _get_expense_routes(self) -> str:
        return '''@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Get current month transactions
    current_month = datetime.now().strftime('%Y-%m')
    c.execute("""SELECT t.*, cat.name as category_name, cat.color 
                 FROM transactions t 
                 JOIN categories cat ON t.category_id = cat.id 
                 WHERE t.user_id = ? AND t.date LIKE ?
                 ORDER BY t.date DESC""", (session['user_id'], f'{current_month}%'))
    transactions = c.fetchall()
    
    # Calculate totals
    c.execute("""SELECT 
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
                 FROM transactions 
                 WHERE user_id = ? AND date LIKE ?""", (session['user_id'], f'{current_month}%'))
    totals = c.fetchone()
    
    # Get categories
    c.execute('SELECT * FROM categories ORDER BY type, name')
    categories = c.fetchall()
    
    conn.close()
    
    balance = (totals[0] or 0) - (totals[1] or 0)
    
    return render_template('dashboard.html', 
                         transactions=transactions,
                         categories=categories,
                         total_income=totals[0] or 0,
                         total_expense=totals[1] or 0,
                         balance=balance)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("""INSERT INTO transactions 
                 (user_id, type, amount, category_id, description, date, created_date) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
             (session['user_id'], request.form['type'], float(request.form['amount']),
              int(request.form['category_id']), request.form.get('description', ''),
              request.form['date'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', 
             (transaction_id, session['user_id']))
    conn.commit()
    conn.close()
    
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('dashboard'))'''
    
    def _generate_advanced_python_app(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        """Generate advanced Python app based on user requirements"""
        query_lower = query.lower()
        
        if 'fastapi' in query_lower or project_type == 'api':
            return self._python_flask_app(project_name, query)
        elif 'django' in query_lower:
            return self._python_flask_app(project_name, query)
        else:
            return self._python_flask_app(project_name, query)
    
    def _generate_advanced_javascript_app(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        """Generate advanced JavaScript app based on user requirements"""
        query_lower = query.lower()
        features = self._analyze_requirements(query_lower)
        
        if 'react' in query_lower:
            return self._generate_node_api(project_name, query)
        elif 'vue' in query_lower:
            return self._generate_node_api(project_name, query)
        elif 'node' in query_lower or project_type == 'api':
            return self._generate_node_api(project_name, query)
        else:
            return self._generate_node_api(project_name, query)
    
    def _generate_advanced_java_app(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        """Generate advanced Java app based on user requirements"""
        query_lower = query.lower()
        
        if 'spring' in query_lower:
            return self._generate_spring_boot(project_name, query)
        else:
            return self._java_console(project_name, query)
    
    def _analyze_requirements(self, query: str) -> dict:
        """Analyze user requirements and return feature flags"""
        return {
            'auth': any(word in query for word in ['login', 'register', 'user', 'auth', 'account', 'signin']),
            'database': any(word in query for word in ['database', 'sqlite', 'mysql', 'postgres', 'data', 'store']),
            'api': any(word in query for word in ['api', 'rest', 'json', 'endpoint']),
            'charts': any(word in query for word in ['chart', 'graph', 'visualization', 'analytics', 'dashboard']),
            'file_upload': any(word in query for word in ['upload', 'file', 'image', 'document']),
            'email': any(word in query for word in ['email', 'notification', 'mail', 'smtp']),
            'search': any(word in query for word in ['search', 'filter', 'find', 'query']),
            'export': any(word in query for word in ['export', 'pdf', 'csv', 'download', 'report']),
            'realtime': any(word in query for word in ['realtime', 'websocket', 'live', 'chat']),
            'payment': any(word in query for word in ['payment', 'stripe', 'paypal', 'billing']),
            'responsive': any(word in query for word in ['responsive', 'mobile', 'bootstrap', 'css']),
            'security': any(word in query for word in ['security', 'encryption', 'ssl', 'secure']),
            'testing': any(word in query for word in ['test', 'testing', 'unit test', 'pytest']),
            'deployment': any(word in query for word in ['deploy', 'docker', 'heroku', 'aws']),
            'admin': any(word in query for word in ['admin', 'management', 'dashboard', 'control panel'])
        }
    
    def _generate_fastapi_app_old(self, project_name: str, query: str, features: dict) -> str:
        """Generate advanced FastAPI application"""
        app_name = project_name.replace('App', '').lower()
        
        imports = ['from fastapi import FastAPI, HTTPException, Depends, status']
        imports.append('from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials')
        imports.append('from pydantic import BaseModel')
        imports.append('import sqlite3')
        imports.append('from datetime import datetime, timedelta')
        imports.append('import jwt')
        imports.append('import bcrypt')
        
        if features['file_upload']:
            imports.append('from fastapi import UploadFile, File')
        if features['email']:
            imports.append('import smtplib')
        if features['export']:
            imports.append('import pandas as pd')
        
        return f'''{chr(10).join(imports)}

app = FastAPI(title="{project_name}", description="Advanced {app_name} API")
security = HTTPBearer()

# Database setup
def init_db():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Users table
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  is_active BOOLEAN DEFAULT TRUE,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    
    # Main data table
    c.execute("""CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  title TEXT NOT NULL,
                  description TEXT,
                  category TEXT,
                  status TEXT DEFAULT 'active',
                  metadata JSON,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))""")
    
    conn.commit()
    conn.close()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ItemCreate(BaseModel):
    title: str
    description: str = None
    category: str = "general"
    metadata: dict = {{}}

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    created_at: str

# Authentication
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({{"exp": expire}})
    return jwt.encode(to_encode, "secret_key", algorithm="HS256")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, "secret_key", algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.post("/register")
def register(user: UserCreate):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                 (user.username, user.email, password_hash))
        conn.commit()
        return {{"message": "User created successfully"}}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    finally:
        conn.close()

@app.post("/login")
def login(user: UserLogin):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (user.username,))
    result = c.fetchone()
    conn.close()
    
    if result and bcrypt.checkpw(user.password.encode('utf-8'), result[0]):
        access_token = create_access_token(data={{"sub": user.username}})
        return {{"access_token": access_token, "token_type": "bearer"}}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/items", response_model=list[ItemResponse])
def get_items(current_user: str = Depends(get_current_user)):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("""SELECT i.* FROM items i 
                 JOIN users u ON i.user_id = u.id 
                 WHERE u.username = ? ORDER BY i.created_at DESC""", (current_user,))
    items = c.fetchall()
    conn.close()
    
    return [ItemResponse(
        id=item[0], title=item[2], description=item[3], 
        category=item[4], status=item[5], created_at=item[7]
    ) for item in items]

@app.post("/items")
def create_item(item: ItemCreate, current_user: str = Depends(get_current_user)):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    
    # Get user ID
    c.execute("SELECT id FROM users WHERE username = ?", (current_user,))
    user_id = c.fetchone()[0]
    
    c.execute("""INSERT INTO items (user_id, title, description, category, metadata) 
                 VALUES (?, ?, ?, ?, ?)""",
             (user_id, item.title, item.description, item.category, str(item.metadata)))
    conn.commit()
    conn.close()
    
    return {{"message": "Item created successfully"}}

@app.delete("/items/{{item_id}}")
def delete_item(item_id: int, current_user: str = Depends(get_current_user)):
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute("""DELETE FROM items WHERE id = ? AND user_id = 
                 (SELECT id FROM users WHERE username = ?)""", (item_id, current_user))
    conn.commit()
    conn.close()
    
    return {{"message": "Item deleted successfully"}}

{"@app.get('/export/csv')" if features['export'] else ""}
{"def export_csv(current_user: str = Depends(get_current_user)):" if features['export'] else ""}
{"    # Export functionality here" if features['export'] else ""}
{"    pass" if features['export'] else ""}

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    def _get_generic_schema(self) -> str:
        return '''    c.execute("""CREATE TABLE IF NOT EXISTS items
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      description TEXT,
                      category TEXT,
                      status TEXT DEFAULT 'active',
                      created_date TEXT NOT NULL)""")
'''
    
    def _get_generic_routes(self) -> str:
        return '''@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
def items():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items ORDER BY created_date DESC')
    items = c.fetchall()
    conn.close()
    return render_template('items.html', items=items)
'''
    
    def _get_auth_routes(self) -> str:
        return '''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Login logic here
        pass
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Registration logic here
        pass
    return render_template('register.html')
'''
    
    def _get_api_routes(self, app_name: str) -> str:
        return f'''@app.route('/api/items')
def api_items():
    conn = sqlite3.connect('{app_name}.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return jsonify(items)
'''
    
    def _get_chart_routes(self) -> str:
        return '''@app.route('/api/charts')
def chart_data():
    # Chart data logic here
    return jsonify({'data': []})
'''
    
    def _get_export_routes(self, app_name: str) -> str:
        return f'''@app.route('/export/csv')
def export_csv():
    # CSV export logic here
    return "CSV export"
'''
    
    def _java_console(self, project_name: str, query: str = '') -> str:
        class_name = project_name.replace('App', '').replace(' ', '')
        return f'''public class {class_name} {{
    public static void main(String[] args) {{
        System.out.println("Welcome to {project_name}!");
        
        // Add your implementation here
        {class_name}Manager manager = new {class_name}Manager();
        manager.start();
    }}
}}

class {class_name}Manager {{
    public void start() {{
        System.out.println("{project_name} is running...");
        // Implementation goes here
    }}
}}'''
    
    def _generate_csharp_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        if project_type == 'web':
            return self._generate_aspnet_core(project_name, query)
        else:
            return self._generate_csharp_console(project_name, query)
    
    def _generate_php_code(self, project_name: str, query: str = '', project_type: str = 'web') -> str:
        if 'laravel' in query.lower():
            return self._generate_laravel_app(project_name, query)
        else:
            return self._generate_php_app(project_name, query)
    
    def _generate_node_api(self, project_name: str, query: str = '') -> str:
        app_name = project_name.replace('App', '').lower()
        return f'''const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = '{app_name}_data.json';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Initialize data file
if (!fs.existsSync(DATA_FILE)) {{
    fs.writeFileSync(DATA_FILE, JSON.stringify([]));
}}

// Helper functions
const readData = () => {{
    try {{
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    }} catch (error) {{
        return [];
    }}
}};

const writeData = (data) => {{
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}};

// Routes
app.get('/api/items', (req, res) => {{
    const items = readData();
    res.json(items);
}});

app.post('/api/items', (req, res) => {{
    const items = readData();
    const newItem = {{
        id: Date.now(),
        ...req.body,
        createdAt: new Date().toISOString()
    }};
    items.push(newItem);
    writeData(items);
    res.status(201).json(newItem);
}});

app.put('/api/items/:id', (req, res) => {{
    const items = readData();
    const itemId = parseInt(req.params.id);
    const itemIndex = items.findIndex(item => item.id === itemId);
    
    if (itemIndex === -1) {{
        return res.status(404).json({{ error: 'Item not found' }});
    }}
    
    items[itemIndex] = {{ ...items[itemIndex], ...req.body }};
    writeData(items);
    res.json(items[itemIndex]);
}});

app.delete('/api/items/:id', (req, res) => {{
    const items = readData();
    const itemId = parseInt(req.params.id);
    const filteredItems = items.filter(item => item.id !== itemId);
    
    if (filteredItems.length === items.length) {{
        return res.status(404).json({{ error: 'Item not found' }});
    }}
    
    writeData(filteredItems);
    res.json({{ message: 'Item deleted successfully' }});
}});

app.listen(PORT, () => {{
    console.log(`{project_name} API running on port ${{PORT}}`);
}});'''
    
    def _generate_static_js(self, project_name: str) -> str:
        return f'''// {project_name} JavaScript
let items = JSON.parse(localStorage.getItem('items')) || [];
let categories = new Set();

// DOM Elements
const addForm = document.getElementById('addForm');
const itemsList = document.getElementById('itemsList');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {{
    renderItems();
    updateCategoryFilter();
    
    // Event listeners
    addForm.addEventListener('submit', addItem);
    searchInput.addEventListener('input', filterItems);
    categoryFilter.addEventListener('change', filterItems);
}});

// Add new item
function addItem(e) {{
    e.preventDefault();
    
    const name = document.getElementById('itemName').value;
    const category = document.getElementById('itemCategory').value || 'General';
    const quantity = parseInt(document.getElementById('itemQuantity').value) || 0;
    const price = parseFloat(document.getElementById('itemPrice').value) || 0;
    const description = document.getElementById('itemDescription').value;
    
    const newItem = {{
        id: Date.now(),
        name,
        category,
        quantity,
        price,
        description,
        createdDate: new Date().toLocaleDateString()
    }};
    
    items.push(newItem);
    categories.add(category);
    
    saveToStorage();
    renderItems();
    updateCategoryFilter();
    addForm.reset();
    
    // Show success message
    showMessage('Item added successfully!', 'success');
}}

// Render items
function renderItems(filteredItems = items) {{
    if (filteredItems.length === 0) {{
        itemsList.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }}
    
    itemsList.style.display = 'grid';
    emptyState.style.display = 'none';
    
    itemsList.innerHTML = filteredItems.map(item => `
        <div class="item-card">
            <h3>${{item.name}}</h3>
            <p>${{item.description || 'No description'}}</p>
            <div class="item-meta">
                <span class="category">${{item.category}}</span>
                <span class="quantity">Qty: ${{item.quantity}}</span>
                <span class="price">$${{item.price.toFixed(2)}}</span>
            </div>
            <div class="item-actions">
                <button class="btn-delete" onclick="deleteItem(${{item.id}})">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
}}

// Delete item
function deleteItem(id) {{
    if (confirm('Are you sure you want to delete this item?')) {{
        items = items.filter(item => item.id !== id);
        saveToStorage();
        renderItems();
        updateCategoryFilter();
        showMessage('Item deleted successfully!', 'success');
    }}
}}

// Filter items
function filterItems() {{
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    
    let filtered = items.filter(item => {{
        const matchesSearch = item.name.toLowerCase().includes(searchTerm) ||
                            item.description.toLowerCase().includes(searchTerm);
        const matchesCategory = !selectedCategory || item.category === selectedCategory;
        
        return matchesSearch && matchesCategory;
    }});
    
    renderItems(filtered);
}}

// Update category filter
function updateCategoryFilter() {{
    categories.clear();
    items.forEach(item => categories.add(item.category));
    
    categoryFilter.innerHTML = '<option value="">All Categories</option>' +
        Array.from(categories).map(cat => `<option value="${{cat}}">${{cat}}</option>`).join('');
}}

// Save to localStorage
function saveToStorage() {{
    localStorage.setItem('items', JSON.stringify(items));
}}

// Show message
function showMessage(message, type) {{
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${{type}}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${{type === 'success' ? '#28a745' : '#dc3545'}};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(messageDiv);
    
    setTimeout(() => {{
        messageDiv.remove();
    }}, 3000);
}}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
`;
document.head.appendChild(style);'''
    
    def _generate_package_json(self, project_name: str) -> str:
        return f'''{{
  "name": "{project_name.lower()}",
  "version": "1.0.0",
  "description": "{project_name} - Generated by Jarvis",
  "main": "server.js",
  "scripts": {{
    "start": "node server.js",
    "dev": "nodemon server.js"
  }},
  "dependencies": {{
    "express": "^4.18.0",
    "cors": "^2.8.5",
    "body-parser": "^1.20.0"
  }},
  "devDependencies": {{
    "nodemon": "^2.0.20"
  }}
}}'''
    
    def _generate_requirements(self, project_type: str) -> str:
        if project_type == 'api':
            return "fastapi>=0.68.0\nuvicorn>=0.15.0\npydantic>=1.8.0"
        else:
            return "Flask>=2.0.0\nrequests>=2.25.0"
    
    def _generate_maven_pom(self, project_name: str) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.jarvis</groupId>
    <artifactId>{project_name.lower()}</artifactId>
    <version>1.0.0</version>
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>2.7.0</version>
        </dependency>
    </dependencies>
</project>'''
    
    def create_project_on_desktop(self, project_data: Dict) -> str:
        try:
            project_name = project_data['project_name']
            project_path = self.desktop_path / project_name
            
            project_path.mkdir(exist_ok=True)
            
            for filename, content in project_data['files'].items():
                file_path = project_path / filename
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return f"Project '{project_name}' created successfully at: {project_path}"
            
        except Exception as e:
            return f"Error creating project: {str(e)}"

auto_code_architect = AutoCodeArchitect()

def generate_inline_code(query: str) -> str:
    """Generate inline code snippets"""
    query_lower = query.lower()
    
    # Detect programming language
    language = 'python'  # default
    if ' c ' in query_lower or query_lower.startswith('c ') or query_lower.endswith(' c'):
        language = 'c'
    elif 'java' in query_lower:
        language = 'java'
    elif 'javascript' in query_lower or 'js' in query_lower:
        language = 'javascript'
    elif 'cpp' in query_lower or 'c++' in query_lower:
        language = 'cpp'
    
    if 'add' in query_lower and 'number' in query_lower:
        if language == 'c':
            return """#include <stdio.h>

int add_two_numbers(int a, int b) {
    return a + b;
}

int main() {
    int num1, num2, result;
    printf("Enter first number: ");
    scanf("%d", &num1);
    printf("Enter second number: ");
    scanf("%d", &num2);
    result = add_two_numbers(num1, num2);
    printf("Sum: %d\n", result);
    return 0;
}"""
        elif language == 'java':
            return """import java.util.Scanner;

public class AddNumbers {
    public static int addTwoNumbers(int a, int b) {
        return a + b;
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter first number: ");
        int num1 = scanner.nextInt();
        System.out.print("Enter second number: ");
        int num2 = scanner.nextInt();
        int result = addTwoNumbers(num1, num2);
        System.out.println("Sum: " + result);
        scanner.close();
    }
}"""
        elif language == 'javascript':
            return """function addTwoNumbers(a, b) {
    return a + b;
}

// Example usage
const num1 = parseFloat(prompt("Enter first number: "));
const num2 = parseFloat(prompt("Enter second number: "));
const result = addTwoNumbers(num1, num2);
console.log(`Sum: ${result}`);
alert(`Sum: ${result}`);"""
        else:  # Python
            return """def add_two_numbers(a, b):
    return a + b

# Example usage
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
result = add_two_numbers(num1, num2)
print(f"Sum: {result}")"""
    
    elif 'calculator' in query_lower:
        return """def calculator(a, b, operation):
    if operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    elif operation == '/':
        return a / b if b != 0 else "Cannot divide by zero"
    else:
        return "Invalid operation"

# Full calculator program
while True:
    try:
        num1 = float(input("Enter first number: "))
        operation = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))
        
        result = calculator(num1, num2, operation)
        print(f"Result: {result}")
        
        if input("Continue? (y/n): ").lower() != 'y':
            break
    except ValueError:
        print("Invalid input! Please enter numbers.")"""
    
    elif 'factorial' in query_lower:
        return """def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Example usage
num = int(input("Enter a number: "))
if num < 0:
    print("Factorial is not defined for negative numbers")
else:
    result = factorial(num)
    print(f"Factorial of {num} is {result}")"""
    
    elif 'fibonacci' in query_lower:
        return """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Example usage
num = int(input("Enter number of terms: "))
print(f"Fibonacci sequence for {num} terms:")
for i in range(num):
    print(fibonacci(i), end=" ")
print()"""
    
    elif 'sort' in query_lower:
        return """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
print(f"Original array: {numbers}")
sorted_numbers = bubble_sort(numbers.copy())
print(f"Sorted array: {sorted_numbers}")"""
    
    else:
        # Generate complete working code based on query keywords
        if 'prime' in query_lower:
            return """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Example usage
num = int(input("Enter a number: "))
if is_prime(num):
    print(f"{num} is a prime number")
else:
    print(f"{num} is not a prime number")"""
        
        else:
            return f"""# Complete implementation for: {query}
def main():
    print("Program started")
    # Add your implementation here
    result = "Hello World"
    print(f"Result: {{result}}")
    return result

if __name__ == "__main__":
    main()"""

def write_code_at_cursor(code: str, file_path: str) -> str:
    """Write code at cursor position in active file"""
    try:
        # For now, append to end of file (cursor position detection would need IDE integration)
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write('\n\n' + code + '\n')
        return f"Code written to {file_path}"
    except Exception as e:
        return f"Error writing code: {str(e)}"

def generate_code_project(query: str) -> str:
    try:
        # Check if user wants inline code
        if any(word in query.lower() for word in ['write here', 'cursor', 'inline', 'here']):
            code = generate_inline_code(query)
            
            # Write at actual cursor position using clipboard method
            import pyautogui
            import pyperclip
            
            try:
                # Copy code to clipboard
                pyperclip.copy(code)
                
                # Paste at current cursor position
                pyautogui.hotkey('ctrl', 'v')
                
                return f"Code written at cursor position"
            except:
                # Fallback: write to active file
                active_file = r"c:\Users\Hp\Desktop\inp\run.py"
                with open(active_file, 'a', encoding='utf-8') as f:
                    f.write('\n\n' + code + '\n')
                return f"Code appended to run.py"
        
        # Otherwise create project
        request_info = auto_code_architect.detect_request_type(query)
        result = auto_code_architect.generate_code(request_info)
        
        creation_result = auto_code_architect.create_project_on_desktop(result)
        return f"Creating project on Desktop...\n\n{creation_result}\n\nProject Type: {result['project_type']}\nLanguage: {result['language']}"
    
    except Exception as e:
        return f"Error generating code: {str(e)}"
import pyttsx3
import speech_recognition as sr
import eel
import time
import threading
import json
import numpy as np
from datetime import datetime, timedelta
import random
import os
import subprocess
import schedule
from engine.command_history import command_history

# Emotion Detection System
class EmotionSystem:
    def __init__(self):
        self.current_emotion = 'neutral'
        self.enabled = False
        self.emotion_history = []
        self.monitoring = False
        self.monitor_thread = None
        self.emotion_file = 'emotion_config.json'
        self.load_emotion_data()
        
        # Emotion response templates
        self.responses = {
            'happy': {
                'greetings': ["Great to see you in such a good mood!", "You sound wonderful today!"],
                'acknowledgments': ["Absolutely! Let's keep this positive momentum!", "Perfect! I'm excited to help!"],
                'completions': ["Done! Hope that keeps your day bright!", "All set! Keep that smile going!"]
            },
            'sad': {
                'greetings': ["I'm here for you. How can I help?", "Let me help make things easier."],
                'acknowledgments': ["I understand. Let me take care of that.", "Of course. I'll handle this gently."],
                'completions': ["All done. I hope this helps a little.", "Completed. Take care of yourself."]
            },
            'stressed': {
                'greetings': ["I can sense you're under pressure. Let me help.", "Take a deep breath. I'll handle this."],
                'acknowledgments': ["Got it. I'll take care of this quickly.", "I'll make this as smooth as possible."],
                'completions': ["Done efficiently. One less thing on your plate!", "Completed quickly. Hope that helps."]
            },
            'angry': {
                'greetings': ["I understand you're frustrated. Let me help.", "I'm here to help make things right."],
                'acknowledgments': ["I understand your frustration. I'll handle this carefully.", "Got it. Let me fix this properly."],
                'completions': ["Completed. I hope this helps resolve the issue.", "Done correctly. Let me know if you need more help."]
            },
            'excited': {
                'greetings': ["I love your enthusiasm! What are we doing today?", "Your energy is incredible!"],
                'acknowledgments': ["Yes! I'm as excited as you are!", "Absolutely! This is going to be fantastic!"],
                'completions': ["Done! That was as exciting as I hoped!", "Completed with enthusiasm! What's next?"]
            },
            'neutral': {
                'greetings': ["Hello! How can I help you today?", "Hi there! I'm ready to help."],
                'acknowledgments': ["Understood. I'll take care of that.", "Got it. Working on it now."],
                'completions': ["Task completed successfully.", "All done! Anything else?"]
            }
        }
    
    def detect_emotion_from_text(self, text):
        """AI-powered emotion detection using Groq"""
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'Analyze emotion in: "{text}". Return only one word: happy, sad, stressed, angry, excited, or neutral.'
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=10
            )
            
            emotion = response.choices[0].message.content.strip().lower()
            
            # Validate emotion
            valid_emotions = ['happy', 'sad', 'stressed', 'angry', 'excited', 'neutral']
            return emotion if emotion in valid_emotions else 'neutral'
            
        except Exception as e:
            print(f"Groq emotion detection error: {e}")
            # Fallback to keyword detection
            text = text.lower()
            if any(word in text for word in ['great', 'awesome', 'fantastic', 'love', 'happy']):
                return 'happy'
            elif any(word in text for word in ['sad', 'down', 'upset', 'cry']):
                return 'sad'
            elif any(word in text for word in ['stress', 'busy', 'overwhelmed', 'pressure']):
                return 'stressed'
            elif any(word in text for word in ['angry', 'mad', 'frustrated']):
                return 'angry'
            elif any(word in text for word in ['amazing', 'incredible', 'wow', 'excited']):
                return 'excited'
            else:
                return 'neutral'
    
    def load_emotion_data(self):
        """Load emotion data from file"""
        try:
            if os.path.exists(self.emotion_file):
                with open(self.emotion_file, 'r') as f:
                    data = json.load(f)
                    self.current_emotion = data.get('last_emotion', 'neutral')
                    self.emotion_history = data.get('emotion_history', [])
                    self.enabled = data.get('enabled', False)
                pass  # Silent loading
        except Exception as e:
            print(f"Error loading emotion data: {e}")
    
    def save_emotion_data(self):
        """Save emotion data to file"""
        try:
            data = {
                'enabled': self.enabled,
                'sensitivity': 0.7,
                'last_emotion': self.current_emotion,
                'timestamp': datetime.now().isoformat(),
                'emotion_history': self.emotion_history
            }
            with open(self.emotion_file, 'w') as f:
                json.dump(data, f)
            pass  # Silent saving
        except Exception as e:
            print(f"Error saving emotion data: {e}")
    
    def update_emotion(self, emotion):
        """Update current emotion"""
        self.current_emotion = emotion
        self.emotion_history.append({
            'emotion': emotion,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.emotion_history) > 10:
            self.emotion_history = self.emotion_history[-10:]
        self.save_emotion_data()
    
    def get_adaptive_response(self, base_text, emotion="neutral"):
        """Fully rephrase sentence with same meaning and emotional tone"""
        if not self.enabled:
            return base_text
        
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'''Rephrase this message for someone feeling {self.current_emotion}: "{base_text}"

Rules:
- Keep EXACT same meaning and information
- Change wording to match {self.current_emotion} tone
- Return ONLY the rephrased sentence
- No explanations or alternatives
- Keep similar length

Examples:
Original: "File uploaded successfully"
Happy: "Your file has been successfully uploaded! 🎉"
Sad: "I've managed to upload your file for you"

Rephrase: "{base_text}"'''
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=100,
                temperature=0.8
            )
            
            adapted_text = response.choices[0].message.content.strip()
            
            # Extract only the first sentence, remove any explanations
            if adapted_text:
                # Split by common separators and take first part
                first_sentence = adapted_text.split('\n')[0].split('.')[0]
                if '"' in first_sentence:
                    # Extract text between quotes if present
                    import re
                    quoted = re.findall(r'"([^"]+)"', first_sentence)
                    if quoted:
                        return quoted[0]
                return first_sentence if first_sentence else base_text
            return base_text
            
        except Exception as e:
            print(f"Groq rephrasing error: {e}")
            return base_text
    
    def get_encouraging_response(self):
        """Get AI-powered encouraging message"""
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'''Generate a warm, encouraging message for someone feeling {self.current_emotion}.
            
Make it:
            - Personal and caring
            - Natural and conversational
            - Specifically tailored to {self.current_emotion} emotion
            - 10-20 words maximum
            - Avoid clichés, be genuine and supportive'''
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=60
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Groq encouragement error: {e}")
            return "I'm here for you."  # Simple fallback
    
    def get_humor_response(self):
        """Get AI-powered appropriate humor"""
        try:
            from groq import Groq
            from engine.groq_config import GROQ_API_KEY
            
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f'''Tell a gentle, appropriate joke for someone feeling {self.current_emotion}.
            
Make it:
            - Light and uplifting
            - Appropriate for their {self.current_emotion} mood
            - Clean and family-friendly
            - Under 25 words
            - Genuinely funny but sensitive to their emotional state'''
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                max_tokens=80
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Groq humor error: {e}")
            return "Here's a smile for you! 😊"  # Simple fallback
    
    def start_real_time_monitoring(self):
        """Start continuous emotion monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Real-time emotion monitoring started")
    
    def stop_real_time_monitoring(self):
        """Stop continuous emotion monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        
        # Clean up temp file
        if hasattr(self, 'temp_audio_file'):
            try:
                import os
                os.unlink(self.temp_audio_file)
                delattr(self, 'temp_audio_file')
            except:
                pass
        
        print("Real-time emotion monitoring stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        try:
            import cv2
            import pyaudio
            import numpy as np
            
            # Initialize camera and audio
            cap = cv2.VideoCapture(0)
            p = pyaudio.PyAudio()
            
            stream = p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=22050,
                input=True,
                frames_per_buffer=1024
            )
            
            while self.monitoring:
                try:
                    # Analyze voice tone continuously with larger buffer for better accuracy
                    audio_data = stream.read(2048, exception_on_overflow=False)  # Larger buffer
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    # Accumulate audio for better analysis
                    if not hasattr(self, 'audio_buffer'):
                        self.audio_buffer = []
                    
                    self.audio_buffer.extend(audio_array)
                    
                    # Analyze when we have enough data (2 seconds for better accuracy)
                    if len(self.audio_buffer) >= 44100:  # 2 seconds at 22050 Hz
                        analysis_data = np.array(self.audio_buffer[-44100:])  # Last 2 seconds
                        
                        # Only analyze if significant audio and enough time passed
                        if not hasattr(self, 'last_analysis_time'):
                            self.last_analysis_time = 0
                        
                        current_time = time.time()
                        if (np.max(np.abs(analysis_data)) > 0.01 and 
                            current_time - self.last_analysis_time >= 5):  # Analyze every 5 seconds max
                            
                            voice_emotion = self._analyze_voice_tone(analysis_data)
                            if voice_emotion != 'neutral' and voice_emotion != self.current_emotion:
                                old_emotion = self.current_emotion
                                self.update_emotion(voice_emotion)
                                print(f"Voice emotion: {old_emotion} → {voice_emotion}")
                            
                            self.last_analysis_time = current_time
                        
                        # Keep only last 3 seconds of audio
                        if len(self.audio_buffer) > 66150:
                            self.audio_buffer = self.audio_buffer[-66150:]
                    
                    # Analyze face emotion every 30 minutes
                    current_time = time.time()
                    if not hasattr(self, 'last_face_check'):
                        self.last_face_check = current_time
                    
                    if current_time - self.last_face_check >= 1800:  # 30 minutes = 1800 seconds
                        ret, frame = cap.read()
                        if ret:
                            emotion = self._analyze_face_emotion(frame)
                            if emotion != 'neutral' and emotion != self.current_emotion:
                                old_emotion = self.current_emotion
                                self.update_emotion(emotion)
                                print(f"Face emotion (30min check): {old_emotion} → {emotion}")
                        self.last_face_check = current_time
                    
                    time.sleep(0.05)  # Check voice every 0.05 seconds for better responsiveness
                    
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(1)
            
            cap.release()
            stream.stop_stream()
            stream.close()
            p.terminate()
            
        except Exception as e:
            print(f"Monitor setup error: {e}")
    
    def _analyze_face_emotion(self, frame):
        """Advanced face emotion analysis without API calls"""
        try:
            import cv2
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                
                # Advanced facial feature analysis
                brightness = np.mean(face_roi)
                contrast = np.std(face_roi)
                
                # Edge detection for expression analysis
                edges = cv2.Canny(face_roi, 50, 150)
                edge_density = np.sum(edges > 0) / (w * h)
                
                # Advanced emotion classification
                if brightness > 130 and edge_density < 0.1:
                    return 'happy'
                elif brightness < 70:
                    return 'sad'
                elif edge_density > 0.15:
                    return 'stressed'
                elif contrast > 80:
                    return 'angry'
                else:
                    return 'neutral'
            
            # Fallback for no face detected
            brightness = np.mean(gray)
            contrast = np.std(gray)
            
            if brightness > 130 and contrast > 45:
                return 'happy'
            elif brightness < 70:
                return 'sad'
            elif contrast > 70:
                return 'stressed'
            else:
                return 'neutral'
                
        except Exception as e:
            return 'neutral'
    
    def _analyze_voice_tone(self, audio_data):
        """Advanced voice emotion detection using audio features"""
        try:
            # Calculate advanced audio features
            energy = np.sum(audio_data**2) / len(audio_data)
            zcr = np.sum(np.diff(np.sign(audio_data)) != 0) / len(audio_data)
            
            # Calculate pitch variation (spectral features)
            fft = np.fft.fft(audio_data)
            magnitude = np.abs(fft)
            spectral_centroid = np.sum(magnitude * np.arange(len(magnitude))) / np.sum(magnitude)
            
            # Advanced emotion classification
            if energy > 0.01 and zcr < 0.1 and spectral_centroid > 5000:
                return 'excited'
            elif energy > 0.003 and zcr < 0.15 and spectral_centroid > 3000:
                return 'happy'
            elif energy < 0.001 or spectral_centroid < 1000:
                return 'sad'
            elif zcr > 0.25 and energy > 0.002:
                return 'stressed'
            elif energy > 0.005 and zcr > 0.2:
                return 'angry'
            else:
                return 'neutral'
                
        except Exception as e:
            # Simple fallback
            energy = np.sum(audio_data**2) / len(audio_data)
            if energy > 0.01:
                return 'excited'
            elif energy > 0.003:
                return 'happy'
            elif energy < 0.001:
                return 'sad'
            else:
                return 'neutral'
    
    def get_voice_settings(self):
        """Get TTS settings based on emotion"""
        settings = {
            'happy': {'rate': 200, 'volume': 0.9},
            'excited': {'rate': 220, 'volume': 1.0},
            'sad': {'rate': 140, 'volume': 0.6},
            'stressed': {'rate': 160, 'volume': 0.7},
            'angry': {'rate': 180, 'volume': 0.8},
            'calm': {'rate': 150, 'volume': 0.8},
            'neutral': {'rate': 174, 'volume': 0.9}
        }
        # Silent voice settings
        return settings.get(self.current_emotion, settings['neutral'])
    
    def enable(self):
        self.enabled = True
        self.save_emotion_data()
        self.start_real_time_monitoring()
        return "Emotion detection enabled. I'll now monitor your mood and adapt in real-time."
    
    def disable(self):
        self.enabled = False
        self.save_emotion_data()
        self.stop_real_time_monitoring()
        return "Emotion detection disabled."
    
    def get_status(self):
        if self.enabled:
            return f"Emotion detection active. Current emotion: {self.current_emotion}. Real-time monitoring: {'ON' if self.monitoring else 'OFF'}"
        return "Emotion detection disabled"

# Global emotion system
emotion_system = EmotionSystem()

# Scheduler System
class TaskScheduler:
    def __init__(self):
        self.scheduled_tasks = []
        self.scheduler_thread = None
        self.running = False
        self.tasks_file = 'scheduled_tasks.json'
        self.load_tasks()
    
    def load_tasks(self):
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as f:
                    self.scheduled_tasks = json.load(f)
        except:
            self.scheduled_tasks = []
    
    def save_tasks(self):
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.scheduled_tasks, f)
        except Exception as e:
            print(f"Save tasks error: {e}")
    
    def schedule_task(self, task_command, schedule_time):
        try:
            task = {
                'command': task_command,
                'time': schedule_time,
                'created': datetime.now().isoformat(),
                'executed': False
            }
            self.scheduled_tasks.append(task)
            self.save_tasks()
            
            # Parse time and schedule
            time_lower = schedule_time.lower().strip()
            
            if 'am' in time_lower or 'pm' in time_lower:
                # Handle AM/PM format (e.g., "2am", "2:30pm")
                clean_time = time_lower.replace(' ', '')
                schedule.every().day.at(clean_time).do(self._execute_task, task_command)
            elif 'second' in time_lower or 'sec' in time_lower:
                # Handle seconds (e.g., "30 seconds", "5sec")
                import re
                match = re.search(r'(\d+)', time_lower)
                if match:
                    secs = int(match.group(1))
                    schedule.every(secs).seconds.do(self._execute_task, task_command)
            elif 'minute' in time_lower or 'min' in time_lower:
                # Handle minutes (e.g., "5 minutes", "10min")
                import re
                match = re.search(r'(\d+)', time_lower)
                if match:
                    mins = int(match.group(1))
                    schedule.every(mins).minutes.do(self._execute_task, task_command)
            elif 'hour' in time_lower or 'hr' in time_lower:
                # Handle hours (e.g., "2 hours", "1hr")
                import re
                match = re.search(r'(\d+)', time_lower)
                if match:
                    hrs = int(match.group(1))
                    schedule.every(hrs).hours.do(self._execute_task, task_command)
            else:
                # Try to parse as time format (e.g., "14:30", "2:00")
                try:
                    schedule.every().day.at(time_lower).do(self._execute_task, task_command)
                except:
                    return f"Invalid time format: {schedule_time}"
            
            self._start_scheduler()
            return f"Task scheduled: {task_command} at {schedule_time}"
        except Exception as e:
            return f"Schedule error: {e}"
    
    def _execute_task(self, command):
        try:
            print(f"Executing scheduled task: {command}")
            if 'open notepad' in command:
                subprocess.Popen(['notepad.exe'])
                print(f"Opened notepad")
            elif 'open' in command:
                app = command.replace('open ', '')
                subprocess.Popen([app])
                print(f"Opened {app}")
            else:
                # Execute as dual AI command
                from engine.dual_ai import dual_ai
                response = dual_ai.execute(command)
                print(f"Dual AI response: {response}")
                # Speak the response
                try:
                    speak(response)
                except:
                    print("Could not speak response")
            return schedule.CancelJob  # Cancel this job after execution
        except Exception as e:
            print(f"Task execution error: {e}")
            return schedule.CancelJob  # Cancel even on error
    
    def _start_scheduler(self):
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
    
    def _scheduler_loop(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)  # Check every second for better precision
    
    def list_tasks(self):
        if not self.scheduled_tasks:
            return "No scheduled tasks"
        tasks = "Scheduled tasks: "
        for task in self.scheduled_tasks[-5:]:
            tasks += f"{task['command']} at {task['time']}, "
        return tasks

# Global scheduler
task_scheduler = TaskScheduler()

# Continuous listening variables
continuous_active = False
continuous_listener = None
listening_paused = False
jarvis_muted = False

def speak(text):
    global jarvis_muted
    text = str(text)
    
    # Check if Jarvis is muted
    if jarvis_muted:
        print(f"[MUTED] Jarvis: {text}")
        return
    
    # Transform text with personality manager
    try:
        from engine.personality_manager import personality_manager
        text = personality_manager.transform_response(text)
    except Exception as e:
        print(f"Personality transform error: {e}")
    
    # Apply emotion-based adaptation
    try:
        text = emotion_system.get_adaptive_response(text)
    except Exception as e:
        print(f"Emotion adaptation error: {e}")
    
    # Get emotion-based voice settings
    voice_settings = emotion_system.get_voice_settings() if emotion_system.enabled else {'rate': 174, 'volume': 0.9}
    
    # Get current language from multilingual support
    try:
        from engine.multilingual_support import multilingual
        current_language = multilingual.current_language
    except:
        current_language = 'english'
    
    # Update command history with response
    try:
        if hasattr(command_history, 'history') and command_history.history:
            last_entry = command_history.history[-1]
            if last_entry.get('jarvis_response') == "Processing...":
                last_entry['jarvis_response'] = text
                command_history.save_history()
    except Exception as e:
        print(f"History update error: {e}")
    
    try:
        eel.DisplayMessage(text)
    except:
        print(f"Jarvis: {text}")
    
    # Handle TTS based on language
    try:
        # For non-English languages, use gTTS
        if current_language != 'english':
            try:
                from gtts import gTTS
                import pygame
                import io
                import os
                
                # Get language code for gTTS
                lang_codes = {
                    'kannada': 'kn',
                    'hindi': 'hi',
                    'bengali': 'bn',
                    'gujarati': 'gu',
                    'malayalam': 'ml',
                    'marathi': 'mr',
                    'tamil': 'ta',
                    'telugu': 'te',
                    'urdu': 'ur'
                }
                
                lang_code = lang_codes.get(current_language, 'en')
                
                # Generate speech using gTTS
                tts = gTTS(text=text, lang=lang_code, slow=False)
                
                # Save to memory buffer
                mp3_buffer = io.BytesIO()
                tts.write_to_fp(mp3_buffer)
                mp3_buffer.seek(0)
                
                # Play using pygame
                pygame.mixer.init()
                pygame.mixer.music.load(mp3_buffer)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                pygame.mixer.quit()
                
            except Exception as e:
                print(f"gTTS error: {e}")
                # Fallback to voice gender control for non-English
                from engine.voice_gender_control import voice_control
                voice_control.speak_with_gender(text)
        else:
            # For English, use voice gender control with emotion settings
            from engine.voice_gender_control import voice_control
            success = voice_control.speak_with_gender(text)
            if not success:
                # Final fallback to basic pyttsx3 with emotion settings
                engine = pyttsx3.init('sapi5')
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)
                engine.setProperty('rate', voice_settings['rate'])
                engine.setProperty('volume', voice_settings['volume'])
                engine.say(text)
                engine.runAndWait()
                
    except Exception as e:
        print(f"TTS error: {e}")
        # Final fallback to basic pyttsx3 with emotion settings
        try:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', voice_settings['rate'])
            engine.setProperty('volume', voice_settings['volume'])
            engine.say(text)
            engine.runAndWait()
        except:
            print(f"All TTS methods failed for: {text}")
    
    try:
        eel.receiverText(text)
    except:
        pass

def takecommand():
    global listening_paused
    
    # Check if listening is paused
    if listening_paused:
        print("Listening is paused")
        return ""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        try:
            eel.DisplayMessage('listening....')
        except:
            pass
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            return ""

    try:
        print('recognizing')
        try:
            eel.DisplayMessage('recognizing....')
        except:
            pass
        
        # Get current language for speech recognition
        try:
            from engine.multilingual_support import multilingual
            current_language = multilingual.current_language
        except:
            current_language = 'english'
        
        # Set recognition language based on current language
        try:
            from engine.multilingual_support import multilingual
            recognition_language = multilingual.get_speech_recognition_language()
        except:
            recognition_language = 'en-IN'
        
        query = r.recognize_google(audio, language=recognition_language)
        print(f"user said: {query}")
        try:
            eel.DisplayMessage(query)
        except:
            pass
        time.sleep(1)
    except Exception as e:
        print(f"Recognition error: {e}")
        return ""
    
    return query.lower()



def parse_multiple_commands(query):
    """Parse multiple commands from a single query"""
    import re
    
    # Common separators for multiple commands
    separators = [
        r'\s+and\s+then\s+',
        r'\s+then\s+',
        r'\s+and\s+',
        r'\s*,\s*and\s+',
        r'\s*,\s*then\s+',
        r'\s*,\s*'
    ]
    
    # Try each separator to split the query
    commands = [query.strip()]
    
    for separator in separators:
        temp_commands = []
        for cmd in commands:
            split_cmds = re.split(separator, cmd, flags=re.IGNORECASE)
            if len(split_cmds) > 1:
                temp_commands.extend([c.strip() for c in split_cmds if c.strip()])
            else:
                temp_commands.append(cmd)
        commands = temp_commands
        if len(commands) > 1:
            break
    
    # Filter out empty commands and very short ones
    commands = [cmd for cmd in commands if cmd and len(cmd.strip()) > 2]
    
    return commands

# @eel.expose
def allCommands(message=1):
    is_voice_input = False
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
        is_voice_input = True
    else:
        query = message
        try:
            eel.senderText(query)
        except:
            print(f"User: {query}")
        is_voice_input = False
    
    # Store the user command immediately
    if query and query.strip():
        command_history.add_command(query, "Processing...", is_voice_input)
    
    # Check for aura mode at the beginning
    if "aura" in query.lower():
        try:
            from engine.ultimate_ai_executor import ultimate_ai
            print(f"🌟 AURA Mode Activated for: {query}")
          
            
            # Remove "aura" from query and execute with ultimate AI
            clean_query = query.lower().replace("aura", "").strip()
            if clean_query:
                # Execute and get AI-generated response from ultimate AI
                response = ultimate_ai.execute(clean_query)
                if response:
                    speak(response)  # Speak the response from ultimate AI
                    
                    # Wait 1 second then show next move prediction
                    time.sleep(1)
                    
                    # Get next move suggestion from ultimate AI
                    try:
                        suggestions = ultimate_ai.predict_next_move(clean_query)
                        if suggestions and len(suggestions) > 0:
                            suggestion = suggestions[0]
                            print(f"\n🤖 AI Suggestion: {suggestion}")
                            
                            # Get simple yes/no confirmation
                            speak(f"Execute {suggestion}?")
                            confirmation = takecommand()  # Get voice input directly
                            
                            if confirmation and ("yes" in confirmation.lower() or "y" in confirmation.lower()):
                                print(f"🚀 Executing: {suggestion}")
                                speak("Executing suggestion")
                                # Execute suggestion using full Ultimate AI system
                                ultimate_ai.execute(suggestion)
                            else:
                                print("👍 Skipping suggestion")
                                speak("Skipping suggestion")
                    except Exception as e:
                        print(f"Next move error: {e}")
                else:
                    speak("Command completed")
            else:
                speak("Please specify what you want me to do with aura mode")
            
            try:
                eel.ShowHood()
            except:
                pass
            return
            
        except Exception as e:
            print(f"Ultimate AI Error: {e}")
            speak("Aura mode failed. Switching to standard mode.")
            # Continue with normal processing
    
    try:
        print(f"Processing query: '{query}'")
        
        # Detect emotion from user input only if it came from voice
        if emotion_system.enabled and is_voice_input:
            detected_emotion = emotion_system.detect_emotion_from_text(query)
            emotion_system.update_emotion(detected_emotion)
            print(f"Detected emotion: {detected_emotion}")
        elif emotion_system.enabled and not is_voice_input:
            print("Command line input - skipping emotion detection")
        
        # Parse multiple commands
        commands = parse_multiple_commands(query)
        
        if len(commands) > 1:
            print(f"Multiple commands detected: {commands}")
            speak(f"Executing {len(commands)} commands")
            
            # Execute each command sequentially
            for i, cmd in enumerate(commands, 1):
                print(f"Executing command {i}/{len(commands)}: {cmd}")
                try:
                    # Add small delay between commands
                    if i > 1:
                        time.sleep(0.5)
                    
                    # Process each command individually
                    process_single_command(cmd.strip())
                    
                except Exception as e:
                    print(f"Error executing command '{cmd}': {e}")
                    try:
                        speak(f"Error with command {i}")
                    except:
                        print(f"Could not speak error for command {i}")
            
            try:
                speak("All commands completed")
            except:
                print("All commands completed")                
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Single command - use existing logic
        process_single_command(query)
        
    except Exception as e:
        print(f"Error in allCommands: {e}")
        speak("Something went wrong")
    
    try:
        eel.ShowHood()
    except:
        pass

def start_continuous_listen():
    """Start continuous listening mode"""
    global continuous_active, continuous_listener
    try:
        if continuous_listener and continuous_active:
            return "Continuous listening already active"
        
        continuous_active = True
        
        def continuous_loop():
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
            print("✅ Ready for continuous listening")
            
            while continuous_active:
                try:
                    # Check if listening is paused
                    if listening_paused:
                        print("⏸️ Listening paused...")
                        try:
                            eel.updateListenStatus("⏸️ Listening paused...")
                        except:
                            pass
                        time.sleep(1)
                        continue
                    
                    print("🎧 Listening...")
                    try:
                        eel.updateListenStatus("🎤 Listening...")
                    except:
                        pass
                    
                    with microphone as source:
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    print("🔍 Recognizing...")
                    try:
                        eel.updateListenStatus("🔍 Recognizing...")
                    except:
                        pass
                    
                    text = recognizer.recognize_google(audio).lower()
                    if text and len(text.strip()) > 2:
                        print(f"✅ Recognized: {text}")
                        try:
                            eel.updateListenStatus(f"✅ Recognized: {text}")
                            eel.senderText(text)
                        except:
                            pass
                        
                        # Parse and process multiple commands
                        commands = parse_multiple_commands(text)
                        
                        if len(commands) > 1:
                            print(f"Multiple commands detected: {commands}")
                            speak(f"Executing {len(commands)} commands")
                            
                            for i, cmd in enumerate(commands, 1):
                                print(f"Executing command {i}/{len(commands)}: {cmd}")
                                try:
                                    if i > 1:
                                        time.sleep(0.5)
                                    process_single_command(cmd.strip())
                                except Exception as e:
                                    print(f"Error executing command '{cmd}': {e}")
                            
                            speak("All commands completed")
                        else:
                            # Single command
                            process_single_command(text)
                        
                        # Return to listening after response
                        time.sleep(1)
                        try:
                            eel.updateListenStatus("🎤 Listening...")
                        except:
                            pass
                        
                except sr.WaitTimeoutError:
                    print("⏰ Timeout - continuing to listen...")
                except sr.UnknownValueError:
                    print("❓ Could not understand - continuing to listen...")
                except Exception as e:
                    print(f"❌ Continuous listen error: {e}")
                    time.sleep(1)
        
        continuous_listener = threading.Thread(target=continuous_loop, daemon=True)
        continuous_listener.start()
        
        print("[START] Initializing continuous listening thread...")
        return "Continuous listening started - speak commands directly"
        
    except Exception as e:
        return f"Error starting continuous listening: {str(e)}"

def stop_continuous_listen():
    """Stop continuous listening mode"""
    global continuous_active, continuous_listener
    try:
        continuous_active = False
        continuous_listener = None
        return "Continuous listening stopped"
    except Exception as e:
        return f"Error stopping continuous listening: {str(e)}"

def get_continuous_listen_status():
    """Get continuous listening status"""
    global continuous_active
    try:
        if continuous_active:
            return "Continuous listening is active"
        return "Continuous listening is inactive"
    except Exception as e:
        return f"Error checking status: {str(e)}"

def pause_listening():
    """Pause listening mode"""
    global listening_paused
    try:
        listening_paused = True
        save_ui_setting('listening_paused', True)
        print("🎤 Microphone paused")
        return "Listening paused - microphone stopped"
    except Exception as e:
        return f"Error pausing listening: {str(e)}"

def resume_listening():
    """Resume listening mode"""
    global listening_paused
    try:
        listening_paused = False
        save_ui_setting('listening_paused', False)
        print("🎤 Microphone resumed")
        return "Listening resumed - microphone active"
    except Exception as e:
        return f"Error resuming listening: {str(e)}"

def mute_jarvis():
    """Mute Jarvis voice"""
    global jarvis_muted
    try:
        jarvis_muted = True
        save_ui_setting('jarvis_muted', True)
        print("Jarvis muted")
        return "Jarvis muted"
    except Exception as e:
        return f"Error muting Jarvis: {str(e)}"

def unmute_jarvis():
    """Unmute Jarvis voice"""
    global jarvis_muted
    try:
        jarvis_muted = False
        save_ui_setting('jarvis_muted', False)
        print("Jarvis unmuted")
        return "Jarvis unmuted"
    except Exception as e:
        return f"Error unmuting Jarvis: {str(e)}"

def save_ui_setting(key, value):
    """Save setting to ui_config.json"""
    try:
        import json
        config_file = 'ui_config.json'
        
        # Load existing config
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except:
            config = {}
        
        # Update setting
        config[key] = value
        
        # Save config
        with open(config_file, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving UI setting: {e}")

def load_ui_settings():
    """Load settings from ui_config.json"""
    global listening_paused, jarvis_muted
    try:
        import json
        with open('ui_config.json', 'r') as f:
            config = json.load(f)
        
        listening_paused = config.get('listening_paused', False)
        jarvis_muted = config.get('jarvis_muted', False)
    except Exception as e:
        print(f"Error loading UI settings: {e}")
        listening_paused = False
        jarvis_muted = False

def process_single_command(query):
    """Process a single command using existing logic"""
    global jarvis_muted
    try:
        print(f"Processing single command: '{query}'")
    
    
        
        # Handle unmute command first to bypass mute check
        if "unmute jarvis" in query or "unmute voice" in query:
       
            jarvis_muted = False
            save_ui_setting('jarvis_muted', False)
            print("Jarvis unmuted")
            speak("Jarvis unmuted")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Direct message command with app, name, and message in one command
        if ("send message to" in query and (" on whatsapp " in query or " on mobile " in query)) or \
           ("whatsapp message to" in query) or ("sms to" in query):
        
            try:
                import re
                from engine.features import findContact, whatsApp, sendMessage
                
                # Extract app, name, and message from query
                app_type = "whatsapp" if ("whatsapp" in query or " on whatsapp " in query) else "mobile"
                
                # Extract contact name and message
                if " on whatsapp " in query:
                    # Pattern: "send message to [name] on whatsapp [message]"
                    match = re.search(r'send message to (\w+) on whatsapp (.+)', query)
                elif " on mobile " in query:
                    # Pattern: "send message to [name] on mobile [message]"
                    match = re.search(r'send message to (\w+) on mobile (.+)', query)
                elif "whatsapp message to" in query:
                    # Pattern: "whatsapp message to [name] [message]"
                    match = re.search(r'whatsapp message to (\w+) (.+)', query)
                elif "sms to" in query:
                    # Pattern: "sms to [name] [message]"
                    match = re.search(r'sms to (\w+) (.+)', query)
                    app_type = "mobile"
                else:
                    match = None
                
                if match:
                    contact_name = match.group(1)
                    message_text = match.group(2)
                    
                    # Find contact
                    contact_no, name = findContact(contact_name)
                    if contact_no != 0:
                        if app_type == "whatsapp":
                            whatsApp(contact_no, message_text, 'message', name)
                        else:
                            sendMessage(message_text, contact_no, name)
                    else:
                        speak(f"Contact {contact_name} not found")
                else:
                    speak("Please use format: send message to name on whatsapp your message")
                    
            except Exception as e:
                print(f"Direct message error: {e}")
                speak("Failed to send message")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Contact-based calling and messaging (existing method)
        elif "send message" in query or "phone call" in query or "video call" in query or "call" in query:
    
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode you want to use whatsapp or mobile")
                preference = takecommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query or "call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preference:
                    message = ""
                    schedule_time = None
                    
                    if "send message" in query:
                        message = 'message'
                        
                        # Check for scheduling keywords
                        if " in " in query and any(word in query for word in ["second", "minute", "hour", "sec", "min", "hr"]):
                            # Extract schedule time from query
                            import re
                            time_match = re.search(r'in\s+(\d+\s*(?:second|minute|hour|sec|min|hr)s?)', query)
                            if time_match:
                                schedule_time = time_match.group(1)
                                speak(f"what message to send? It will be scheduled for {schedule_time}")
                            else:
                                speak("what message to send")
                        else:
                            speak("what message to send")
                        
                        query = takecommand()
                                        
                    elif "phone call" in query or "call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name, schedule_time)
            eel.ShowHood()
            return
        
        # SMS Test Commands
        elif "test sms" in query or "sms test" in query:
            from engine.features import testSMS
            testSMS()
            eel.ShowHood()
            return
        
        # Phone Commands (must have "on phone" suffix)
        elif "on phone" in query:
            from engine.phone import handle_phone_commands
            if handle_phone_commands(query):
                eel.ShowHood()
                return
        
        # Voice gender switching commands - HIGHER PRIORITY than language switching
        elif any(phrase in query.lower() for phrase in ["switch to male", "switch to female", "male voice", "female voice", "current voice", "voice status"]):
        
            try:
                from engine.voice_gender_control import voice_control
                query_lower = query.lower()
                
                if "female voice" in query_lower or "switch to female" in query_lower:
                    response = voice_control.switch_to_female()
                    speak(response)
                    print(f"Voice switched to female: {response}")
                elif "male voice" in query_lower or "switch to male" in query_lower:
                    response = voice_control.switch_to_male()
                    speak(response)
                    print(f"Voice switched to male: {response}")
                elif "current voice" in query_lower or "voice status" in query_lower:
                    gender = voice_control.get_current_gender()
                    speak(f"Current voice is set to {gender}")
                    print(f"Current voice gender: {gender}")
                    
            except Exception as e:
                print(f"Voice switch error: {e}")
                speak("Voice switching failed")
            print("Voice gender command completed, returning")
            return
        
        # Language switching commands (exclude voice gender commands)
        elif ("switch to" in query or "change language" in query) and not any(voice_term in query.lower() for voice_term in ["male", "female", "voice"]):
            try:
                from engine.multilingual_support import multilingual
                response = multilingual.process_multilingual_command(query)
                speak(response)
            except Exception as e:
                print(f"Language switch error: {e}")
                speak("Language switching is not available")
            eel.ShowHood()
            return
        
        # Add contact command
        elif "add contact" in query:
            try:
                import re
                import sqlite3
                
                # Extract name and number from query
                match = re.search(r'add contact (\w+) (\d+)', query)
                if match:
                    name = match.group(1)
                    number = match.group(2)
                    
                    # Add to database
                    con = sqlite3.connect("jarvis.db")
                    cursor = con.cursor()
                    cursor.execute('INSERT INTO contacts (name, mobile_no) VALUES (?, ?)', (name, number))
                    con.commit()
                    con.close()
                    
                    speak(f"Contact {name} with number {number} added successfully")
                else:
                    speak("Please say add contact name number")
                    
            except Exception as e:
                print(f"Add contact error: {e}")
                speak("Failed to add contact")
            eel.ShowHood()
            return
        
        # Delete contact command
        elif "delete contact" in query:
            try:
                import re
                import sqlite3
                
                # Extract name from query
                match = re.search(r'delete contact (\w+)', query)
                if match:
                    name = match.group(1)
                    
                    con = sqlite3.connect("jarvis.db")
                    cursor = con.cursor()
                    
                    # Check if contact exists
                    cursor.execute('SELECT name FROM contacts WHERE LOWER(name) LIKE ?', ('%' + name.lower() + '%',))
                    result = cursor.fetchone()
                    
                    if result:
                        cursor.execute('DELETE FROM contacts WHERE LOWER(name) LIKE ?', ('%' + name.lower() + '%',))
                        con.commit()
                        speak(f"Contact {name} deleted successfully")
                    else:
                        speak(f"Contact {name} not found")
                    
                    con.close()
                else:
                    speak("Please say delete contact name")
                    
            except Exception as e:
                print(f"Delete contact error: {e}")
                speak("Failed to delete contact")
            eel.ShowHood()
            return
        
        # View contacts command
        elif "view contacts" in query or "show contacts" in query or "list contacts" in query:
            try:
                import sqlite3
                
                con = sqlite3.connect("jarvis.db")
                cursor = con.cursor()
                cursor.execute('SELECT name, mobile_no FROM contacts')
                results = cursor.fetchall()
                con.close()
                
                if results:
                    contact_list = "Your contacts are: "
                    for contact in results:
                        contact_list += f"{contact[0]} {contact[1]}, "
                    speak(contact_list)
                else:
                    speak("No contacts found")
                    
            except Exception as e:
                print(f"View contacts error: {e}")
                speak("Failed to view contacts")
            eel.ShowHood()
            return
        
        # Emotion detection commands
        elif "start emotion" in query or "enable emotion" in query:
            response = emotion_system.enable()
            speak(response)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "stop emotion" in query or "disable emotion" in query:
            response = emotion_system.disable()
            speak(response)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "emotion status" in query or "current emotion" in query:
            response = emotion_system.get_status()
            speak(response)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "encourage me" in query or "cheer me up" in query:
            encouragement = emotion_system.get_encouraging_response()
            speak(encouragement)
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "make me laugh" in query or "tell joke" in query:
            humor = emotion_system.get_humor_response()
            speak(humor)
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Calendar event scheduling (for events with "at" time)
        elif "add event" in query or ("add" in query and "event" in query):
            try:
                from engine.voice_advanced_ai import get_voice_advanced_response
                response = get_voice_advanced_response(query)
                speak(response)
            except Exception as e:
                speak(f"Calendar scheduling failed: {e}")
            eel.ShowHood()
            return
        
        # Task scheduling (for system tasks with "in" time)
        elif "schedule" in query and "in" in query and "event" not in query:
            try:
                import re
                # Extract command and time
                parts = query.split(" in ", 1)
                command = parts[0].replace("schedule ", "")
                time_part = parts[1]
                
                response = task_scheduler.schedule_task(command, time_part)
                speak(response)
            except Exception as e:
                speak(f"Task scheduling failed: {e}")
            eel.ShowHood()
            return
        elif "list scheduled" in query or "show scheduled" in query:
            response = task_scheduler.list_tasks()
            speak(response)
            eel.ShowHood()
            return
        
        # Calendar commands
        elif "show calendar" in query or "check calendar" in query or "my events" in query:
            try:
                from engine.voice_advanced_ai import get_voice_advanced_response
                response = get_voice_advanced_response(query)
                speak(response)
            except Exception as e:
                speak(f"Calendar display failed: {e}")
            eel.ShowHood()
            return
        
        # Previous command queries - execute must come first
        elif "execute previous command" in query or "run previous command" in query or "repeat last command" in query:
            try:
                recent = command_history.get_recent_commands(10)
                # Find the last command that's not an "execute" or "what is" command
                prev_cmd = None
                for cmd in reversed(recent):
                    if ("execute previous" not in cmd['user_input'].lower() and 
                        "run previous" not in cmd['user_input'].lower() and
                        "repeat last" not in cmd['user_input'].lower() and
                        "what is previous" not in cmd['user_input'].lower() and
                        "last command" not in cmd['user_input'].lower() and
                        "previous command" not in cmd['user_input'].lower()):
                        prev_cmd = cmd['user_input']
                        break
                
                if prev_cmd:
                    speak(f"Executing previous command: {prev_cmd}")
                    process_single_command(prev_cmd)
                else:
                    speak("No previous command to execute")
            except:
                speak("Cannot execute previous command")
            try:
                eel.ShowHood()
            except:
                pass
            return
        elif "what is previous command" in query or "last command" in query or "previous command" in query:
            try:
                recent = command_history.get_recent_commands(10)
                # Find the last command that's not a query command
                prev_cmd = None
                for cmd in reversed(recent):
                    if ("what is previous" not in cmd['user_input'].lower() and 
                        "last command" not in cmd['user_input'].lower() and
                        "previous command" not in cmd['user_input'].lower()):
                        prev_cmd = cmd['user_input']
                        break
                
                if prev_cmd:
                    speak(f"Your previous command was: {prev_cmd}")
                else:
                    speak("No previous command found")
            except:
                speak("Cannot retrieve previous command")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Continuous listening commands
        elif "start continuous" in query or "continuous listen" in query:
            response = start_continuous_listen()
            speak(response)
            eel.ShowHood()
            return
        elif "stop continuous" in query:
            response = stop_continuous_listen()
            speak(response)
            eel.ShowHood()
            return
        elif "continuous status" in query:
            response = get_continuous_listen_status()
            speak(response)
            eel.ShowHood()
            return
        
        # Pause/Resume listening commands
        elif "pause listening" in query:
            response = pause_listening()
            speak(response)
            eel.ShowHood()
            return
        elif "resume listening" in query:
            response = resume_listening()
            speak(response)
            eel.ShowHood()
            return
        
        # Mute/Unmute Jarvis commands
        elif "mute jarvis" in query or "mute voice" in query:
            response = mute_jarvis()
            # Don't speak when muting
            print(response)
            eel.ShowHood()
            return
        # Unmute is handled at the beginning of the function
        
        # Direct website search commands - "open search for ml"
        elif "open" in query and "search for" in query:
            try:
                import webbrowser
                import pyautogui
                import time
                
                # Extract website and search terms
                parts = query.split("search for", 1)
                website_part = parts[0].replace("open", "").strip().lower()
                search_terms = parts[1].strip()
                
                import urllib.parse
                
                # Direct search URLs for specific websites
                search_urls = {
                    'youtube': f'https://www.youtube.com/results?search_query={urllib.parse.quote(search_terms)}',
                    'amazon': f'https://www.amazon.in/s?k={urllib.parse.quote(search_terms)}',
                    'flipkart': f'https://www.flipkart.com/search?q={urllib.parse.quote(search_terms)}',
                    'myntra': f'https://www.myntra.com/{urllib.parse.quote(search_terms)}',
                    'ajio': f'https://www.ajio.com/search/?text={urllib.parse.quote(search_terms)}',
                    'meesho': f'https://www.meesho.com/search?q={urllib.parse.quote(search_terms)}',
                    'wikipedia': f'https://en.wikipedia.org/w/index.php?search={urllib.parse.quote(search_terms)}',
                    'youtube music': f'https://music.youtube.com/search?q={urllib.parse.quote(search_terms)}',
                    'stackoverflow': f'https://stackoverflow.com/search?q={urllib.parse.quote(search_terms)}',
                    'github': f'https://github.com/search?q={urllib.parse.quote(search_terms)}',
                    'npm': f'https://www.npmjs.com/search?q={urllib.parse.quote(search_terms)}',
                    'coursera': f'https://www.coursera.org/search?query={urllib.parse.quote(search_terms)}',
                    'udemy': f'https://www.udemy.com/courses/search/?q={urllib.parse.quote(search_terms)}',
                    'perplexity': f'https://www.perplexity.ai/search?q={urllib.parse.quote(search_terms)}',
                    'linkedin': f'https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(search_terms)}',
                    'linkedin jobs': f'https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(search_terms)}',
                    'google': f'https://www.google.com/search?q={urllib.parse.quote(search_terms)}',
                    'facebook': f'https://www.facebook.com/search/top/?q={urllib.parse.quote(search_terms)}',
                    'twitter': f'https://twitter.com/search?q={urllib.parse.quote(search_terms)}',
                    'instagram': f'https://www.instagram.com/explore/tags/{urllib.parse.quote(search_terms)}',
                    'reddit': f'https://www.reddit.com/search/?q={urllib.parse.quote(search_terms)}',
                    'netflix': f'https://www.netflix.com/search?q={urllib.parse.quote(search_terms)}',
                    'ebay': f'https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(search_terms)}',
                    'pinterest': f'https://www.pinterest.com/search/pins/?q={urllib.parse.quote(search_terms)}',
                    'quora': f'https://www.quora.com/search?q={urllib.parse.quote(search_terms)}',
                    'medium': f'https://medium.com/search?q={urllib.parse.quote(search_terms)}',
                    'dribbble': f'https://dribbble.com/search/{urllib.parse.quote(search_terms)}',
                    'behance': f'https://www.behance.net/search/projects?search={urllib.parse.quote(search_terms)}',
                    'unsplash': f'https://unsplash.com/s/photos/{urllib.parse.quote(search_terms)}',
                    'pixabay': f'https://pixabay.com/images/search/{urllib.parse.quote(search_terms)}',
                    'freepik': f'https://www.freepik.com/search?query={urllib.parse.quote(search_terms)}',
                    'codepen': f'https://codepen.io/search/pens?q={urllib.parse.quote(search_terms)}',
                    'devto': f'https://dev.to/search?q={urllib.parse.quote(search_terms)}',
                    'hashnode': f'https://hashnode.com/search?q={urllib.parse.quote(search_terms)}',
                    'producthunt': f'https://www.producthunt.com/search?q={urllib.parse.quote(search_terms)}',
                    'hackernews': f'https://hn.algolia.com/?q={urllib.parse.quote(search_terms)}',
                    'duckduckgo': f'https://duckduckgo.com/?q={urllib.parse.quote(search_terms)}',
                    'bing': f'https://www.bing.com/search?q={urllib.parse.quote(search_terms)}',
                    'yandex': f'https://yandex.com/search/?text={urllib.parse.quote(search_terms)}',
                    'maps': f'https://www.google.com/maps/search/{urllib.parse.quote(search_terms)}',
                    'zomato': f'https://www.zomato.com/search?q={urllib.parse.quote(search_terms)}',
                    'swiggy': f'https://www.swiggy.com/search?q={urllib.parse.quote(search_terms)}',
                    'bookmyshow': f'https://in.bookmyshow.com/explore/search/{urllib.parse.quote(search_terms)}',
                    'makemytrip': f'https://www.makemytrip.com/search?q={urllib.parse.quote(search_terms)}',
                    'airbnb': f'https://www.airbnb.com/s/{urllib.parse.quote(search_terms)}',
                    'booking': f'https://www.booking.com/searchresults.html?ss={urllib.parse.quote(search_terms)}',
                    'justdial': f'https://www.justdial.com/search/all/{urllib.parse.quote(search_terms)}',
                    'bigbasket': f'https://www.bigbasket.com/ps/?q={urllib.parse.quote(search_terms)}',
                    'nykaa': f'https://www.nykaa.com/search/result/?q={urllib.parse.quote(search_terms)}',
                    'lenskart': f'https://www.lenskart.com/search?q={urllib.parse.quote(search_terms)}',
                    'pharmeasy': f'https://pharmeasy.in/search/all?name={urllib.parse.quote(search_terms)}',
                    'practo': f'https://www.practo.com/search/doctors?results_type=doctor&q={urllib.parse.quote(search_terms)}',
                    'hotstar': f'https://www.hotstar.com/in/search?q={urllib.parse.quote(search_terms)}',
                    'spotify': f'https://open.spotify.com/search/{urllib.parse.quote(search_terms)}',
                    'gaana': f'https://gaana.com/search/{urllib.parse.quote(search_terms)}'
                }
                
                # Regular websites (open and type)
                regular_sites = {
                    'chatgpt': 'https://chat.openai.com',
                    'gemini': 'https://gemini.google.com',
                    'claude': 'https://claude.ai',
                    'bard': 'https://bard.google.com',
                    'copilot': 'https://copilot.microsoft.com'
                }
                
                # Check if website has direct search URL
                if website_part in search_urls:
                    webbrowser.open(search_urls[website_part])
                    speak(f"Searching for {search_terms}")
                elif website_part in regular_sites:
                    webbrowser.open(regular_sites[website_part])
                    speak(f"Opening and typing {search_terms}")
                    time.sleep(3)
                    pyautogui.typewrite(search_terms)
                    pyautogui.press('enter')
                else:
                    # Fallback for unknown websites
                    website_url = f"https://{website_part}.com"
                    webbrowser.open(website_url)
                    speak(f"Opening and typing {search_terms}")
                    time.sleep(3)
                    pyautogui.typewrite(search_terms)
                    pyautogui.press('enter')
                
            except Exception as e:
                print(f"Website search error: {e}")
                speak("Failed to open website")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # General web search with AI
           
        # Browser and Website Management Commands - handle before app management
        elif any(word in query.lower() for word in ['open ', 'launch ', 'run ']) and any(word in query.lower() for word in ['browser', 'web', 'website', 'site']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"Browser/website opener error: {e}")
                speak("Failed to open browser or website")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        elif any(word in query.lower() for word in ['close ', 'quit ', 'exit ', 'kill ']) and any(word in query.lower() for word in ['browser', 'web', 'website', 'site']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"Browser/website closer error: {e}")
                speak("Failed to close browser or website")
            try:
                eel.ShowHood()
            except:
                pass
            return
        

        
        # Direct calculator command - HIGH PRIORITY
        elif "open calculator" in query.lower():
            try:
                import subprocess
                subprocess.Popen('calc', shell=True)
                speak("Calculator opened")
            except Exception as e:
                print(f"Calculator error: {e}")
                speak("Failed to open calculator")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        # Universal App Management Commands - handle before dual AI
        elif any(word in query.lower() for word in ['open ', 'launch ', 'run ']) and not any(word in query.lower() for word in ['file', 'folder']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"App opener error: {e}")
                speak("Failed to open application")
            try:
                eel.ShowHood()
            except:
                pass
            return
        
        elif any(word in query.lower() for word in ['close ', 'quit ', 'exit ', 'kill ']) and not any(word in query.lower() for word in ['file', 'folder', 'browser', 'website']):
            try:
                from engine.new_features import get_new_feature_response
                response = get_new_feature_response(query)
                speak(response)
            except Exception as e:
                print(f"App closer error: {e}")
                speak("Failed to close application")
            try:
                eel.ShowHood()
            except:
                pass
            return
        

        
        # Everything else handled by Dual AI (reliable functions only)
        else:
         
            try:
                from engine.dual_ai import dual_ai
                # Use dual_ai.execute instead of get_simple_response for multilingual support
                response = dual_ai.execute(query)
                print(f"Dual AI response: {response}")
                speak(response)
            except Exception as e:
                print(f"Dual AI Error: {e}")
                # Get error message in current language
                try:
                    from engine.multilingual_support import multilingual
                    speak(multilingual.get_response('processing'))
                except:
                    speak("I'm processing your request")
                    
    except Exception as e:
        print(f"Error in process_single_command: {e}")
        speak("Command failed")

# Load UI settings on startup
load_ui_settings()
import json
import os
from datetime import datetime

class CommandHistory:
    def __init__(self):
        self.history_file = 'command_history.json'
        self.history = []
        self.load_history()
    
    def load_history(self):
        """Load command history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Error loading command history: {e}")
            self.history = []
    
    def save_history(self):
        """Save command history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving command history: {e}")
    
    def add_command(self, user_input, jarvis_response, is_voice=False):
        """Add a command to history"""
        try:
            command_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input,
                'jarvis_response': jarvis_response,
                'input_type': 'voice' if is_voice else 'text'
            }
            
            self.history.append(command_entry)
            
            # Keep only last 100 commands to prevent file from getting too large
            if len(self.history) > 100:
                self.history = self.history[-100:]
            
            self.save_history()
        except Exception as e:
            print(f"Error adding command to history: {e}")
    
    def get_recent_commands(self, count=10):
        """Get recent commands"""
        return self.history[-count:] if len(self.history) >= count else self.history
    
    def search_commands(self, query="", date_filter="", input_type=""):
        """Search commands by query, date, or type"""
        filtered = self.history
        
        if query:
            filtered = [cmd for cmd in filtered if query.lower() in cmd['user_input'].lower()]
        
        if date_filter:
            from datetime import datetime, timedelta
            today = datetime.now()
            if date_filter == "today":
                start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date_filter == "week":
                start_date = today - timedelta(days=7)
            elif date_filter == "month":
                start_date = today - timedelta(days=30)
            else:
                return filtered
            
            filtered = [cmd for cmd in filtered if datetime.fromisoformat(cmd['timestamp']) >= start_date]
        
        if input_type:
            filtered = [cmd for cmd in filtered if cmd['input_type'] == input_type]
        
        return filtered
    
    def get_statistics(self):
        """Get command statistics"""
        if not self.history:
            return {"total": 0, "voice": 0, "text": 0, "most_used": [], "success_rate": 0}
        
        total = len(self.history)
        voice_count = sum(1 for cmd in self.history if cmd['input_type'] == 'voice')
        text_count = total - voice_count
        
        # Count command frequency
        command_freq = {}
        successful = 0
        
        for cmd in self.history:
            base_cmd = cmd['user_input'].strip().lower().split()[0] if cmd['user_input'].strip() else "unknown"
            command_freq[base_cmd] = command_freq.get(base_cmd, 0) + 1
            
            if cmd['jarvis_response'] and "error" not in cmd['jarvis_response'].lower() and "failed" not in cmd['jarvis_response'].lower():
                successful += 1
        
        # Get top 5 most used commands
        most_used = sorted(command_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        success_rate = round((successful / total) * 100, 1) if total > 0 else 0
        
        return {
            "total": total,
            "voice": voice_count,
            "text": text_count,
            "most_used": most_used,
            "success_rate": success_rate
        }
    
    def clear_history(self):
        """Clear all command history"""
        self.history = []
        self.save_history()

# Global instance
command_history = CommandHistory()
ASSISTANT_NAME = "jarvis"
import csv
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()


# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 30]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()

# query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])
"""
Dictation methods for dual_ai.py
"""

def dictate_to_file(self, query=""):
    """Voice-to-text dictation to file"""
    try:
        import speech_recognition as sr
        import re
        import os
        from datetime import datetime
        
        # Extract filename from query
        filename = "dictation.txt"  # default
        mode = "write"  # default
        
        file_match = re.search(r'to file\s+([^\s]+)', query.lower())
        if file_match:
            filename = file_match.group(1).strip()
            if not filename.endswith('.txt'):
                filename += '.txt'
    
        if "append" in query.lower():
            mode = "append"
    
        # Initialize recognizer
        r = sr.Recognizer()
    
        # Start recording
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source)
            print(f"🎤 Dictating to {filename}. Say 'stop dictation' to finish...")
        
            text_content = ""
        
            while True:
                try:
                    # Listen for audio
                    audio = r.listen(source, timeout=1, phrase_time_limit=5)
                
                    # Convert to text
                    text = r.recognize_google(audio)
                
                    # Check for stop command
                    if "stop dictation" in text.lower():
                        break
                
                    # Process punctuation commands
                    text = self._process_punctuation_commands(text)
                
                    text_content += text + " "
                    print(f"📝 {text}")
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    return f"Speech recognition error: {e}"
    
        # Save to file
        if text_content.strip():
            if mode == "append" and os.path.exists(filename):
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write("\n" + text_content.strip())
            else:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text_content.strip())
        
            return f"📝 Dictation saved to {filename} ({len(text_content.split())} words)"
        else:
            return "No speech detected"
        
    except ImportError:
        return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
    except Exception as e:
        return f"Dictation failed: {e}"

def dictate_to_document(self, query=""):
    """Advanced voice-to-text for formatted documents"""
    try:
        import speech_recognition as sr
        import re
        from datetime import datetime
    
        # Determine document type
        doc_type = "word"
        if "google docs" in query.lower():
            doc_type = "gdocs"
        elif "email" in query.lower():
            doc_type = "email"
    
        # Initialize recognizer
        r = sr.Recognizer()
    
        # Start recording
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source)
            print(f"🎤 Dictating to {doc_type}. Say formatting commands like 'bold this', 'new paragraph'...")
        
            document_content = []
            current_text = ""
        
            while True:
                try:
                    # Listen for audio
                    audio = r.listen(source, timeout=1, phrase_time_limit=5)
                
                    # Convert to text
                    text = r.recognize_google(audio)
                
                    # Check for stop command
                    if "stop dictation" in text.lower():
                        break
                
                    # Process formatting commands
                    if self._is_formatting_command(text):
                        formatted_text = self._process_formatting_command(text, current_text)
                        document_content.append(formatted_text)
                        current_text = ""
                    else:
                        # Process punctuation commands
                        text = self._process_punctuation_commands(text)
                        current_text += text + " "
                        print(f"📝 {text}")
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    return f"Speech recognition error: {e}"
    
        # Add remaining text
        if current_text.strip():
            document_content.append(current_text.strip())
    
        # Save formatted document
        if document_content:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
            if doc_type == "email":
                filename = f"email_draft_{timestamp}.txt"
                content = self._format_as_email(document_content)
            elif doc_type == "gdocs":
                filename = f"gdocs_draft_{timestamp}.txt"
                content = self._format_as_document(document_content)
            else:
                filename = f"document_{timestamp}.docx"
                content = self._format_as_document(document_content)
        
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
            word_count = len(' '.join(document_content).split())
            return f"📄 Document saved to {filename} ({word_count} words)\nFormatting commands processed"
        else:
            return "No content dictated"
        
    except ImportError:
        return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
    except Exception as e:
        return f"Document dictation failed: {e}"

def process_punctuation_commands(self, text):
    """Process voice punctuation commands"""
    punctuation_map = {
        'period': '.',
        'comma': ',',
        'question mark': '?',
        'exclamation point': '!',
        'colon': ':',
        'semicolon': ';',
        'new line': '\n',
        'new paragraph': '\n\n'
    }

    for command, punctuation in punctuation_map.items():
        text = text.replace(command, punctuation)

    return text

def is_formatting_command(self, text):
    """Check if text contains formatting commands"""
    formatting_commands = [
        'bold this', 'italic this', 'underline this',
        'bullet point', 'numbered list', 'new paragraph',
        'heading', 'title', 'center this'
    ]

    return any(cmd in text.lower() for cmd in formatting_commands)

def process_formatting_command(self, command, text):
    """Process formatting commands and return formatted text"""
    command_lower = command.lower()

    if 'bold this' in command_lower:
        return f"**{text.strip()}**"
    elif 'italic this' in command_lower:
        return f"*{text.strip()}*"
    elif 'underline this' in command_lower:
        return f"_{text.strip()}_"
    elif 'bullet point' in command_lower:
        return f"• {text.strip()}"
    elif 'numbered list' in command_lower:
        return f"1. {text.strip()}"
    elif 'heading' in command_lower:
        return f"# {text.strip()}"
    elif 'title' in command_lower:
        return f"## {text.strip()}"
    elif 'center this' in command_lower:
        return f"<center>{text.strip()}</center>"
    else:
        return text

def format_as_email(self, content_list):
    """Format content as email"""
    email_content = "Subject: [Your Subject]\n\n"
    email_content += "Dear [Recipient],\n\n"

    for content in content_list:
        email_content += content + "\n\n"

    email_content += "Best regards,\n[Your Name]"
    return email_content

def format_as_document(self, content_list):
    """Format content as document"""
    document_content = ""

    for content in content_list:
        document_content += content + "\n\n"

    return document_content.strip()
import subprocess
import pyautogui
import psutil
from datetime import datetime, timedelta
import json
import os
import ctypes
import shutil
import socket
import time
import random
import requests
import winreg
import base64
import hashlib
import sqlite3
from collections import Counter
from typing import Optional, Dict, Any, List
import zipfile
import re
import warnings
from tkinter import simpledialog
import re, subprocess, urllib.parse
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Import multilingual support
try:
    from engine.multilingual_support import multilingual
except:
    multilingual = None

class DualAI:
    def __init__(self):
        """Initialize DualAI with dictation state"""
        self.ai_provider = self._get_ai_provider()
        self._init_ai_models()
        self.active_alarm = None
        # Load saved alarm
        try:
            import json
            from datetime import datetime
            with open('alarm.json', 'r') as f:
                data = json.load(f)
                saved_time = datetime.fromisoformat(data['time'])
                if saved_time > datetime.now():
                    self.active_alarm = saved_time
                    self._start_alarm_thread(saved_time)
        except:
            pass
        # Initialize multilingual support
        from engine.multilingual_support import multilingual
        self.multilingual = multilingual
        
        # Initialize personality manager
        try:
            from engine.personality_manager import personality_manager
            self.personality_manager = personality_manager
        except:
            self.personality_manager = None
        
        # All system functions
        self.functions = {
            # Power
            'shutdown': lambda: subprocess.run('shutdown /s /t 5', shell=True),
            'restart': lambda: subprocess.run('shutdown /r /t 5', shell=True),
             'sleep': lambda: subprocess.run('powershell -command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)"',shell=True),
            'lock': lambda: subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True),
            'hibernate': lambda: subprocess.run('shutdown /h', shell=True),
            
            # Apps
            'calculator': lambda: subprocess.Popen('calc', shell=True),
            'notepad': lambda: subprocess.Popen('notepad', shell=True),
            'chrome': lambda: subprocess.Popen('start chrome', shell=True),
            'edge': lambda: subprocess.Popen('start msedge', shell=True),
            'explorer': lambda: subprocess.Popen('explorer', shell=True),
            'settings': lambda: subprocess.Popen('start ms-settings:', shell=True),
            'taskmanager': lambda: subprocess.Popen('taskmgr', shell=True),
            'cmd': lambda: subprocess.Popen('cmd', shell=True),
            'paint': lambda: subprocess.Popen('mspaint', shell=True),
            'firefox': lambda: subprocess.Popen('start firefox', shell=True),
            'word': lambda: subprocess.Popen('start winword', shell=True),
            'excel': lambda: subprocess.Popen('start excel', shell=True),
            'powerpoint': self._ai_presentation,
            'vlc': lambda: subprocess.Popen('start vlc', shell=True),
            'vscode': lambda: subprocess.Popen('start code', shell=True),
            'spotify': lambda: subprocess.Popen('start spotify:', shell=True),
            'steam': lambda: subprocess.Popen('start steam', shell=True),
            
            # Websites
            'google': lambda: subprocess.Popen('start chrome https://www.google.com', shell=True),
            'youtube': lambda: subprocess.Popen('start chrome https://www.youtube.com', shell=True),
            'wikipedia': lambda: subprocess.Popen('start chrome https://www.wikipedia.org', shell=True),
            'stackoverflow': lambda: subprocess.Popen('start chrome https://stackoverflow.com', shell=True),
            'github': lambda: subprocess.Popen('start chrome https://github.com', shell=True),
            'amazon': lambda: subprocess.Popen('start chrome https://www.amazon.in', shell=True),
            'flipkart': lambda: subprocess.Popen('start chrome https://www.flipkart.com', shell=True),
            'instagram': lambda: subprocess.Popen('start chrome https://www.instagram.com', shell=True),
            'facebook': lambda: subprocess.Popen('start chrome https://www.facebook.com', shell=True),
            'twitter': lambda: subprocess.Popen('start chrome https://www.twitter.com', shell=True),
            'linkedin': lambda: subprocess.Popen('start chrome https://www.linkedin.com', shell=True),
            'whatsapp_web': lambda: subprocess.Popen('start chrome https://web.whatsapp.com', shell=True),
            'gmail': lambda: subprocess.Popen('start chrome https://mail.google.com', shell=True),
            'netflix': lambda: subprocess.Popen('start chrome https://www.netflix.com', shell=True),
            
            # Volume
            'volume_up': lambda: pyautogui.press('volumeup'),
            'volume_down': lambda: pyautogui.press('volumedown'),
            'mute': lambda: pyautogui.press('volumemute'),
            
            # Screen
            'screenshot': lambda: pyautogui.screenshot().save(f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'),
            'show desktop': lambda: pyautogui.hotkey('win', 'd'),
            'minimize_all': lambda: pyautogui.hotkey('win', 'm'),
            'brightness_up': self._brightness_up,
            'brightness_down': self._brightness_down,
            
            # Keyboard
            'alt_tab': lambda: pyautogui.hotkey('alt', 'tab'),
            'copy': lambda: pyautogui.hotkey('ctrl', 'c'),
            'paste': lambda: pyautogui.hotkey('ctrl', 'v'),
            'save': lambda: pyautogui.hotkey('ctrl', 's'),
            'undo': lambda: pyautogui.hotkey('ctrl', 'z'),
            'select_all': lambda: pyautogui.hotkey('ctrl', 'a'),
            
            # Close apps
            'close_chrome': lambda: subprocess.run('taskkill /f /im chrome.exe', shell=True),
            'close_edge': lambda: subprocess.run('taskkill /f /im msedge.exe', shell=True),
            'close_notepad': lambda: subprocess.run('taskkill /f /im notepad.exe', shell=True),
            
            # Folders
            'downloads': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Downloads")}"', shell=True),
            'documents': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Documents")}"', shell=True),
            'pictures': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Pictures")}"', shell=True),
            'videos': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Videos")}"', shell=True),
            'music': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Music")}"', shell=True),
            'desktop': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "Desktop")}"', shell=True),
            'appdata': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "AppData")}"', shell=True),
            'temp': lambda: subprocess.run('explorer "%TEMP%"', shell=True),
            'programfiles': lambda: subprocess.run('explorer "C:\\Program Files"', shell=True),
            'programfilesx86': lambda: subprocess.run('explorer "C:\\Program Files (x86)"', shell=True),
            'windows': lambda: subprocess.run('explorer "C:\\Windows"', shell=True),
            'system32': lambda: subprocess.run('explorer "C:\\Windows\\System32"', shell=True),
            'startup': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")}"', shell=True),
            'recent': lambda: subprocess.run(f'explorer "{os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Recent")}"', shell=True),
            'open_path': self._open_path,

        
            'open_file': self._open_path,
            'open_folder': self._open_path,
            'launch_file': self._open_path,
            'launch_folder': self._open_path,
            'show_me': self._open_path,
            'find_file': self._open_path,
            'locate_file': self._open_path,
            
            # Random generators
            'dice': self._roll_dice,
            'coin': self._flip_coin,
            'roll_dice': self._roll_dice,
            'flip_coin': self._flip_coin,
            'age_calculator': self._age_calculator,
            'calculate_age': self._age_calculator,
            
            # System info
            'cpu': lambda: psutil.cpu_percent(interval=1),
            'memory': lambda: psutil.virtual_memory().percent,
            'battery': lambda: psutil.sensors_battery().percent if psutil.sensors_battery() else None,
            'time': lambda: datetime.now().strftime('%I:%M %p'),
            'date': lambda: datetime.now().strftime('%A, %B %d, %Y'),
            
            # AI Control
            'switch_to_gemini': self._switch_to_gemini,
            'switch_to_groq': self._switch_to_groq,
            'current_ai': self._get_current_ai,
            'switch_language_hindi': self._switch_to_hindi,
            'switch_language_kannada': self._switch_to_kannada,
            'switch_language_english': self._switch_to_english,
            
            # Calendar
            'schedule': self._schedule_event,
            'show_calendar': self._show_calendar,
            
            # Advanced AI Features
            'daily_briefing': self._daily_briefing,
            'predictive_assistance': self._predictive_assistance,
            'context_memory_store': self._context_memory_store,
            'context_memory_recall': self._context_memory_recall,
            'recall': self._context_memory_recall,
            
            # Security & Authentication
            'file_vault_encrypt': self._file_vault_encrypt,
            'file_vault_decrypt': self._file_vault_decrypt,
            'anomaly_detection': self._anomaly_detection,
            'phishing_scan': self._phishing_scan,
            'parental_control': self._parental_control,
            
            # Cloud & Multi-Device
            'cloud_backup': self._cloud_backup,
            'email_summarize': self._email_summarize,
            'sync_devices': self._sync_devices,
            
            # AI Productivity
            'realtime_transcription': self._realtime_transcription,
            'summarize_meeting': self._summarize_meeting,
            'smart_clipboard': self._smart_clipboard,
            'document_qa': self._document_qa,
            'ai_presentation': self._ai_presentation,
            
            # Smart Home
            'smart_home_control': self._smart_home_control,
            'set_home_scene': self._set_home_scene,
            'security_camera': self._security_camera,
            'energy_monitoring': self._energy_monitoring,
            
            # Entertainment Plus
            'ai_dj_mode': self._ai_dj_mode,
            'trivia_game': self._trivia_game,
            'storytelling': self._storytelling,
            'fitness_coach': self._fitness_coach,
            
            # Health & Wellness
            'posture_detection': self._posture_detection,
            'eye_care_mode': self._eye_care_mode,
            'daily_health_log': self._daily_health_log,
            'mood_tracker': self._mood_tracker,
            'meditation_prompt': self._meditation_prompt,
            
            # System Monitoring
            # 'system_monitor_live': self._system_monitor_live,
            'auto_fix_system': self._auto_fix_system,
            
            # All Advanced AI Features Integration
            'manage_package': self._manage_package,
            'docker_control': self._docker_control,
            'context_memory_store': self._context_memory_store,
            'context_memory_recall': self._context_memory_recall,
            'adaptive_learning': self._adaptive_learning,
            'check_proactive': self._check_proactive,
            'enable_proactive_mode': self._enable_proactive_mode,
            'enable proactive mode': self._enable_proactive_mode,
            'disable_proactive_mode': self._disable_proactive_mode,
            'disable proactive mode': self._disable_proactive_mode,
            'manual_learn': self._manual_learn,
            'file_vault_encrypt': self._file_vault_encrypt,
            'file_vault_decrypt': self._file_vault_decrypt,
            'anomaly_detection': self._anomaly_detection,
            'phishing_scan': self._phishing_scan,
            'parental_control': self._parental_control,
            'calendar_schedule': self._calendar_schedule,
            'cloud_backup': self._cloud_backup,
            'realtime_transcription': self._realtime_transcription,
            'summarize_meeting': self._summarize_meeting,
            'smart_clipboard': self._smart_clipboard,
            'document_qa': self._document_qa,
            'ai_presentation': self._ai_presentation,
            'smart_home_control': self._smart_home_control,
            'set_home_scene': self._set_home_scene,
            'security_camera': self._security_camera,
            'energy_monitoring': self._energy_monitoring,
            'ai_dj_mode': self._ai_dj_mode,
            'trivia_game': self._trivia_game,
            'storytelling': self._storytelling,
            'fitness_coach': self._fitness_coach,
            'debug_screen': self._debug_screen_code,
            'fix_my_code': self._debug_screen_code,
            'check_code': self._debug_screen_code,
            'code_agent': self._code_agent,
            'research_agent': self._research_agent,
            'organizer_agent': self._organizer_agent,
            'multi_agent_collab': self._multi_agent_collab,
            'scholar_search': self._scholar_search,
            'stock_updates': self._stock_updates,
            'crypto_updates': self._crypto_updates,
            'realtime_translation': self._realtime_translation,
            'posture_detection': self._posture_detection,
            'eye_care_mode': self._eye_care_mode,
            'daily_health_log': self._daily_health_log,
            'mood_tracker': self._mood_tracker,
            'meditation_prompt': self._meditation_prompt,
            
            # Face Auth
            'enable_face_auth': self._enable_face_auth,
            'disable_face_auth': self._disable_face_auth,
            'face_auth_status': self._get_face_auth_status,
            
            # Voice Gender Control
            'switch_to_male_voice': self._switch_to_male_voice,
            'switch_to_female_voice': self._switch_to_female_voice,
            'male_voice': self._switch_to_male_voice,
            'female_voice': self._switch_to_female_voice,
            'current_voice_gender': self._get_current_voice_gender,
            'voice_status': self._get_current_voice_gender,
            
            # Token Usage
            'token_usage': self._get_token_usage,
            'tokens_used': self._get_token_usage,
            'token_status': self._get_token_usage,
            'reset_tokens': self._reset_token_count,
            

            
            # Media Controls
            'play_pause': self._play_pause,
            'next_track': self._next_track,
            'previous_track': self._previous_track,
            'stop_media': self._stop_media,
            
            # Window Management
            'maximize_window': self._maximize_window,
            'minimize_window': self._minimize_window,
            'split_screen_left': self._split_screen_left,
            'split_screen_right': self._split_screen_right,
            'close_window': self._close_window,
            'switch_window': self._switch_window,
            
            # Text Operations
            'find_text': self._find_text,
            'replace_text': self._replace_text,
            'new_document': self._new_document,
            'print_document': self._print_document,
            'zoom_in': self._zoom_in,
            'zoom_out': self._zoom_out,
            
            # Security Features
            'clear_clipboard': self._clear_clipboard,
            'clear_history': self._clear_browser_history,
            'empty_recycle_bin': self._empty_recycle_bin,
            'lock_screen': self._lock_screen,
            
            # Automation
          
            'schedule_shutdown': self._schedule_shutdown,
            'auto_backup': self._backup_files,
            'clean_temp': self._clean_temp_files,
            
            # Entertainment
            'play_music': self._play_music,
            'random_wallpaper': self._change_wallpaper,
            'joke': self._tell_joke,
   
            'news': self._get_news,
            'quote': self._get_quote,
            
            # Voice Mouse Control
            'move_mouse_up': self._move_mouse_up,
            'move_mouse_down': self._move_mouse_down,
            'move_mouse_left': self._move_mouse_left,
            'move_mouse_right': self._move_mouse_right,
            'move_mouse_center': self._move_mouse_center,
            'left_click': self._left_click,
            'right_click': self._right_click,
            'double_click': self._double_click,
            'start_drag': self._start_drag,
            'drop_here': self._drop_here,
            'scroll_up': self._scroll_up,
            'scroll_down': self._scroll_down,
            'scroll_to_top': self._scroll_to_top,
            
            # Voice Keyboard Control
            'type_text': self._type_text,
            'press_enter': self._press_enter,
            'press_tab': self._press_tab,
            'press_escape': self._press_escape,
            'press_backspace': self._press_backspace,
            'press_delete': self._press_delete,
            'go_to_beginning': self._go_to_beginning,
            'go_to_end': self._go_to_end,
            
            # ALL ADVANCED FEATURES INTEGRATED
            # File Operations
            'create_folder': self._create_folder,
            'delete_file': self._delete_file,
            'search_files': self._search_files,
            'copy_file': self._copy_file,
            'move_file': self._move_file,
            'rename_file': self._rename_file_cmd,
            'zip_file': self._zip_file,
            'unzip_file': self._unzip_file,
            'file_size': self._get_file_size,
            'list_files': self._list_files,
            
            # Network & Internet
            'check_internet': self._ping_test,
            'ip_address': self._get_ip,
            'wifi_password': self._get_wifi_password,
            'network_speed': self._speed_test,
            
            # System Monitoring
            'disk_space': self._get_disk_space,
            'running_processes': self._list_processes,
            'system_uptime': self._get_uptime,
            'temperature': self._get_cpu_temp,
            
            # Advanced Window Management
            'next_window': self._next_window,
            'previous_window': self._previous_window,
            'close_all_windows': self._close_all_windows,
            'snap_left': self._snap_left,
            'snap_right': self._snap_right,
            'full_screen': self._full_screen,
            'restore_window': self._restore_window,
            
            # Advanced File Operations
            'open_recent_file': self._open_recent_file,
            'create_new_file': self._create_new_file,
            'rename_file': self._rename_file,
            'duplicate_file': self._duplicate_file,
            'compress_file': self._compress_file,
            'extract_archive': self._extract_archive,
            
            # Web Browsing Control
            'open_new_tab': self._open_new_tab,
            'close_current_tab': self._close_current_tab,
            'switch_to_next_tab': self._switch_to_next_tab,
            'switch_to_previous_tab': self._switch_to_previous_tab,
            'refresh_page': self._refresh_page,
            'go_back': self._go_back,
            'go_forward': self._go_forward,
            'bookmark_page': self._bookmark_page,
            'open_bookmarks': self._open_bookmarks,
            'search_web': self._search_web,
            
            # Advanced Media Control
            'skip_forward': self._skip_forward,
            'skip_backward': self._skip_backward,
            'increase_speed': self._increase_speed,
            'decrease_speed': self._decrease_speed,
            'toggle_fullscreen': self._toggle_fullscreen,
            'toggle_subtitles': self._toggle_subtitles,
            
            # Voice Dictation
            'start_dictation': self._start_dictation,
            'stop_dictation': self._stop_dictation,
  
            
            # Screen Control
            'take_screenshot_window': self._take_screenshot_window,
            'take_screenshot_area': self._take_screenshot_area,
            'start_screen_recording': self._start_screen_recording,
            'stop_screen_recording': self._stop_screen_recording,

            

            # Learning & Education
            'wikipedia_search': self._wikipedia_search,
            
            # Entertainment Plus
            'movie_recommend': self._movie_recommend,
         
            'game_launch': self._game_launch,
            'streaming_control': self._streaming_control,
            'playlist_manage': self._playlist_manage,
            
          
            
            # Built-in Entertainment
            'tell_joke': self._tell_joke,
            'get_quote': self._get_quote,
       
            'get_news': self._get_news,
            
            # YouTube Automation
            'youtube_play': self._youtube_play,
            'youtube_pause': self._youtube_pause,
            'youtube_next': self._youtube_next,
            'youtube_previous': self._youtube_previous,
            'youtube_fullscreen': self._youtube_fullscreen,
            'youtube_volume_up': self._youtube_volume_up,
            'youtube_volume_down': self._youtube_volume_down,
            'youtube_mute': self._youtube_mute,
            'youtube_speed_up': self._youtube_speed_up,
            'youtube_speed_down': self._youtube_speed_down,
            'youtube_skip_forward': self._youtube_skip_forward,
            'youtube_skip_backward': self._youtube_skip_backward,
            'youtube_search': self._youtube_search,
            'youtube_subscribe': self._youtube_subscribe,
            'youtube_like': self._youtube_like,
            'youtube_dislike': self._youtube_dislike,
            'youtube_comment': self._youtube_comment,
            'youtube_share': self._youtube_share,
            'youtube_theater_mode': self._youtube_theater_mode,
            'youtube_miniplayer': self._youtube_miniplayer,
            'youtube_captions': self._youtube_captions,
            'play_video': self._play_video,
            'play_movie': self._play_movie,
            'play_song': self._play_song,
            'search_and_play': self._search_and_play,
            
            # Multiple App/Website Opening
     
            
            # Chrome Automation
            'chrome_new_tab': self._chrome_new_tab,
            'chrome_close_tab': self._chrome_close_tab,
            'chrome_next_tab': self._chrome_next_tab,
            'chrome_previous_tab': self._chrome_previous_tab,
            'chrome_reload': self._chrome_reload,
            'chrome_back': self._chrome_back,
            'chrome_forward': self._chrome_forward,
            'chrome_home': self._chrome_home,
            'chrome_bookmark': self._chrome_bookmark,
            'chrome_history': self._chrome_history,
            'chrome_downloads': self._chrome_downloads,
            'chrome_incognito': self._chrome_incognito,
            'chrome_developer_tools': self._chrome_developer_tools,
            'chrome_zoom_in': self._chrome_zoom_in,
            'chrome_zoom_out': self._chrome_zoom_out,
            'chrome_zoom_reset': self._chrome_zoom_reset,
            'chrome_find': self._chrome_find,
            'chrome_print': self._chrome_print,
            'chrome_save_page': self._chrome_save_page,
            'chrome_view_source': self._chrome_view_source,
            'chrome_extensions': self._chrome_extensions,
            'chrome_settings': self._chrome_settings,
            'chrome_clear_data': self._chrome_clear_data,
            
            # Proactive mode commands
            'enable proactive mode': self._enable_proactive_mode,
            'disable proactive mode': self._disable_proactive_mode,
            
            # Gesture Control
            'start_gesture_control': self._start_gesture_control,
            'stop_gesture_control': self._stop_gesture_control,
            'hand_control': self._start_gesture_control,
            'eye_control': self._start_gesture_control,
            'head_control': self._start_gesture_control,
            'gesture_control': self._start_gesture_control,
            'start gesture control': self._start_gesture_control,
            'stop gesture control': self._stop_gesture_control,
            
            # Code Review Functions
            'code_review': self._code_review,
            'folder_review': self._folder_review,
            'file_review': self._file_review,
            'live_code_review': self._live_code_review,
            'start_live_review': self._start_live_review,
            'stop_live_review': self._stop_live_review,
            
            # Code Writer Functions
            'write_code': self._write_code,
            'create_project': self._create_project,
            'generate_code': self._write_code,
            'code_generator': self._write_code,
            'build_project': self._create_project,
            'make_project': self._create_project,
            
            # Mapping Functions
            'open_maps': self._open_maps,
            'find_location': self._find_location,
            'get_directions': self._get_directions,
            'nearby_places': self._nearby_places,
            'traffic_info': self._traffic_info,
            'map_satellite': self._map_satellite,
            'map_terrain': self._map_terrain,
            'save_location': self._save_location,
            'my_location': self._my_location,
            'dictate_to_file': self._dictate_to_file,
            'dictate_to_document': self._dictate_to_document,
            'start_dictation': self._start_dictation,
            'stop_dictation': self._stop_dictation,
            'dictate_anywhere': self._dictate_anywhere,
            
            # Advanced File Management
            'search_content': self._search_content,
            'find_similar': self._find_similar_files,
            'suggest_folder': self._suggest_folder,
            'map_relationships': self._map_file_relationships,
            
            # Google Search
            'search_google': self._search_google,
            'search_images': self._search_images,
            'search_gifs': self._search_gifs,
            'copy_webpage_link': self._copy_webpage_link,
            'translate_webpage': self._translate_webpage,
            'check_website_status': self._check_website_status,
            'play_radio': self._play_radio,
            'play_podcast': self._play_podcast,
            'weekday': self._get_weekday,
            'current_weekday': self._get_weekday,
            'traffic_updates': self._get_traffic,
            'public_holidays': self._get_holidays,
            'covid_stats': self._get_covid_stats,
            
            # Product Price Tracking
            'track_amazon_price': self._track_amazon_price,
            'track_flipkart_price': self._track_flipkart_price,
            'check_product_price': self._check_product_price,
            
            # DEBUG Product Price Tracking
            'track_amazon_price_debug': self._track_amazon_price_debug,
            'track_flipkart_price_debug': self._track_flipkart_price_debug,
            'check_product_price_debug': self._check_product_price_debug,
            
            # Timer & Stopwatch
            'countdown_timer': self._countdown_timer,
            'start_timer': self._countdown_timer,
            'set_timer': self._countdown_timer,
            'start_stopwatch': self._start_stopwatch,
            'stop_stopwatch': self._stop_stopwatch,
            'reset_stopwatch': self._reset_stopwatch,
            'show_elapsed': self._show_elapsed,
            
            # Mini Games
            'open_mini_game': self._open_mini_game,
            'play_game': self._open_mini_game,
            'launch_game': self._open_mini_game,
            
            # Travel Search
            'search_flights': self._search_flights,
            'search_hotels': self._search_hotels,
            'find_flights': self._search_flights,
            'find_hotels': self._search_hotels,
            
            # Streaming Search
            'find_movie_streaming': self._find_movie_streaming,
            'find_show_streaming': self._find_show_streaming,
            'where_to_watch': self._where_to_watch,
            'streaming_availability': self._streaming_availability,
            
            # Continuous Listening Functions
            
            
            
            # Smart Clipboard Assistant
            'clipboard_assistant': self._clipboard_assistant,
            'start_clipboard_assistant': self._start_clipboard_assistant,
            'stop_clipboard_assistant': self._stop_clipboard_assistant,
            'set_alarm': self._set_alarm,
            'cancel_alarm': self._cancel_alarm,
            
            # AI Image Generation
            'create_image': self._create_image,
            'generate_image': self._create_image,
            'make_image': self._create_image,
            'ai_image': self._create_image,
            
            # AI Video Generation
            'create_video': self._create_video,
            'generate_video': self._create_video,
            'make_video': self._create_video,
            'ai_video': self._create_video,
            
            # File Sorting
            'sort_files': self._sort_files,
            'ai_document': self._ai_document_maker,
            'create_document': self._ai_document_maker,
            'create_report': self._ai_document_maker,
            'create_letter': self._ai_document_maker,

        }
    
    # Ambient Awareness Methods
 
    def _get_ai_provider(self):
        try:
            with open('ai_config.json', 'r') as f:
                config = json.load(f)
                return config.get('ai_provider', 'groq')
        except:
            return 'groq'
    
    def _set_ai_provider(self, provider):
        try:
            config = {'ai_provider': provider}
            with open('ai_config.json', 'w') as f:
                json.dump(config, f)
            self.ai_provider = provider
            self._init_ai_models()
            return True
        except:
            return False
    
    def _init_ai_models(self):
        if self.ai_provider == 'groq':
            try:
                from groq import Groq
                from engine.groq_config import GROQ_API_KEY
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                self.primary_model = "llama-3.1-8b-instant"
                self.fallback_model = "llama-3.3-70b-versatile"
                self.token_count = 0
                self.token_limit = 6000
                # Test the API key with a simple request
                test_response = self.groq_client.chat.completions.create(
                    model=self.primary_model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
            except Exception as e:
                print(f"Groq failed: {e}, switching to Gemini")
                self.ai_provider = 'gemini'
                self._init_gemini()

        elif self.ai_provider == 'ollama':
            pass
        else:
            self._init_gemini()
        
        # Initialize Ollama as fallback
        self._init_ollama()
        
        # Initialize GPT4All as final fallback
        self._init_gpt4all()
    
    def _get_groq_model(self):
        """Get appropriate Groq model based on token usage"""
        if self.token_count >= self.token_limit:
            print(f"Token limit reached ({self.token_count}/{self.token_limit}), switching to 70B model")
            return self.fallback_model
        return self.primary_model
    
    def _reset_token_count(self):
        """Reset token count (call this every minute or when needed)"""
        self.token_count = 0
        return "Token count reset to 0"
    
    def _get_token_usage(self):
        """Get current token usage status"""
        if self.ai_provider == 'groq':
            percentage = (self.token_count / self.token_limit) * 100
            current_model = "70B" if self.token_count >= self.token_limit else "8B"
            return f"Tokens used: {self.token_count}/{self.token_limit} ({percentage:.1f}%) - Current model: {current_model}"
        else:
            return "Token tracking only available for Groq AI"
               
     
    
    def _init_gemini(self):
        try:
            import google.generativeai as genai
            from engine.gemini_config import GEMINI_API_KEY
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            print("Using Gemini AI")
        except Exception as e:
            print(f"AI init error: {e}")
    
    def _init_ollama(self):
        """Initialize Ollama client for local Llama model"""
        try:
            from engine.ollama_client import ollama_client
            # Test connection
            success, message = ollama_client.test_connection()
            if success:
                self.ollama_client = ollama_client
                print(f"Ollama initialized: {message}")
            else:
                print(f"Ollama not available: {message}")
                self.ollama_client = None
        except Exception as e:
            print(f"Ollama init error: {e}")
            self.ollama_client = None
    
    def _init_gpt4all(self):
        """Initialize GPT4All as final fallback"""
        try:
            from gpt4all import GPT4All
            import os
            
            # Use model from GPT4All default directory
            model_path = r"C:\Users\Hp\AppData\Local\nomic.ai\GPT4All"
            available_models = [
                "Llama-3.2-1B-Instruct-Q4_0.gguf",
            ]
            
            model_name = None
            for model in available_models:
                if os.path.exists(os.path.join(model_path, model)):
                    model_name = model
                    break
            
            if model_name:
                self.local_model = GPT4All(
                    model_name,
                    model_path=model_path,
                    verbose=False,
                    device='cpu',
                    n_threads=6,
                    n_ctx=1024
                )
                print(f"SUCCESS: GPT4All {model_name} initialized (optimized)")
            else:
                print("No GPT4All models found in default directory")
                self.local_model = None
        except Exception as e:
            print(f"ERROR: GPT4All init failed: {e}")
            self.local_model = None
    
    def execute(self, query):
        try:
            # Store current query for functions that need it
            self._current_query = query
            
            # Handle timer/stopwatch commands - ABSOLUTE HIGHEST PRIORITY
            query_lower = query.lower().strip()
            if 'stopwatch' in query_lower:
                if 'start' in query_lower:
                    return self._start_stopwatch()
                elif 'stop' in query_lower:
                    return self._stop_stopwatch()
                elif 'reset' in query_lower:
                    return self._reset_stopwatch()
                elif 'show' in query_lower or 'elapsed' in query_lower:
                    return self._show_elapsed()
            elif any(word in query_lower for word in ['timer', 'countdown']) and any(num.isdigit() for num in query_lower.split()):
                return self._countdown_timer()
            
            # Handle game commands - VERY HIGH PRIORITY
            if 'play' in query_lower and any(game in query_lower for game in ['chess', 'snake', 'tetris', '2048', 'dino', 'mario', 'solitaire', 'sudoku', 'game']):
                return self._open_mini_game()
            
            # Handle image creation commands FIRST (highest priority)
            if any(cmd in query_lower for cmd in ['create image', 'generate image', 'make image', 'ai image']):
                return self._create_image()
            
            # Handle video creation commands (highest priority)
            if any(cmd in query_lower for cmd in ['create video', 'generate video', 'make video', 'ai video']):
                return self._create_video()
            
            # Handle clipboard assistant commands FIRST (highest priority)
            if 'clipboard assistant' in query_lower:
                if 'start' in query_lower:
                    return self._start_clipboard_assistant()
                elif 'stop' in query_lower:
                    return self._stop_clipboard_assistant()
                else:
                    return self._clipboard_assistant()
            
        
            
            # Handle voice gender switching commands FIRST (highest priority)
            
            # Exact voice command matching
            if 'female voice' in query_lower:
                return self._switch_to_female_voice()
            elif 'male voice' in query_lower:
                return self._switch_to_male_voice()
            elif 'switch to female' in query_lower:
                return self._switch_to_female_voice()
            elif 'switch to male' in query_lower:
                return self._switch_to_male_voice()
            elif 'current voice' in query_lower or 'voice status' in query_lower:
                return self._get_current_voice_gender()
            
            # Handle token usage commands
            if any(cmd in query_lower for cmd in ['token usage', 'tokens used', 'token status']):
                return self._get_token_usage()
            elif 'reset tokens' in query_lower:
                return self._reset_token_count()
            
            # Process multilingual commands AFTER English commands
            # Skip multilingual processing for basic English "open" commands
            if not query.lower().startswith('open ') and self.multilingual:
                # Check if it's a language switching command
                if any(word in query.lower() for word in ['switch to', 'change language', 'भाषा', 'ভাষা', 'ભાষા', 'ಭಾಷೆ', 'ഭാഷ', 'भाषा', 'மொழி', 'భాష', 'زبان']):
                    response = self.multilingual.process_multilingual_command(query)
                    return response
                
                # Process command in current language context only for non-English commands
                detected_lang = self.multilingual.detect_language(query)
                if detected_lang != 'english':
                    response = self.multilingual.process_command_in_language(query, self.multilingual.current_language)
                    if response != self.multilingual.get_response('processing'):
                        return response
            # Handle continuous listening commands FIRST
            query_clean = query.lower().strip()
          
            
            # Handle code review commands FIRST to prevent interference
            if query_clean == 'code review':
                return self._code_review()
            
            if query_clean == 'folder review' or query_clean == 'review':
                return self._folder_review()
            
                        # Check new features FIRST before any other processing
            new_feature_result = self._check_new_features(query)
            if new_feature_result:
                return new_feature_result
            
            if query_clean.startswith('folder review '):
                folder_name = query[14:].strip()
                return self._folder_review(folder_name)
            
            if "start dictation" in query_lower or "begin dictation" in query_lower or "start writing" in query_lower:
                return self._start_dictation(query)
            elif "stop dictation" in query_lower or "end dictation" in query_lower or "stop writing" in query_lower:
                return self._stop_dictation()
            elif "dictate document" in query_lower:
                return self._dictate_document(query)
            elif "dictate email" in query_lower:
                return self._dictate_document(query, "email")
            elif "dictate anywhere" in query_lower or "write anywhere" in query_lower:
                return self._dictate_anywhere(query)
            
            
            if query_clean.startswith('file review '):
                file_path = query[12:].strip()
                return self._file_review(file_path)
            
            if query_clean == 'start live review':
                return self._start_live_review()
            
            if query_clean == 'stop live review':
                return self._stop_live_review()
            
            if query_clean == 'live code review':
                return self._live_code_review()
            
            # Skip all other processing for review commands
            if 'review' in query_clean and not query_clean.startswith('folder review ') and not query_clean.startswith('live'):
                return self._folder_review()
            
            # Check for dynamic commands - HIGHEST PRIORITY
            import re
            
            # Volume/brightness with numbers - PROCESS IMMEDIATELY
            volume_match = re.search(r'(?:set )?volume (?:to )?([0-9]+)', query.lower())
            brightness_match = re.search(r'(?:set )?brightness (?:to )?([0-9]+)', query.lower())
            
            if volume_match:
                level = int(volume_match.group(1))
                self._set_volume(level)
                return f"Volume set to {level}%"
            
            if brightness_match:
                level = int(brightness_match.group(1))
                self._set_brightness(level)
                return f"Brightness set to {level}%"
            
            # Handle age calculation commands - HIGH PRIORITY
            if 'my age' in query.lower() or 'calculate my age' in query.lower() or 'age calculator' in query.lower():
                return self._age_calculator()
            
            # Handle code writer commands - HIGH PRIORITY
            if any(cmd in query.lower() for cmd in ['write code', 'generate code', 'create code', 'code generator', 'write python code', 'write javascript code', 'write java code', 'write c++ code', 'write c# code', 'write html code', 'write css code', 'write php code', 'write ruby code', 'write go code', 'write rust code', 'write swift code', 'write kotlin code']):
                return self._write_code()
            
            # Handle project creation commands - HIGH PRIORITY
            if any(cmd in query.lower() for cmd in ['create project', 'build project', 'make project']):
                return self._create_project()
            
            # Handle "create document" commands - HIGH PRIORITY
            if any(cmd in query.lower() for cmd in ['create document', 'create report', 'create letter']):
                return self._ai_document_maker()
            
            # Handle "create file" commands - HIGH PRIORITY
            if 'create file' in query.lower() or 'new file' in query.lower():
                result = self._create_new_file()
                return result
            
            # Handle "copy file" commands - HIGH PRIORITY
            if query.lower().startswith('copy ') and ' to ' in query.lower():
                result = self._copy_file()
                return result
            
            # Handle "move file" commands - HIGH PRIORITY
            if query.lower().startswith('move ') and ' to ' in query.lower():
                result = self._move_file()
                return result
            
            # Handle file operations
            if query.lower().startswith('rename '):
                return self._rename_file_cmd()
            if query.lower().startswith('delete ') and 'file' in query.lower():
                return self._delete_file()
            if 'zip' in query.lower() and 'file' in query.lower():
                return self._zip_file()
            if 'unzip' in query.lower() or 'extract' in query.lower():
                return self._unzip_file()
            if 'file size' in query.lower():
                return self._get_file_size()
            if 'list files' in query.lower():
                return self._list_files()
            if 'find file' in query.lower() or 'search file' in query.lower():
                return self._find_file()
            if 'duplicate' in query.lower() and 'file' in query.lower():
                return self._find_duplicates()
            if 'large file' in query.lower() or 'big file' in query.lower():
                return self._find_large_files()
            if 'empty folder' in query.lower():
                return self._find_empty_folders()
            if 'file info' in query.lower():
                return self._get_file_info()
            if 'backup' in query.lower() and 'folder' in query.lower():
                return self._backup_folder()
            if 'search content' in query.lower() or 'content search' in query.lower():
                return self._search_content()
            if 'find similar' in query.lower() or 'similar files' in query.lower():
                return self._find_similar_files()
            if 'suggest folder' in query.lower() or 'smart folder' in query.lower():
                return self._suggest_folder()
            if 'map relationships' in query.lower() or 'file relationships' in query.lower():
                return self._map_file_relationships()
           
            
            # Handle Google search commands
            if 'search google' in query.lower() or 'google search' in query.lower():
                return self._search_google()
            
            # Handle Wikipedia search commands (with typo handling)
            if 'wikipedia search' in query.lower() or 'wekipidea search' in query.lower() or 'wiki search' in query.lower():
                search_term = re.sub(r'(?:wikipedia|wekipidea|wiki)\s+search\s+(?:for\s+)?', '', query.lower()).strip()
                return self._wikipedia_search(search_term)
            
            # Handle image search commands
            if 'search images' in query.lower() or 'image search' in query.lower() or 'search for images' in query.lower():
                return self._search_images()
            
            # Handle GIF search commands
            if 'search gifs' in query.lower() or 'gif search' in query.lower() or 'search for gifs' in query.lower():
                return self._search_gifs()
            
            # Handle copy webpage link commands
            if 'copy link' in query.lower() or 'copy webpage link' in query.lower() or 'copy url' in query.lower():
                return self._copy_webpage_link()
            
            # Handle translate webpage commands
            if 'translate page' in query.lower() or 'translate webpage' in query.lower() or 'translate this page' in query.lower():
                return self._translate_webpage()
            
            # Handle website status check commands
            if 'check website' in query.lower() or 'website status' in query.lower() or 'is website up' in query.lower():
                return self._check_website_status()
            
            # Handle radio commands
            if 'play radio' in query.lower() or 'online radio' in query.lower() or 'radio station' in query.lower():
                return self._play_radio()
            
            # Handle podcast commands
            if 'play podcast' in query.lower() or 'online podcast' in query.lower() or 'listen podcast' in query.lower():
                return self._play_podcast()
            
            # Handle radio commands before YouTube search
            if 'radio' in query.lower() and ('play' in query.lower() or 'listen' in query.lower()):
                return self._play_radio()
            
            # Handle traffic commands - HIGH PRIORITY
            if 'traffic' in query.lower() and ('updates' in query.lower() or 'info' in query.lower() or 'conditions' in query.lower() or query.lower().strip() == 'traffic'):
                return self._get_traffic()
            

            

            
            # Handle travel search commands - HIGH PRIORITY
            if 'search' in query.lower():
                if 'flight' in query.lower() or 'flights' in query.lower():
                    return self._search_flights()
                elif 'hotel' in query.lower() or 'hotels' in query.lower():
                    return self._search_hotels()
            
            # Handle price tracking commands - HIGH PRIORITY
            if 'track' in query.lower() and 'price' in query.lower():
                if 'amazon' in query.lower():
                    return self._track_amazon_price_debug()
                elif 'flipkart' in query.lower():
                    return self._track_flipkart_price_debug()
                else:
                    return self._check_product_price_debug()
            
            # Handle reminder commands - HIGHEST PRIORITY
            if 'set reminder' in query.lower() or 'remind me' in query.lower() or 'task reminder' in query.lower():
                try:
                    from engine.new_features import task_reminder
                    return task_reminder(query)
                except Exception as e:
                    return f"Reminder feature error: {str(e)}"
            
            # Handle AI presentation commands - HIGHEST PRIORITY
            if any(phrase in query.lower() for phrase in ['make slides', 'create slides', 'create presentation', 'make presentation', 'slides of', 'presentation of', 'create ppt', 'make ppt']):
                return self._ai_presentation()
            
            # Handle "open" commands - HIGHEST PRIORITY
            if query.lower().startswith('open '):
                content = query[5:].strip().lower()  # Remove 'open '
                
                # Direct mappings for open commands
                direct_mappings = {
                    'facebook': 'facebook',
                    'instagram': 'instagram',
                    'google': 'google',
                    'youtube': 'youtube',
                    'gmail': 'gmail',
                    'twitter': 'twitter',
                    'linkedin': 'linkedin',
                    'whatsapp': 'whatsapp_web',
                    'netflix': 'netflix',
                    'amazon': 'amazon',
                    'flipkart': 'flipkart',
                    'wikipedia': 'wikipedia',
                    'stackoverflow': 'stackoverflow',
                    'github': 'github',
                    'notepad': 'notepad',
                    'calculator': 'calculator',
                    'chrome': 'chrome',
                    'edge': 'edge',
                    'firefox': 'firefox',
                    'word': 'word',
                    'excel': 'excel',
                    'powerpoint': 'powerpoint',
                    'vlc': 'vlc',
                    'vscode': 'vscode',
                    'spotify': 'spotify',
                    'steam': 'steam',
                    'explorer': 'explorer',
                    'settings': 'settings',
                    'taskmanager': 'taskmanager',
                    'cmd': 'cmd',
                    'paint': 'paint'
                }
                
                # Check for exact single command match first
                if content in direct_mappings:
                    func_name = direct_mappings[content]
                    try:
                        result = self.functions[func_name]()
                        return self._get_response(func_name, result)
                    except Exception as e:
                        return f"Error opening {content}"
                
            
                
                # If not found in direct mappings, try original function check
                if content in self.functions:
                    result = self.functions[content]()
                    return self._get_response(content, result)
            
            # Handle volume commands with better parsing
            if 'volume' in query.lower():
                if 'up' in query.lower() or 'increase' in query.lower():
                    result = self.functions['volume_up']()
                    return self._get_response('volume_up', result)
                elif 'down' in query.lower() or 'decrease' in query.lower():
                    result = self.functions['volume_down']()
                    return self._get_response('volume_down', result)
                elif 'mute' in query.lower():
                    result = self.functions['mute']()
                    return self._get_response('mute', result)
            
        
            
            # Handle brightness commands
            if 'brightness' in query.lower():
                if 'up' in query.lower() or 'increase' in query.lower():
                    result = self.functions['brightness_up']()
                    return self._get_response('brightness_up', result)
                elif 'down' in query.lower() or 'decrease' in query.lower():
                    result = self.functions['brightness_down']()
                    return self._get_response('brightness_down', result)
            
            # Chrome automation commands
            if query.lower().startswith('chrome '):
                chrome_cmd = query.lower().replace('chrome ', '').strip().replace(' ', '_')
                # Handle singular/plural variations
                if chrome_cmd == 'setting':
                    chrome_cmd = 'settings'
                chrome_function = f'chrome_{chrome_cmd}'
                if chrome_function in self.functions:
                    result = self.functions[chrome_function]()
                    return self._get_response(chrome_function, result)
            
            # YouTube automation commands  
            if query.lower().startswith('youtube '):
                youtube_cmd = query.lower().replace('youtube ', '').strip()
                # Handle common variations
                if 'next video' in youtube_cmd or 'next song' in youtube_cmd:
                    youtube_cmd = 'next'
                elif 'previous video' in youtube_cmd or 'previous song' in youtube_cmd:
                    youtube_cmd = 'previous'
                elif 'skip forward' in youtube_cmd:
                    youtube_cmd = 'skip_forward'
                elif 'skip backward' in youtube_cmd or 'skip back' in youtube_cmd:
                    youtube_cmd = 'skip_backward'
                
                youtube_cmd = youtube_cmd.replace(' ', '_')
                youtube_function = f'youtube_{youtube_cmd}'
                if youtube_function in self.functions:
                    result = self.functions[youtube_function]()
                    return self._get_response(youtube_function, result)
            
            # Email summarization with content
            if query.lower().startswith('summarize email '):
                email_content = query[16:].strip()  # Remove 'summarize email '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.email_summarize(email_content)
                except:
                    return "Error summarizing email"
            
            # Calendar commands - force use of voice_advanced_ai
            if 'show calendar' in query.lower() or 'check calendar' in query.lower() or 'add event' in query.lower():
                try:
                    from engine.voice_advanced_ai import get_voice_advanced_response
                    return get_voice_advanced_response(query)
                except:
                    pass
            
            # Package management commands
            if query.lower().startswith('install '):
                package = query[8:].strip()  # Remove 'install '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.install_package(package)
                except:
                    return "Error installing package"
            
            if query.lower() == 'list packages':
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.list_packages()
                except:
                    return "Error listing packages"
            
            # Check for research agent before search patterns
            if 'research agent' in query.lower() or 'research help' in query.lower():
                return self._research_agent()
            
            # Health & Wellness dynamic commands
            if query.lower().startswith('health log '):
                entry = query[11:].strip()  # Remove 'health log '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.daily_health_log(entry)
                except:
                    return "Error logging health data"
            
            if query.lower().startswith('mood tracker ') or query.lower().startswith('track mood '):
                if query.lower().startswith('mood tracker '):
                    mood = query[13:].strip()  # Remove 'mood tracker '
                else:
                    mood = query[11:].strip()  # Remove 'track mood '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.mood_tracker(mood)
                except:
                    return "Error tracking mood"
            
            if query.lower().startswith('meditate ') or query.lower().startswith('meditation '):
                if query.lower().startswith('meditate '):
                    duration = query[9:].strip()  # Remove 'meditate '
                else:
                    duration = query[11:].strip()  # Remove 'meditation '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    if duration and duration.isdigit():
                        return voice_advanced_ai.meditation_prompt(duration)
                    return voice_advanced_ai.meditation_prompt()
                except:
                    return "Error starting meditation"
            
            # Security & Authentication dynamic commands
            if query.lower().startswith('encrypt file '):
                file_path = query[13:].strip()  # Remove 'encrypt file '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.file_vault_encrypt(file_path)
                except:
                    return "Error encrypting file"
            
            if query.lower().startswith('decrypt file '):
                file_path = query[13:].strip()  # Remove 'decrypt file '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.file_vault_decrypt(file_path)
                except:
                    return "Error decrypting file"
            
            if query.lower().startswith('phishing scan '):
                url = query[14:].strip()  # Remove 'phishing scan '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.phishing_malware_scan_link(url)
                except:
                    return "Error scanning URL"
            
            if query.lower().startswith('parental control '):
                action = query[17:].strip()  # Remove 'parental control '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.parental_control_set(action)
                except:
                    return "Error with parental control"
            
            # Adaptive Learning dynamic commands
            if query.lower().startswith('adaptive learning '):
                action = query[18:].strip()  # Remove 'adaptive learning '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.adaptive_learning(action)
                except:
                    return "Error with adaptive learning"
            
            if query.lower().startswith('manual learn '):
                action = query[13:].strip()  # Remove 'manual learn '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.manual_learn(action)
                except:
                    return "Error with manual learning"
            
            if query.lower().startswith('teach jarvis '):
                action = query[14:].strip()  # Remove 'teach jarvis '
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    return voice_advanced_ai.manual_learn(action)
                except:
                    return "Error teaching Jarvis"
            

            
            # Dynamic search and play commands - more flexible detection
            play_patterns = [
                r'(?:play|search)\s+(?:video|movie|song|music|on youtube)?\s*(.+)',
                r'youtube\s+(?:play|search)\s+(.+)',
                r'(?:play|search)\s+(.+?)\s+(?:on youtube|video|song|music)',
                r'(?:play|search)\s+(.+)'
            ]
            
            for pattern in play_patterns:
                play_match = re.search(pattern, query.lower())
                if play_match:
                    search_term = play_match.group(1).strip()
                    # Only trigger YouTube search if "youtube", "search", or "play" is explicitly mentioned
                    if ('youtube' in query.lower() and 'search' in query.lower() or 'play' in query.lower()) and search_term:
                        # Exclude system commands
                        system_commands = ['notepad', 'calculator', 'chrome', 'word', 'excel']
                        if not any(cmd in search_term.lower() for cmd in system_commands):
                            return self._search_and_play(search_term)
                    break
            
            # Face auth commands - handle before general on/off
            if 'face auth' in query.lower() or 'face recognition' in query.lower():
                if 'enable' in query.lower() or 'turn on' in query.lower():
                    result = self._enable_face_auth()
                    return self._get_response('enable_face_auth', result)
                elif 'disable' in query.lower() or 'turn off' in query.lower():
                    result = self._disable_face_auth()
                    return self._get_response('disable_face_auth', result)
                elif 'status' in query.lower() or 'check' in query.lower():
                    result = self._get_face_auth_status()
                    return self._get_response('face_auth_status', result)
            
            # Dynamic on/off commands using AI
            on_off_match = re.search(r'(?:turn (on|off)|(?:enable|disable)) (.+)', query.lower())
            if on_off_match:
                action = on_off_match.group(1) if on_off_match.group(1) else ('on' if 'enable' in query.lower() else 'off')
                feature = on_off_match.group(2).strip()
                # Skip face auth as it's handled above
                if 'face' not in feature:
                    return self._handle_on_off(feature, action)
            
            if volume_match:
                level = int(volume_match.group(1))
                self._set_volume(level)
                return f"Volume set to {level}%"
            
            if brightness_match:
                level = int(brightness_match.group(1))
                self._set_brightness(level)
                return f"Brightness set to {level}%"
            

            
            if self._is_question(query):
                return self._answer_question(query)
            
            # Enhanced command matching with better natural language processing
            query_lower = query.lower().strip()
            
            # First try exact matches
            if query_lower in self.functions:
                func_name = query_lower
                print(f"Exact match found: {func_name}")
            else:
                # Try natural language understanding with enhanced matching
                func_name = self.understand_natural_speech(query)
                print(f"Natural language result: {func_name}")
                
                # If still no match, try fuzzy matching for common commands
                if not func_name:
                    func_name = self._fuzzy_match_command(query_lower)
                    print(f"Fuzzy match result: {func_name}")
                
                
                if not func_name:
                  
                    # try:
                    #     from engine.voice_advanced_ai import get_voice_advanced_response
                    #     advanced_response = get_voice_advanced_response(query)
                    #     print(f"Advanced AI response: '{advanced_response}'")
                    #     if advanced_response and "Voice command not recognized" not in advanced_response and "Error:" not in advanced_response:
                    #         print("Returning advanced AI response")
                    #         return advanced_response
                    # except Exception as e:
                    #     print(f"Advanced AI failed: {e}")
                    #     pass
                    
                    # Final fallback to AI model for function selection
                    # Check new features first
                    try:
                        from engine.new_features import get_new_feature_response
                        new_feature_result = get_new_feature_response(query)
                        if new_feature_result:
                            return new_feature_result
                    except:
                        pass
                    
                    # AI mapping for both dual_ai and new_features
                    print("Starting AI mapping process...")
                    all_functions = list(self.functions.keys())
                    try:
                        from engine.new_features import _new_features_instance
                        if _new_features_instance:
                            all_functions.extend(list(_new_features_instance.features.keys()))
                    except:
                        pass
                    
                    prompt = f'''TASK: Find exact function name for user command.

USER COMMAND: "{query}"
AVAILABLE FUNCTIONS: {all_functions}

MATCH EXAMPLES:
"mouse to center" = move_mouse_center
"turn off computer" = shutdown
"make louder" = volume_up
"take picture" = screenshot
"remind me" = task_reminder

INSTRUCTIONS:
- Return ONLY the exact function name from the list
- If no match found, return: none
- No explanations, no extra text

RESPONSE:'''
                    
                    try:
                        raw_response = self.get_ai_response(prompt)
                        print(f"Raw AI response: '{raw_response}'")
                        # Clean and validate the AI response
                        func_name = self._clean_ai_response(raw_response, all_functions)
                      
                        if func_name:
                            print(f"AI mapping successful: '{query}' -> {func_name}")
                        else:
                            print(f"AI mapping failed for: '{query}' (raw response: '{raw_response}')")
                    except Exception as e:
                        print(f"AI API error: {e}")
                        # Reset token count if we hit rate limits
                        if 'rate limit' in str(e).lower():
                            print("Rate limit hit, resetting token count")
                            self._reset_token_count()
                        func_name = None
                        

            # Check dual_ai functions first
            if func_name and func_name in self.functions:
                print(f"Executing dual_ai function: {func_name}")
                result = self.functions[func_name]()
                # For advanced features, return the actual result
                advanced_result_features = ['joke', 'quote', 'disk_space', 'ip_address', 'system_uptime', 'temperature', 'running_processes', 'check_internet', 'wifi_password', 'network_speed', 'create_folder', 'create_new_file', 'delete_file', 'search_files', 'set_reminder', 'schedule_shutdown', 'auto_backup', 'clean_temp', 'move_mouse_up', 'move_mouse_down', 'move_mouse_left', 'move_mouse_right', 'move_mouse_center', 'left_click', 'right_click', 'double_click', 'start_drag', 'drop_here', 'scroll_up', 'scroll_down', 'scroll_to_top', 'type_text', 'press_enter', 'press_tab', 'press_escape', 'press_backspace', 'press_delete', 'go_to_beginning', 'go_to_end', 'play_video', 'play_movie', 'play_song', 'search_and_play', 'open_multiple', 'daily_briefing', 'predictive_assistance', 'context_memory_recall', 'show_calendar', 'schedule', 'email_summarize', 'sync_devices', 'auto_fix_system', 'manage_package', 'docker_control', 'adaptive_learning', 'check_proactive', 'enable_proactive_mode', 'disable_proactive_mode', 'manual_learn', 'file_vault_encrypt', 'file_vault_decrypt', 'anomaly_detection', 'phishing_scan', 'parental_control', 'calendar_schedule', 'cloud_backup', 'realtime_transcription', 'summarize_meeting', 'smart_clipboard', 'document_qa', 'ai_presentation', 'smart_home_control', 'set_home_scene', 'security_camera', 'energy_monitoring', 'ai_dj_mode', 'trivia_game', 'storytelling', 'fitness_coach', 'code_agent', 'research_agent', 'organizer_agent', 'multi_agent_collab', 'scholar_search', 'stock_updates', 'crypto_updates', 'realtime_translation', 'posture_detection', 'eye_care_mode', 'daily_health_log', 'mood_tracker', 'meditation_prompt', 'start_gesture_control', 'stop_gesture_control', 'weekday', 'current_weekday', 'traffic_updates', 'public_holidays', 'covid_stats', 'open_path', 'sort_files', 'create_document', 'create_report', 'create_letter', 'ai_document']
                if func_name in advanced_result_features:
                    return result
                response = self._get_response(func_name, result)
                return response
            # Check new_features functions
            elif func_name:
                try:
                    from engine.new_features import _new_features_instance
                    if _new_features_instance and func_name in _new_features_instance.features:
                        # Execute new features function with query parameter if needed
                        query_functions = ['weather_forecast', 'email_templates', 'meeting_scheduler', 'task_reminder', 'list_reminders', 'image_editor', 'audio_converter', 'video_downloader', 'voice_recorder', 'screen_recorder', 'water_reminder', 'exercise_timer', 'calorie_calculator', 'sleep_tracker', 'stress_meter', 'mood_tracker', 'heart_rate_monitor', 'medication_reminder', 'bmi_calculator', 'system_monitor', 'network_monitor', 'language_translator', 'dictionary_lookup', 'wikipedia_search', 'calculator_advanced', 'unit_converter', 'flashcard_system', 'quiz_generator', 'meme_generator', 'logo_generator', 'color_palette_generator', 'font_viewer', 'ascii_art_generator', 'barcode_generator', 'mind_map_creator', 'password_manager', 'startup_manager', 'git_helper', 'port_scanner', 'email_sender', 'financial_tools', 'speed_test', 'battery_health', 'thermal_monitor', 'quick_note_taker', 'large_file_scanner', 'file_search_engine', 'recent_files_tracker', 'open_app', 'close_app', 'open_website', 'close_website']
                        
                        if func_name in query_functions:
                            result = _new_features_instance.features[func_name](query)
                        else:
                            result = _new_features_instance.features[func_name]()
                        
                        return result if result else f"{func_name} completed"
                except:
                    pass
            
            # Final fallback
            print("Checking if question...")
            if self._is_question(query):
                print("Processing as question")
                response = self._answer_question(query)
                return response
            # Try multilingual processing as fallback
            print("Trying multilingual processing...")
            if self.multilingual:
                ml_response = self.multilingual.process_command_in_language(query, self.multilingual.current_language)
                print(f"Multilingual response: '{ml_response}'")
                if ml_response != self.multilingual.get_response('processing'):
                    print("Returning multilingual response")
                    return ml_response
            
            print("Returning 'Command not recognized'")
            return "Command not recognized"
                
        except Exception as e:
            print(f"Error: {e}")
            return "Command not recognized"
    
    def _clean_ai_response(self, response, valid_functions):
        """Clean and validate AI response to ensure it returns a valid function name"""
        if not response:
            return None
            
        # Clean the response - remove quotes, whitespace, and common prefixes
        cleaned = response.strip().strip('"').strip("'").strip()
        
        # Remove common AI response patterns
        patterns_to_remove = [
            'function name:', 'the function is:', 'answer:', 'result:', 
            'i suggest:', 'i recommend:', 'use:', 'call:', 'execute:'
        ]
        
        for pattern in patterns_to_remove:
            if cleaned.lower().startswith(pattern):
                cleaned = cleaned[len(pattern):].strip()
        
        # Handle multi-line responses - take only the first line
        cleaned = cleaned.split('\n')[0].strip()
        
        # Check if it's a valid function name
        if cleaned in valid_functions:
            return cleaned
        
        # Check for partial matches (case insensitive)
        cleaned_lower = cleaned.lower()
        for func in valid_functions:
            if func.lower() == cleaned_lower:
                return func
        
        # Check if response indicates no match
        no_match_indicators = ['none', 'no match', 'not found', 'unknown', 'null', 'n/a']
        if cleaned.lower() in no_match_indicators:
            return None
            
        return None

    def understand_natural_speech(self, query):
        """Complete natural language processing for ALL functions"""
        query = query.lower().strip()
        
        mappings = {
            'shutdown': ['shut down', 'turn off computer', 'power off', 'shutdown computer'],
            'restart': ['restart', 'reboot', 'restart computer', 'reboot system'],
            'sleep': ['sleep', 'put to sleep', 'sleep mode'],
            'lock': ['lock', 'lock screen', 'secure screen'],
            'hibernate': ['hibernate', 'deep sleep', 'hibernation'],
            'volume_up': ['volume up', 'louder', 'increase volume', 'make it louder', 'turn up sound', 'increase the volume'],
            'volume_down': ['volume down', 'quieter', 'decrease volume', 'make it quieter', 'turn down sound'],
            'mute': ['mute', 'silence', 'turn off sound', 'mute audio'],
            'screenshot': ['screenshot', 'take screenshot', 'capture screen', 'take a picture of screen'],
            'brightness_up': ['brightness up', 'brighter', 'increase brightness', 'brighten screen'],
            'brightness_down': ['brightness down', 'dimmer', 'decrease brightness', 'my screen is too bright'],
            'show desktop': ['show desktop', 'go to desktop', 'minimize all'],
            'calculator': ['calculator', 'calc', 'open calculator'],
            'notepad': ['notepad', 'text editor', 'open notepad'],
            'chrome': ['chrome', 'browser', 'open chrome', 'web browser'],
            'stop_ambient_awareness': ['stop ambient awareness', 'end ambient awareness'],
            'sort_files': ['sort files', 'sort by date', 'sort by time', 'sort by name', 'sort by size', 'arrange files', 'organize files', 'arrange files by size', 'arrange files by date', 'arrange files by name', 'sort files by size', 'sort files by date', 'sort files by name'],
            'ambient_status': ['ambient status', 'check ambient status'],
            'start_ambient_awareness': ['start ambient awareness', 'ambient awareness', 'start ambient', 'begin ambient awareness', 'activate ambient awareness'],
            'edge': ['edge', 'microsoft edge', 'open edge'],
            'firefox': ['firefox', 'open firefox', 'mozilla'],
            'word': ['word', 'microsoft word', 'document editor'],
            'excel': ['excel', 'spreadsheet', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'presentation', 'slides'],
            'vlc': ['vlc', 'video player', 'media player'],
            'vscode': ['vscode', 'code editor', 'visual studio'],
            'spotify': ['spotify', 'music', 'music player'],

            'steam': ['steam', 'games', 'gaming'],
            'explorer': ['explorer', 'file manager'],
            'settings': ['settings', 'system settings', 'control panel'],
            'taskmanager': ['task manager', 'processes', 'taskmanager'],
            'cmd': ['command prompt', 'cmd', 'terminal'],
            'paint': ['paint', 'drawing', 'mspaint'],
            'google': ['google', 'search', 'google search'],
            'youtube': ['youtube', 'videos', 'watch videos'],
            'wikipedia': ['wikipedia', 'wiki', 'encyclopedia'],
            'stackoverflow': ['stackoverflow', 'programming help', 'coding help'],
            'github': ['github', 'git', 'code repository'],
            'amazon': ['amazon', 'shopping', 'buy online'],
            'flipkart': ['flipkart', 'shopping india'],
            'instagram': ['instagram', 'insta', 'photos'],
            'facebook': ['facebook', 'fb', 'social media'],
            'twitter': ['twitter', 'tweets', 'social'],
            'linkedin': ['linkedin', 'professional network'],
            'whatsapp_web': ['whatsapp', 'messaging', 'chat'],
            'gmail': ['gmail', 'email', 'mail'],
            'netflix': ['netflix', 'movies', 'streaming'],
            'copy': ['copy', 'copy text', 'copy this'],
            'paste': ['paste', 'paste text', 'paste here'],
            'save': ['save', 'save file', 'save document'],
            'undo': ['undo', 'undo last action', 'go back'],
            'select_all': ['select all', 'select everything'],
            'alt_tab': ['switch window', 'alt tab', 'change window'],
            'time': ['time', 'what time is it', 'current time', 'tell me the time','time now','what is time now'],
            'date': ['date', 'what date is it', 'current date', 'today'],
            'cpu': ['cpu usage', 'processor usage', 'cpu load'],
            'memory': ['memory usage', 'ram usage', 'memory load'],
            'battery': ['battery', 'battery level', 'battery percentage'],
            'downloads': [ 'download folder','downloads folder'],
            'documents': ['documents', 'my documents'],
            'pictures': ['pictures', 'photos', 'image folder'],
            'switch_to_gemini': ['switch to gemini', 'use gemini', 'gemini ai'],
            'switch_to_groq': ['switch to groq', 'use groq', 'groq ai'],
            'current_ai': ['current ai', 'which ai', 'ai status'],
            'switch_language_hindi': ['hindi', 'switch to hindi'],
            'switch_language_kannada': ['kannada', 'switch to kannada'],
            'switch_language_english': ['english', 'switch to english'],
            'close_chrome': ['close chrome', 'quit chrome'],
            'close_edge': ['close edge', 'quit edge'],
            'close_notepad': ['close notepad', 'quit notepad'],
            'switch_to_male_voice': ['male voice', 'switch to male'],
            'switch_to_female_voice': ['female voice', 'switch to female'],
            'current_voice_gender': ['voice status', 'current voice'],
            'context_memory_recall': ['what do you remember', 'recall memory', 'show memories'],
            'daily_briefing': ['daily briefing', 'morning briefing'],
            'predictive_assistance': ['predictive help', 'smart suggestions'],
            'schedule': ['schedule meeting', 'add event', 'book appointment'],
            'show_calendar': ['show calendar', 'check calendar'],
            'posture_detection': ['posture check', 'check posture'],
            'eye_care_mode': ['eye care', 'protect eyes'],
            'daily_health_log': ['health log', 'log health'],
            'mood_tracker': ['mood tracker', 'track mood'],
            'meditation_prompt': ['meditate', 'meditation', 'relax'],
            'trivia_game': ['trivia', 'quiz game', 'test knowledge'],
            'storytelling': ['tell story', 'story time'],
            'fitness_coach': ['fitness coach', 'workout guide'],
            'ai_dj_mode': ['dj mode', 'music mix'],
            'code_agent': ['code help', 'programming assistant'],
            'research_agent': ['research help', 'research assistant'],
            'organizer_agent': ['organize', 'task organizer'],
            'smart_home_control': ['smart home', 'home automation'],
            'set_home_scene': ['home scene', 'set scene'],
            'start_gesture_control': ['gesture control', 'hand control'],
            'stop_gesture_control': ['stop gestures', 'disable gestures'],
            'code_review': ['code review', 'review code', 'check code'],
            'folder_review': ['folder review', 'review folder'],
            'live_code_review': ['live review', 'real time review'],
            'joke': ['tell joke', 'joke', 'make me laugh'],
            'quote': ['quote', 'inspirational quote', 'wisdom'],
    
            'news': ['news', 'latest news', 'headlines'],
            'disk_space': ['disk space', 'storage space', 'free space'],
            'system_uptime': ['uptime', 'system uptime', 'how long running'],
            'temperature': ['temperature', 'cpu temperature', 'system temp'],
            'running_processes': ['processes', 'running programs', 'active processes', 'show running processes', 'list processes', 'running processes'],
            'check_internet': ['internet', 'check internet', 'connection test'],
            'ip_address': ['ip address', 'my ip', 'network address'],
            'wifi_password': ['wifi password', 'network password'],
            'network_speed': ['speed test', 'internet speed', 'connection speed'],
            'create_folder': ['create folder', 'new folder', 'make folder', 'folder create'],
            'create_new_file': ['create file', 'new file', 'make file', 'create new file'],
            'delete_file': ['delete file', 'remove file'],
            'search_files': ['search files', 'find files'],
            'copy_file': ['copy file', 'duplicate file', 'copy', 'file copy'],
            'move_file': ['move file', 'relocate file'],
            'maximize_window': ['maximize', 'maximize window', 'make bigger'],
            'minimize_window': ['minimize', 'minimize window', 'hide window'],
            'close_window': ['close window', 'close this'],
            'split_screen_left': ['split left', 'snap left', 'window left'],
            'split_screen_right': ['split right', 'snap right', 'window right'],
            'full_screen': ['full screen', 'fullscreen'],
            'play_pause': ['play', 'pause', 'play pause'],
            'next_track': ['next', 'next song', 'skip'],
            'previous_track': ['previous', 'previous song', 'back'],
            'stop_media': ['stop', 'stop playing'],
            'find_text': ['find', 'search text', 'find text'],
            'replace_text': ['replace', 'find replace'],
            'new_document': ['new document', 'new file'],
            'print_document': ['print', 'print document'],
            'zoom_in': ['zoom in', 'magnify', 'make bigger'],
            'zoom_out': ['zoom out', 'make smaller'],
            'clear_clipboard': ['clear clipboard', 'empty clipboard'],
            'clear_history': ['clear history', 'delete history'],
            'empty_recycle_bin': ['empty recycle bin', 'clear trash'],
            'lock_screen': ['lock screen', 'secure computer'],
       
            'schedule_shutdown': ['schedule shutdown', 'auto shutdown'],
            'auto_backup': ['backup', 'backup files'],
            'clean_temp': ['clean temp', 'delete temp files'],
            'play_music': ['play music', 'start music'],
            'random_wallpaper': ['change wallpaper', 'new wallpaper'],
            'move_mouse_up': ['mouse up', 'move mouse up', 'cursor up'],
            'move_mouse_down': ['mouse down', 'move mouse down', 'cursor down'],
            'move_mouse_left': ['mouse left', 'move mouse left', 'cursor left'],
            'move_mouse_right': ['mouse right', 'move mouse right', 'cursor right'],
            'move_mouse_center': ['mouse center', 'center mouse'],
            'left_click': ['left click', 'click', 'mouse click'],
            'right_click': ['right click', 'context menu'],
            'double_click': ['double click', 'double tap'],
            'scroll_up': ['scroll up', 'page up'],
            'scroll_down': ['scroll down', 'page down'],
            'press_enter': ['press enter', 'hit enter', 'enter key'],
            'press_tab': ['press tab', 'tab key'],
            'press_escape': ['press escape', 'escape key'],
            'press_backspace': ['backspace', 'delete back'],
            'press_delete': ['delete key', 'delete forward'],
            'youtube_play': ['youtube play', 'play video'],
            'youtube_pause': ['youtube pause', 'pause video'],
            'youtube_next': ['youtube next', 'next video'],
            'youtube_previous': ['youtube previous', 'previous video'],
            'youtube_fullscreen': ['youtube fullscreen', 'video fullscreen'],
            'youtube_volume_up': ['youtube louder', 'video volume up'],
            'youtube_volume_down': ['youtube quieter', 'video volume down'],
            'youtube_mute': ['youtube mute', 'mute video'],
            'youtube_speed_up': ['youtube faster', 'speed up video'],
            'youtube_speed_down': ['youtube slower', 'slow down video'],
            'youtube_skip_forward': ['youtube skip', 'skip ahead'],
            'youtube_skip_backward': ['youtube back', 'skip back'],
            'youtube_search': ['youtube search', 'search video'],
            'youtube_subscribe': ['youtube subscribe', 'subscribe channel'],
            'youtube_like': ['youtube like', 'like video'],
            'youtube_theater_mode': ['theater mode', 'cinema mode'],
            'youtube_captions': ['captions', 'subtitles'],
            'chrome_new_tab': ['new tab', 'open tab'],
            'chrome_close_tab': ['close tab', 'close current tab'],
            'chrome_next_tab': ['next tab', 'switch tab'],
            'chrome_previous_tab': ['previous tab', 'last tab'],
            'chrome_reload': ['reload', 'refresh'],
            'chrome_back': ['go back', 'back page'],
            'chrome_forward': ['go forward', 'forward page'],
            'chrome_bookmark': ['bookmark', 'save bookmark'],
            'chrome_history': ['history', 'browser history'],
            'chrome_downloads': ['downloads', 'download history'],
            'chrome_incognito': ['incognito', 'private browsing'],
            'chrome_settings': ['chrome settings', 'browser settings'],
            'enable_face_auth': ['enable face auth', 'face recognition on'],
            'disable_face_auth': ['disable face auth', 'face recognition off'],
            'face_auth_status': ['face auth status', 'check face auth'],
            # 'system_monitor_live': ['system monitor', 'live monitoring'],
            'auto_fix_system': ['auto fix', 'fix system'],
            'performance_monitor': ['performance monitor', 'system performance'],
            'enable_narrator': ['narrator on', 'enable narrator'],
            'disable_narrator': ['narrator off', 'disable narrator'],
            'enable_magnifier': ['magnifier on', 'enable magnifier'],
            'disable_magnifier': ['magnifier off', 'disable magnifier'],
            'high_contrast_mode': ['high contrast', 'contrast mode'],
            'connect_wifi': ['connect wifi', 'join network'],
            'disconnect_wifi': ['disconnect wifi', 'leave network'],
            'show_wifi_networks': ['wifi networks', 'available networks'],
            'enable_hotspot': ['hotspot on', 'mobile hotspot'],
            'disable_hotspot': ['hotspot off', 'disable hotspot'],
            'search_files_content': ['search in files', 'find in files'],
            'find_large_files': ['large files', 'big files'],
            'find_duplicate_files': ['duplicate files', 'find duplicates'],
            'smart_lights': ['smart lights', 'control lights'],
            'smart_fan': ['smart fan', 'control fan'],
            'smart_ac': ['smart ac', 'air conditioning'],
            'write_code': ['write code', 'generate code', 'create code', 'code generator', 'write python code', 'write javascript code', 'write java code', 'write html code', 'write css code', 'python code for', 'javascript code for', 'java code for', 'code for'],
            'create_project': ['create project', 'build project', 'make project', 'new project', 'project for'],
            'generate_code': ['generate code', 'write code'],
            'debug_code': ['debug code', 'fix code'],
            'translate_text': ['translate', 'translate text'],
            'summarize_text': ['summarize', 'summary'],
            'analyze_image': ['analyze image', 'image analysis'],
            'send_email': ['send email', 'compose email'],
            'schedule_meeting': ['schedule meeting', 'book meeting'],
            'create_task': ['create task', 'new task'],
            'convert_document': ['convert document', 'change format'],
            'merge_pdf': ['merge pdf', 'combine pdf'],
            'git_status': ['git status', 'check git'],
            'git_commit': ['git commit', 'commit changes'],
            'run_tests': ['run tests', 'execute tests'],
            'format_code': ['format code', 'beautify code'],
            'api_test': ['api test', 'test api'],
            'water_reminder': ['water reminder', 'drink water'],
            'break_reminder': ['break reminder', 'take break'],
            'fitness_track': ['fitness track', 'exercise log'],
            'wikipedia_search': ['wikipedia', 'wiki search'],
            'dictionary_lookup': ['dictionary', 'word meaning'],
            'unit_convert': ['convert units', 'unit conversion'],
            'math_calculate': ['calculate', 'math calculation'],
            'language_learn': ['learn language', 'language learning'],
            'movie_recommend': ['movie recommendation', 'suggest movie'],

            'game_launch': ['launch game', 'start game'],
            'streaming_control': ['streaming control', 'media streaming'],
            'playlist_manage': ['manage playlist', 'playlist control'],
            'workflow_automate': ['automate workflow', 'automation'],
            'batch_operations': ['batch operation', 'bulk operation'],
            'scheduled_tasks': ['scheduled task', 'task scheduler'],
            'system_maintenance': ['system maintenance', 'maintain system'],
            'auto_updates': ['auto updates', 'automatic updates'],
            'tell_joke': ['tell joke', 'joke', 'make me laugh'],
            'get_quote': ['quote', 'inspirational quote'],
      
            'get_news': ['news', 'latest news'],
            'play_video': ['play video', 'watch video'],
            'play_movie': ['play movie', 'watch movie'],
            'play_song': ['play song', 'play music'],
            'search_and_play': ['search and play', 'find and play'],
            'open_multiple': ['open multiple', 'open several'],
            
            # Mapping Commands
            'open_maps': ['open maps', 'show maps', 'google maps', 'maps'],
            'find_location': ['find location', 'search location', 'locate', 'where is'],
            'get_directions': ['directions', 'navigate to', 'route to', 'how to get to'],
            'nearby_places': ['nearby', 'find nearby', 'places near me', 'restaurants near me'],
            'traffic_info': ['traffic', 'traffic info', 'show traffic', 'traffic conditions'],
            'map_satellite': ['satellite view', 'satellite map', 'aerial view'],
            'map_terrain': ['terrain view', 'terrain map', 'topographic map'],
            'save_location': ['save location', 'bookmark location', 'remember this place'],
            'my_location': ['my location', 'current location', 'where am i'],
            'dictate_to_file': ['dictate to file', 'voice to file', 'speech to file'],
            'dictate_to_document': ['dictate document', 'voice document', 'speech document'],
            'hibernate_computer': ['hibernate computer', 'deep sleep'],
            'log_off': ['log off', 'sign out'],
            'switch_user': ['switch user', 'change user'],
            'enable_airplane_mode': ['airplane mode on', 'flight mode'],
            'disable_airplane_mode': ['airplane mode off', 'disable flight mode'],
            'start_screen_recording': ['start recording', 'record screen'],
            'stop_screen_recording': ['stop recording', 'end recording'],
            'start_dictation': ['start dictation', 'voice typing', 'dictate anywhere', 'open and dictate','start writting'],
            'stop_dictation': ['stop dictation', 'end dictation', 'stop lies', 'stop writing'],
            'dictate_anywhere': ['dictate anywhere', 'universal dictation', 'type anywhere'],
            'take_screenshot_window': ['window screenshot', 'capture window'],
            'take_screenshot_area': ['area screenshot', 'capture area'],
            'file_vault_encrypt': ['encrypt file', 'secure file'],
            'file_vault_decrypt': ['decrypt file', 'unlock file'],
            'anomaly_detection': ['scan for threats', 'security scan'],
            'phishing_scan': ['check for phishing', 'scan link'],
            'parental_control': ['parental control', 'child safety'],
            'cloud_backup': ['cloud backup', 'backup to cloud'],
            'email_summarize': ['summarize email', 'email summary'],
            'sync_devices': ['sync devices', 'synchronize'],
            'realtime_transcription': ['transcribe audio', 'voice to text'],
            'summarize_meeting': ['meeting summary', 'summarize discussion'],
            'smart_clipboard': ['smart clipboard', 'clipboard manager'],
            'document_qa': ['document questions', 'ask about document'],
            'ai_presentation': ['create presentation', 'make slides','create ppt'],
            'security_camera': ['security camera', 'surveillance'],
            'energy_monitoring': ['energy monitor', 'power usage'],
            'scholar_search': ['academic search', 'research papers'],
            'stock_updates': ['stock market', 'stock prices'],
            'crypto_updates': ['cryptocurrency', 'crypto prices'],
            'realtime_translation': ['translate text', 'language translation'],
            'manage_package': ['install package', 'manage software'],
            'docker_control': ['docker control', 'container management'],
            'adaptive_learning': ['learn from me', 'adapt to me'],
            'check_proactive': ['check suggestions', 'proactive help'],
            'enable_proactive_mode': ['enable proactive', 'turn on suggestions'],
            'disable_proactive_mode': ['disable proactive', 'turn off suggestions'],
            'manual_learn': ['teach you', 'manual learning'],
            'calendar_schedule': ['calendar event', 'schedule appointment'],
            'debug_screen': ['debug code', 'fix my code'],
            'fix_my_code': ['fix my code', 'repair code'],
            'check_code': ['check code', 'review code'],
            'multi_agent_collab': ['multi agent', 'agent collaboration'],
            'start_live_review': ['start live review', 'begin monitoring'],
            'stop_live_review': ['stop live review', 'end monitoring'],
            'switch_language_kannada': ['kannada', 'switch to kannada'],
            'switch_language_english': ['english', 'switch to english'],
            'close_chrome': ['close chrome', 'quit chrome'],
            'close_edge': ['close edge', 'quit edge'],
            'close_notepad': ['close notepad', 'quit notepad'],
            'switch_to_male_voice': ['male voice', 'switch to male'],
            'switch_to_female_voice': ['female voice', 'switch to female'],
            'current_voice_gender': ['voice status', 'current voice'],
            'context_memory_recall': ['what do you remember', 'recall memory', 'show memories'],
            'daily_briefing': ['daily briefing', 'morning briefing'],
            'predictive_assistance': ['predictive help', 'smart suggestions'],
            'schedule': ['schedule meeting', 'add event', 'book appointment'],
            'show_calendar': ['show calendar', 'check calendar'],
            'posture_detection': ['posture check', 'check posture'],
            'eye_care_mode': ['eye care', 'protect eyes'],
            'daily_health_log': ['health log', 'log health'],
            'mood_tracker': ['mood tracker', 'track mood'],
            'meditation_prompt': ['meditate', 'meditation', 'relax'],
            'trivia_game': ['trivia', 'quiz game', 'test knowledge'],
            'storytelling': ['tell story', 'story time'],
            'fitness_coach': ['fitness coach', 'workout guide'],
            'ai_dj_mode': ['dj mode', 'music mix'],
            'code_agent': ['code help', 'programming assistant'],
            'research_agent': ['research help', 'research assistant'],
            'organizer_agent': ['organize', 'task organizer'],
            'smart_home_control': ['smart home', 'home automation'],
            'set_home_scene': ['home scene', 'set scene'],
            'start_gesture_control': ['gesture control', 'hand control'],
            'stop_gesture_control': ['stop gestures', 'disable gestures'],
            'code_review': ['code review', 'review code', 'check code'],
            'folder_review': ['folder review', 'review folder'],
            'live_code_review': ['live review', 'real time review'],
            'joke': ['tell joke', 'joke', 'make me laugh'],
            'quote': ['quote', 'inspirational quote', 'wisdom'],
        
            'news': ['news', 'latest news', 'headlines'],
            'dice': ['dice', 'roll dice', 'roll a dice', 'roll the dice'],
            'coin': ['coin', 'flip coin', 'coin flip', 'flip the coin'],
            'roll_dice': ['roll dice', 'roll a dice', 'roll the dice'],
            'flip_coin': ['flip coin', 'coin flip', 'flip the coin'],
            'age_calculator': ['age calculator', 'calculate age', 'my age', 'how old am i', 'calculate my age', 'age calculation'],
            'calculate_age': ['calculate age', 'age calculator', 'find my age', 'determine age', 'age finder'],
            
            # Complete Voice Advanced AI Features Mappings
            # 'system_monitor_live': ['system monitor', 'monitor system', 'live monitoring', 'system status', 'system dashboard'],
            'auto_fix_system': ['auto fix', 'fix system', 'system fix', 'repair system', 'system repair'],
            'install_package': ['install package', 'install software', 'add package', 'package install'],
            'list_packages': ['list packages', 'show packages', 'installed packages', 'package list'],
            'uninstall_package': ['uninstall package', 'remove package', 'delete package', 'package remove'],
            'manage_package': ['manage package', 'package manager', 'software manager', 'package management'],
            
            # Advanced Memory & Context
            'context_memory_store': ['remember this', 'store memory', 'save this', 'store this'],
            'context_memory_recall': ['what do you remember', 'recall memory', 'show memories', 'my memories', 'stored memories'],
            'daily_briefing': ['daily briefing', 'morning briefing', 'get briefing', 'today summary', 'daily summary'],
            
            # Advanced Calendar & Scheduling
            'calendar_schedule': ['schedule event', 'book appointment', 'add event', 'create meeting', 'schedule meeting'],
            'show_calendar': ['show calendar', 'check calendar', 'my events', 'what meetings', 'calendar view', 'upcoming events'],
            
            # Advanced Email & Communication
            'email_summarize': ['summarize email', 'email summary', 'email brief', 'email digest'],
            'sync_devices': ['sync devices', 'device sync', 'synchronize', 'sync data'],
            'cloud_backup': ['cloud backup', 'backup files', 'backup to cloud', 'cloud storage'],
            
            # Advanced AI Productivity
            'realtime_transcription': ['transcribe audio', 'voice to text', 'speech to text', 'audio transcription'],
            'summarize_meeting': ['meeting summary', 'summarize discussion', 'meeting notes', 'discussion summary'],
            'smart_clipboard': ['smart clipboard', 'clipboard manager', 'clipboard history', 'clipboard storage'],
            'clipboard_assistant': ['clipboard assistant', 'smart clipboard help', 'clipboard helper'],
            'start_clipboard_assistant': ['start clipboard assistant', 'monitor clipboard', 'clipboard monitoring'],
            'stop_clipboard_assistant': ['stop clipboard assistant', 'stop clipboard monitoring'],
            'set_alarm': ['set alarm', 'alarm for', 'wake me up', 'reminder at', 'alarm at'],
            'cancel_alarm': ['cancel alarm', 'stop alarm', 'turn off alarm', 'disable alarm', 'remove alarm'],
            'create_image': ['create image', 'generate image', 'make image', 'ai image', 'image generation', 'draw image'],
            'document_qa': ['document questions', 'ask document', 'document help', 'document assistant'],
            'ai_presentation': ['create presentation', 'make slides', 'presentation maker', 'ai presentation'],
            'ai_report': ['create report', 'make report', 'generate report', 'ai report'],
            
            # Advanced Smart Home
            'smart_home_control': ['smart home', 'home automation', 'control home', 'home control'],
            'set_home_scene': ['home scene', 'set scene', 'activate scene', 'scene control'],
            'security_camera': ['security camera', 'camera snapshot', 'surveillance', 'camera view'],
            'energy_monitoring': ['energy monitor', 'power usage', 'energy report', 'power monitoring'],
            
            # Advanced Entertainment Plus
            'ai_dj_mode': ['dj mode', 'music dj', 'ai dj', 'music mix', 'dj assistant'],
            'trivia_game': ['trivia game', 'play trivia', 'quiz game', 'trivia quiz', 'knowledge game'],
            'storytelling': ['tell story', 'story mode', 'story time', 'create story', 'story generator'],
            'fitness_coach': ['fitness coach', 'workout coach', 'exercise guide', 'fitness help', 'workout assistant'],
            
            # Advanced AI Agents
            'code_agent': ['code agent', 'coding help', 'programming assistant', 'code help', 'coding assistant'],
            'debug_screen': ['debug screen', 'debug code', 'fix my code', 'check code', 'code debugging'],
            'research_agent': ['research agent', 'research help', 'research assistant', 'research support'],
            'organizer_agent': ['organizer agent', 'organize tasks', 'task organizer', 'task manager'],
            'multi_agent_collab': ['multi agent', 'agent collaboration', 'multiple agents', 'agent teamwork'],
            
            # Advanced Web Intelligence
            'scholar_search': ['scholar search', 'academic search', 'research papers', 'scholarly articles'],
            'stock_updates': ['stock updates', 'stock market', 'stock prices', 'market news', 'financial updates'],
            'crypto_updates': ['crypto updates', 'cryptocurrency', 'crypto prices', 'bitcoin', 'crypto market'],
            'realtime_translation': ['translate text', 'real time translation', 'language translate', 'translation service'],
            
            # Advanced Health & Wellness
            'posture_detection': ['posture check', 'check posture', 'posture analysis', 'posture monitoring'],
            'eye_care_mode': ['eye care', 'protect eyes', 'eye break', 'eye health', 'eye protection'],
            'daily_health_log': ['health log', 'track health', 'health diary', 'wellness log', 'health tracking'],
            'mood_tracker': ['mood tracker', 'track mood', 'mood log', 'how am i feeling', 'mood monitoring'],
            'meditation_prompt': ['meditation', 'meditate', 'mindfulness', 'relax', 'meditation guide'],
            'open_path': ['open file', 'open folder', 'open path', 'launch file', 'launch folder', 'run file', 'run folder', 'open documents', 'open downloads', 'open desktop', 'open pictures', 'open music', 'open videos', 'open docs', 'open pics', 'open vids', 'show me', 'find file', 'find folder', 'locate file', 'locate folder', 'access file', 'access folder', 'browse to', 'navigate to', 'go to file', 'go to folder'],

            
            # Advanced Security & Authentication
            'file_vault_encrypt': ['encrypt file', 'secure file', 'protect file', 'file encryption'],
            'file_vault_decrypt': ['decrypt file', 'unlock file', 'unsecure file', 'file decryption'],
            'anomaly_detection': ['scan for threats', 'security scan', 'system scan', 'threat detection'],
            'phishing_scan': ['phishing scan', 'check link', 'scan url', 'link safety', 'url security'],
            'parental_control': ['parental control', 'child safety', 'family safety', 'content filtering'],
            
            # Advanced Learning & Adaptation
            'adaptive_learning': ['adaptive learning', 'learn from me', 'adapt to me'],
            'check_proactive': ['check proactive', 'proactive suggestions', 'smart suggestions', 'ai suggestions'],
            'enable_proactive_mode': ['enable proactive', 'turn on suggestions', 'proactive mode on', 'smart mode on'],
            'disable_proactive_mode': ['disable proactive', 'turn off suggestions', 'proactive mode off', 'smart mode off'],
            'manual_learn': ['manual learn', 'teach jarvis', 'teach you', 'learn this', 'training mode'],
            'predictive_assistance': ['predictive help', 'smart suggestions', 'predict actions', 'ai predictions'],
            
            # Advanced Docker & Development
            'docker_control': ['docker control', 'docker help', 'container management', 'docker commands'],
            
            # Google Search
            'search_google': ['search google', 'google search', 'search on google', 'google it', 'search web'],
            'search_images': ['search images', 'image search', 'sehiiiiiiiarch for images', 'find images'],
            'search_gifs': ['search gifs', 'gif search', 'search for gifs', 'find gifs'],
            'copy_webpage_link': ['copy link', 'copy webpage link', 'copy url', 'copy page link'],
            'translate_webpage': ['translate page', 'translate webpage', 'translate this page', 'page translate'],
            'weekday': ['weekday', 'what day', 'current day', 'today day', 'day of week'],
            'traffic_updates': ['traffic updates', 'traffic conditions', 'traffic info', 'check traffic', 'traffic status'],
            'public_holidays': ['public holidays', 'holidays today', 'holiday check', 'is today holiday', 'holiday status'],
            'covid_stats': ['covid stats', 'covid updates', 'coronavirus stats', 'covid cases', 'covid data'],
            
            # Product Price Tracking
            'track_amazon_price': ['track amazon price', 'amazon price track', 'check amazon price', 'amazon price check', 'track price on amazon', 'price track amazon', 'track price of', 'amazon track price'],
            'track_flipkart_price': ['track flipkart price', 'flipkart price track', 'check flipkart price', 'flipkart price check', 'track price on flipkart', 'price track flipkart', 'flipkart track price'],
            'check_product_price': ['check product price', 'compare price', 'price comparison', 'product price', 'check price', 'price check'],
            
            # Travel Search
            'search_flights': ['search flights', 'find flights', 'book flights', 'flight search', 'flight booking', 'flights from', 'flights to'],
            'search_hotels': ['search hotels', 'find hotels', 'book hotels', 'hotel search', 'hotel booking', 'hotels in', 'hotels at'],
            
            # Streaming Search
            'find_movie_streaming': ['find movie streaming', 'where to watch movie', 'movie streaming', 'watch movie online'],
            'find_show_streaming': ['find show streaming', 'where to watch show', 'show streaming', 'watch show online'],
            'where_to_watch': ['where to watch', 'streaming availability', 'find streaming', 'watch online'],
            'streaming_availability': ['streaming availability', 'available on streaming', 'streaming platforms', 'watch platforms'],
            
            # Debug price tracking functions
            'track_amazon_price_debug': ['track amazon price debug', 'debug amazon price', 'amazon price debug'],
            'track_flipkart_price_debug': ['track flipkart price debug', 'debug flipkart price', 'flipkart price debug'],
            'check_product_price_debug': ['check product price debug', 'debug product price', 'price debug'],
            
            # File Sorting
            'sort_files': ['sort files', 'sort by date', 'sort by time', 'sort by name', 'sort by size', 'arrange files', 'organize files', 'arrange files by size', 'arrange files by date', 'arrange files by name', 'sort files by size', 'sort files by date', 'sort files by name']
                      
        }
        
        # Check for exact phrase matches first
        for func_name, phrases in mappings.items():
            for phrase in phrases:
                if phrase in query:
                    return func_name
        
        # Check for partial matches with higher priority functions
        priority_functions = [
            # 'system_monitor_live', 'auto_fix_system', 'code_agent', 'research_agent',
            'ai_presentation', 'smart_home_control', 'posture_detection', 'eye_care_mode',
            'meditation_prompt', 'trivia_game', 'storytelling', 'fitness_coach'
        ]
        
        for func_name in priority_functions:
            if func_name in mappings:
                for phrase in mappings[func_name]:
                    # Check for partial matches
                    phrase_words = phrase.split()
                    query_words = query.split()
                    if len(phrase_words) > 1 and any(word in query for word in phrase_words):
                        # Check if at least 2 words match for multi-word phrases
                        matches = sum(1 for word in phrase_words if word in query)
                        if matches >= min(2, len(phrase_words)):
                            return func_name
        
        return None
    
    def _fuzzy_match_command(self, query):
        """Fuzzy matching using existing natural speech mappings"""
        return self.understand_natural_speech(query)
    
    
    def execute_multiple_commands(self, commands):
        """Execute multiple commands sequentially"""
        results = []
        for i, command in enumerate(commands):
            try:
                result = self.execute(command.strip())
                results.append(f"Command {i+1}: {result}")
                # Small delay between commands for better execution
                if i < len(commands) - 1:
                    time.sleep(0.3)
            except Exception as e:
                results.append(f"Command {i+1} failed: {str(e)}")
        
        return " | ".join(results)
    
    def _is_question(self, query):
        question_words = ['who', 'what', 'when', 'where', 'why', 'how']
        return any(word in query.lower() for word in question_words) or query.strip().endswith('?')
    
    def get_ai_response(self, prompt):
        """Get AI response for function mapping with fallback mechanism"""
        try:
            if self.ai_provider == 'groq':
                # Get appropriate model based on token usage
                model = self._get_groq_model()
                
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                    max_tokens=50
                )
                
                # Track token usage (approximate)
                self.token_count += len(prompt.split()) + len(response.choices[0].message.content.split())
                
                return response.choices[0].message.content.strip()
            elif self.ai_provider == 'ollama':
                return self.ollama_client.generate(prompt)
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            print(f"AI response error: {e}")
            # If 8B model fails due to rate limit, try 70B model
            if self.ai_provider == 'groq' and 'rate limit' in str(e).lower():
                try:
                    print("Trying fallback to 70B model...")
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=self.fallback_model,
                        max_tokens=50
                    )
                    return response.choices[0].message.content.strip()
                except:
                    pass
            return None
    
    def _answer_question(self, query):
        try:
            # Check stored memories first for any personal questions
            if any(word in query.lower() for word in ['my ', 'what is my', 'who am i', 'do you remember', 'what do you know about me']):
                try:
                    from engine.voice_advanced_ai import voice_advanced_ai
                    memories = voice_advanced_ai.context_memory_recall()
                    
                    # Search through all stored memories
                    for key in memories.keys():
                        memory_data = voice_advanced_ai._memory_get_all(key)
                        if memory_data:
                            data_str = str(memory_data[0]).lower()
                            query_words = query.lower().split()
                            
                            # Check if any words from the query match the stored data
                            for word in query_words:
                                if len(word) > 2 and word in data_str:  # Skip short words
                                    return f"Based on what you told me: {memory_data[0]}"
                            
                            # Specific pattern matching
                            if 'name' in query.lower() and 'name is' in data_str:
                                name_part = str(memory_data[0]).split('name is')[-1].strip()
                                return f"Your name is {name_part}"
                            elif any(word in query.lower() for word in ['color', 'colour']) and 'color is' in data_str:
                                color_part = str(memory_data[0]).split('color is')[-1].strip()
                                return f"Your favorite color is {color_part}"
                            elif 'age' in query.lower() and 'age is' in data_str:
                                age_part = str(memory_data[0]).split('age is')[-1].strip()
                                return f"Your age is {age_part}"
                            elif 'live' in query.lower() and 'live in' in data_str:
                                location_part = str(memory_data[0]).split('live in')[-1].strip()
                                return f"You live in {location_part}"
                except:
                    pass
            
            prompt = f'You are Jarvis. Answer briefly: "{query}"'
            
            if self.ai_provider == 'groq':
                # Get appropriate model based on token usage
                model = self._get_groq_model()
                
                try:
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model
                    )
                    
                    # Track token usage (approximate)
                    self.token_count += len(prompt.split()) + len(response.choices[0].message.content.split())
                    
                    return response.choices[0].message.content.strip()
                    
                except Exception as e:
                    # If rate limit reached, try fallback model
                    if 'rate limit' in str(e).lower() or self.token_count >= self.token_limit:
                        print(f"Switching to {self.fallback_model} due to rate limit")
                        try:
                            response = self.groq_client.chat.completions.create(
                                messages=[{"role": "user", "content": prompt}],
                                model=self.fallback_model
                            )
                            return response.choices[0].message.content.strip()
                        except:
                            return "I'm having trouble answering that."
                    raise e
            elif self.ai_provider == 'ollama':
                return self.ollama_client.generate(prompt)
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
        except:
            return "I'm having trouble answering that."
    
    def _get_response(self, func, result):
        responses = {
            'shutdown': "Shutting down computer in 5 seconds.",
            'restart': "Restarting computer in 5 seconds.",
            'sleep': "Computer going to sleep.",
            'lock': "Screen locked.",
            'hibernate': "Computer hibernating.",
            'calculator': "Calculator opened.",
            'notepad': "Notepad opened.",
            'chrome': "Chrome opened.",
            'edge': "Edge opened.",
            'explorer': "File Explorer opened.",
            'settings': "Windows Settings opened.",
            'taskmanager': "Task Manager opened.",
            'cmd': "Command Prompt opened.",
            'paint': "Paint opened.",
            'firefox': "Firefox opened.",
            'word': "Microsoft Word opened.",
            'excel': "Microsoft Excel opened.",
            'powerpoint': "PowerPoint opened.",
            'vlc': "VLC Media Player opened.",
            'vscode': "VS Code opened.",
            'spotify': "Spotify opened.",
            'steam': "Steam opened.",
            'google': "Google opened.",
            'youtube': "YouTube opened.",
            'wikipedia': "Wikipedia opened.",
            'stackoverflow': "Stack Overflow opened.",
            'github': "GitHub opened.",
            'amazon': "Amazon opened.",
            'flipkart': "Flipkart opened.",
            'instagram': "Instagram opened.",
            'facebook': "Facebook opened.",
            'twitter': "Twitter opened.",
            'linkedin': "LinkedIn opened.",
            'whatsapp_web': "WhatsApp Web opened.",
            'gmail': "Gmail opened.",
            'netflix': "Netflix opened.",
            'volume_up': "Volume increased.",
            'volume_down': "Volume decreased.",
            'mute': "Audio muted.",
            'screenshot': "Screenshot saved.",
            'desktop': "Desktop shown.",
            'minimize_all': "All windows minimized.",
            'brightness_up': "Brightness increased.",
            'brightness_down': "Brightness decreased.",
            'set_volume_60': "Volume set to 60%.",
            'volume_60': "Volume set to 60%.",
            'set_brightness_60': "Brightness set to 60%.",
            'brightness_60': "Brightness set to 60%.",
            'alt_tab': "Switched windows.",
            'copy': "Text copied.",
            'paste': "Text pasted.",
            'save': "File saved.",
            'undo': "Action undone.",
            'select_all': "All selected.",
            'close_chrome': "Chrome closed.",
            'close_edge': "Edge closed.",
            'close_notepad': "Notepad closed.",
            'downloads': "Downloads folder opened.",
            'documents': "Documents folder opened.",
            'pictures': "Pictures folder opened.",
            'cpu': f"CPU usage: {result}%",
            'memory': f"Memory usage: {result}%",
            'battery': f"Battery: {result}%" if result else "No battery detected",
            'time': f"Current time: {result}",
            'date': f"Today is {result}",
            'switch_to_gemini': "Switched to Gemini AI.",
            'switch_to_groq': "Switched to Groq AI.",
            'current_ai': f"Currently using {self.ai_provider.title()} AI.",
            'enable_face_auth': "Face recognition enabled.",
            'disable_face_auth': "Face recognition disabled.",
            'face_auth_status': "Face recognition status checked.",
            'switch_to_male_voice': "Voice switched to male.",
            'switch_to_female_voice': "Voice switched to female.",
            'male_voice': "Voice switched to male.",
            'female_voice': "Voice switched to female.",
            'current_voice_gender': "Voice gender status checked.",
            'voice_status': "Voice gender status checked.",
            
            # Advanced Features Responses
            'create_folder': "Folder created.",
            'create_new_file': "File created successfully.",
            'delete_file': "File deleted.",
            'search_files': "File search completed.",
            'copy_file': "File copied successfully.",
            'move_file': "File moved.",
            'check_internet': "Internet connection checked.",
            'ip_address': "IP address retrieved.",
            'wifi_password': "WiFi information retrieved.",
            'network_speed': "Network speed tested.",
            'disk_space': "Disk space checked.",
            'running_processes': "Process list retrieved.",
            'system_uptime': "System uptime checked.",
            'temperature': "System temperature checked.",
            'play_pause': "Media play/pause toggled.",
            'next_track': "Next track.",
            'previous_track': "Previous track.",
            'stop_media': "Media stopped.",
            'maximize_window': "Window maximized.",
            'minimize_window': "Window minimized.",
            'split_screen_left': "Screen split left.",
            'split_screen_right': "Screen split right.",
            'close_window': "Window closed.",
            'switch_window': "Window switched.",
            'find_text': "Find dialog opened.",
            'replace_text': "Replace dialog opened.",
            'new_document': "New document created.",
            'print_document': "Print dialog opened.",
            'zoom_in': "Zoomed in.",
            'zoom_out': "Zoomed out.",
            'clear_clipboard': "Clipboard cleared.",
            'clear_history': "Browser history cleared.",
            'empty_recycle_bin': "Recycle bin emptied.",
            'lock_screen': "Screen locked.",
        
            'schedule_shutdown': "Shutdown scheduled.",
            'auto_backup': "Backup completed.",
            'clean_temp': "Temporary files cleaned.",
            'play_music': "Music started.",
            'random_wallpaper': "Wallpaper changed.",
   
            'news': "News opened.",
            'quote': "Here's an inspirational quote.",
            
            # YouTube Automation Responses
            'youtube_play': "YouTube video play/paused.",
            'youtube_pause': "YouTube video paused.",
            'youtube_next': "Next YouTube video.",
            'youtube_previous': "Previous YouTube video.",
            'youtube_fullscreen': "YouTube fullscreen toggled.",
            'youtube_volume_up': "YouTube volume increased.",
            'youtube_volume_down': "YouTube volume decreased.",
            'youtube_mute': "YouTube muted/unmuted.",
            'youtube_speed_up': "YouTube speed increased.",
            'youtube_speed_down': "YouTube speed decreased.",
            'youtube_skip_forward': "YouTube skipped forward.",
            'youtube_skip_backward': "YouTube skipped backward.",
            'youtube_search': "YouTube search activated.",
            'youtube_subscribe': "YouTube subscribe clicked.",
            'youtube_like': "YouTube like clicked.",
            'youtube_dislike': "YouTube dislike clicked.",
            'youtube_comment': "YouTube comment box activated.",
            'youtube_share': "YouTube share clicked.",
            'youtube_theater_mode': "YouTube theater mode toggled.",
            'youtube_miniplayer': "YouTube miniplayer toggled.",
            'youtube_captions': "YouTube captions toggled.",
            'play_video': "Video search and play completed.",
            'play_movie': "Movie search and play completed.",
            'play_song': "Song search and play completed.",
            'search_and_play': "Search and play completed.",
            'open_multiple': "Multiple apps/websites opened.",
            
            # Chrome Automation Responses
            'chrome_new_tab': "New Chrome tab opened.",
            'chrome_close_tab': "Chrome tab closed.",
            'chrome_next_tab': "Switched to next Chrome tab.",
            'chrome_previous_tab': "Switched to previous Chrome tab.",
            'chrome_reload': "Chrome page reloaded.",
            'chrome_back': "Chrome navigated back.",
            'chrome_forward': "Chrome navigated forward.",
            'chrome_home': "Chrome home page opened.",
            'chrome_bookmark': "Chrome bookmark added.",
            'chrome_history': "Chrome history opened.",
            'chrome_downloads': "Chrome downloads opened.",
            'chrome_incognito': "Chrome incognito window opened.",
            'chrome_developer_tools': "Chrome developer tools toggled.",
            'chrome_zoom_in': "Chrome zoomed in.",
            'chrome_zoom_out': "Chrome zoomed out.",
            'chrome_zoom_reset': "Chrome zoom reset.",
            'chrome_find': "Chrome find dialog opened.",
            'chrome_print': "Chrome print dialog opened.",
            'chrome_save_page': "Chrome page saved.",
            'chrome_view_source': "Chrome page source opened.",
            'chrome_extensions': "Chrome extensions opened.",
            'chrome_settings': "Chrome settings opened.",
            'chrome_clear_data': "Chrome clear data dialog opened.",
            
            # Mapping Responses
            'open_maps': "Google Maps opened.",
            'find_location': "Location search opened.",
            'get_directions': "Directions opened.",
            'nearby_places': "Nearby places search opened.",
            'traffic_info': "Traffic information displayed.",
            'map_satellite': "Satellite view activated.",
            'map_terrain': "Terrain view activated.",
            'save_location': "Location saved.",
            'my_location': "Current location displayed.",
            'dictate_to_file': "Dictation to file completed.",
            'dictate_to_document': "Document dictation completed.",
            
            # System Monitoring Responses
            # 'system_monitor_live': "System monitoring dashboard displayed.",
            'auto_fix_system': "System auto-fix completed.",
            
            # Gesture Control Responses
            'start_gesture_control': "Hand, eye, and head control started.",
            'stop_gesture_control': "Gesture control stopped.",
            
            # Continuous Listening Responses
            'start_continuous_listen': "Continuous listening started.",
            'stop_continuous_listen': "Continuous listening stopped.",
            'continuous_listen_status': "Continuous listening status checked.",
            'weekday': "Current weekday retrieved.",
            'current_weekday': "Current weekday retrieved.",
            'traffic_updates': "Traffic information retrieved.",
            'public_holidays': "Holiday information retrieved.",
            'covid_stats': "COVID-19 statistics retrieved.",
            
            # Product Price Tracking Responses
            'track_amazon_price': "Amazon price tracking opened.",
            'track_flipkart_price': "Flipkart price tracking opened.",
            'check_product_price': "Product price comparison opened.",
            
            # Travel Search Responses
            'search_flights': "Flight search opened.",
            'search_hotels': "Hotel search opened.",
            'find_flights': "Flight search opened.",
            'find_hotels': "Hotel search opened.",
            
            # Streaming Search Responses
            'find_movie_streaming': "Movie streaming search opened.",
            'find_show_streaming': "Show streaming search opened.",
            'where_to_watch': "Streaming availability search opened.",
            'streaming_availability': "Streaming platforms search opened.",
            
            # File/Folder Opening Response
            'open_path': "File or folder opened.",
            
            # Alarm Responses
            'set_alarm': "Alarm set successfully.",
            'cancel_alarm': "Alarm cancelled.",
            
            # Random Generator Responses
            'dice': f" Dice rolled: {result}",
            'coin': f" Coin flip: {result}",
            'roll_dice': f" Dice rolled: {result}",
            'flip_coin': f" Coin flip: {result}",
        }
        
     
        
        # Get base response
        base_response = responses.get(func, "Task completed.")
        
        # Apply personality transformation safely
        if self.personality_manager:
            try:
                transformed = self.personality_manager.transform_response(base_response, 'success')
                if transformed and transformed.strip():
                    return transformed
            except:
                pass
        
        return base_response
    
    def _switch_to_gemini(self):
        return "gemini" if self._set_ai_provider('gemini') else "error"
    
    def _switch_to_groq(self):
        return "groq" if self._set_ai_provider('groq') else "error"
    
    def _get_current_ai(self):
        return self.ai_provider
    
    def _switch_to_hindi(self):
        if self.multilingual and self.multilingual.set_language('hindi'):
            # Reload the multilingual instance
            from engine.multilingual_support import reload_multilingual
            reload_multilingual()
            self.multilingual = multilingual
            return "भाषा हिंदी में बदल गई।"
        return "Language switched to Hindi."
    
    def _switch_to_kannada(self):
        if self.multilingual and self.multilingual.set_language('kannada'):
            # Reload the multilingual instance
            from engine.multilingual_support import reload_multilingual
            reload_multilingual()
            self.multilingual = multilingual
            return "ಭಾಷೆಯನ್ನು ಕನ್ನಡಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗಿದೆ।"
        return "Language switched to Kannada."
    
    def _switch_to_english(self):
        if self.multilingual and self.multilingual.set_language('english'):
            # Reload the multilingual instance
            from engine.multilingual_support import reload_multilingual
            reload_multilingual()
            self.multilingual = multilingual
            return "Language switched to English."
        return "Language switched to English."
    
    def _enable_face_auth(self):
        try:
            from engine.face_auth_config import set_face_auth_status
            set_face_auth_status(True)
            return "enabled"
        except:
            return "error"
    
    def _disable_face_auth(self):
        try:
            from engine.face_auth_config import set_face_auth_status
            set_face_auth_status(False)
            return "disabled"
        except:
            return "error"
    
    def _get_face_auth_status(self):
        try:
            from engine.face_auth_config import get_face_auth_status
            return "enabled" if get_face_auth_status() else "disabled"
        except:
            return "error"
    
    def _set_volume(self, level):
        try:
            level = max(0, min(100, level))
            subprocess.run(f'powershell -c "$obj = new-object -com wscript.shell; $obj.SendKeys([char]173); for($i=0; $i -lt 50; $i++){{$obj.SendKeys([char]174)}}; for($i=0; $i -lt {level//2}; $i++){{$obj.SendKeys([char]175)}}"', shell=True)
            return str(level)
        except:
            return "error"
    
    def _set_brightness(self, level):
        try:
            level = max(0, min(100, level))
            subprocess.run(f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"', shell=True)
            return str(level)
        except:
            return "error"
    
    def _handle_on_off(self, feature, action):
        """Handle dynamic on/off commands for any feature"""
        try:
            feature = feature.lower().strip()
            
            # WiFi - Quick toggle via Action Center
            if 'wifi' in feature or 'wi-fi' in feature:
                pyautogui.hotkey('win', 'a')  # Open Action Center
                pyautogui.sleep(0.5)
                pyautogui.press('space')  # Click WiFi tile
                pyautogui.press('escape')  # Close Action Center
                return f"WiFi toggled"
            
            # Bluetooth - Quick toggle via Action Center
            elif 'bluetooth' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                # Sometimes focus is not on first tile, so ensure keyboard focus lands
                pyautogui.press('right')   # Move focus to Bluetooth (if needed)
                time.sleep(0.2)
                pyautogui.press('space')      # Toggle Bluetooth (first tile focus)
                time.sleep(0.2)

                pyautogui.press('escape')
                return f"bluetooth toggled"
            
            # Airplane Mode - Admin control
            elif 'airplane' in feature or 'flight' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                # Sometimes focus is not on first tile, so ensure keyboard focus lands
                pyautogui.press('right')   # Move focus to Bluetooth (if needed)
                time.sleep(0.1)
                pyautogui.press('right')
                time.sleep(0.1) 
                pyautogui.press('space')      # Toggle Bluetooth (first tile focus)
                time.sleep(0.2)

                pyautogui.press('escape')
                return f"airplane toggled"
            
            elif 'battery saver' in feature or 'energy saver' in feature or 'save battery' in feature:
                    pyautogui.hotkey('win', 'a')   # Open Quick Settings
                    time.sleep(0.5)

                    pyautogui.press('down')        # Move to Battery Saver tile
                    time.sleep(0.1)

                    pyautogui.press('space')       # Toggle Battery Saver
                    time.sleep(0.2)

                    pyautogui.press('escape')      # Close panel
                    return "Battery Saver toggled"

            elif 'night' in feature or 'night mode' in feature or 'night light' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                pyautogui.press('down')        # Move to the second row
                time.sleep(0.1)
                pyautogui.press('right')       # Move to Night Mode tile
                time.sleep(0.1)
                pyautogui.press('space')       # Toggle Night Mode
                time.sleep(0.2)
                pyautogui.press('escape')      # Close Quick Settings
                return "Night Mode toggled"

            elif 'hotspot' in feature or 'mobile hotspot' in feature or 'wi-fi hotspot' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                pyautogui.press('down')        # Move to 2nd row
                time.sleep(0.1)
                pyautogui.press('down')        # Move to 3rd row (Hotspot row)
                time.sleep(0.1)
                pyautogui.press('right')       # Move to Hotspot tile
                time.sleep(0.1)
                pyautogui.press('space')       # Toggle Hotspot
                time.sleep(0.2)
                pyautogui.press('escape')      # Close Quick Settings
                return "Hotspot toggled"

            elif 'nearby' in feature or 'nearby share' in feature or 'share nearby' in feature:
                pyautogui.hotkey('win', 'a')   # Open Quick Settings
                time.sleep(0.5)
                pyautogui.press('down')        # Move to 2nd row
                time.sleep(0.1)
                pyautogui.press('down')        # Move to 3rd row
                time.sleep(0.1)
                pyautogui.press('right')       # Move to next tile
                time.sleep(0.1)
                pyautogui.press('right')       # Move to Nearby Share tile
                time.sleep(0.1)
                pyautogui.press('space')       # Toggle Nearby Share
                time.sleep(0.2)
                pyautogui.press('escape')      # Close Quick Settings
                return "Nearby Share toggled"

            
            # Location - Admin control
            elif 'location' in feature or 'gps' in feature:
                # Open Location Settings Page
                subprocess.Popen('start ms-settings:privacy-location', shell=True)
                time.sleep(1.8)  # wait for settings to open
              
                pyautogui.press('space')
                time.sleep(0.2)
               

                return "Location toggled"


            # Camera - Admin control
            elif 'camera' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam -Name Value -Value Allow\' -Verb RunAs"', shell=True)
                else:
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam -Name Value -Value Deny\' -Verb RunAs"', shell=True)
                return f"Camera {action}"
            
            # Microphone - Admin control
            elif 'microphone' in feature or 'mic' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone -Name Value -Value Allow\' -Verb RunAs"', shell=True)
                else:
                    subprocess.run('powershell -c "Start-Process powershell -ArgumentList \'Set-ItemProperty -Path HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone -Name Value -Value Deny\' -Verb RunAs"', shell=True)
                return f"Microphone {action}"
            
            # Dark Mode
            elif 'dark mode' in feature or 'dark theme' in feature:
                if action == 'on':
                    subprocess.run('powershell -c "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0"', shell=True)
                else:
                    subprocess.run('powershell -c "Set-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1"', shell=True)
                return f"Dark mode {action}"
  
            

                
        except Exception as e:
            return f"Error controlling {feature}: {str(e)}"
    

    
    # ===== ALL ADVANCED FEATURES METHODS =====
    
    # Voice Mouse Control
    def _move_mouse_up(self, pixels=50):
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(x, max(0, y - pixels))
            return f"Mouse moved up {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_down(self, pixels=50):
        try:
            x, y = pyautogui.position()
            screen_height = pyautogui.size().height
            pyautogui.moveTo(x, min(screen_height, y + pixels))
            return f"Mouse moved down {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_left(self, pixels=50):
        try:
            x, y = pyautogui.position()
            pyautogui.moveTo(max(0, x - pixels), y)
            return f"Mouse moved left {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_right(self, pixels=50):
        try:
            x, y = pyautogui.position()
            screen_width = pyautogui.size().width
            pyautogui.moveTo(min(screen_width, x + pixels), y)
            return f"Mouse moved right {pixels} pixels"
        except:
            return "Mouse movement failed"
    
    def _move_mouse_center(self):
        try:
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2)
            return "Mouse moved to center"
        except:
            return "Mouse movement failed"
    
    def _left_click(self):
        try:
            pyautogui.click()
            return "Left click performed"
        except:
            return "Click failed"
    
    def _right_click(self):
        try:
            pyautogui.rightClick()
            return "Right click performed"
        except:
            return "Right click failed"
    
    def _double_click(self):
        try:
            pyautogui.doubleClick()
            return "Double click performed"
        except:
            return "Double click failed"
    
    def _start_drag(self):
        try:
            pyautogui.mouseDown()
            return "Drag started"
        except:
            return "Drag start failed"
    
    def _drop_here(self):
        try:
            pyautogui.mouseUp()
            return "Drop completed"
        except:
            return "Drop failed"
    


    def _scroll_up(self, clicks=5):
        try:
            for _ in range(clicks):
                ctypes.windll.user32.mouse_event(0x0800, 0, 0, 120, 0)
            return f"Scrolled up {clicks}"
        except:
            return "Scroll failed"

    def _scroll_down(self, clicks=5):
        try:
            for _ in range(clicks):
                ctypes.windll.user32.mouse_event(0x0800, 0, 0, -120, 0)
            return f"Scrolled down {clicks}"
        except:
            return "Scroll failed"

    def _scroll_to_top(self):
        try:
            pyautogui.hotkey('ctrl', 'home')
            return "Scrolled to top"
        except:
            return "Scroll to top failed"
    
    # Voice Keyboard Control
    def _type_text(self, text=""):
        try:
            pyautogui.typewrite(text)
            return f"Typed: {text}"
        except:
            return "Text typing failed"
    
    def _press_enter(self):
        try:
            pyautogui.press('enter')
            return "Enter key pressed"
        except:
            return "Enter key failed"
    
    def _press_tab(self):
        try:
            pyautogui.press('tab')
            return "Tab key pressed"
        except:
            return "Tab key failed"
    
    def _press_escape(self):
        try:
            pyautogui.press('escape')
            return "Escape key pressed"
        except:
            return "Escape key failed"
    
    def _press_backspace(self):
        try:
            pyautogui.press('backspace')
            return "Backspace pressed"
        except:
            return "Backspace failed"
    
    def _press_delete(self):
        try:
            pyautogui.press('delete')
            return "Delete key pressed"
        except:
            return "Delete key failed"
    
    def _go_to_beginning(self):
        try:
            pyautogui.hotkey('ctrl', 'home')
            return "Moved to beginning"
        except:
            return "Go to beginning failed"
    
    def _go_to_end(self):
        try:
            pyautogui.hotkey('ctrl', 'end')
            return "Moved to end"
        except:
            return "Go to end failed"
    
    # File Operations
    def _create_folder(self, path="New Folder"):
        try:
            # Extract folder name and directory from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract folder name
                match = re.search(r'create folder\s+([^\s]+)', query)
                if match:
                    path = match.group(1)
                
                # Extract directory path
                target_dir = None
                dir_match = re.search(r'(?:on|in|to)\s+([^\s]+)', query)
                if dir_match:
                    dir_name = dir_match.group(1)
                    
                    # Common directory mappings
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads', 'doenload': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Check if it's a known directory
                    if dir_name in directory_map:
                        target_dir = os.path.join(os.path.expanduser("~"), directory_map[dir_name])
                    else:
                        # Use as direct path
                        if os.path.isabs(dir_name):
                            target_dir = dir_name
                        else:
                            home_path = os.path.join(os.path.expanduser("~"), dir_name)
                            target_dir = home_path if os.path.exists(home_path) else os.path.abspath(dir_name)
                
                # Default to Desktop if no directory specified
                if not target_dir:
                    target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            os.makedirs(target_dir, exist_ok=True)
            folder_path = os.path.join(target_dir, path)
            os.makedirs(folder_path, exist_ok=True)
            return f"Folder '{path}' created in {os.path.basename(target_dir)}"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"
    
    def _create_new_file(self, filename="new_file.txt", content=""):
        try:
            # Extract filename and directory from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract filename
                match = re.search(r'create (?:new )?file\s+([^\s]+)', query)
                if match:
                    filename = match.group(1)
                    if '.' not in filename:
                        filename += '.txt'
                
                # Extract directory path
                target_dir = None
                dir_match = re.search(r'(?:on|in|to)\s+([^\s]+)', query)
                if dir_match:
                    dir_name = dir_match.group(1)
                    
                    # Common directory mappings
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads', 'doenload': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Check if it's a known directory
                    if dir_name in directory_map:
                        target_dir = os.path.join(os.path.expanduser("~"), directory_map[dir_name])
                    else:
                        # Use as direct path
                        if os.path.isabs(dir_name):
                            target_dir = dir_name
                        else:
                            home_path = os.path.join(os.path.expanduser("~"), dir_name)
                            target_dir = home_path if os.path.exists(home_path) else os.path.abspath(dir_name)
                
                # Default to Desktop if no directory specified
                if not target_dir:
                    target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            os.makedirs(target_dir, exist_ok=True)
            file_path = os.path.join(target_dir, filename)
            
            # Handle duplicates
            counter = 1
            original_path = file_path
            while os.path.exists(file_path):
                name, ext = os.path.splitext(original_path)
                file_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Create the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content if content else "")
            
            return f"File '{os.path.basename(file_path)}' created at {file_path}"
            
        except Exception as e:
            return f"Error creating file: {str(e)}"
    
    def _delete_file(self, filename=""):
        try:
            # Extract filename and directory from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract filename
                match = re.search(r'delete file\s+([^\s]+)', query)
                if match:
                    filename = match.group(1)
                
                # Extract directory - support common directory names
                directory_map = {
                    'download': 'Downloads',
                    'downloads': 'Downloads', 
                    'doenload': 'Downloads',  # Handle typo
                    'document': 'Documents',
                    'documents': 'Documents',
                    'desktop': 'Desktop',
                    'picture': 'Pictures',
                    'pictures': 'Pictures',
                    'music': 'Music',
                    'video': 'Videos',
                    'videos': 'Videos'
                }
                
                target_dir = None
                for key, folder in directory_map.items():
                    if f'on {key}' in query or f'in {key}' in query or f'from {key}' in query:
                        target_dir = os.path.join(os.path.expanduser("~"), folder)
                        break
                
                # Default to Desktop if no directory specified
                if not target_dir:
                    target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            else:
                target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            file_path = os.path.join(target_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return f"File '{filename}' deleted from {os.path.basename(target_dir)}"
            return f"File '{filename}' not found in {os.path.basename(target_dir)}"
        except Exception as e:
            return f"Failed to delete file: {str(e)}"
    
    def _search_files(self, query=""):
        try:
            # Extract filename from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query_text = self._current_query.lower()
                
                # Extract filename from "search file filename" pattern
                match = re.search(r'search file\s+([^\s]+)', query_text)
                if match:
                    query = match.group(1)
            
            if not query:
                return "Please specify filename to search for"
            
            # Search in common directories
            search_dirs = [
                os.path.join(os.path.expanduser("~"), "Desktop"),
                os.path.join(os.path.expanduser("~"), "Downloads"),
                os.path.join(os.path.expanduser("~"), "Documents"),
                os.path.join(os.path.expanduser("~"), "Pictures"),
                os.path.join(os.path.expanduser("~"), "Videos"),
                os.path.join(os.path.expanduser("~"), "Music")
            ]
            
            matches = []
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for file in os.listdir(search_dir):
                        if query.lower() in file.lower():
                            matches.append(f"{file} (in {os.path.basename(search_dir)})")
            
            if matches:
                return f"Found {len(matches)} files: {', '.join(matches[:5])}{'...' if len(matches) > 5 else ''}"
            else:
                return f"No files found matching '{query}'"
        except Exception as e:
            return f"Error finding files: {str(e)}"
    
    def _copy_file(self, source="", destination=""):
        try:
            # Extract file copy details from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Parse "copy filename from_location to to_location" pattern
                copy_match = re.search(r'copy\s+([^\s]+)\s+([^\s]+)\s+to\s+([^\s]+)', query)
                if copy_match:
                    filename = copy_match.group(1)
                    from_location = copy_match.group(2)
                    to_location = copy_match.group(3)
                    
                    # Map common directory names
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'deckstop': 'Desktop',  # Handle typo
                        'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Get source directory
                    if from_location in directory_map:
                        source_dir = os.path.join(os.path.expanduser("~"), directory_map[from_location])
                    else:
                        source_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                    
                    # Get destination directory
                    if to_location in directory_map:
                        dest_dir = os.path.join(os.path.expanduser("~"), directory_map[to_location])
                    else:
                        dest_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                    
                    source = os.path.join(source_dir, filename)
                    destination = os.path.join(dest_dir, filename)
                    
                    # Check if source file exists
                    if not os.path.exists(source):
                        return f"File '{filename}' not found in {os.path.basename(source_dir)}"
                    
                    # Create destination directory if it doesn't exist
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Handle duplicate files
                    counter = 1
                    original_dest = destination
                    while os.path.exists(destination):
                        name, ext = os.path.splitext(original_dest)
                        destination = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    # Copy the file
                    shutil.copy2(source, destination)
                    return f"File '{filename}' copied from {os.path.basename(source_dir)} to {os.path.basename(dest_dir)}"
            
            # Fallback to original parameters
            if source and destination:
                shutil.copy2(source, destination)
                return "File copied successfully"
            
            return "Please specify source and destination"
            
        except Exception as e:
            return f"Failed to copy file: {str(e)}"
    
    def _move_file(self, source="", destination=""):
        try:
            # Extract file move details from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Parse "move filename from_location to to_location" pattern
                move_match = re.search(r'move\s+([^\s]+)\s+(?:from\s+)?([^\s]+)\s+to\s+([^\s]+)', query)
                if move_match:
                    filename = move_match.group(1)
                    from_location = move_match.group(2)
                    to_location = move_match.group(3)
                    
                    # Map common directory names
                    directory_map = {
                        'download': 'Downloads', 'downloads': 'Downloads',
                        'document': 'Documents', 'documents': 'Documents',
                        'desktop': 'Desktop', 'deckstop': 'Desktop',  # Handle typo
                        'picture': 'Pictures', 'pictures': 'Pictures',
                        'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
                    }
                    
                    # Get source directory
                    if from_location in directory_map:
                        source_dir = os.path.join(os.path.expanduser("~"), directory_map[from_location])
                    else:
                        source_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                    
                    # Get destination directory
                    if to_location in directory_map:
                        dest_dir = os.path.join(os.path.expanduser("~"), directory_map[to_location])
                    else:
                        dest_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                    
                    source = os.path.join(source_dir, filename)
                    destination = os.path.join(dest_dir, filename)
                    
                    # Check if source file exists
                    if not os.path.exists(source):
                        return f"File '{filename}' not found in {os.path.basename(source_dir)}"
                    
                    # Create destination directory if it doesn't exist
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Handle duplicate files
                    counter = 1
                    original_dest = destination
                    while os.path.exists(destination):
                        name, ext = os.path.splitext(original_dest)
                        destination = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    # Move the file
                    shutil.move(source, destination)
                    return f"File '{filename}' moved from {os.path.basename(source_dir)} to {os.path.basename(dest_dir)}"
            
            # Fallback to original parameters
            if source and destination:
                shutil.move(source, destination)
                return "File moved successfully"
            
            return "Please specify source and destination"
            
        except Exception as e:
            return f"Failed to move file: {str(e)}"
    
    def _rename_file_cmd(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'rename\s+([^\s]+)\s+to\s+([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                old_name, new_name, location = match.groups()
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                old_path = os.path.join(target_dir, old_name)
                new_path = os.path.join(target_dir, new_name)
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    return f"Renamed '{old_name}' to '{new_name}' in {os.path.basename(target_dir)}"
                return f"File '{old_name}' not found in {os.path.basename(target_dir)}"
            return "Usage: rename oldname to newname [in folder]"
        except Exception as e:
            return f"Rename failed: {str(e)}"
    
    def _zip_file(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'zip\s+(?:file\s+)?([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                filename, location = match.groups()
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(target_dir, filename)
                zip_path = file_path + '.zip'
                if os.path.exists(file_path):
                    with zipfile.ZipFile(zip_path, 'w') as zf:
                        zf.write(file_path, filename)
                    return f"Created {filename}.zip in {os.path.basename(target_dir)}"
                return f"File '{filename}' not found in {os.path.basename(target_dir)}"
            return "Usage: zip file filename [in folder]"
        except Exception as e:
            return f"Zip failed: {str(e)}"
    
    def _unzip_file(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'(?:unzip|extract)\s+([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                filename, location = match.groups()
                if not filename.endswith('.zip'):
                    filename += '.zip'
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                zip_path = os.path.join(target_dir, filename)
                if os.path.exists(zip_path):
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        zf.extractall(target_dir)
                    return f"Extracted {filename} in {os.path.basename(target_dir)}"
                return f"Zip file '{filename}' not found in {os.path.basename(target_dir)}"
            return "Usage: unzip filename [in folder]"
        except Exception as e:
            return f"Unzip failed: {str(e)}"
    
    def _get_file_size(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'(?:file\s+size|size\s+of)\s+([^\s]+)(?:\s+in\s+([^\s]+))?', query)
            if match:
                filename, location = match.groups()
                target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(target_dir, filename)
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path)
                    if size < 1024:
                        return f"{filename}: {size} bytes"
                    elif size < 1024*1024:
                        return f"{filename}: {size/1024:.1f} KB"
                    else:
                        return f"{filename}: {size/(1024*1024):.1f} MB"
                return f"File '{filename}' not found in {os.path.basename(target_dir)}"
            return "Usage: file size filename [in folder]"
        except Exception as e:
            return f"Get file size failed: {str(e)}"
    
    def _list_files(self):
        try:
            import re
            query = self._current_query.lower()
            match = re.search(r'list\s+files(?:\s+in\s+([^\s]+))?', query)
            location = match.group(1) if match else None
            target_dir = self._get_directory(location) if location else os.path.join(os.path.expanduser("~"), "Desktop")
            files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
            folders = [f for f in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, f))]
            return f"{os.path.basename(target_dir)}: {len(files)} files, {len(folders)} folders. Recent: {', '.join(files[:3])}"
        except Exception as e:
            return f"List files failed: {str(e)}"
    
    def _get_directory(self, query_or_location):
        """Get directory path from query or location name"""
        if not query_or_location:
            return os.path.join(os.path.expanduser("~"), "Desktop")
        
        # If it's a query, extract directory from it
        if isinstance(query_or_location, str) and len(query_or_location) > 20:
            import re
            # Look for directory patterns in query
            dir_match = re.search(r'(?:in|on|from|to)\s+([^\s]+)', query_or_location.lower())
            if dir_match:
                location = dir_match.group(1)
            else:
                location = None
        else:
            location = query_or_location
        
        if not location:
            return os.path.join(os.path.expanduser("~"), "Desktop")
        
        directory_map = {
            'download': 'Downloads', 'downloads': 'Downloads',
            'document': 'Documents', 'documents': 'Documents',
            'desktop': 'Desktop', 'deckstop': 'Desktop',
            'picture': 'Pictures', 'pictures': 'Pictures',
            'music': 'Music', 'video': 'Videos', 'videos': 'Videos'
        }
        
        if location in directory_map:
            return os.path.join(os.path.expanduser("~"), directory_map[location])
        elif os.path.isabs(location):
            return location
        else:
            # Try as relative path from home directory
            home_path = os.path.join(os.path.expanduser("~"), location)
            if os.path.exists(home_path):
                return home_path
            # Fallback to Desktop
            return os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Network & Internet
    def _ping_test(self):
        try:
            result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                                  capture_output=True, text=True, timeout=5)
            return "Internet connected" if result.returncode == 0 else "No internet connection"
        except:
            return "Network check failed"
    
    def _get_ip(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"Your IP address is {ip}"
        except:
            return "Could not get IP address"
    
    def _get_wifi_password(self):
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile'], 
                                  capture_output=True, text=True)
            profiles = [line.split(':')[1].strip() for line in result.stdout.split('\n') 
                       if 'All User Profile' in line]
            if profiles:
                return f"Found {len(profiles)} WiFi networks"
            return "No WiFi profiles found"
        except:
            return "Could not retrieve WiFi information"
    
    def _speed_test(self):
        try:
            response = requests.get('http://www.google.com', timeout=3)
            return f"Internet speed test completed in {response.elapsed.total_seconds():.2f} seconds"
        except:
            return "Speed test failed"
    
    # System Monitoring
    def _get_disk_space(self):
        try:
            disk = psutil.disk_usage('C:')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            return f"Disk space: {free_gb:.1f}GB free of {total_gb:.1f}GB total"
        except:
            return "Could not get disk space"
    
    def _list_processes(self):
        try:
            processes = len(psutil.pids())
            return f"Currently running {processes} processes"
        except:
            return "Could not get process information"
    
    def _get_uptime(self):
        try:
            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            return f"System uptime: {hours} hours, {minutes} minutes"
        except:
            return "Could not get uptime"
    
    def _get_cpu_temp(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"CPU usage: {cpu_percent}%"
        except:
            return "Could not get CPU information"
    
    # Entertainment
    def _tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why don't programmers like nature? It has too many bugs!",
            "What do you call a computer that sings? A Dell!",
            "Why was the computer cold? It left its Windows open!"
        ]
        return random.choice(jokes)
    
    def _get_quote(self):
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle"
        ]
        return random.choice(quotes)
    

    
    def _get_news(self):
        try:
            return "Opening news website for latest updates"
        except:
            return "Could not get news"
    
    # Placeholder methods for remaining features
    def _next_window(self):
        try:
            pyautogui.hotkey('alt', 'tab')
            return "Switched to next window"
        except:
            return "Window switch failed"
    
    def _previous_window(self):
        try:
            pyautogui.hotkey('alt', 'shift', 'tab')
            return "Switched to previous window"
        except:
            return "Window switch failed"
    
    def _close_all_windows(self):
        try:
            pyautogui.hotkey('win', 'd')
            return "All windows minimized"
        except:
            return "Minimize all failed"
    
    def _snap_left(self):
        try:
            pyautogui.hotkey('win', 'left')
            return "Window snapped left"
        except:
            return "Snap left failed"
    
    def _snap_right(self):
        try:
            pyautogui.hotkey('win', 'right')
            return "Window snapped right"
        except:
            return "Snap right failed"
    
    def _full_screen(self):
        try:
            pyautogui.press('f11')
            return "Full screen toggled"
        except:
            return "Full screen failed"
    
    def _restore_window(self):
        try:
            pyautogui.hotkey('win', 'up')
            return "Window restored"
        except:
            return "Window restore failed"
    
    def _open_recent_file(self):
        try:
            pyautogui.hotkey('ctrl', 'o')
            return "Recent file dialog opened"
        except:
            return "Open file failed"
    
    def _rename_file(self):
        try:
            pyautogui.press('f2')
            return "File rename activated"
        except:
            return "Rename failed"
    
    def _duplicate_file(self):
        try:
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey('ctrl', 'v')
            return "File duplicated"
        except:
            return "Duplicate failed"
    
    def _compress_file(self):
        try:
            pyautogui.rightClick()
            time.sleep(0.5)
            pyautogui.typewrite('compress')
            return "File compression started"
        except:
            return "Compression failed"
    
    def _extract_archive(self):
        try:
            pyautogui.rightClick()
            time.sleep(0.5)
            pyautogui.typewrite('extract')
            return "Archive extraction started"
        except:
            return "Extraction failed"
    
    def _open_new_tab(self):
        try:
            pyautogui.hotkey('ctrl', 't')
            return "New tab opened"
        except:
            return "New tab failed"
    
    def _close_current_tab(self):
        try:
            pyautogui.hotkey('ctrl', 'w')
            return "Tab closed"
        except:
            return "Close tab failed"
    
    def _switch_to_next_tab(self):
        try:
            pyautogui.hotkey('ctrl', 'tab')
            return "Switched to next tab"
        except:
            return "Tab switch failed"
    
    def _switch_to_previous_tab(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            return "Switched to previous tab"
        except:
            return "Tab switch failed"
    
    def _refresh_page(self):
        try:
            pyautogui.press('f5')
            return "Page refreshed"
        except:
            return "Refresh failed"
    
    def _go_back(self):
        try:
            pyautogui.hotkey('alt', 'left')
            return "Navigated back"
        except:
            return "Back navigation failed"
    
    def _go_forward(self):
        try:
            pyautogui.hotkey('alt', 'right')
            return "Navigated forward"
        except:
            return "Forward navigation failed"
    
    def _bookmark_page(self):
        try:
            pyautogui.hotkey('ctrl', 'd')
            return "Page bookmarked"
        except:
            return "Bookmark failed"
    
    def _open_bookmarks(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'b')
            return "Bookmarks opened"
        except:
            return "Bookmarks failed"
    
    def _search_web(self, query=""):
        try:
            pyautogui.hotkey('ctrl', 'l')
            pyautogui.typewrite(query)
            pyautogui.press('enter')
            return f"Searching for: {query}"
        except:
            return "Web search failed"
    
    def _skip_forward(self):
        try:
            pyautogui.hotkey('ctrl', 'right')
            return "Skipped forward"
        except:
            return "Skip forward failed"
    
    def _skip_backward(self):
        try:
            pyautogui.hotkey('ctrl', 'left')
            return "Skipped backward"
        except:
            return "Skip backward failed"
    
    def _increase_speed(self):
        try:
            pyautogui.hotkey('shift', '>')
            return "Speed increased"
        except:
            return "Speed increase failed"
    
    def _decrease_speed(self):
        try:
            pyautogui.hotkey('shift', '<')
            return "Speed decreased"
        except:
            return "Speed decrease failed"
    
    def _toggle_fullscreen(self):
        try:
            pyautogui.press('f')
            return "Fullscreen toggled"
        except:
            return "Fullscreen failed"
    
    def _toggle_subtitles(self):
        try:
            pyautogui.press('c')
            return "Subtitles toggled"
        except:
            return "Subtitles failed"
    
    def _dictate_email(self):
        try:
            subprocess.Popen('start mailto:', shell=True)
            return "Email dictation started"
        except:
            return "Email dictation failed"
    
    def _dictate_document(self):
        try:
            subprocess.Popen('notepad', shell=True)
            return "Document dictation started"
        except:
            return "Document dictation failed"
    
    def _take_screenshot_window(self):
        try:
            pyautogui.hotkey('alt', 'printscreen')
            return "Window screenshot taken"
        except:
            return "Window screenshot failed"
    
    def _take_screenshot_area(self):
        try:
            pyautogui.hotkey('win', 'shift', 's')
            return "Screenshot area selected"
        except:
            return "Area screenshot failed"
    
    def _start_screen_recording(self):
        try:
            pyautogui.hotkey('win', 'g')
            return "Screen recording started"
        except:
            return "Screen recording failed"
    
    def _stop_screen_recording(self):
        try:
            pyautogui.hotkey('win', 'alt', 'r')
            return "Screen recording stopped"
        except:
            return "Stop recording failed"
    
    def _wikipedia_search(self, query=""):
        try:
            import urllib.parse
            if not query:
                subprocess.Popen('start https://wikipedia.org', shell=True)
            else:
                url = f"https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(query)}"
                subprocess.Popen(f'start {url}', shell=True)
            return "Wikipedia search opened"
        except:
            return "Wikipedia search failed"
    
    def _movie_recommend(self):
        try:
            subprocess.Popen('start https://www.imdb.com/chart/top', shell=True)
            return "Movie recommendations opened"
        except:
            return "Movie recommendations failed"
    
   
    
    def _game_launch(self):
        try:
            subprocess.Popen('start steam:', shell=True)
            return "Game launcher opened"
        except:
            return "Game launch failed"
    
    def _streaming_control(self):
        try:
            subprocess.Popen('start https://netflix.com', shell=True)
            return "Streaming service opened"
        except:
            return "Streaming control failed"
    
    def _playlist_manage(self):
        try:
            subprocess.Popen('start spotify:', shell=True)
            return "Playlist manager opened"
        except:
            return "Playlist management failed"

   
    
    # Additional missing methods
    def _play_music(self, genre="random"):
        try:
            subprocess.run('start spotify:', shell=True)
            time.sleep(3)
            pyautogui.press('space')
            return f"Playing {genre} music on Spotify"
        except:
            return "Could not play music"
    
    def _change_wallpaper(self):
        try:
            subprocess.run('start ms-settings:personalization-background', shell=True)
            return "Wallpaper settings opened"
        except:
            return "Could not change wallpaper"
    
   
    
    def _schedule_shutdown(self, time_str="1 hour"):
        try:
            minutes = 60
            if "minute" in time_str:
                minutes = int(''.join(filter(str.isdigit, time_str))) or 60
            elif "hour" in time_str:
                hours = int(''.join(filter(str.isdigit, time_str))) or 1
                minutes = hours * 60
            seconds = minutes * 60
            subprocess.run(f'shutdown /s /t {seconds}', shell=True)
            return f"Shutdown scheduled in {minutes} minutes"
        except:
            return "Could not schedule shutdown"
    
    def _backup_files(self):
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            backup_folder = os.path.join(desktop, f"Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            documents = os.path.join(os.path.expanduser("~"), "Documents")
            os.makedirs(backup_folder, exist_ok=True)
            for file in os.listdir(documents)[:5]:
                try:
                    shutil.copy2(os.path.join(documents, file), backup_folder)
                except:
                    continue
            return f"Backup created in {backup_folder}"
        except:
            return "Backup failed"
    
    def _clean_temp_files(self):
        try:
            temp_folder = os.environ.get('TEMP')
            if temp_folder:
                files_deleted = 0
                for file in os.listdir(temp_folder):
                    try:
                        file_path = os.path.join(temp_folder, file)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                    except:
                        continue
                return f"Cleaned {files_deleted} temporary files"
            return "Could not access temp folder"
        except:
            return "Temp cleanup failed"
    
    def _clear_clipboard(self): 
        try:
            pyautogui.copy('')
            return "Clipboard cleared"
        except:
            return "Clipboard clear failed"
    
    def _clear_browser_history(self):
        try:
            chrome_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
            if os.path.exists(chrome_path):
                subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], shell=True)
                time.sleep(2)
                os.remove(chrome_path)
            return "Browser history cleared"
        except:
            return "Could not clear browser history"
    
    def _empty_recycle_bin(self):
        try:
            subprocess.run('powershell -c "Clear-RecycleBin -Force"', shell=True)
            return "Recycle bin emptied"
        except:
            return "Could not empty recycle bin"
    
    def _lock_screen(self):
        try:
            subprocess.run('rundll32.exe user32.dll,LockWorkStation', shell=True)
            return "Screen locked"
        except:
            return "Screen lock failed"
    
    def _find_text(self): 
        try:
            pyautogui.hotkey('ctrl', 'f')
            return "Find dialog opened"
        except:
            return "Find text failed"
    
    def _replace_text(self): 
        try:
            pyautogui.hotkey('ctrl', 'h')
            return "Replace dialog opened"
        except:
            return "Replace text failed"
    
    def _new_document(self): 
        try:
            pyautogui.hotkey('ctrl', 'n')
            return "New document created"
        except:
            return "New document failed"
    
    def _print_document(self): 
        try:
            pyautogui.hotkey('ctrl', 'p')
            return "Print dialog opened"
        except:
            return "Print document failed"
    
    def _zoom_in(self): 
        try:
            pyautogui.hotkey('ctrl', 'plus')
            return "Zoomed in"
        except:
            return "Zoom in failed"
    
    def _zoom_out(self): 
        try:
            pyautogui.hotkey('ctrl', 'minus')
            return "Zoomed out"
        except:
            return "Zoom out failed"
    
    def _maximize_window(self): 
        try:
            pyautogui.hotkey('win', 'up')
            return "Window maximized"
        except:
            return "Maximize window failed"
    
    def _minimize_window(self): 
        try:
            pyautogui.hotkey('win', 'down')
            pyautogui.hotkey('win', 'down')
            return "Window minimized"
        except:
            return "Minimize window failed"
    
    def _split_screen_left(self): 
        try:
            pyautogui.hotkey('win', 'left')
            return "Screen split left"
        except:
            return "Split screen left failed"
    
    def _split_screen_right(self): 
        try:
            pyautogui.hotkey('win', 'right')
            return "Screen split right"
        except:
            return "Split screen right failed"
    
    def _close_window(self): 
        try:
            pyautogui.hotkey('alt', 'f4')
            return "Window closed"
        except:
            return "Close window failed"
    
    def _switch_window(self): 
        try:
            pyautogui.hotkey('alt', 'tab')
            return "Window switched"
        except:
            return "Switch window failed"
    
    def _play_pause(self): 
        try:
            pyautogui.press('space')
            return "Media play/pause toggled"
        except:
            return "Play/pause failed"
    
    def _next_track(self): 
        try:
            pyautogui.press('nexttrack')
            return "Next track"
        except:
            return "Next track failed"
    
    def _previous_track(self): 
        try:
            pyautogui.press('prevtrack')
            return "Previous track"
        except:
            return "Previous track failed"
    
    def _stop_media(self): 
        try:
            pyautogui.press('stop')
            return "Media stopped"
        except:
            return "Stop media failed"
    
    # YouTube Automation Methods
    def _youtube_play(self):
        try:
            # Try both space and k key for play/pause
            pyautogui.press('space')
            time.sleep(0.2)
            return "YouTube video play/paused"
        except:
            try:
                pyautogui.press('k')
                return "YouTube video play/paused"
            except:
                return "YouTube play failed"
    
    def _youtube_pause(self):
        try:
            pyautogui.press('space')
            return "YouTube video paused"
        except:
            try:
                pyautogui.press('k')
                return "YouTube video paused"
            except:
                return "YouTube pause failed"
    
    def _youtube_next(self):
        try:
            pyautogui.hotkey('shift', 'n')
            return "Next YouTube video"
        except:
            return "YouTube next failed"
    
    def _youtube_previous(self):
        try:
            pyautogui.hotkey('shift', 'p')
            return "Previous YouTube video"
        except:
            return "YouTube previous failed"
    
    def _youtube_fullscreen(self):
        try:
            pyautogui.press('f')
            return "YouTube fullscreen toggled"
        except:
            return "YouTube fullscreen failed"
    
    def _youtube_volume_up(self):
        try:
            pyautogui.press('up')
            return "YouTube volume increased"
        except:
            return "YouTube volume up failed"
    
    def _youtube_volume_down(self):
        try:
            pyautogui.press('down')
            return "YouTube volume decreased"
        except:
            return "YouTube volume down failed"
    
    def _youtube_mute(self):
        try:
            pyautogui.press('m')
            return "YouTube muted/unmuted"
        except:
            return "YouTube mute failed"
    
    def _youtube_speed_up(self):
        try:
            pyautogui.hotkey('shift', '>')
            return "YouTube speed increased"
        except:
            return "YouTube speed up failed"
    
    def _youtube_speed_down(self):
        try:
            pyautogui.hotkey('shift', '<')
            return "YouTube speed decreased"
        except:
            return "YouTube speed down failed"
    
    def _youtube_skip_forward(self):
        try:
            pyautogui.press('l')
            return "YouTube skipped forward 10 seconds"
        except:
            return "YouTube skip forward failed"
    
    def _youtube_skip_backward(self):
        try:
            pyautogui.press('j')
            return "YouTube skipped backward 10 seconds"
        except:
            return "YouTube skip backward failed"
    
    def _youtube_search(self):
        try:
            pyautogui.press('/')
            return "YouTube search activated"
        except:
            return "YouTube search failed"
    
    def _youtube_subscribe(self):
        try:
            pyautogui.click(1200, 400)  # Approximate subscribe button location
            return "YouTube subscribe clicked"
        except:
            return "YouTube subscribe failed"
    
    def _youtube_like(self):
        try:
            pyautogui.click(1100, 500)  # Approximate like button location
            return "YouTube like clicked"
        except:
            return "YouTube like failed"
    
    def _youtube_dislike(self):
        try:
            pyautogui.click(1150, 500)  # Approximate dislike button location
            return "YouTube dislike clicked"
        except:
            return "YouTube dislike failed"
    
    def _youtube_comment(self):
        try:
            pyautogui.scroll(-5)
            pyautogui.click(600, 700)  # Approximate comment box location
            return "YouTube comment box activated"
        except:
            return "YouTube comment failed"
    
    def _youtube_share(self):
        try:
            pyautogui.click(1200, 500)  # Approximate share button location
            return "YouTube share clicked"
        except:
            return "YouTube share failed"
    
    def _youtube_theater_mode(self):
        try:
            pyautogui.press('t')
            return "YouTube theater mode toggled"
        except:
            return "YouTube theater mode failed"
    
    def _youtube_miniplayer(self):
        try:
            pyautogui.press('i')
            return "YouTube miniplayer toggled"
        except:
            return "YouTube miniplayer failed"
    
    def _youtube_captions(self):
        try:
            pyautogui.press('c')
            return "YouTube captions toggled"
        except:
            return "YouTube captions failed"
    
    def _play_video(self, video_name=""):
        return self._search_and_play(video_name)
    
    def _play_movie(self, movie_name=""):
        return self._search_and_play(f"{movie_name} movie")
    
    def _play_song(self, song_name=""):
        return self._search_and_play(f"{song_name} song")
    
    def _search_and_play(self, search_term=""):
        try:
            if not search_term:
                return "Please specify what to search for"
            
            # Method 1: Try to get first video using requests and parse HTML
            try:
                import requests
                import re
                import webbrowser
                import urllib.parse
                
                # Search YouTube and get first video ID
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_term)}"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                
                response = requests.get(search_url, headers=headers)
                
                # Find first video ID in the HTML
                video_id_match = re.search(r'"videoId":"([^"]+)"', response.text)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(video_url)
                    # Wait for page to load then press space to play
                    import threading
                    def auto_play():
                        time.sleep(5)
                        pyautogui.press('space')
                    threading.Thread(target=auto_play, daemon=True).start()
                    return f"Playing first result for: {search_term}"
                
            except:
                pass
            
            # Method 2: Fallback to search results
            import webbrowser
            import urllib.parse
            
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_term)
            webbrowser.open(url)
            return f"Opened YouTube search for: {search_term} (click first video to play)"
                
        except Exception as e:
            return f"Failed to play {search_term}: {str(e)}"
    
    def _search_and_play_simple(self, search_term):
        try:
            # Simple direct approach - open YouTube and search
            subprocess.run('start chrome https://www.youtube.com', shell=True)
            time.sleep(3)
            
            # Click search box
            pyautogui.click(640, 100)
            time.sleep(1)
            
            # Type and search
            pyautogui.typewrite(search_term)
            pyautogui.press('enter')
            time.sleep(4)
            
            # Click first video - try multiple positions
            positions = [(320, 300), (320, 350), (320, 400), (280, 350), (360, 350)]
            for x, y in positions:
                pyautogui.click(x, y)
                time.sleep(3)  # Wait for video page to load
                
                # Click play button on video player
                pyautogui.click(640, 360)  # Center of video player
                time.sleep(1)
                pyautogui.press('space')  # Ensure video starts playing
                break
            
            return f"Playing: {search_term}"
        except Exception as e:
            return f"Simple method failed: {str(e)}"
    
    def _play_direct_video(self, search_term):
        """Direct method using webbrowser"""
        try:
            import webbrowser
            import urllib.parse
            
            # Create YouTube search URL
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_term)
            webbrowser.open(url)
            
            return f"Opened YouTube search for: {search_term}"
                
        except Exception as e:
            return f"Direct video failed: {str(e)}"
    
    def _focus_chrome(self):
        """Helper method to ensure Chrome window is focused"""
        try:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(0.2)
        except:
            pass
   
    
    # Chrome Automation Methods - Fixed and Improved
    def _chrome_new_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 't')
            time.sleep(0.3)
            return "New Chrome tab opened"
        except Exception as e:
            return f"Chrome new tab failed: {str(e)}"
    
    def _chrome_close_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.3)
            return "Chrome tab closed"
        except Exception as e:
            return f"Chrome close tab failed: {str(e)}"
    
    def _chrome_next_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'pagedown')
            time.sleep(0.2)
            return "Switched to next Chrome tab"
        except:
            try:
                pyautogui.hotkey('ctrl', 'tab')
                return "Switched to next Chrome tab"
            except Exception as e:
                return f"Chrome next tab failed: {str(e)}"
    
    def _chrome_previous_tab(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'pageup')
            time.sleep(0.2)
            return "Switched to previous Chrome tab"
        except:
            try:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                return "Switched to previous Chrome tab"
            except Exception as e:
                return f"Chrome previous tab failed: {str(e)}"
    
    def _chrome_reload(self):
        try:
            self._focus_chrome()
            pyautogui.hotkey('ctrl', 'r')
            time.sleep(0.3)
            return "Chrome page reloaded"
        except:
            try:
                pyautogui.press('f5')
                return "Chrome page reloaded"
            except Exception as e:
                return f"Chrome reload failed: {str(e)}"
    
    def _chrome_back(self):
        try:
            pyautogui.hotkey('alt', 'left')
            return "Chrome navigated back"
        except:
            return "Chrome back failed"
    
    def _chrome_forward(self):
        try:
            pyautogui.hotkey('alt', 'right')
            return "Chrome navigated forward"
        except:
            return "Chrome forward failed"
    
    def _chrome_home(self):
        try:
            pyautogui.hotkey('alt', 'home')
            return "Chrome home page opened"
        except:
            return "Chrome home failed"
    
    def _chrome_bookmark(self):
        try:
            pyautogui.hotkey('ctrl', 'd')
            return "Chrome bookmark added"
        except:
            return "Chrome bookmark failed"
    
    def _chrome_history(self):
        try:
            pyautogui.hotkey('ctrl', 'h')
            return "Chrome history opened"
        except:
            return "Chrome history failed"
    
    def _chrome_downloads(self):
        try:
            pyautogui.hotkey('ctrl', 'j')
            return "Chrome downloads opened"
        except:
            return "Chrome downloads failed"
    
    def _chrome_incognito(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'n')
            return "Chrome incognito window opened"
        except:
            return "Chrome incognito failed"
    
    def _chrome_developer_tools(self):
        try:
            pyautogui.press('f12')
            return "Chrome developer tools toggled"
        except:
            return "Chrome developer tools failed"
    
    def _chrome_zoom_in(self):
        try:
            pyautogui.hotkey('ctrl', 'plus')
            return "Chrome zoomed in"
        except:
            return "Chrome zoom in failed"
    
    def _chrome_zoom_out(self):
        try:
            pyautogui.hotkey('ctrl', 'minus')
            return "Chrome zoomed out"
        except:
            return "Chrome zoom out failed"
    
    def _chrome_zoom_reset(self):
        try:
            pyautogui.hotkey('ctrl', '0')
            return "Chrome zoom reset"
        except:
            return "Chrome zoom reset failed"
    
    def _chrome_find(self):
        try:
            pyautogui.hotkey('ctrl', 'f')
            return "Chrome find dialog opened"
        except:
            return "Chrome find failed"
    
    def _chrome_print(self):
        try:
            pyautogui.hotkey('ctrl', 'p')
            return "Chrome print dialog opened"
        except:
            return "Chrome print failed"
    
    def _chrome_save_page(self):
        try:
            pyautogui.hotkey('ctrl', 's')
            return "Chrome page saved"
        except:
            return "Chrome save page failed"
    
    def _chrome_view_source(self):
        try:
            pyautogui.hotkey('ctrl', 'u')
            return "Chrome page source opened"
        except:
            return "Chrome view source failed"
    
    def _chrome_extensions(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'delete')
            return "Chrome extensions opened"
        except:
            return "Chrome extensions failed"
    
    def _chrome_settings(self):
        try:
            # Method 1: Try to open Chrome first, then navigate to settings
            subprocess.Popen('start chrome', shell=True)
            time.sleep(3)  # Wait for Chrome to open
            
            # Navigate to settings using keyboard shortcut
            pyautogui.hotkey('ctrl', 'l')  # Focus address bar
            time.sleep(0.5)
            pyautogui.typewrite('chrome://settings/')
            pyautogui.press('enter')
            time.sleep(1)
            return "Chrome settings opened"
        except Exception as e:
            try:
                # Method 2: Direct webbrowser approach
                import webbrowser
                webbrowser.open('chrome://settings/')
                time.sleep(2)
                return "Chrome settings opened"
            except Exception as e2:
                try:
                    # Method 3: Use Chrome command line
                    subprocess.Popen(['chrome', '--new-tab', 'chrome://settings/'], shell=True)
                    time.sleep(2)
                    return "Chrome settings opened"
                except Exception as e3:
                    return f"Chrome settings failed: {str(e3)}"
    
    def _chrome_clear_data(self):
        try:
            pyautogui.hotkey('ctrl', 'shift', 'delete')
            return "Chrome clear data dialog opened"
        except:
            return "Chrome clear data failed"
    
    def _open_path(self, path_query=""):
        """Enhanced file/folder opening with smart mapping and search"""
        try:
            import os
            import subprocess
            import glob
            
            # Get query from current command if not provided
            if not path_query and hasattr(self, '_current_query'):
                path_query = self._current_query
            
            if not path_query:
                return "Please specify what to open"
            
            query = path_query.lower().strip()
            
            # Handle recent files commands
            if any(phrase in query for phrase in ["recent files", "recent documents", "recently used files", "show recent files", "show recently used", "open recent"]):
                try:
                    import glob
                    import time
                    
                    # Windows stores recent files in this folder
                    recent_folder = os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Recent")
                    
                    # Get all recent items (*.lnk = shortcut files)
                    recent_files = glob.glob(os.path.join(recent_folder, "*.lnk"))
                    
                    if not recent_files:
                        return "No recent files found"
                    
                    # Filter out system files and keep only user documents
                    user_files = []
                    for file in recent_files:
                        name = os.path.basename(file).lower()
                        # Skip system files and keep user documents
                        if not any(skip in name for skip in ['ms-', 'system', 'windows', 'program', 'temp', 'cache']):
                            # Keep files with common document extensions
                            if any(ext in name for ext in ['.doc', '.pdf', '.ppt', '.xls', '.txt', '.jpg', '.png', '.mp4', '.mp3']):
                                user_files.append(file)
                    
                    # If no user files found, use all recent files
                    if not user_files:
                        user_files = recent_files
                    
                    # Sort by last modified (newest first)
                    user_files.sort(key=os.path.getmtime, reverse=True)
                    recent_files = user_files
                    
                    # Check if user wants to open recent file
                    if "open recent" in query:
                        # Open the first (most recent) file
                        first_recent = recent_files[0]
                        file_name = os.path.basename(first_recent).replace(".lnk", "")
                        # Clean file name to avoid encoding issues
                        file_name = ''.join(char for char in file_name if ord(char) < 128)
                        
                        # Try to resolve the shortcut and open the actual file
                        try:
                            # Use PowerShell to resolve the shortcut
                            ps_command = f'powershell -c "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(\"{first_recent}\"); $s.TargetPath"'
                            result = subprocess.run(ps_command, shell=True, capture_output=True, text=True)
                            
                            if result.returncode == 0 and result.stdout.strip():
                                target_path = result.stdout.strip()
                                if os.path.exists(target_path):
                                    subprocess.run(f'start "" "{target_path}"', shell=True)
                                    return f"{file_name} recent file opened"
                        except:
                            pass
                        
                        # Fallback: try to open the shortcut directly
                        subprocess.run(f'start "" "{first_recent}"', shell=True)
                        return f"{file_name} recent file opened"
                    
                    # Check for specific number of files to show
                    import re
                    number_match = re.search(r'(\d+)', query)
                    if number_match:
                        num_files = min(int(number_match.group(1)), len(recent_files))
                        top_recent = recent_files[:num_files]
                        # Limit the actual display to requested number
                        recent_files = top_recent
                    else:
                        # Default to 5 files
                        top_recent = recent_files[:5]
                        recent_files = top_recent
                    
                    # Get file names without .lnk extension and clean them
                    recent_names = []
                    for f in top_recent:
                        name = os.path.basename(f).replace(".lnk", "")
                        # Remove special characters that might cause encoding issues
                        clean_name = ''.join(char for char in name if ord(char) < 128)
                        recent_names.append(clean_name)
                    
                    # Open the Windows Recent Items folder
                    subprocess.run(f'explorer "{recent_folder}"', shell=True)
                    
                    # Create safe output string
                    if len(recent_names) > 3:
                        display_names = recent_names[:3]
                        return f"Showing {len(top_recent)} recent files: {', '.join(display_names)} and more"
                    else:
                        return f"Showing {len(top_recent)} recent files: {', '.join(recent_names)}"
                    
                except Exception as e:
                    # Handle encoding errors specifically
                    error_msg = str(e)
                    if 'charmap' in error_msg or 'codec' in error_msg:
                        return "Recent files found but cannot display due to special characters"
                    return f"Unable to show recent files: {error_msg}"
            
            # Enhanced folder shortcuts with multiple variations
            folder_shortcuts = {
                'downloads': ['downloads', 'download', 'dl'],
                'documents': ['documents', 'document', 'docs', 'doc'],
                'desktop': ['desktop', 'desk'],
                'pictures': ['pictures', 'picture', 'pics', 'pic', 'images', 'photos'],
                'music': ['music', 'songs', 'audio'],
                'videos': ['videos', 'video', 'movies', 'films'],
                'appdata': ['appdata', 'app data'],
                'temp': ['temp', 'temporary'],
                'startup': ['startup', 'start up']
            }
            
            # Check for folder shortcuts
            for folder, variations in folder_shortcuts.items():
                if any(var in query for var in variations):
                    if folder == 'appdata':
                        path = os.path.join(os.path.expanduser("~"), "AppData")
                    elif folder == 'temp':
                        path = os.environ.get('TEMP', 'C:\\Windows\\Temp')
                    elif folder == 'startup':
                        path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
                    else:
                        path = os.path.join(os.path.expanduser("~"), folder.title())
                    
                    if os.path.exists(path):
                        subprocess.run(f'explorer "{path}"', shell=True)
                        return f"{folder.title()} folder opened"
            
            # Extract filename from query FIRST
            import re
            # Look for patterns like "open file.txt" or "find document.pdf"
            file_match = re.search(r'(?:open|find|locate)\s+(?:file\s+)?([^\s]+\.[^\s]+)', query)
            if file_match:
                filename = file_match.group(1)
            else:
                # If no extension found, look for quoted filenames
                quote_match = re.search(r'["\']([^"\'\/\\]+\.[^"\'\/\\]+)["\']', query)
                if quote_match:
                    filename = quote_match.group(1)
                else:
                    filename = None
            
            if filename:
                
                # Search in common directories
                search_dirs = [
                    os.path.join(os.path.expanduser("~"), "Desktop"),
                    os.path.join(os.path.expanduser("~"), "Downloads"),
                    os.path.join(os.path.expanduser("~"), "Documents"),
                    os.path.join(os.path.expanduser("~"), "Pictures"),
                    os.path.join(os.path.expanduser("~"), "Videos"),
                    os.path.join(os.path.expanduser("~"), "Music")
                ]
                
                # Fuzzy search for files
                found_files = []
                for search_dir in search_dirs:
                    if os.path.exists(search_dir):
                        # Exact match
                        exact_path = os.path.join(search_dir, filename)
                        if os.path.exists(exact_path):
                            found_files.append(exact_path)
                        
                        # Fuzzy match
                        try:
                            matches = glob.glob(os.path.join(search_dir, f"*{filename}*"))
                            found_files.extend(matches)
                        except:
                            pass
                
                if found_files:
                    file_path = found_files[0]
                    if os.path.isfile(file_path):
                        subprocess.run(f'start "" "{file_path}"', shell=True)
                        return f"{os.path.basename(file_path)} opened"
                    else:
                        subprocess.run(f'explorer "{file_path}"', shell=True)
                        return f"{os.path.basename(file_path)} folder opened"
                else:
                    return f"'{filename}' not found"
            
            # Search for custom folder names with exact and fuzzy matching
            folder_name = None
            folder_patterns = [
                r'open\s+folder\s+(.+)',
                r'open\s+(.+)\s+folder',
                r'open\s+([^.]+)$'  # only match if no file extension
            ]
            for pat in folder_patterns:
                m = re.search(pat, query)
                if m:
                    folder_name = m.group(1).strip()
                    break

            if folder_name:
                folder_name = folder_name.lower()
                search_roots = [
                    os.path.join(os.path.expanduser("~"), "Desktop"),
                    os.path.join(os.path.expanduser("~"), "Documents"),
                    os.path.join(os.path.expanduser("~"), "Downloads"),
                    os.path.expanduser("~")
                ]

                exact_match = []
                fuzzy_match = []

                for root in search_roots:
                    for dirpath, dirnames, _ in os.walk(root):
                        for d in dirnames:
                            name = d.lower()
                            if name == folder_name:
                                exact_match.append(os.path.join(dirpath, d))
                            elif folder_name in name:
                                fuzzy_match.append(os.path.join(dirpath, d))

                if exact_match:
                    subprocess.run(f'explorer "{exact_match[0]}"', shell=True)
                    return f"Opened folder: {os.path.basename(exact_match[0])}"

                if fuzzy_match:
                    subprocess.run(f'explorer "{fuzzy_match[0]}"', shell=True)
                    return f"Opened folder: {os.path.basename(fuzzy_match[0])}"
                
                return f"Folder '{folder_name}' not found"
            
            # Default: open file explorer
            subprocess.run('explorer', shell=True)
            return "File Explorer opened"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _create_video(self):
        """Create AI video based on query"""
        try:
            # Extract prompt from query
            query = self._current_query.lower()
            
            # Remove command words to get the actual prompt
            for cmd in ['create video', 'generate video', 'make video', 'ai video']:
                if cmd in query:
                    prompt = query.replace(cmd, '').strip()
                    break
            else:
                prompt = query
            
            # Remove common words
            prompt = prompt.replace('of', '').replace('a', '').replace('an', '').strip()
            
            if not prompt:
                return "Please specify what video you want me to create"
            
            # Start video generation in background
            from engine.simple_video_gen import create_simple_video
            return create_simple_video(prompt)
            
        except Exception as e:
            return f"Video creation failed: {str(e)}"
    
    def _brightness_up(self):
        try:
            # Get current brightness and increase by 10%
            get_cmd = 'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"'
            result = subprocess.run(get_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                current = int(result.stdout.strip())
                new_brightness = min(100, current + 10)
                
                set_cmd = f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_brightness})"'
                subprocess.run(set_cmd, shell=True)
                return f"Brightness increased to {new_brightness}%"
            else:
                # Fallback to keyboard method
                pyautogui.press('brightnessup')
                return "Brightness increased"
        except:
            return "Brightness control not supported on this system"
    
    def _brightness_down(self):
        try:
            # Get current brightness and decrease by 10%
            get_cmd = 'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightness).CurrentBrightness"'
            result = subprocess.run(get_cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0 and result.stdout.strip():
                current = int(result.stdout.strip())
                new_brightness = max(0, current - 10)

                set_cmd = f'powershell -c "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{new_brightness})"'
                subprocess.run(set_cmd, shell=True)
                return f"Brightness decreased to {new_brightness}%"
            else:
                # Fallback to keyboard brightness down
                pyautogui.press('brightnessdown')
                return "Brightness decreased"
        except Exception as e:
            return f"Brightness control not supported on this system: {e}"


    def _schedule_event(self, event_text=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            if event_text:
                return voice_advanced_ai.calendar_schedule(event_text)
            return "Please specify an event to schedule"
        except Exception as e:
            return f"Scheduling failed: {str(e)}"
        except:
            return "Error scheduling event"
    
    def _show_calendar(self):
        try:
            from engine.voice_advanced_ai import get_voice_advanced_response
            result = get_voice_advanced_response('show calendar')
            return result
        except Exception as e:
            return f"Error showing calendar: {str(e)}"
    
    # Advanced AI Features
    def _daily_briefing(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.daily_briefing()
        except:
            return "Error getting daily briefing"
    
    def _predictive_assistance(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.predictive_assistance()
        except:
            return "Error with predictive assistance"
    
    def _context_memory_store(self, data=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.context_memory_store("user_input", data)
        except:
            return "Error storing memory"
    
    def _context_memory_recall(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            result = voice_advanced_ai.context_memory_recall()
            return result
        except Exception as e:
            return f"Error recalling memory: {str(e)}"
    
    # Security & Authentication
    def _file_vault_encrypt(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.file_vault_encrypt()
        except Exception as e:
            return f"File encryption error: {str(e)}"
    
    def _file_vault_decrypt(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.file_vault_decrypt()
        except Exception as e:
            return f"File decryption error: {str(e)}"
    
    def _anomaly_detection(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.anomaly_detection_recent_processes()
        except Exception as e:
            return f"Anomaly detection error: {str(e)}"
    
    def _phishing_scan(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.phishing_malware_scan_link()
        except Exception as e:
            return f"Phishing scan error: {str(e)}"
    
    def _parental_control(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.parental_control_set()
        except Exception as e:
            return f"Parental control error: {str(e)}"
    
    # Cloud & Multi-Device
    def _cloud_backup(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Cloud backup feature available"
        except:
            return "Error with cloud backup"
    
    def _email_summarize(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.email_summarize()
        except Exception as e:
            return f"Error with email summarization: {str(e)}"
    
    def _sync_devices(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.sync_across_devices()
        except Exception as e:
            return f"Error with device sync: {str(e)}"
    
    # AI Productivity
    def _realtime_transcription(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.realtime_transcription()
        except:
            return "Error with transcription"
    
    def _summarize_meeting(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Meeting summarization feature available"
        except:
            return "Error with meeting summary"
    
    def _smart_clipboard(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.smart_clipboard_store()
        except:
            return "Error with smart clipboard"
    
    def _document_qa(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Document Q&A feature available"
        except:
            return "Error with document Q&A"
    
# Update your dual AI call to support PowerPoint creation

    def _ai_presentation(self, topic="", create_ppt=True):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            
            # Extract topic from current query if available
            if hasattr(self, '_current_query') and self._current_query and not topic:
                import re
                query = self._current_query.lower()
                
                # Extract topic from various patterns
                patterns = [
                    r'(?:make|create)\s+(?:slides|presentation|ppt)\s+(?:of|on|about)\s+(.+)',
                    r'(?:slides|presentation|ppt)\s+(?:of|on|about)\s+(.+)',
                    r'(?:make|create)\s+(.+?)\s+(?:slides|presentation|ppt)',
                    r'presentation\s+(.+)',
                    r'slides\s+(.+)'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, query)
                    if match:
                        topic = match.group(1).strip()
                        break
            
            if not topic:
                topic = "ai assistant"
                
            return voice_advanced_ai.ai_presentation_maker(topic, create_ppt)
        except Exception as e:
            return f"Error with AI presentation: {str(e)}"

# Usage examples:
# _ai_presentation("machine learning")           # Text outline only
# _ai_presentation("AI", create_ppt=True)        # Creates actual PowerPoint file
    
    def _ai_report(self, topic=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            if not topic:
                topic = "business analysis"
            return voice_advanced_ai.ai_report_maker(topic)
        except Exception as e:
            return f"Error with AI report: {str(e)}"
    
    # Smart Home
    def _smart_home_control(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Smart home control available"
        except:
            return "Error with smart home control"

    def _check_new_features(self, query):
        """Check new features from external file"""
        try:
            from engine.new_features import get_new_feature_response
            result = get_new_feature_response(query)
            return result
        except:
            return None
    
    def _set_home_scene(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Home scene setting available"
        except:
            return "Error setting home scene"
    
    def _security_camera(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Security camera feature available"
        except:
            return "Error with security camera"
    
    def _energy_monitoring(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return "Energy monitoring available"
        except:
            return "Error with energy monitoring"
    
    # Entertainment Plus
    def _ai_dj_mode(self):
        try:
            from engine.ai_dj_enhanced import ai_dj_mode_enhanced
            return ai_dj_mode_enhanced()
        except:
            return "Error with AI DJ mode"
    
    def _trivia_game(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.trivia_game_start()
        except Exception as e:
            return f"Trivia game error: {str(e)}"
    
    def _storytelling(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.storytelling_mode()
        except Exception as e:
            return f"Storytelling error: {str(e)}"
    
    def _fitness_coach(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.fitness_coach()
        except Exception as e:
            return f"Fitness coach error: {str(e)}"
    
    # Health & Wellness
    def _posture_detection(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.posture_detection()
        except Exception as e:
            return f"Posture detection error: {str(e)}"
    
    def _eye_care_mode(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.eye_care_mode()
        except Exception as e:
            return f"Eye care mode error: {str(e)}"
    
    def _daily_health_log(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.daily_health_log()
        except Exception as e:
            return f"Daily health log error: {str(e)}"
    
    def _mood_tracker(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.mood_tracker()
        except Exception as e:
            return f"Mood tracker error: {str(e)}"
    
    def _meditation_prompt(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.meditation_prompt()
        except Exception as e:
            return f"Meditation prompt error: {str(e)}"
    
    def _system_monitor_live(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.system_monitor_dashboard_live()
        except Exception as e:
            return f"System monitoring error: {str(e)}"
    
    def _auto_fix_system(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.auto_fix_system_basic()
        except Exception as e:
            return f"Auto-fix system error: {str(e)}"
    
    # All Advanced AI Features Implementation
    def _manage_package(self, action="list", package=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.manage_package(action, package)
        except Exception as e:
            return f"Package management error: {str(e)}"
    
    def _docker_control(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.docker_control()
        except Exception as e:
            return f"Docker control error: {str(e)}"
    
    def _adaptive_learning(self, action="general_action"):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.adaptive_learning(action)
        except Exception as e:
            return f"Adaptive learning error: {str(e)}"
    
    def _check_proactive(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.check_proactive_suggestions()
        except Exception as e:
            return f"Proactive check error: {str(e)}"
    
    def _enable_proactive_mode(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.enable_proactive_mode()
        except Exception as e:
            return f"Enable proactive error: {str(e)}"
    
    def _disable_proactive_mode(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.disable_proactive_mode()
        except Exception as e:
            return f"Disable proactive error: {str(e)}"
    
    def _manual_learn(self, action=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.manual_learn(action)
        except Exception as e:
            return f"Manual learn error: {str(e)}"
    
    def _calendar_schedule(self, event_data=""):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.calendar_schedule(event_data)
        except Exception as e:
            return f"Calendar schedule error: {str(e)}"
    
    # All other advanced features with the same pattern
    def _code_agent(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.code_agent()
        except Exception as e:
            return f"Code agent error: {str(e)}"
    
    def _research_agent(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.research_agent()
        except Exception as e:
            return f"Research agent error: {str(e)}"
    
    def _debug_screen_code(self):
        try:
            from engine.voice_advanced_ai import VoiceAdvancedAI
            ai = VoiceAdvancedAI()
            return ai.debug_screen_code()
        except Exception as e:
            return f"Debug screen error: {str(e)}"
    
    def _organizer_agent(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.organizer_agent()
        except Exception as e:
            return f"Organizer agent error: {str(e)}"
    
    def _multi_agent_collab(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.multi_agent_collab()
        except Exception as e:
            return f"Multi-agent collaboration error: {str(e)}"
    
    def _scholar_search(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.scholar_search()
        except Exception as e:
            return f"Scholar search error: {str(e)}"
    
    def _stock_updates(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.stock_updates()
        except Exception as e:
            return f"Stock updates error: {str(e)}"
    
    def _crypto_updates(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.crypto_updates()
        except Exception as e:
            return f"Crypto updates error: {str(e)}"
    
    def _realtime_translation(self):
        try:
            from engine.voice_advanced_ai import voice_advanced_ai
            return voice_advanced_ai.realtime_translation()
        except Exception as e:
            return f"Real-time translation error: {str(e)}"
    
    def _start_gesture_control(self):
        try:
            return "Gesture control started"
        except Exception as e:
            return f"Gesture control error: {str(e)}"
    
    def _stop_gesture_control(self):
        try:
            return "Gesture control stopped"
        except Exception as e:
            return f"Gesture control error: {str(e)}"
    
    def _code_review(self, code_text=""):
        try:
            import pyperclip
            
            if not code_text:
                try:
                    code_text = pyperclip.paste()
                    if not code_text or len(code_text.strip()) < 5:
                        return "Please select code and copy to clipboard first"
                except:
                    return "Please select code and copy to clipboard first"
            
            # Add line numbers to code
            lines = code_text.split('\n')
            numbered_code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])
            
            prompt = f'''Find errors. Be extremely brief.

{numbered_code}

Answer format: Line X: change Y to Z'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            return f"Code review error: {str(e)}"
    
    def _folder_review(self, folder_path="."):
        try:
            import os
            
            files_scanned = 0
            all_code = ""
            file_list = []
            
            code_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.ts', '.jsx', '.tsx', '.vue', '.html', '.css', '.sql', '.sh', '.bat']
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if any(file.endswith(ext) for ext in code_extensions):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                code = f.read()
                                all_code += f"\n\n=== {file_path} ===\n{code}"
                                file_list.append(file_path)
                                files_scanned += 1
                        except Exception as e:
                            continue
            
            if not all_code:
                return "No code files found in the specified folder"
            
            prompt = f'''Review {files_scanned} code files. Be extremely brief.

{all_code[:4000]}...

Give only:
1. Main issues
2. Quick fixes

Max 2 lines each.'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return f"Scanned {files_scanned} code files\n\n" + response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return f"Scanned {files_scanned} code files\n\n" + response.text.strip()
                
        except Exception as e:
            return f"Folder review error: {str(e)}"
    
    def _file_review(self, file_path="a.py"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_text = f.read()
            
            lines = code_text.split('\n')
            numbered_code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])
            
            prompt = f'''Code:\n{numbered_code}\n\nUndefined variable? Answer only: Line 6: z should be i'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                return response.text.strip()
                
        except Exception as e:
            return f"File review error: {str(e)}"
    
    def _live_code_review(self):
        try:
            import threading
            import time
            import os
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class CodeReviewHandler(FileSystemEventHandler):
                def __init__(self, dual_ai_instance):
                    self.dual_ai = dual_ai_instance
                    self.last_check = {}
                    self.file_sizes = {}  # Track file sizes for polling
                    self.corrected_files = {}  # Track corrected files with their content hash
                    self.processing_files = set()  # Track files currently being processed
                    self.start_polling()
                
                def on_modified(self, event):
                    print(f"File modified: {event.src_path}")
                    
                    if event.is_directory:
                        print("Skipping directory")
                        return
                        
                    if not event.src_path.endswith('.py'):
                        print(f"Skipping non-Python file: {event.src_path}")
                        return
                    
                    current_time = time.time()
                    # Check if file is already being processed
                    if event.src_path in self.processing_files:
                        print("Skipping - file already being processed")
                        return
                    
                    if event.src_path in self.last_check:
                        time_diff = current_time - self.last_check[event.src_path]
                        if time_diff < 2.0:  # Increased cooldown to prevent duplicates
                            print(f"Skipping - too soon ({time_diff:.1f}s)")
                            return
                    
                    print(f"Processing file: {event.src_path}")
                    self.last_check[event.src_path] = current_time
                    self.processing_files.add(event.src_path)
                    
                    # Add small delay for file operations
                    time.sleep(0.2)
                    
                    # Process the file inline
                    try:
                        print(f"Starting file processing for: {event.src_path}")
                        
                        # Try multiple times for notepad compatibility
                        code = None
                        for attempt in range(5):  # More attempts for Notepad
                            try:
                                print(f"Reading attempt {attempt + 1}")
                                with open(event.src_path, 'r', encoding='utf-8') as f:
                                    code = f.read()
                                print(f"Successfully read {len(code)} characters")
                                break
                            except (PermissionError, FileNotFoundError, OSError) as e:
                                print(f"Read attempt {attempt + 1} failed: {e}")
                                time.sleep(0.1)  # Shorter delay between attempts
                        
                        if code is None:
                            print("Could not read file after 3 attempts")
                            return
                        
                        if len(code.strip()) < 5:
                            print("File too short, skipping")
                            return
                        
                        print("Checking for syntax errors...")
                        
                        # Check for syntax errors using compile
                        error_msg = None
                        try:
                            compile(code, event.src_path, 'exec')
                            print("Compile check passed")
                        except SyntaxError as e:
                            print(f"🚨 Syntax error detected: {e}")
                            error_msg = f"Line {e.lineno}: {e.msg}"
                        except Exception as e:
                            print(f"🚨 Other error detected: {e}")
                            error_msg = str(e)
                        
                        # Use AI to find all types of errors
                        if not error_msg:
                            print("Running AI analysis for all error types...")
                            error_msg = self.dual_ai._ai_code_analysis(code)
                            if error_msg:
                                print(f"🚨 AI detected error: {error_msg}")
                        
                        if not error_msg:
                            print("✅ No errors found")
                            return
                        
                        # Check if this file was recently corrected with same content
                        import hashlib
                        content_hash = hashlib.md5(code.encode()).hexdigest()
                        if event.src_path in self.corrected_files and self.corrected_files[event.src_path] == content_hash:
                            print("Skipping - file already corrected")
                            return
                        
                        print(f"Showing notification for error: {error_msg}")
                        
                        # Show notification immediately
                        import threading
                        def delayed_notification():
                            time.sleep(0.5)
                            self.dual_ai._show_error_notification(event.src_path, error_msg)
                        
                        threading.Thread(target=delayed_notification, daemon=True).start()
                    
                    except Exception as e:
                        print(f"❌ Exception in file processing: {e}")
                        import traceback
                        traceback.print_exc()
                    finally:
                        # Remove from processing set
                        self.processing_files.discard(event.src_path)
                
                def start_polling(self):
                    """Start polling for file changes as fallback for Notepad"""
                    import threading
                    def poll_files():
                        while True:
                            try:
                                import glob
                                for py_file in glob.glob('*.py'):
                                    try:
                                        current_size = os.path.getsize(py_file)
                                        if py_file not in self.file_sizes:
                                            self.file_sizes[py_file] = current_size
                                        elif self.file_sizes[py_file] != current_size:
                                            print(f"Polling detected change in {py_file}")
                                            self.file_sizes[py_file] = current_size
                                            # Create mock event
                                            class MockEvent:
                                                def __init__(self, path):
                                                    self.src_path = path
                                                    self.is_directory = False
                                            self.on_modified(MockEvent(py_file))
                                    except (OSError, FileNotFoundError):
                                        pass
                                time.sleep(1)  # Poll every second
                            except Exception as e:
                                print(f"Polling error: {e}")
                                time.sleep(2)
                    
                    polling_thread = threading.Thread(target=poll_files, daemon=True)
                    polling_thread.start()
                    print("Started file polling for Notepad compatibility")
                
                def on_created(self, event):
                    print(f"File created: {event.src_path}")
                    if not event.is_directory and event.src_path.endswith('.py'):
                        time.sleep(1)
                        self.on_modified(event)
                
                def on_moved(self, event):
                    print(f"File moved: {getattr(event, 'src_path', 'unknown')} -> {getattr(event, 'dest_path', 'unknown')}")
                    if not event.is_directory and hasattr(event, 'dest_path') and event.dest_path.endswith('.py'):
                        time.sleep(1)
                        class MockEvent:
                            def __init__(self, path):
                                self.src_path = path
                                self.is_directory = False
                        self.on_modified(MockEvent(event.dest_path))
                    

            
            self.observer = Observer()
            self.handler = CodeReviewHandler(self)
            self.observer.schedule(self.handler, '.', recursive=True)
            self.observer.start()
            
            print("🔍 Live code review started - monitoring Python files")
            print(f"Watching directory: {os.path.abspath('.')}")
            return "Live code review active - will notify about errors and offer fixes"
            
        except Exception as e:
            return f"Live code review error: {str(e)}"
    
    def _ai_code_analysis(self, code):
        """Use AI to analyze code for all types of errors"""
        try:
            lines = code.split('\n')
            numbered_code = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])
            
            prompt = f'''Check this Python code for CRITICAL errors only:\n{numbered_code}\n\nOnly report:\n- Undefined variables\n- Syntax errors\n- Missing imports that cause errors\n\nIgnore style suggestions, variable naming, and input validation.\n\nIf you find a CRITICAL error, respond with: "Line X: [error]"\nIf no critical errors, respond with: "OK"'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                result = response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(prompt)
                result = response.text.strip()
            
            # Check if AI found critical errors
            if 'line' in result.lower() and 'ok' not in result.lower():
                return result
            
            return None
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return None
    
    def _show_error_notification(self, file_path, error_message):
        import os
        import time
        
        title = f"Code Error in {os.path.basename(file_path)}"
        print(f"🚨 {title}: {error_message}")
        
        # Simple console notification to avoid crashes
        print(f"🚨 {title}: {error_message}")
        
        # Ask for correction
        if self._ask_for_correction(title, error_message):
            self._auto_correct_code(file_path, error_message)
        
    def _ask_for_correction(self, title, message):
        try:
            import tkinter as tk
            from tkinter import messagebox
            import time
            
            # Create root window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            root.attributes('-alpha', 0.0)  # Make invisible
            root.deiconify()  # Show window
            root.lift()
            root.focus_force()
            root.update()
            
            # Small delay to ensure window is ready
            time.sleep(0.2)
            
            # Show dialog
            result = messagebox.askyesno(
                "Auto-Fix Code?",
                f"{title}\n\n{message[:200]}\n\nWould you like to automatically fix this error?",
                parent=root
            )
            
            root.destroy()
            print(f"User choice: {'YES' if result else 'NO'}")
            return result
            
        except Exception as e:
            print(f"Dialog error: {e}")
            return False
        
    def _auto_correct_code(self, file_path, error_message):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            print("Using AI to fix the code...")
            correction_prompt = f'''Fix this Python code error. Return ONLY the corrected code without explanations:\n\nOriginal code:\n{original_code}\n\nError: {error_message}\n\nCorrected code:'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": correction_prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(correction_prompt)
                corrected_code = response.text.strip()
            
            # Clean AI response
            if corrected_code.startswith('```'):
                lines = corrected_code.split('\n')
                corrected_code = '\n'.join(lines[1:-1])
            
            # Create backup
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup_{timestamp}"
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            print(f"File created: {backup_path}")
            
            # Apply correction
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_code)
            
            # Mark file as corrected
            import hashlib
            content_hash = hashlib.md5(corrected_code.encode()).hexdigest()
            if hasattr(self, 'handler') and self.handler:
                self.handler.corrected_files[file_path] = content_hash
            
            print(f"✅ Code fixed in {os.path.basename(file_path)}")
            self._show_notification("🎉 Code Fixed!", f"Error corrected in {os.path.basename(file_path)}")
        
        except Exception as e:
            print(f"❌ Auto-correction failed: {e}")
            self._show_notification("Auto-Correction Failed", f"Could not fix: {str(e)}")
    
    def _old_auto_correct_code(self, file_path, error_message):
        try:
            import os
            import datetime
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            correction_prompt = f'''Fix this Python code. Return ONLY the corrected code:\n\n{original_code}\n\nError: {error_message}'''
            
            if self.ai_provider == 'groq':
                response = self.groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": correction_prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
            else:
                response = self.gemini_model.generate_content(correction_prompt)
                corrected_code = response.text.strip()
            
            # Clean markdown
            if corrected_code.startswith('```'):
                lines = corrected_code.split('\n')
                corrected_code = '\n'.join(lines[1:-1])
            
            # Create backup
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup_{timestamp}"
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_code)
            
            # Apply fix
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_code)
            
            print(f"✅ Code fixed in {os.path.basename(file_path)}")
            self._show_notification("🎉 Code Fixed!", f"Fixed {os.path.basename(file_path)}\nBackup: {os.path.basename(backup_path)}")
        
        except Exception as e:
            print(f"❌ Fix failed: {str(e)}")
            self._show_notification("❌ Fix Failed", f"Could not fix: {str(e)}")
    
    def _show_notification(self, title, message):
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            messagebox.showinfo(title, message[:300])
            root.destroy()
            print(f"✅ Popup shown: {title}")
        except:
            print(f"📢 {title}: {message}")
    
    def _start_live_review(self):
        return self._live_code_review()
    
    def _stop_live_review(self):
        try:
            if hasattr(self, 'observer') and self.observer:
                self.observer.stop()
                self.observer.join()
                print("🛑 Live code review stopped")
                return "Live code review stopped"
            return "Live code review not running"
        except Exception as e:
            return f"Error stopping live code review: {str(e)}"
    
    # Voice Gender Control Methods
    def _switch_to_male_voice(self):
        try:
            from engine.voice_gender_control import voice_control
            response = voice_control.switch_to_male()
            return response
        except Exception as e:
            return f"Error switching to male voice: {str(e)}"
    
    def _switch_to_female_voice(self):
        try:
            from engine.voice_gender_control import voice_control
            response = voice_control.switch_to_female()
            return response
        except Exception as e:
            return f"Error switching to female voice: {str(e)}"
    
    def _get_current_voice_gender(self):
        try:
            from engine.voice_gender_control import voice_control
            gender = voice_control.get_current_gender()
            return f"Current voice is set to {gender}"
        except Exception as e:
            return f"Error getting voice status: {str(e)}"
    
    # Mapping Functions
    def _open_maps(self):
        try:
            subprocess.Popen('start https://maps.google.com', shell=True)
            return "Google Maps opened"
        except:
            return "Failed to open maps"
    
    def _find_location(self, location=""):
        try:
            import urllib.parse
            if not location:
                location = "current location"
            encoded_location = urllib.parse.quote(location)
            url = f"https://maps.google.com/maps?q={encoded_location}"
            subprocess.Popen(f'start {url}', shell=True)
            return f"Searching for {location} on maps"
        except:
            return "Failed to search location"
    
    def _get_directions(self, destination=""):
        try:
            import urllib.parse
            if not destination:
                return "Please specify a destination"
            encoded_dest = urllib.parse.quote(destination)
            url = f"https://maps.google.com/maps/dir//{encoded_dest}"
            subprocess.Popen(f'start {url}', shell=True)
            return f"Getting directions to {destination}"
        except:
            return "Failed to get directions"
    
    def _nearby_places(self, place_type="restaurants"):
        try:
            import urllib.parse
            encoded_type = urllib.parse.quote(f"{place_type} near me")
            url = f"https://maps.google.com/maps/search/{encoded_type}"
            subprocess.Popen(f'start {url}', shell=True)
            return f"Finding nearby {place_type}"
        except:
            return "Failed to find nearby places"
    
    def _traffic_info(self):
        try:
            url = "https://maps.google.com/maps/@?layer=t"
            subprocess.Popen(f'start {url}', shell=True)
            return "Showing traffic information"
        except:
            return "Failed to show traffic info"
    
    def _map_satellite(self):
        try:
            url = "https://maps.google.com/maps/@?layer=s"
            subprocess.Popen(f'start {url}', shell=True)
            return "Switched to satellite view"
        except:
            return "Failed to switch to satellite view"
    
    def _map_terrain(self):
        try:
            url = "https://maps.google.com/maps/@?layer=p"
            subprocess.Popen(f'start {url}', shell=True)
            return "Switched to terrain view"
        except:
            return "Failed to switch to terrain view"
    
    def _save_location(self, location=""):
        try:
            if not location:
                return "Please specify a location to save"
            # Save to a simple text file
            with open('saved_locations.txt', 'a', encoding='utf-8') as f:
                f.write(f"{location}\n")
            return f"Location '{location}' saved"
        except:
            return "Failed to save location"
    
    def _my_location(self):
        try:
            url = "https://maps.google.com/maps/@?layer=c"
            subprocess.Popen(f'start {url}', shell=True)
            return "Showing your current location"
        except:
            return "Failed to show current location"

    def _dictate_to_file(self, query=""):
        """Voice-to-text dictation to file"""
        try:
            import speech_recognition as sr
            import re
            import os
            
            filename = "dictation.txt"
            file_match = re.search(r'to file\s+([^\s]+)', query.lower())
            if file_match:
                filename = file_match.group(1).strip()
                if not filename.endswith('.txt'):
                    filename += '.txt'
            
            mode = "append" if "append" in query.lower() else "write"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {filename}. Say 'stop dictation' to finish...")
                
                text_content = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        text = self._process_punctuation_commands(text)
                        text_content += text + " "
                        print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if text_content.strip():
                if mode == "append" and os.path.exists(filename):
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write("\n" + text_content.strip())
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text_content.strip())
                
                return f"📝 Dictation saved to {filename} ({len(text_content.split())} words)"
            else:
                return "No speech detected"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Dictation failed: {e}"

    def _dictate_to_document(self, query=""):
        """Advanced voice-to-text for formatted documents"""
        try:
            import speech_recognition as sr
            import re
            from datetime import datetime
            
            doc_type = "word"
            if "google docs" in query.lower():
                doc_type = "gdocs"
            elif "email" in query.lower():
                doc_type = "email"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {doc_type}. Say formatting commands like 'bold this', 'new paragraph'...")
                
                document_content = []
                current_text = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        if self._is_formatting_command(text):
                            formatted_text = self._process_formatting_command(text, current_text)
                            document_content.append(formatted_text)
                            current_text = ""
                        else:
                            text = self._process_punctuation_commands(text)
                            current_text += text + " "
                            print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if current_text.strip():
                document_content.append(current_text.strip())
            
            if document_content:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if doc_type == "email":
                    filename = f"email_draft_{timestamp}.txt"
                    content = self._format_as_email(document_content)
                elif doc_type == "gdocs":
                    filename = f"gdocs_draft_{timestamp}.txt"
                    content = self._format_as_document(document_content)
                else:
                    filename = f"document_{timestamp}.docx"
                    content = self._format_as_document(document_content)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                word_count = len(' '.join(document_content).split())
                return f"📄 Document saved to {filename} ({word_count} words)\nFormatting commands processed"
            else:
                return "No content dictated"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Document dictation failed: {e}"
    def _dictate_to_file(self, query=""):
        """Voice-to-text dictation to file"""
        try:
            import speech_recognition as sr
            import re
            import os
            
            filename = "dictation.txt"
            file_match = re.search(r'to file\s+([^\s]+)', query.lower())
            if file_match:
                filename = file_match.group(1).strip()
                if not filename.endswith('.txt'):
                    filename += '.txt'
            
            mode = "append" if "append" in query.lower() else "write"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {filename}. Say 'stop dictation' to finish...")
                
                text_content = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        text = self._process_punctuation_commands(text)
                        text_content += text + " "
                        print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if text_content.strip():
                if mode == "append" and os.path.exists(filename):
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write("\n" + text_content.strip())
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text_content.strip())
                
                return f"📝 Dictation saved to {filename} ({len(text_content.split())} words)"
            else:
                return "No speech detected"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Dictation failed: {e}"

    def _dictate_to_document(self, query=""):
        """Advanced voice-to-text for formatted documents"""
        try:
            import speech_recognition as sr
            import re
            from datetime import datetime
            
            doc_type = "word"
            if "google docs" in query.lower():
                doc_type = "gdocs"
            elif "email" in query.lower():
                doc_type = "email"
            
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                print(f"🎤 Dictating to {doc_type}. Say formatting commands like 'bold this', 'new paragraph'...")
                
                document_content = []
                current_text = ""
                
                while True:
                    try:
                        audio = r.listen(source, timeout=1, phrase_time_limit=5)
                        text = r.recognize_google(audio)
                        
                        if "stop dictation" in text.lower():
                            break
                        
                        if self._is_formatting_command(text):
                            formatted_text = self._process_formatting_command(text, current_text)
                            document_content.append(formatted_text)
                            current_text = ""
                        else:
                            text = self._process_punctuation_commands(text)
                            current_text += text + " "
                            print(f"📝 {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        return f"Speech recognition error: {e}"
            
            if current_text.strip():
                document_content.append(current_text.strip())
            
            if document_content:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if doc_type == "email":
                    filename = f"email_draft_{timestamp}.txt"
                    content = self._format_as_email(document_content)
                elif doc_type == "gdocs":
                    filename = f"gdocs_draft_{timestamp}.txt"
                    content = self._format_as_document(document_content)
                else:
                    filename = f"document_{timestamp}.docx"
                    content = self._format_as_document(document_content)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                word_count = len(' '.join(document_content).split())
                return f"📄 Document saved to {filename} ({word_count} words)\nFormatting commands processed"
            else:
                return "No content dictated"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Document dictation failed: {e}"

    def _process_punctuation_commands(self, text):
        """Process voice punctuation commands"""
        # More comprehensive punctuation mapping
        punctuation_map = {
            ' period': '.',
            ' comma': ',',
            ' question mark': '?',
            ' exclamation point': '!',
            ' exclamation mark': '!',
            ' colon': ':',
            ' semicolon': ';',
            ' new line': '\n',
            ' new paragraph': '\n\n',
            ' dot': '.',
            ' full stop': '.'
        }
    
        # Process punctuation commands (case insensitive)
        for command, punctuation in punctuation_map.items():
            text = text.replace(command, punctuation)
            text = text.replace(command.title(), punctuation)
            text = text.replace(command.upper(), punctuation)
    
        return text

    def _is_formatting_command(self, text):
        """Check if text contains formatting commands"""
        formatting_commands = [
            'bold this', 'italic this', 'underline this',
            'bullet point', 'numbered list', 'new paragraph',
            'heading', 'title', 'center this'
        ]
    
        return any(cmd in text.lower() for cmd in formatting_commands)

    def _process_formatting_command(self, command, text):
        """Process formatting commands and return formatted text"""
        command_lower = command.lower()
    
        if 'bold this' in command_lower:
            return f"**{text.strip()}**"
        elif 'italic this' in command_lower:
            return f"*{text.strip()}*"
        elif 'underline this' in command_lower:
            return f"_{text.strip()}_"
        elif 'bullet point' in command_lower:
            return f"• {text.strip()}"
        elif 'numbered list' in command_lower:
            return f"1. {text.strip()}"
        elif 'heading' in command_lower:
            return f"# {text.strip()}"
        elif 'title' in command_lower:
            return f"## {text.strip()}"
        elif 'center this' in command_lower:
            return f"<center>{text.strip()}</center>"
        else:
            return text

    def _format_as_email(self, content_list):
        """Format content as email"""
        email_content = "Subject: [Your Subject]\n\n"
        email_content += "Dear [Recipient],\n\n"
    
        for content in content_list:
            email_content += content + "\n\n"
    
        email_content += "Best regards,\n[Your Name]"
        return email_content

    def _format_as_document(self, content_list):
        """Format content as document"""
        document_content = ""
    
        for content in content_list:
            document_content += content + "\n\n"
    
        return document_content.strip()


    def _process_formatting_command(self, command, text):
        """Process formatting commands and return formatted text"""
        command_lower = command.lower()
    
        if 'bold this' in command_lower:
            return f"**{text.strip()}**"
        elif 'italic this' in command_lower:
            return f"*{text.strip()}*"
        elif 'underline this' in command_lower:
            return f"_{text.strip()}_"
        elif 'bullet point' in command_lower:
            return f"• {text.strip()}"
        elif 'numbered list' in command_lower:
            return f"1. {text.strip()}"
        elif 'heading' in command_lower:
            return f"# {text.strip()}"
        elif 'title' in command_lower:
            return f"## {text.strip()}"
        elif 'center this' in command_lower:
            return f"<center>{text.strip()}</center>"
        else:
            return text

    def _format_as_email(self, content_list):
        """Format content as email"""
        email_content = "Subject: [Your Subject]\n\n"
        email_content += "Dear [Recipient],\n\n"
    
        for content in content_list:
            email_content += content + "\n\n"
    
        email_content += "Best regards,\n[Your Name]"
        return email_content

    def _format_as_document(self, content_list):
        """Format content as document"""
        document_content = ""
    
        for content in content_list:
            document_content += content + "\n\n"
    
        return document_content.strip()

    def _simple_fallback_match(self, query):
        """Simple fallback matching for basic commands"""
        query_lower = query.lower()
        
        # Basic command mappings
        if 'open' in query_lower:
            if 'chrome' in query_lower:
                return 'chrome'
            elif 'notepad' in query_lower:
                return 'notepad'
            elif 'calculator' in query_lower:
                return 'calculator'
        
        if 'volume' in query_lower:
            if 'up' in query_lower:
                return 'volume_up'
            elif 'down' in query_lower:
                return 'volume_down'
        
        if 'brightness' in query_lower:
            if 'up' in query_lower:
                return 'brightness_up'
            elif 'down' in query_lower:
                return 'brightness_down'
        
        return None

    def _pause_dictation(self):
        """Pause dictation mode"""
        try:
            self.dictation_paused = True
            return "Dictation paused"
        except Exception as e:
            return f"Failed to pause dictation: {e}"
    
    def _resume_dictation(self):
        """Resume dictation mode"""
        try:
            self.dictation_paused = False
            return "Dictation resumed"
        except Exception as e:
            return f"Failed to resume dictation: {e}"
    def _start_dictation(self, query=""):
        """Start dictation mode - opens app and starts listening"""
        try:
            import speech_recognition as sr
            import pyautogui
            import time
            
            # Determine which app to open
            self.current_app = "notepad"  # default
            
            if "notepad" in query.lower():
                self.current_app = "notepad"
                subprocess.Popen('notepad', shell=True)
                time.sleep(2)
            elif "word" in query.lower():
                self.current_app = "word"
                subprocess.Popen('start winword', shell=True)
                time.sleep(3)  # Word takes longer to load
                # Create new document in Word
                pyautogui.hotkey('ctrl', 'n')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)
                pyautogui.press('enter')   # Press enter after ctrl+n
            elif "chrome" in query.lower():
                self.current_app = "chrome"
                subprocess.Popen('start chrome', shell=True)
                time.sleep(2)
            elif "anywhere" in query.lower() or not query.strip():
                self.current_app = "anywhere"
                # Don't open any specific app, just start dictating
            else:
                # If no specific app mentioned, open notepad
                self.current_app = "notepad"
                subprocess.Popen('notepad', shell=True)
                time.sleep(2)
            
            # Start dictation
            return self._dictate_anywhere()
            
        except Exception as e:
            return f"Failed to start dictation: {e}"
    
    def _auto_save_file(self):
        """Auto-save the dictated file"""
        try:
            # Only save if we opened notepad or word
            if hasattr(self, 'current_app') and self.current_app in ['notepad', 'word']:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if self.current_app == 'word':
                    filename = f"dictation_{timestamp}"
                else:
                    filename = f"dictation_{timestamp}"
                
                # Press Ctrl+S to save
                pyautogui.hotkey('ctrl', 's')
                time.sleep(2)
                
                # Type filename and save
                pyautogui.typewrite(filename)
                time.sleep(1)
                pyautogui.press('enter')
                
                print(f"💾 File saved as {filename}")
        except Exception as e:
            print(f"Save error: {e}")
    
    def _stop_dictation(self):
        """Stop dictation mode"""
        try:
            self.dictation_active = False
            return "Dictation stopped"
        except Exception as e:
            return f"Failed to stop dictation: {e}"
    
    def _dictate_anywhere(self, query=""):
        """Universal dictation that works in any application"""
        try:
            import speech_recognition as sr
            import pyautogui
            import time
            
            r = sr.Recognizer()
            # Improve recognition settings
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.8
            r.phrase_threshold = 0.3
            
            self.dictation_active = True
            
            with sr.Microphone() as source:
                print("🎤 Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=2)
                print("🎤 Universal dictation started. Say 'stop dictation' to finish...")
                print("📝 Speaking will type directly into the active application")
                
                while self.dictation_active:
                    try:
                        # Adjust listening parameters for better recognition
                        audio = r.listen(source, timeout=3, phrase_time_limit=6)
                        text = r.recognize_google(audio, language='en-US', show_all=False)
                        
                        # Check for control commands
                        text_lower = text.lower()
                        if any(stop_phrase in text_lower for stop_phrase in ["stop dictation", "end dictation", "finish dictation", "stop writing", "stop typing"]):
                            self.dictation_active = False
                            print("🛑 Dictation stopped")
                            # Auto-save the file
                            self._auto_save_file()
                            break
                        # Automation features
                        elif "press enter" in text_lower or "new line" in text_lower:
                            pyautogui.press('enter')
                            print("↵ Enter pressed")
                            continue
                        elif "press tab" in text_lower:
                            pyautogui.press('tab')
                            print("⇥ Tab pressed")
                            continue
                        elif "press space" in text_lower:
                            pyautogui.press('space')
                            print("␣ Space pressed")
                            continue
                        elif "backspace" in text_lower or "delete back" in text_lower:
                            pyautogui.press('backspace')
                            print("⌫ Backspace pressed")
                            continue
                        elif "delete" in text_lower and "back" not in text_lower:
                            pyautogui.press('delete')
                            print("⌦ Delete pressed")
                            continue
                        elif any(pause_phrase in text_lower for pause_phrase in ["pause dictation", "pause typing"]):
                            if not hasattr(self, 'dictation_paused'):
                                self.dictation_paused = False
                            self.dictation_paused = True
                            print("⏸️ Dictation paused - say 'resume dictation' to continue")
                            continue
                        elif any(resume_phrase in text_lower for resume_phrase in ["resume dictation", "continue dictation"]):
                            if not hasattr(self, 'dictation_paused'):
                                self.dictation_paused = False
                            if self.dictation_paused:
                                self.dictation_paused = False
                                print("▶️ Dictation resumed")
                            continue
                        
                        # Skip typing if paused
                        if hasattr(self, 'dictation_paused') and self.dictation_paused:
                            continue
                        
                        # Clean up the text
                        text = text.strip()
                        if len(text) < 2:  # Skip very short utterances
                            continue
                            
                        # Process punctuation commands
                        text = self._process_punctuation_commands(text)
                        
                        # Type the text with proper spacing
                        if text:
                            pyautogui.typewrite(text + " ", interval=0.01)
                            print(f"📝 Typed: {text}")
                        
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        # Don't print for every unrecognized audio to reduce noise
                        continue
                    except sr.RequestError as e:
                        print(f"Speech service error: {e}")
                        return f"Speech recognition error: {e}"
                    except Exception as e:
                        print(f"Typing error: {e}")
                        continue
            
            return "📝 Universal dictation completed"
                
        except ImportError:
            return "Speech recognition not installed. Run: pip install SpeechRecognition pyaudio"
        except Exception as e:
            return f"Universal dictation failed: {e}"
        

    def _find_file(self):
        """Find files by name in specified directory"""
        try:
            query = self._current_query.lower()
            
            # Parse directory from query
            directory = self._get_directory(query)
            
            # Get search pattern
            pattern = simpledialog.askstring("Find File", "Enter filename or pattern to search for:")
            if not pattern:
                return "Search cancelled"
            
            found_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if pattern.lower() in file.lower():
                        found_files.append(os.path.join(root, file))
            
            if found_files:
                return f"Found {len(found_files)} files:\n" + "\n".join(found_files[:10])
            else:
                return f"No files found matching '{pattern}' in {directory}"
                
        except Exception as e:
            return f"Error finding files: {str(e)}"
    
    def _find_duplicates(self):
        """Find duplicate files in specified directory"""
        try:
            import hashlib
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            file_hashes = {}
            duplicates = []
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.md5(f.read()).hexdigest()
                        
                        if file_hash in file_hashes:
                            duplicates.append((file_path, file_hashes[file_hash]))
                        else:
                            file_hashes[file_hash] = file_path
                    except:
                        continue
            
            if duplicates:
                result = f"Found {len(duplicates)} duplicate file pairs:\n"
                for dup in duplicates[:5]:
                    result += f"Duplicate: {dup[0]} = {dup[1]}\n"
                return result
            else:
                return f"No duplicate files found in {directory}"
                
        except Exception as e:
            return f"Error finding duplicates: {str(e)}"
    
    def _find_large_files(self):
        """Find large files in specified directory"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            large_files = []
            size_limit = 100 * 1024 * 1024  # 100MB
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        if size > size_limit:
                            large_files.append((file_path, size))
                    except:
                        continue
            
            if large_files:
                large_files.sort(key=lambda x: x[1], reverse=True)
                result = f"Found {len(large_files)} large files (>100MB):\n"
                for file_path, size in large_files[:10]:
                    size_mb = size / (1024 * 1024)
                    result += f"{file_path} - {size_mb:.1f}MB\n"
                return result
            else:
                return f"No large files found in {directory}"
                
        except Exception as e:
            return f"Error finding large files: {str(e)}"
    
    def _find_empty_folders(self):
        """Find empty folders in specified directory"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            empty_folders = []
            
            for root, dirs, files in os.walk(directory, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        if not os.listdir(dir_path):
                            empty_folders.append(dir_path)
                    except:
                        continue
            
            if empty_folders:
                return f"Found {len(empty_folders)} empty folders:\n" + "\n".join(empty_folders[:10])
            else:
                return f"No empty folders found in {directory}"
                
        except Exception as e:
            return f"Error finding empty folders: {str(e)}"
    
    def _get_file_info(self):
        """Get detailed file information"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            file_name = simpledialog.askstring("File Info", "Enter filename:")
            if not file_name:
                return "Operation cancelled"
            
            file_path = os.path.join(directory, file_name)
            
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            import time
            stat = os.stat(file_path)
            
            info = f"File Information for {file_name}:\n"
            info += f"Path: {file_path}\n"
            info += f"Size: {stat.st_size} bytes ({stat.st_size / (1024*1024):.2f} MB)\n"
            info += f"Created: {time.ctime(stat.st_ctime)}\n"
            info += f"Modified: {time.ctime(stat.st_mtime)}\n"
            info += f"Accessed: {time.ctime(stat.st_atime)}\n"
            
            return info
            
        except Exception as e:
            return f"Error getting file info: {str(e)}"
    
    def _backup_folder(self):
        """Backup a folder in specified location"""
        try:
            import shutil
            from datetime import datetime
            
            query = self._current_query.lower()
            
            # Get folder to backup
            folder_path = simpledialog.askstring("Backup Folder", "Enter folder path to backup:")
            if not folder_path:
                return "Backup cancelled"
            
            # Handle relative paths and common names
            if not os.path.isabs(folder_path):
                folder_path = os.path.join(self._get_directory(query), folder_path)
            
            if not os.path.exists(folder_path):
                return f"Folder not found: {folder_path}"
            
            # Get backup location from query or use same directory
            backup_dir = self._get_directory(query) if 'in ' in query else os.path.dirname(folder_path)
            
            # Create backup with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.basename(folder_path)}_backup_{timestamp}"
            backup_path = os.path.join(backup_dir, backup_name)
            
            shutil.copytree(folder_path, backup_path)
            return f"Folder backed up to: {backup_path}"
            
        except Exception as e:
            return f"Error backing up folder: {str(e)}"
        


    
    def _search_content(self):
        """Search inside files for content"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            search_term = simpledialog.askstring("Content Search", "Enter text to search for:")
            if not search_term:
                return "Search cancelled"
            
            results = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if file.lower().endswith(('.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml')):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if search_term.lower() in content.lower():
                                    results.append(file_path)
                        elif file.lower().endswith('.pdf'):
                            try:
                                import PyPDF2
                                with open(file_path, 'rb') as f:
                                    reader = PyPDF2.PdfReader(f)
                                    text = ''.join(page.extract_text() for page in reader.pages)
                                    if search_term.lower() in text.lower():
                                        results.append(file_path)
                            except:
                                pass
                    except:
                        continue
            
            if results:
                return f"Found '{search_term}' in {len(results)} files:\n" + "\n".join(results[:10])
            else:
                return f"No files found containing '{search_term}'"
                
        except Exception as e:
            return f"Error searching content: {str(e)}"
    
    def _find_similar_files(self):
        """Find files with similar content"""
        try:
            import difflib
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            file_contents = {}
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(('.txt', '.py', '.js', '.html', '.css', '.md')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                file_contents[file_path] = f.read()
                        except:
                            continue
            
            similar_pairs = []
            files = list(file_contents.keys())
            for i, file1 in enumerate(files):
                for file2 in files[i+1:]:
                    similarity = difflib.SequenceMatcher(None, file_contents[file1], file_contents[file2]).ratio()
                    if similarity > 0.7:
                        similar_pairs.append((file1, file2, similarity))
            
            if similar_pairs:
                result = f"Found {len(similar_pairs)} similar file pairs:\n"
                for file1, file2, sim in similar_pairs[:5]:
                    result += f"{sim:.1%} similar: {os.path.basename(file1)} ↔ {os.path.basename(file2)}\n"
                return result
            else:
                return "No similar files found"
                
        except Exception as e:
            return f"Error finding similar files: {str(e)}"
    
    def _suggest_folder(self):
        """Suggest folder based on file content"""
        try:
            file_path = simpledialog.askstring("Smart Folder", "Enter file path to analyze:")
            if not file_path:
                return "Operation cancelled"
            
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            suggestions = []
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Extension-based suggestions
            ext_map = {
                '.py': 'Code/Python', '.js': 'Code/JavaScript', '.html': 'Web/HTML',
                '.pdf': 'Documents/PDFs', '.docx': 'Documents/Word', '.xlsx': 'Documents/Excel',
                '.jpg': 'Images/Photos', '.png': 'Images/Graphics', '.mp4': 'Media/Videos',
                '.mp3': 'Media/Audio', '.zip': 'Archives', '.exe': 'Programs'
            }
            
            if file_ext in ext_map:
                suggestions.append(ext_map[file_ext])
            
            # Content-based suggestions
            try:
                if file_ext in ['.txt', '.py', '.js', '.html']:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        if 'import' in content or 'function' in content:
                            suggestions.append('Code/Scripts')
                        elif 'todo' in content or 'task' in content:
                            suggestions.append('Tasks/Notes')
                        elif 'project' in content:
                            suggestions.append('Projects')
            except:
                pass
            
            if suggestions:
                return f"Suggested folders for {os.path.basename(file_path)}:\n" + "\n".join(f"• {s}" for s in suggestions)
            else:
                return f"No specific folder suggestions for {os.path.basename(file_path)}"
                
        except Exception as e:
            return f"Error suggesting folder: {str(e)}"
    
    def _map_file_relationships(self):
        """Map relationships between files"""
        try:
            query = self._current_query.lower()
            directory = self._get_directory(query)
            
            relationships = {}
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    relationships[file_path] = {'imports': [], 'references': [], 'similar_name': []}
                    
                    try:
                        if file.lower().endswith(('.py', '.js', '.html', '.css')):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                # Find imports/includes
                                for other_file in files:
                                    if other_file != file and other_file.replace('.', '') in content:
                                        relationships[file_path]['references'].append(other_file)
                                
                                # Find similar names
                                base_name = os.path.splitext(file)[0]
                                for other_file in files:
                                    if other_file != file and base_name in other_file:
                                        relationships[file_path]['similar_name'].append(other_file)
                    except:
                        continue
            
            result = "File Relationships:\n"
            for file_path, relations in relationships.items():
                if any(relations.values()):
                    result += f"\n{os.path.basename(file_path)}:\n"
                    if relations['references']:
                        result += f"  References: {', '.join(relations['references'])}\n"
                    if relations['similar_name']:
                        result += f"  Similar names: {', '.join(relations['similar_name'])}\n"
            
            return result if len(result) > 20 else "No file relationships found"
                
        except Exception as e:
            return f"Error mapping relationships: {str(e)}"
        



    def _search_google(self, query=""):
        """Search Google directly with query"""
        try:
            import webbrowser
            import urllib.parse
            
            # Extract search term from current query if available
            if hasattr(self, '_current_query') and self._current_query:
                import re
                search_query = self._current_query.lower()
                
                # Remove "search google" or "google search" from the query
                search_query = re.sub(r'(?:search\s+google|google\s+search)\s*', '', search_query)
                
                # If there's remaining text, use it as search term
                if search_query.strip():
                    query = search_query.strip()
            
            if not query:
                query = "python programming"  # Default search
            
            # Create Google search URL
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(search_url)
            
            return f"Searching Google for: {query}"
            
        except Exception as e:
            return f"Google search failed: {str(e)}"
        

    def _search_images(self, query=""):
        """Search Google Images"""
        try:
            import webbrowser
            import urllib.parse
            
            if hasattr(self, '_current_query') and self._current_query:
                import re
                search_query = self._current_query.lower()
                search_query = re.sub(r'(?:search\s+(?:for\s+)?images?|images?\s+search)\s*', '', search_query)
                if search_query.strip():
                    query = search_query.strip()
            
            if not query:
                query = "nature"
            
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
            webbrowser.open(search_url)
            return f"Searching images for: {query}"
            
        except Exception as e:
            return f"Image search failed: {str(e)}"

    def _search_gifs(self, query=""):
        """Search Google for GIFs"""
        try:
            import webbrowser
            import urllib.parse
            
            if hasattr(self, '_current_query') and self._current_query:
                import re
                search_query = self._current_query.lower()
                search_query = re.sub(r'(?:search\s+(?:for\s+)?gifs?|gifs?\s+search)\s*', '', search_query)
                if search_query.strip():
                    query = search_query.strip()
            
            if not query:
                query = "funny"
            
            search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}+gif&tbm=isch&tbs=itp:animated"
            webbrowser.open(search_url)
            return f"Searching GIFs for: {query}"
            
        except Exception as e:
            return f"GIF search failed: {str(e)}"
        

    def _copy_webpage_link(self):
        """Copy current webpage URL to clipboard"""
        try:
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.press('escape')
            return "Webpage link copied to clipboard"
        except Exception as e:
            return f"Failed to copy link: {str(e)}"

    def _translate_webpage(self):
        """Translate current webpage using Google Translate"""
        try:
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.2)
            
            import pyperclip
            current_url = pyperclip.paste()
            
            if current_url and current_url.startswith('http'):
                import webbrowser
                import urllib.parse
                translate_url = f"https://translate.google.com/translate?sl=auto&tl=en&u={urllib.parse.quote(current_url)}"
                webbrowser.open(translate_url)
                return "Opening webpage translation"
            else:
                return "No valid webpage URL found"
                
        except Exception as e:
            return f"Translation failed: {str(e)}"


    def _check_website_status(self):
        """Check if a website is up or down"""
        try:
            import re
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                # Extract website from query
                match = re.search(r'(?:check|status|up)\s+(?:website\s+)?([^\s]+)', query)
                if match:
                    website = match.group(1)
                    if not website.startswith('http'):
                        website = f"https://{website}"
                    
                    response = requests.get(website, timeout=5)
                    if response.status_code == 200:
                        return f"Website {website} is UP (Status: {response.status_code})"
                    else:
                        return f"Website {website} returned status: {response.status_code}"
                else:
                    return "Please specify a website to check"
            return "Please specify a website to check"
        except Exception as e:
            return f"Website appears to be DOWN or unreachable: {str(e)}"

    def _play_radio(self):
        """Play online radio stations"""
        try:
            import webbrowser
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                if 'bbc' in query:
                    webbrowser.open("https://www.bbc.co.uk/sounds/play/live:bbc_radio_one")
                elif 'npr' in query:
                    webbrowser.open("https://www.npr.org/player/live/500005/")
                elif 'classical' in query:
                    webbrowser.open("https://www.classicfm.com/radio/live/")
                else:
                    webbrowser.open("https://radio.garden/")
            else:
                webbrowser.open("https://radio.garden/")
            return "Opening online radio"
        except Exception as e:
            return f"Radio playback failed: {str(e)}"

    def _play_podcast(self):
        """Play online podcasts"""
        try:
            import webbrowser
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                if 'spotify' in query:
                    webbrowser.open("https://open.spotify.com/genre/podcasts-web")
                elif 'apple' in query:
                    webbrowser.open("https://podcasts.apple.com/")
                else:
                    webbrowser.open("https://www.google.com/podcasts")
            else:
                webbrowser.open("https://www.google.com/podcasts")
            return "Opening podcast platform"
        except Exception as e:
            return f"Podcast playback failed: {str(e)}"

    def _get_weekday(self):
        try:
            return datetime.now().strftime('%A')
        except:
            return "Could not get weekday"
    
    def _get_traffic(self, origin="current location", destination="office"):
        try:
            import webbrowser
            import urllib.parse
            
            # Extract locations from query if provided
            if hasattr(self, '_current_query') and self._current_query:
                query = self._current_query.lower()
                if 'from' in query and 'to' in query:
                    parts = query.split('from')[1].split('to')
                    if len(parts) == 2:
                        origin = parts[0].strip()
                        destination = parts[1].strip()
                elif 'traffic' in query and ('to' in query or 'from' in query):
                    # Handle "traffic to location" or "traffic from location"
                    if 'to' in query:
                        destination = query.split('to')[1].strip()
                    elif 'from' in query:
                        origin = query.split('from')[1].strip()
            
            # Open Google Maps with traffic layer
            if origin != "current location" and destination != "office":
                # Specific route
                maps_url = f"https://www.google.com/maps/dir/{urllib.parse.quote(origin)}/{urllib.parse.quote(destination)}/@?layer=t"
            elif destination != "office":
                # To specific destination
                maps_url = f"https://www.google.com/maps/dir//{urllib.parse.quote(destination)}/@?layer=t"
            else:
                # General traffic view
                maps_url = "https://www.google.com/maps/@?layer=t"
            
            webbrowser.open(maps_url)
            
            # Return informative message
            if origin != "current location" and destination != "office":
                return f"Opening traffic information from {origin} to {destination} in Google Maps"
            elif destination != "office":
                return f"Opening traffic information to {destination} in Google Maps"
            else:
                return "Opening Google Maps with live traffic information"
                
        except Exception as e:
            return f"Could not get traffic information: {str(e)}"
    
    def _get_holidays(self, country="IN"):
        try:
            year = datetime.now().year
            url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"
            response = requests.get(url, timeout=5)
            
            # Handle 204 No Content or other non-200 responses
            if response.status_code == 204 or response.status_code != 200:
                return self._get_simple_holidays()
            
            # Check if response has content
            if not response.text.strip():
                return self._get_simple_holidays()
            
            # Try to parse JSON
            try:
                holidays = response.json()
            except json.JSONDecodeError:
                return self._get_simple_holidays()
            
            if not holidays or not isinstance(holidays, list):
                return self._get_simple_holidays()
            
            today = datetime.now().strftime("%Y-%m-%d")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            for holiday in holidays:
                if holiday.get('date') == today:
                    return f"Today is {holiday.get('localName', 'a holiday')}, a public holiday in {country}."
                elif holiday.get('date') == tomorrow:
                    return f"Tomorrow is {holiday.get('localName', 'a holiday')}, a public holiday in {country}."
            
            # Find next upcoming holiday
            upcoming = None
            for holiday in holidays:
                if holiday.get('date'):
                    try:
                        holiday_date = datetime.strptime(holiday['date'], "%Y-%m-%d")
                        if holiday_date > datetime.now():
                            upcoming = holiday
                            break
                    except ValueError:
                        continue
            
            if upcoming:
                try:
                    days_until = (datetime.strptime(upcoming['date'], "%Y-%m-%d") - datetime.now()).days
                    return f"Next holiday: {upcoming.get('localName', 'Holiday')} in {days_until} days ({upcoming['date']})."
                except ValueError:
                    return "Found upcoming holidays but couldn't calculate dates"
            
            return "No public holidays today or tomorrow."
        except requests.RequestException:
            return self._get_simple_holidays()
        except Exception as e:
            return self._get_simple_holidays()
    
    def _get_simple_holidays(self):
        """Fallback method for when API fails"""
        try:
            today = datetime.now()
            month = today.month
            day = today.day
            year = today.year
            
            # Common holidays with dates
            holidays = {
                (1, 1): "New Year's Day",
                (1, 26): "Republic Day (India)",
                (3, 8): "Holi (approximate)",
                (4, 14): "Baisakhi",
                (8, 15): "Independence Day (India)",
                (10, 2): "Gandhi Jayanti",
                (10, 31): "Halloween",
                (11, 14): "Children's Day (India)",
                (12, 25): "Christmas Day",
                (12, 31): "New Year's Eve"
            }
            
            # Check today
            if (month, day) in holidays:
                return f"Today is {holidays[(month, day)]}"
            
            # Check tomorrow
            tomorrow = today + timedelta(days=1)
            if (tomorrow.month, tomorrow.day) in holidays:
                return f"Tomorrow is {holidays[(tomorrow.month, tomorrow.day)]}"
            
            # Find next holiday
            for i in range(1, 365):
                future_date = today + timedelta(days=i)
                if (future_date.month, future_date.day) in holidays:
                    return f"Next major holiday: {holidays[(future_date.month, future_date.day)]} in {i} days ({future_date.strftime('%B %d')})"
            
            return "No major public holidays found in the next year"
        except Exception:
            return "Could not check holidays"
    
    def _get_covid_stats(self, country="India"):
        try:
            url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                return f"COVID API returned status code: {response.status_code}"
            
            if not response.text.strip():
                return "COVID API returned empty response"
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                return "COVID API returned invalid data format"
            
            new_cases = data.get('todayCases', 0)
            deaths = data.get('todayDeaths', 0)
            recovered = data.get('todayRecovered', 0)
            total_cases = data.get('cases', 0)
            
            return f"COVID-19 update for {country}: {new_cases:,} new cases, {deaths:,} deaths, and {recovered:,} recoveries today. Total cases: {total_cases:,}."
        except requests.RequestException:
            return "Could not connect to COVID-19 statistics service"
        except Exception as e:
            return f"Could not get COVID-19 statistics: {str(e)}"
        


    
    def _extract_product_name(self, query: str, site: str):
        """
        Extracts product name from query like 'track price of iPhone 15 on flipkart'
        """
        query = query.lower()
        print(f"DEBUG: Extracting from query: '{query}' for site: '{site}'")
        
        # Pattern 1: "track price of <product> on site"
        pattern1 = rf"track\s+price\s+of\s+(.+?)\s+on\s+{site}"
        match = re.search(pattern1, query)
        if match:
            result = match.group(1).strip()
            print(f"DEBUG: Pattern 1 matched: '{result}'")
            return result
        
        # Pattern 2: "track <product> on site"
        pattern2 = rf"track\s+(.+?)\s+on\s+{site}"
        match = re.search(pattern2, query)
        if match:
            result = match.group(1).strip()
            print(f"DEBUG: Pattern 2 matched: '{result}'")
            return result
        
        print(f"DEBUG: No pattern matched")
        return None

    # ===== PRODUCT PRICE TRACKING =====#
    def _track_amazon_price(self, product_name=""):
        try:
            if not product_name and hasattr(self, '_current_query'):
                product_name = self._extract_product_name(self._current_query, "amazon")
            
            if not product_name:
                product_name = "laptop"
            
            search_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
            subprocess.Popen(f'start chrome "{search_url}"', shell=True)
            return f"Opened Amazon price tracking for: {product_name}"
        except Exception as e:
            return f"Amazon price tracking failed: {str(e)}"

    def _track_flipkart_price(self, product_name=""):
        try:
            if not product_name and hasattr(self, '_current_query'):
                print(f"DEBUG: Current query: {self._current_query}")
                product_name = self._extract_product_name(self._current_query, "flipkart")
                print(f"DEBUG: Extracted product name: '{product_name}'")

            if not product_name:
                product_name = "smartphone"

            search_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
            subprocess.Popen(f'start chrome "{search_url}"', shell=True)
            return f"Opened Flipkart price tracking for: {product_name}"
        except Exception as e:
            return f"Flipkart price tracking failed: {str(e)}"
    
    def _check_product_price(self, product_name=""):
        try:
            if not product_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:check|price).*?(?:of|for)\s+(.+)', query)
                if match:
                    product_name = match.group(1).strip()
            
            if not product_name:
                return "Please specify a product to check price"
            
            # Open both Amazon and Flipkart for price comparison
            import urllib.parse
            amazon_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
            flipkart_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
            
            subprocess.Popen(f'start chrome "{amazon_url}"', shell=True)
            time.sleep(2)
            subprocess.Popen(f'start chrome "{flipkart_url}"', shell=True)
            
            return f"Opened price comparison for: {product_name} on Amazon and Flipkart"
        except Exception as e:
            return f"Price check failed: {str(e)}"
    
    # ===== TRAVEL SEARCH =====
    def _search_flights(self, route=""):
        try:
            if not route and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract route from query
                match = re.search(r'(?:flight|flights).*?(?:from|to)\s+(.+)', query)
                if match:
                    route = match.group(1).strip()
                else:
                    match = re.search(r'search.*?flights?\s+(.+)', query)
                    if match:
                        route = match.group(1).strip()
            
            if not route:
                route = "Delhi to Mumbai"
            
            # Open multiple flight booking sites
            flight_sites = [
                "https://www.makemytrip.com/flight/search",
                "https://www.goibibo.com/flights/",
                "https://www.cleartrip.com/flights"
            ]
            
            for site in flight_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Opened flight search for: {route}"
        except Exception as e:
            return f"Flight search failed: {str(e)}"
    
    def _search_hotels(self, location=""):
        try:
            if not location and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract location from query
                match = re.search(r'(?:hotel|hotels).*?(?:in|at)\s+(.+)', query)
                if match:
                    location = match.group(1).strip()
                else:
                    match = re.search(r'search.*?hotels?\s+(.+)', query)
                    if match:
                        location = match.group(1).strip()
            
            if not location:
                location = "Goa"
            
            # Open multiple hotel booking sites
            hotel_sites = [
                f"https://www.booking.com/searchresults.html?ss={location}",
                f"https://www.makemytrip.com/hotels/{location.lower().replace(' ', '-')}-hotels.html",
                f"https://www.oyo.com/search/?location={location}"
            ]
            
            for site in hotel_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Opened hotel search for: {location}"
        except Exception as e:
            return f"Hotel search failed: {str(e)}"
    
    # ===== STREAMING AVAILABILITY =====
    def _find_movie_streaming(self, movie_name=""):
        try:
            if not movie_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract movie name from query
                match = re.search(r'(?:movie|film).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    movie_name = match.group(1).strip()
                else:
                    match = re.search(r'(?:find|search).*?movie\s+(.+)', query)
                    if match:
                        movie_name = match.group(1).strip()
            
            if not movie_name:
                return "Please specify a movie name"
            
            # Open streaming platforms and search engines
            import urllib.parse
            search_query = f"{movie_name} streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={urllib.parse.quote(movie_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for movie: {movie_name}"
        except Exception as e:
            return f"Movie streaming search failed: {str(e)}"
    
    def _find_show_streaming(self, show_name=""):
        try:
            if not show_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract show name from query
                match = re.search(r'(?:show|series).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    show_name = match.group(1).strip()
                else:
                    match = re.search(r'(?:find|search).*?show\s+(.+)', query)
                    if match:
                        show_name = match.group(1).strip()
            
            if not show_name:
                return "Please specify a show name"
            
            # Open streaming platforms and search engines
            import urllib.parse
            search_query = f"{show_name} TV show streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(show_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(show_name)}",
                f"https://www.hotstar.com/in/search?q={urllib.parse.quote(show_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for show: {show_name}"
        except Exception as e:
            return f"Show streaming search failed: {str(e)}"
    
    def _where_to_watch(self, content_name=""):
        try:
            if not content_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                # Extract content name from query
                match = re.search(r'where.*?watch\s+(.+)', query)
                if match:
                    content_name = match.group(1).strip()
            
            if not content_name:
                return "Please specify what you want to watch"
            
            # Open JustWatch - the best platform for finding streaming availability
            import urllib.parse
            justwatch_url = f"https://www.justwatch.com/in/search?q={urllib.parse.quote(content_name)}"
            google_search = f"https://www.google.com/search?q={urllib.parse.quote(content_name + ' where to watch streaming')}"
            
            subprocess.Popen(f'start chrome "{justwatch_url}"', shell=True)
            time.sleep(2)
            subprocess.Popen(f'start chrome "{google_search}"', shell=True)
            
            return f"Finding where to watch: {content_name}"
        except Exception as e:
            return f"Streaming search failed: {str(e)}"
    
    def _streaming_availability(self, content_name=""):
        try:
            return self._where_to_watch(content_name)
        except Exception as e:
            return f"Streaming availability check failed: {str(e)}"
    
    def _get_weekday(self):
        try:
            return datetime.now().strftime('%A')
        except:
            return "Could not get weekday"
    
    def _get_traffic(self):
        try:
            subprocess.Popen('start https://maps.google.com/maps?layer=t', shell=True)
            return "Traffic information opened"
        except:
            return "Could not get traffic info"
    
    def _get_holidays(self):
        try:
            subprocess.Popen('start https://www.google.com/search?q=public+holidays+today+india', shell=True)
            return "Holiday information opened"
        except:
            return "Could not get holiday info"
    
    def _get_covid_stats(self):
        try:
            subprocess.Popen('start https://www.google.com/search?q=covid+cases+india+today', shell=True)
            return "COVID-19 statistics opened"
        except:
            return "Could not get COVID stats"
    
   
    
    # Advanced Flight/Hotel Search with API Integration
    def _search_flights(self, route=""):
        try:
            import requests, re, datetime
            
            if not route and hasattr(self, '_current_query'):
                query = self._current_query.lower()
                match = re.search(r'(?:flight|flights).*?(?:from|to)\s+(.+)', query)
                if match:
                    route = match.group(1).strip()
            
            if not route:
                route = "Delhi to Mumbai"
            
            # City code mapping
            city_map = {"bengaluru": "BLR", "delhi": "DEL", "mumbai": "BOM", "chennai": "MAA", "goa": "GOI"}
            from_city = next((city_map[k] for k in city_map if k in route.lower()), "DEL")
            to_city = next((city_map[k] for k in city_map if k in route.lower().split("to")[-1]), "BOM")
            
            # Open multiple flight booking sites
            flight_sites = [
                "https://www.makemytrip.com/flights/",
                "https://www.goibibo.com/flights/",
                "https://www.easemytrip.com/flights.html"
            ]
            
            for site in flight_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Flight search opened for: {route}"
        except Exception as e:
            return f"Flight search failed: {str(e)}"
    
    def _search_hotels(self, location=""):
        try:
            if not location and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:hotel|hotels).*?(?:in|at)\s+(.+)', query)
                if match:
                    location = match.group(1).strip()
            
            if not location:
                location = "Goa"
            
            # Open multiple hotel booking sites
            hotel_sites = [
                f"https://www.booking.com/searchresults.html?ss={location}",
                f"https://www.makemytrip.com/hotels/{location.lower().replace(' ', '-')}-hotels.html",
                f"https://www.oyo.com/search/?location={location}"
            ]
            
            for site in hotel_sites:
                subprocess.Popen(f'start chrome "{site}"', shell=True)
                time.sleep(1)
            
            return f"Hotel search opened for: {location}"
        except Exception as e:
            return f"Hotel search failed: {str(e)}"
    
    # Advanced Movie/Show Streaming Search with TMDb API
    def _find_movie_streaming(self, movie_name=""):
        try:
            import requests
            
            if not movie_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:movie|film).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    movie_name = match.group(1).strip()
            
            if not movie_name:
                return "Please specify a movie name"
            
            # Use JustWatch and Google for streaming availability
            import urllib.parse
            search_query = f"{movie_name} streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(movie_name)}",
                f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={urllib.parse.quote(movie_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for movie: {movie_name}"
        except Exception as e:
            return f"Movie streaming search failed: {str(e)}"
    
    def _find_show_streaming(self, show_name=""):
        try:
            if not show_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'(?:show|series).*?(?:streaming|watch)\s+(.+)', query)
                if match:
                    show_name = match.group(1).strip()
            
            if not show_name:
                return "Please specify a show name"
            
            # Open streaming platforms and search engines
            import urllib.parse
            search_query = f"{show_name} TV show streaming where to watch"
            
            streaming_searches = [
                f"https://www.google.com/search?q={urllib.parse.quote(search_query)}",
                f"https://www.justwatch.com/in/search?q={urllib.parse.quote(show_name)}",
                f"https://www.netflix.com/search?q={urllib.parse.quote(show_name)}",
                f"https://www.hotstar.com/in/search?q={urllib.parse.quote(show_name)}"
            ]
            
            for url in streaming_searches:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                time.sleep(1)
            
            return f"Searching streaming availability for show: {show_name}"
        except Exception as e:
            return f"Show streaming search failed: {str(e)}"
    
    def _where_to_watch(self, content_name=""):
        try:
            if not content_name and hasattr(self, '_current_query'):
                import re
                query = self._current_query.lower()
                match = re.search(r'where.*?watch\s+(.+)', query)
                if match:
                    content_name = match.group(1).strip()
            
            if not content_name:
                return "Please specify what you want to watch"
            
            # Open JustWatch - the best platform for finding streaming availability
            import urllib.parse
            justwatch_url = f"https://www.justwatch.com/in/search?q={urllib.parse.quote(content_name)}"
            google_search = f"https://www.google.com/search?q={urllib.parse.quote(content_name + ' where to watch streaming')}"
            
            subprocess.Popen(f'start chrome "{justwatch_url}"', shell=True)
            time.sleep(2)
            subprocess.Popen(f'start chrome "{google_search}"', shell=True)
            
            return f"Finding where to watch: {content_name}"
        except Exception as e:
            return f"Streaming search failed: {str(e)}"
    
    def _streaming_availability(self, content_name=""):
        try:
            return self._where_to_watch(content_name)
        except Exception as e:
            return f"Streaming availability check failed: {str(e)}"



    # DEBUG Price Tracking Functions
    def _track_amazon_price_debug(self):
        try:
            print("DEBUG: Amazon price tracking function called")
            query = getattr(self, '_current_query', 'No query stored')
            print(f"DEBUG: Current query: {query}")
            
            # Extract product name from query
            import re
            product_match = re.search(r'track price.*?(?:of|for)\s+(.+?)\s+(?:on|in|from)\s+amazon', query.lower())
            if product_match:
                product_name = product_match.group(1).strip()
                print(f"DEBUG: Extracted product name: {product_name}")
                import urllib.parse
                search_url = f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}"
                subprocess.Popen(['start', search_url], shell=True)
                return f"DEBUG: Amazon search opened for: {product_name}"
            else:
                subprocess.Popen('start https://www.amazon.in', shell=True)
                return "DEBUG: Amazon opened (no product extracted)"
        except Exception as e:
            return f"DEBUG: Amazon price tracking failed - {str(e)}"
    
    def _track_flipkart_price_debug(self):
        try:
            print("DEBUG: Flipkart price tracking function called")
            query = getattr(self, '_current_query', 'No query stored')
            print(f"DEBUG: Current query: {query}")
            
            # Extract product name from query
            import re
            product_match = re.search(r'track price.*?(?:of|for)\s+(.+?)\s+(?:on|in|from)\s+flipkart', query.lower())
            if product_match:
                product_name = product_match.group(1).strip()
                print(f"DEBUG: Extracted product name: {product_name}")
                import urllib.parse
                search_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}"
                subprocess.Popen(['start', search_url], shell=True)
                return f"DEBUG: Flipkart search opened for: {product_name}"
            else:
                subprocess.Popen('start https://www.flipkart.com', shell=True)
                return "DEBUG: Flipkart opened (no product extracted)"
        except Exception as e:
            return f"DEBUG: Flipkart price tracking failed - {str(e)}"
    
    def _check_product_price_debug(self):
        try:
            print("DEBUG: Product price comparison function called")
            query = getattr(self, '_current_query', 'No query stored')
            print(f"DEBUG: Current query: {query}")
            
            # Extract product name from query
            import re
            product_match = re.search(r'(?:track|check)\s+price.*?(?:of|for)\s+(.+)', query.lower())
            if product_match:
                product_name = product_match.group(1).strip()
                print(f"DEBUG: Extracted product name: {product_name}")
                import urllib.parse
                # Open multiple price comparison sites
                sites = [
                    f"https://www.amazon.in/s?k={urllib.parse.quote(product_name)}",
                    f"https://www.flipkart.com/search?q={urllib.parse.quote(product_name)}",
                    f"https://www.google.com/search?q={urllib.parse.quote(product_name + ' price comparison')}"
                ]
                for site in sites:
                    subprocess.Popen(['start', site], shell=True)
                    time.sleep(1)
                return f"DEBUG: Price comparison opened for: {product_name}"
            else:
                subprocess.Popen('start https://www.pricehistory.in', shell=True)
                return "DEBUG: Price comparison opened (no product extracted)"
        except Exception as e:
            return f"DEBUG: Product price comparison failed - {str(e)}"
        

    # Timer & Stopwatch Features
    def __init_timer_vars(self):
        if not hasattr(self, 'stopwatch_start'):
            self.stopwatch_start = None
            self.elapsed_time = 0
            self.running = False
    
    def _countdown_timer(self):
        try:
            self.__init_timer_vars()
            import threading, re
            query = getattr(self, '_current_query', '')
            
            # Extract duration from query
            duration = 0
            words = query.lower().split()
            for i, word in enumerate(words):
                if word.isdigit():
                    duration = int(word)
                    if i+1 < len(words) and 'minute' in words[i+1]:
                        duration *= 60
                    break
            
            if duration > 0:
                def countdown():
                    seconds = duration
                    while seconds > 0:
                        mins, secs = divmod(seconds, 60)
                        print(f"\r⏳ Time left: {mins:02d}:{secs:02d}", end="")
                        time.sleep(1)
                        seconds -= 1
                    print("\n✅ Time's up!")
                    try:
                        from engine.command import speak
                        speak("Time's up!")
                    except:
                        pass
                
                threading.Thread(target=countdown, daemon=True).start()
                return f"Timer started for {duration} seconds"
            return "Please specify a valid duration"
        except Exception as e:
            return f"Timer error: {str(e)}"
    
    def _start_stopwatch(self):
        try:
            self.__init_timer_vars()
            if not self.running:
                self.stopwatch_start = time.time()
                self.running = True
                return "⏱️ Stopwatch started"
            return "Stopwatch already running"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    def _stop_stopwatch(self):
        try:
            self.__init_timer_vars()
            if self.running:
                self.elapsed_time += time.time() - self.stopwatch_start
                self.running = False
                return f"⏹️ Stopwatch stopped. Elapsed: {self.elapsed_time:.2f} seconds"
            return "Stopwatch not running"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    def _reset_stopwatch(self):
        try:
            self.__init_timer_vars()
            self.elapsed_time = 0
            self.stopwatch_start = None
            self.running = False
            return "🔁 Stopwatch reset"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    def _show_elapsed(self):
        try:
            self.__init_timer_vars()
            if self.running:
                current = self.elapsed_time + (time.time() - self.stopwatch_start)
            else:
                current = self.elapsed_time
            return f"⏳ Elapsed time: {current:.2f} seconds"
        except Exception as e:
            return f"Stopwatch error: {str(e)}"
    
    # Mini Games Feature
    def _open_mini_game(self):
        try:
            query = getattr(self, '_current_query', '').lower()
            
            mini_games = {
                "chess": "https://www.chess.com/play/computer",
                "snake": "https://playsnake.org/",
                "flappy bird": "https://flappybird.io/",
                "car": "https://simmer.io/@gqcar/game-car-driving",
                "tetris": "https://tetris.com/play-tetris",
                "2048": "https://play2048.co/",
                "dino": "https://chromedino.com/",
                "pac man": "https://pacman.live/",
                "mario": "https://supermario-game.com/",
                "solitaire": "https://solitaired.com/",
                "sudoku": "https://sudoku.com/",
                "crossword": "https://crosswordpuzzles.com/",
                "bubble shooter": "https://bubble-shooter.co/",
                "candy crush": "https://king.com/game/candycrushsaga",
                "angry birds": "https://angrybirds.com/",
                "pool": "https://www.crazygames.com/game/8-ball-pool",
                "racing": "https://www.crazygames.com/game/madalin-stunt-cars-2",
                "puzzle": "https://www.jigsawplanet.com/",
                "word": "https://wordscapes.com/"
            }
            
            # Check for specific game in query
            for name, url in mini_games.items():
                if name in query:
                    subprocess.Popen(['start', url], shell=True)
                    return f"🎮 Opening {name} game"
            
            # Open default games site
            subprocess.Popen(['start', 'https://crazygames.com'], shell=True)
            return "🎯 Opening games collection"
        except Exception as e:
            return f"Game launch error: {str(e)}"



               # Smart Clipboard Assistant Methods
    def _clipboard_assistant(self):
        """Smart clipboard assistant that analyzes clipboard content"""
        try:
            import pyperclip
            import re
            
            clipboard_text = pyperclip.paste()
            if not clipboard_text or len(clipboard_text.strip()) < 3:
                return "Clipboard is empty or too short to analyze"
            
            # Analyze clipboard content using AI
            return self._analyze_clipboard_content(clipboard_text)
        except Exception as e:
            return f"Clipboard assistant error: {str(e)}"
    
    def _start_clipboard_assistant(self):
        """Start monitoring clipboard for context-aware help"""
        try:
            import threading
            import time
            import pyperclip
            
            if hasattr(self, 'clipboard_monitor_active') and self.clipboard_monitor_active:
                return "Clipboard assistant already running"
            
            self.clipboard_monitor_active = True
            self.last_clipboard = ""
            
            def monitor_clipboard():
                while self.clipboard_monitor_active:
                    try:
                        current_clipboard = pyperclip.paste()
                        if current_clipboard != self.last_clipboard and current_clipboard.strip():
                            self.last_clipboard = current_clipboard
                            suggestion = self._analyze_clipboard_content(current_clipboard)
                            if suggestion:
                                print(f"📋 Clipboard Assistant: {suggestion}")
                        time.sleep(2)
                    except:
                        time.sleep(2)
            
            threading.Thread(target=monitor_clipboard, daemon=True).start()
            return "Clipboard assistant started - monitoring clipboard for smart suggestions"
        except Exception as e:
            return f"Failed to start clipboard assistant: {str(e)}"
    
    def _stop_clipboard_assistant(self):
        """Stop clipboard monitoring"""
        try:
            self.clipboard_monitor_active = False
            return "Clipboard assistant stopped"
        except Exception as e:
            return f"Error stopping clipboard assistant: {str(e)}"
    
    def _analyze_clipboard_content(self, text):
        """Analyze clipboard content and provide context-aware suggestions"""
        try:
            import re
            
            text = text.strip()
            
            # Phone number detection
            if re.match(r'^[+]?[\d\s\-\(\)]{10,15}$', text):
                return "📞 Phone number detected! Want me to save this contact or make a call?"
            
            # Email detection
            if re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', text):
                return "📧 Email address detected! Want me to compose an email or save this contact?"
            
            # URL detection
            if re.match(r'https?://[\w\.-]+', text):
                return "🔗 URL detected! Want me to open this link or bookmark it?"
            
            # Long text (paragraph)
            if len(text) > 100 and '.' in text:
                return "📄 Long text detected! Shall I summarize this or save it to a document?"
            
            # Code detection
            if any(keyword in text for keyword in ['def ', 'function', 'class ', 'import ', 'const ', 'var ']):
                return "💻 Code detected! Want me to format it, review it, or save to a file?"
            
            # Address detection
            if any(word in text.lower() for word in ['street', 'avenue', 'road', 'city', 'zip']):
                return "📍 Address detected! Want me to find directions or save this location?"
            
            # Date/time detection
            if re.search(r'\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|\d{1,2}:\d{2}', text):
                return "📅 Date/time detected! Want me to create a calendar event or set a reminder?"
            
            # Password-like text
            if len(text) > 8 and re.search(r'[A-Z]', text) and re.search(r'[0-9]', text) and re.search(r'[!@#$%^&*]', text):
                return "🔐 Strong password detected! Want me to save this securely?"
            
            # Shopping list
            if '\n' in text and len(text.split('\n')) > 3:
                return "📝 List detected! Want me to organize this or create a task list?"
            
            # Default for other text
            if len(text) > 20:
                return "📋 Text copied! Want me to translate, search, or save this?"
            
            return None
        except Exception as e:
            return None
    


    
    def _create_image(self):
        """Create image using AI"""
        try:
            query = getattr(self, '_current_query', '')
            prompt = query.replace('create image', '').replace('generate image', '').replace('make image', '').strip()
            
            if not prompt:
                return "Please specify what image to create (e.g., 'create image of a sunset')"
            
            from engine.simple_image_gen import create_simple_image
            return create_simple_image(prompt)
        except Exception as e:
            return f"Image creation error: {str(e)}"
    
    def _explain_capabilities(self):
        """Explain what Jarvis can do"""
        return "I can control your computer (open apps, manage files, system controls), help with productivity (alarms, reminders, clipboard assistant), browse the web (YouTube, search, websites), create AI images, and answer questions using AI. I support voice commands for hands-free operation and can adapt to your preferences. Just ask me to open something, control media, set alarms, create images, or help with tasks!"
    
    def _set_alarm(self):
        """Set alarm with voice notification"""
        try:
            import threading
            import time
            import re
            import json
            from datetime import datetime, timedelta
            
            query = getattr(self, '_current_query', '')
            
            # Extract time from query
            time_match = re.search(r'(\d{1,2}):?(\d{2})\s*(am|pm)?', query.lower())
            if not time_match:
                time_match = re.search(r'(\d{1,2})\s*(am|pm)', query.lower())
                if time_match:
                    hour = int(time_match.group(1))
                    if 'pm' in query.lower() and hour != 12:
                        hour += 12
                    elif 'am' in query.lower() and hour == 12:
                        hour = 0
                    minute = 0
                else:
                    return "Please specify time (e.g., 'set alarm 7:30' or 'alarm 8 am')"
            else:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                # Handle AM/PM for time with minutes
                if 'pm' in query.lower() and hour != 12:
                    hour += 12
                elif 'am' in query.lower() and hour == 12:
                    hour = 0
            
            # Calculate alarm time
            now = datetime.now()
            alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Only set for tomorrow if time has already passed today
            if alarm_time <= now:
                alarm_time += timedelta(days=1)
            
            # Store alarm
            self.active_alarm = alarm_time
            
            # Save to file
            with open('alarm.json', 'w') as f:
                json.dump({'time': alarm_time.isoformat()}, f)
            
            self._start_alarm_thread(alarm_time)
            return f"⏰ Alarm set for {alarm_time.strftime('%I:%M %p')}"
            
        except Exception as e:
            return f"Error setting alarm: {e}"
    
    def _cancel_alarm(self):
        """Cancel active alarm with voice confirmation"""
        try:
            if self.active_alarm:
                self.active_alarm = None
                # Remove file
                import os
                if os.path.exists('alarm.json'):
                    os.remove('alarm.json')
                print("⏰ Alarm cancelled")
                return "⏰ Alarm cancelled successfully"
            else:
                return "No active alarm to cancel"
        except Exception as e:
            return f"Error cancelling alarm: {e}"
    



    def _start_alarm_thread(self, alarm_time):
        """Helper method to start alarm thread"""
        import threading
        import time
        from datetime import datetime
        
        def alarm_thread():
            while datetime.now() < alarm_time:
                if not self.active_alarm:
                    return
                time.sleep(1)
            
            # Trigger alarm notification
            try:
                from engine.voice_gender_control import voice_control
                voice_control.speak_with_gender("Good morning! This is your alarm notification. Wake up! Wake up! It's time to get up and start your day. Your alarm time has arrived. Please wake up now!")
            except:
                print("⏰ ALARM: Good morning! Wake up! Wake up! It's time to get up and start your day!")
            
            # Clean up
            self.active_alarm = None
            import os
            if os.path.exists('alarm.json'):
                os.remove('alarm.json')
        
        threading.Thread(target=alarm_thread, daemon=True).start()



    def _roll_dice(self):
        """Roll a dice and return the result"""
        result = random.randint(1, 6)
        return f" {result}"
    
    def _flip_coin(self):
        """Flip a coin and return the result"""
        result = random.choice(['Heads', 'Tails'])
        return f"  {result}"
    
    def _age_calculator(self):
        """Calculate age from birth date"""
        try:
            from datetime import datetime
            import re
            
            query = getattr(self, '_current_query', '')
            
            # Extract date from query (DD/MM/YYYY or DD-MM-YYYY)
            date_match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', query)
            if date_match:
                day, month, year = map(int, date_match.groups())
                
                # Validate year (reasonable range)
                if year < 1900 or year > 2024:
                    return f"Invalid year: {year}. Please use a year between 1900 and 2024"
                
                # Validate month
                if month < 1 or month > 12:
                    return f"Invalid month: {month}. Please use month between 1-12"
                
                # Validate day
                if day < 1 or day > 31:
                    return f"Invalid day: {day}. Please use day between 1-31"
                
                try:
                    birth_date = datetime(year, month, day)
                except ValueError as ve:
                    return f"Invalid date: {day}/{month}/{year}. {str(ve)}"
                
                today = datetime.now()
                
                # Check if birth date is in the future
                if birth_date > today:
                    return f"Birth date {day}/{month}/{year} is in the future!"
                
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                
                days_diff = (today - birth_date).days
                return f"Age: {age} years ({days_diff} days old)"
            
            return "Please provide birth date (e.g., 'my age 15/03/1990')"
        except Exception as e:
            return f"Age calculation error: {str(e)}"


    def _sort_files(self):
        """Sort files by date, time, name, or size"""
        try:
            import os
            import re
            from datetime import datetime
            
            query = getattr(self, '_current_query', '').lower()
            
            # Extract sort criteria and directory
            sort_by = 'name'  # default
            if 'date' in query or 'time' in query:
                sort_by = 'date'
            elif 'size' in query:
                sort_by = 'size'
            elif 'name' in query:
                sort_by = 'name'
            
            # Extract directory
            target_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            dir_match = re.search(r'(?:in|on)\s+(\w+)', query)
            if dir_match:
                dir_name = dir_match.group(1)
                dirs = {
                    'downloads': 'Downloads', 'documents': 'Documents',
                    'desktop': 'Desktop', 'pictures': 'Pictures',
                    'music': 'Music', 'videos': 'Videos'
                }
                if dir_name in dirs:
                    target_dir = os.path.join(os.path.expanduser("~"), dirs[dir_name])
            
            if not os.path.exists(target_dir):
                return f"Directory not found: {target_dir}"
            
            # Get files
            files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
            
            if not files:
                return f"No files found in {os.path.basename(target_dir)}"
            
            # Sort files
            if sort_by == 'date':
                files.sort(key=lambda f: os.path.getmtime(os.path.join(target_dir, f)), reverse=True)
                criteria = "date (newest first)"
            elif sort_by == 'size':
                files.sort(key=lambda f: os.path.getsize(os.path.join(target_dir, f)), reverse=True)
                criteria = "size (largest first)"
            else:  # name
                files.sort()
                criteria = "name (A-Z)"
            
            # Show top 5 files with details
            result = f"Files in {os.path.basename(target_dir)} sorted by {criteria}:\n"
            for i, file in enumerate(files[:5]):
                file_path = os.path.join(target_dir, file)
                if sort_by == 'date':
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    result += f"{i+1}. {file} ({mod_time.strftime('%Y-%m-%d %H:%M')})\n"
                elif sort_by == 'size':
                    size = os.path.getsize(file_path)
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024*1024:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/(1024*1024):.1f} MB"
                    result += f"{i+1}. {file} ({size_str})\n"
                else:
                    result += f"{i+1}. {file}\n"
            
            if len(files) > 5:
                result += f"... and {len(files)-5} more files"
            
            return result.strip()
            
        except Exception as e:
            return f"Sort failed: {str(e)}"


    def _ai_document_maker(self, doc_type="document"):
        try:
            topic = "Document"
            user_info = ""
            num_pages = 2
            
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()

                # Document type
                if 'report' in query:
                    doc_type = "report"
                elif 'letter' in query:
                    doc_type = "letter"

                # Extract page count
                page_match = re.search(r'(\d+)\s+page', query)
                if page_match:
                    num_pages = int(page_match.group(1))

                # Extract topic correctly
                patterns = [
                    r'(?:create|make)\s+(?:a\s+)?(?:document|report|letter)\s+(?:about|on|regarding)\s+(.+?)(?:\s+\d+\s+page)?$',
                    r'(?:document|report|letter)\s+(?:about|on|regarding)\s+(.+?)(?:\s+\d+\s+page)?$',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, query)
                    if match:
                        topic = match.group(1).strip()
                        topic = re.sub(r'\b\d+\s*page(s)?\b', '', topic).strip()
                        break
            
            try:
                from engine.voice_advanced_ai import voice_advanced_ai
                return voice_advanced_ai.ai_document_maker(doc_type, topic, user_info, num_pages)
            except:
                return f"{doc_type.title()} creation started for: {topic} ({num_pages} pages)"
        except Exception as e:
            return f"Document creation error: {str(e)}"
    
    def _write_code(self):
        """AI Code Writer - Write code in any language"""
        try:
            if hasattr(self, '_current_query') and self._current_query:
                import re
                query = self._current_query.lower()
                
                # Extract programming language
                languages = ['python', 'javascript', 'java', 'c++', 'c#', 'html', 'css', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin']
                language = 'python'  # default
                for lang in languages:
                    if lang in query:
                        language = lang
                        break
                
                # Extract code description with improved patterns
                patterns = [
                    r'write\s+(?:' + '|'.join(languages) + r')\s+code\s+(?:for|to)\s+(.+)',
                    r'write\s+code\s+(?:in\s+(?:' + '|'.join(languages) + r')\s+)?(?:for|to)\s+(.+)',
                    r'generate\s+(?:' + '|'.join(languages) + r')\s+code\s+(?:for|to)\s+(.+)',
                    r'generate\s+code\s+(?:in\s+(?:' + '|'.join(languages) + r')\s+)?(?:for|to)\s+(.+)',
                    r'create\s+(?:' + '|'.join(languages) + r')\s+code\s+(?:for|to)\s+(.+)',
                    r'create\s+code\s+(?:in\s+(?:' + '|'.join(languages) + r')\s+)?(?:for|to)\s+(.+)'
                ]
                
                description = None
                for pattern in patterns:
                    match = re.search(pattern, query)
                    if match:
                        description = match.group(1).strip()
                        break
                
                # Fallback extraction if patterns fail
                if not description:
                    # Remove common words and extract the main request
                    temp = query
                    for word in ['write', 'generate', 'create', 'code', 'program', 'script'] + languages:
                        temp = temp.replace(word, '')
                    temp = re.sub(r'\b(?:for|to|in|a|an|the)\b', '', temp)
                    description = temp.strip() or "a simple program"
                
                # Generate code using AI with better prompt
                prompt = f"""Write ONLY the {language} code for: {description}

Requirements:
- Write clean, working {language} code
- Include proper comments
- Make it functional and ready to run
- Focus specifically on: {description}
- No explanations, just code

Code:"""
                
                if self.ai_provider == 'groq':
                    response = self.groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.1-8b-instant",
                        max_tokens=1500
                    )
                    code = response.choices[0].message.content.strip()
                else:
                    response = self.gemini_model.generate_content(prompt)
                    code = response.text.strip()
                
                # Clean up the response to get only code
                if '```' in code:
                    # Extract code from markdown blocks
                    import re
                    code_match = re.search(r'```(?:python|javascript|java|html|css)?\n?([\s\S]*?)```', code)
                    if code_match:
                        code = code_match.group(1).strip()
                
                # Remove any leading explanatory text
                lines = code.split('\n')
                code_lines = []
                code_started = False
                for line in lines:
                    if not code_started and (line.strip().startswith('#') or line.strip().startswith('//') or 
                                           line.strip().startswith('def ') or line.strip().startswith('function ') or
                                           line.strip().startswith('class ') or line.strip().startswith('import ') or
                                           line.strip().startswith('from ') or line.strip().startswith('<!DOCTYPE') or
                                           line.strip().startswith('<') or line.strip().startswith('var ') or
                                           line.strip().startswith('let ') or line.strip().startswith('const ')):
                        code_started = True
                    if code_started:
                        code_lines.append(line)
                
                if code_lines:
                    code = '\n'.join(code_lines)
                
                # Save to file
                extensions = {
                    'python': '.py', 'javascript': '.js', 'java': '.java', 'c++': '.cpp',
                    'c#': '.cs', 'html': '.html', 'css': '.css', 'php': '.php',
                    'ruby': '.rb', 'go': '.go', 'rust': '.rs', 'swift': '.swift', 'kotlin': '.kt'
                }
                
                ext = extensions.get(language, '.txt')
                # Clean description for filename
                clean_desc = re.sub(r'[^a-zA-Z0-9_\s]', '', description)
                clean_desc = clean_desc.replace(' ', '_')[:20]
                filename = f"ai_code_{clean_desc}_{datetime.now().strftime('%H%M%S')}{ext}"
                file_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Open in notepad
                subprocess.Popen(f'notepad "{file_path}"', shell=True)
                
                return f"AI {language} code generated and opened: {filename}"
            
            return "Please specify what code to write (e.g., 'write python code for calculator')"
            
        except Exception as e:
            return f"Code generation failed: {str(e)}"
    

    def _create_project(self):
        """AI Project Creator - generates complete multi-file projects"""
        import os
        import re
        import subprocess

        try:
            if not hasattr(self, '_current_query') or not self._current_query:
                return "Please specify what project to create (e.g., 'create todo app using python')"

            query = self._current_query.strip()

            tech_keywords = ['python', 'javascript', 'html', 'css', 'react', 'flask', 'django', 'node', 'java', 'c++']
            mentioned_tech = [tech for tech in tech_keywords if tech in query.lower()]

            project_name_raw = query.replace("create", "").replace("project", "").strip()
            project_name = re.sub(r'[^a-zA-Z0-9_]', '_', project_name_raw)[:30]
            if not project_name:
                project_name = "AI_Project"

            prompt = f"""
Create a complete working project for: "{query}"

Technologies detected: {', '.join(mentioned_tech) if mentioned_tech else 'auto-select best stack'}

Generate 3–6 FULL files. Format EXACTLY like this:

**FILENAME: main.py**
```python
# code here
```

**FILENAME: README.md**
```markdown
# content here
```

CRITICAL RULES:
- ONLY complete, working code inside ``` blocks
- Enterprise-grade, production-ready implementation with better ui and backend
- Professional UI with perfect alignment, modern design, responsive layout
- Zero placeholders, TODOs, or incomplete features
- No explanations or text outside file blocks
- Comprehensive README with installation and usage
- All functionality must work flawlessly
"""

            ai_response = ""
            try:
                if hasattr(self, "groq_client") and self.groq_client:
                    resp = self.groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=4096
                    )
                    ai_response = resp.choices[0].message.content

                elif hasattr(self, "gemini_model") and self.gemini_model:
                    resp = self.gemini_model.generate_content(prompt)
                    ai_response = resp.text

                else:
                    return "❌ No AI provider available."
            except Exception as e:
                return f"❌ AI Generation Failed: {e}"

            if not ai_response:
                return "❌ AI returned empty response."

            file_blocks = re.findall(
                r'\*\*FILENAME:\s*(.*?)\*\*.*?```(?:[a-zA-Z]*)\n(.*?)```',
                ai_response,
                flags=re.DOTALL
            )

            files = []
            for filename, content in file_blocks:
                filename = filename.strip()
                content = content.strip("\n")
                files.append((filename, content))

            if not files:
                files = [
                    ("main.py", f'# Fallback generated project\nprint("Project: {query}")'),
                    ("README.md", f'# {project_name}\n\nAI formatting error fallback.')
                ]

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            project_dir = os.path.join(desktop, f"AI_Project_{project_name}")
            os.makedirs(project_dir, exist_ok=True)

            for filename, content in files:
                file_path = os.path.join(project_dir, filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)

            try:
                subprocess.run(["explorer", project_dir], check=False)
            except:
                pass

            return (
                f"✅ Project '{project_name}' created successfully!\n"
                f"📁 Location: {project_dir}\n"
                f"📄 Files created: {len(files)}\n"
                f"🚀 Folder opened automatically."
            )

        except Exception as e:
            return f"❌ Project creation failed: {str(e)}"


dual_ai = DualAI()

def get_simple_response(query):
    return dual_ai.execute(query)
