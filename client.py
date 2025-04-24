from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from query_validation import QueryValidator
import os
import nltk

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

validator = QueryValidator()

def generate_sql(schema: str, question: str):
    # Validate question
    validation = validator.validate(question)
    if not validation['is_safe']:
        raise ValueError(f"Invalid query: {validation.get('warning', 'Unknown error')}")
    
    # Create chat client
    chat = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-8b-8192"
    )
    
    prompt = f"""Given this database schema:
{schema}

Convert this question to SQL: {question}

Rules:
1. Return ONLY the SQL query
2. Use proper SQL syntax
3. Include necessary JOINs
4. Add appropriate WHERE clauses"""

    response = chat([HumanMessage(content=prompt)])
    return response.content.strip(), nltk.word_tokenize(question)