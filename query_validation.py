import nltk
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
import re

class QueryValidator:
    def __init__(self):
        self.tokenizer = Tokenizer(num_words=1000)
        self.max_length = 20
        self.model = self._create_model()
        
        # Download NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # SQL-related keywords that should be present in valid queries
        self.sql_keywords = {
            'show', 'select', 'find', 'get', 'list', 'count', 'display',
            'where', 'how many', 'which', 'what', 'table', 'database',
            'total', 'average', 'sum', 'join', 'group', 'filter'
        }
        
        # Common informal/chat patterns
        self.informal_patterns = [
            r'^hi\b',
            r'^hello\b',
            r'^hey\b',
            r'how are you',
            r'who are you',
            r'what is your name',
            r'tell me about yourself',
            r'^thanks?\b',
            r'^ok\b',
            r'^bye\b'
        ]
        
        # Suspicious patterns
        self.patterns = [
            r"drop\s+table",
            r"delete\s+from",
            r"truncate\s+table",
            r"alter\s+table",
            r"exec\s*\(",
            r"system\s*\(",
            r"union\s+select",
            r"information_schema",
            r"--",  # SQL comment
            r";\s*\w+",  # Multiple statements
            r"xp_cmdshell",
            r"INTO\s+OUTFILE",
            r"LOAD_FILE",
            r"0x[0-9a-fA-F]+",  # Hex values
            r"@@",  # System variables
            r"waitfor\s+delay",
            r"benchmark\s*\("
        ]
    
    def _create_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(1000, 16, input_length=self.max_length),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model
    
    def validate(self, query):
        # Check for informal or chat-like text
        query_lower = query.lower()
        
        # Check for informal patterns
        for pattern in self.informal_patterns:
            if re.search(pattern, query_lower):
                return {
                    'is_safe': False,
                    'warning': "This appears to be informal text. Please ask a database-related question."
                }
        
        # Check if query contains any SQL-related keywords
        tokens = nltk.word_tokenize(query_lower)
        words = set(tokens) - self.stop_words
        has_sql_keyword = any(kw in query_lower for kw in self.sql_keywords)
        
        if not has_sql_keyword:
            return {
                'is_safe': False,
                'warning': "Your question doesn't appear to be related to database querying. Please rephrase with SQL-related terms."
            }
        
        # Check for suspicious SQL patterns
        for pattern in self.patterns:
            if re.search(pattern, query_lower):
                return {
                    'is_safe': False,
                    'warning': f"Suspicious pattern detected: {pattern}"
                }
        
        # Check complexity
        if len(tokens) > 20:
            return {
                'is_safe': False,
                'warning': "Query too complex"
            }
        
        # Check for multiple statements
        if query.count(';') > 1:
            return {
                'is_safe': False,
                'warning': "Multiple SQL statements not allowed"
            }
        
        # Check for direct string literals
        if "'" in query or '"' in query:
            return {
                'is_safe': False,
                'warning': "Direct string literals not allowed in natural language query"
            }
        
        # Check for numeric overflow attempts
        if re.search(r'\d{10,}', query):
            return {
                'is_safe': False,
                'warning': "Suspicious numeric values detected"
            }
        
        return {'is_safe': True}