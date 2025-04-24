# AI2SQL – Llama 3 Edition

A sophisticated natural language to SQL converter using FastAPI, LangChain, and Groq's Llama 3 API, featuring advanced query validation and security measures.

## Features

### Core Features
- Natural language to SQL conversion
- Session-based schema persistence
- Interactive schema management
- Query history tracking
- Copy-to-clipboard functionality
- Dark mode interface

### Advanced Security

#### Query Validation
- **Pattern-Based Security**
  - SQL injection prevention
  - System command blocking
  - Multiple statement detection
  - Hex value detection
  - Time-delay attack prevention

- **Natural Language Processing**
  - Informal text detection
  - Non-SQL query filtering
  - Query complexity analysis
  - SQL keyword validation

- **Input Sanitization**
  - String literal validation
  - Numeric overflow prevention
  - Special character filtering

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

1. First visit: Enter your database schema
2. Ask questions in natural language
3. Get instant SQL translations
4. View and copy previous queries from history
5. Edit or clear schema as needed

### Query Examples

✅ Valid Queries:
- "Show all users"
- "How many orders were placed today?"
- "Find total sales by category"

❌ Invalid Queries:
- "Hi, who are you?"
- "What's the weather today?"
- "SELECT * FROM users; DROP TABLE users;"

## Technology Stack

- Frontend: HTML/CSS/JS, Dark Mode Theme
- Backend: FastAPI, LangChain
- AI: Groq's Llama 3 API
- Security: NLTK, TensorFlow for query validation
- Database: PostgreSQL/MySQL support

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

MIT License