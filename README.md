# AI2SQL – Llama 3 Edition (Zero-DB MVP)

A lightweight natural language to SQL converter using Groq's Llama 3 API.

## Setup

1. Create virtual environment and activate:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Unix
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. First visit: Enter your database schema and question
2. Subsequent visits: Schema persists in session, just enter new questions
3. Get SQL output instantly

## Features

- Natural language to SQL conversion
- Session-based schema persistence
- NLTK token analysis (dev console)
- Minimalist interface
