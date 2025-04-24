from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
from client import generate_sql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

@app.route('/')
def index():
    # If we're in edit mode, move schema to edit
    edit_schema = session.pop('edit_schema', None)
    if edit_schema:
        session.clear()
        return render_template('index.html', edit_schema=edit_schema)
    
    return render_template('index.html', 
                         sql=session.get('last_sql'),
                         error=session.get('error'),
                         history=session.get('history', []))

@app.route('/set-schema', methods=['POST'])
def set_schema():
    schema = request.form.get('schema')
    if not schema:
        session['error'] = "Schema cannot be empty"
        return redirect(url_for('index'))
    
    session['schema'] = schema.strip()
    session.pop('last_sql', None)
    session.pop('error', None)
    return redirect(url_for('index'))

@app.route('/edit-schema', methods=['POST'])
def edit_schema():
    current_schema = request.form.get('current_schema', '')
    if not current_schema:
        return redirect(url_for('index'))
    
    # Clear session but keep the schema for editing
    session.clear()
    session['edit_schema'] = current_schema
    return redirect(url_for('index'))

@app.route('/clear-schema', methods=['POST'])
def clear_schema():
    session.clear()
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'schema' not in session:
            raise ValueError("Please set the database schema first")
        
        question = request.form['question']
        sql, _ = generate_sql(session['schema'], question)
        
        # Store in history
        history = session.get('history', [])
        history.insert(0, {
            'question': question,
            'sql': sql,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        session['history'] = history[:15]  # Keep last 15 queries
        
        session['last_sql'] = sql
        session.pop('error', None)
        
    except Exception as e:
        session['error'] = str(e)
        session.pop('last_sql', None)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
