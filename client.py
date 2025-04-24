from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os
import nltk
from typing import Tuple

# Download required NLTK data
nltk.download('punkt', quiet=True)

def generate_sql(schema: str, question: str) -> Tuple[str, list]:
    """Generate SQL from natural language using Groq's Llama 3."""
    
    # Tokenize input for analysis
    tokens = nltk.word_tokenize(question)
    print(f"Tokens: {tokens}")  # For dev console

    # Create chat client
    chat = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )
    
    # Construct prompt
    prompt = f"""Given this database schema:
{schema}

Convert this question to SQL: {question}

Rules:
1. Return ONLY the SQL query, no explanations
2. Use proper SQL syntax
3. Include necessary JOINs
4. Add appropriate WHERE clauses"""

    # Get response
    response = chat([HumanMessage(content=prompt)])
    sql = response.content.strip()
    
    return sql, tokens
