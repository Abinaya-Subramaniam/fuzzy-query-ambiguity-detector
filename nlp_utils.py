import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

STOP_WORDS = set(stopwords.words('english'))

VAGUE_WORDS = {
    'pronouns': ['it', 'they', 'them', 'their', 'this', 'that', 'these', 'those'],
    'general': ['something', 'anything', 'everything', 'nothing', 'thing', 'things', 'stuff'],
    'vague_verbs': ['do', 'make', 'get', 'have', 'work', 'happen', 'go', 'use'],
    'ambiguous': ['way', 'method', 'process', 'kind', 'sort', 'type'],
    'question_words': ['how', 'what', 'why', 'where', 'when', 'who']
}

SPECIFIC_TERMS = {
    'proper_nouns': r'\b[A-Z][a-z]+\b',  
    'numbers': r'\b\d+\b',
    'technical_terms': ['algorithm', 'function', 'variable', 'class', 'method', 
                       'database', 'server', 'api', 'machine', 'learning',
                       'neural', 'network', 'photosynthesis', 'chemical',
                       'historical', 'scientific', 'mathematical'],
    'action_words': ['explain', 'calculate', 'implement', 'build', 'create',
                    'analyze', 'compare', 'contrast', 'describe', 'define']
}

def preprocess_query(query):
    if not query or not query.strip():
        return []
    
    original = query
    query_lower = query.lower().strip()
    tokens = word_tokenize(query_lower)
    
    filtered_tokens = []
    for token in tokens:
        if token == '?':
            filtered_tokens.append('?')
        elif token.isalpha() and token not in STOP_WORDS:
            filtered_tokens.append(token)
    
    return filtered_tokens

def calculate_features(query, tokens):
    if not tokens:
        return {
            'length': 0,
            'vague_ratio': 0,
            'specificity': 0,
            'question_clarity': 0
        }
    
    char_length = len(query.strip())
    length_score = min(char_length, 100)  
    
    all_vague = set()
    for category in VAGUE_WORDS.values():
        all_vague.update(category)
    
    vague_count = sum(1 for token in tokens if token in all_vague)
    vague_ratio = (vague_count / len(tokens)) * 100 if tokens else 0
    
    specificity_score = calculate_specificity_score(query, tokens)
    
    question_clarity = calculate_question_clarity(query, tokens)
    
    return {
        'length': float(length_score),
        'vague_ratio': float(vague_ratio),
        'specificity': float(specificity_score),
        'question_clarity': float(question_clarity)
    }

def calculate_specificity_score(query, tokens):
    if not tokens:
        return 0
    
    score = 0
    max_score = 100
    
    proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', query)
    score += min(len(proper_nouns) * 15, 30)  
    
    numbers = re.findall(r'\b\d+\b', query)
    score += min(len(numbers) * 10, 20)  
    
    tech_terms_found = 0
    for term in SPECIFIC_TERMS['technical_terms']:
        if term in query.lower():
            tech_terms_found += 1
    score += min(tech_terms_found * 5, 25)  
    
    action_words_found = 0
    for word in SPECIFIC_TERMS['action_words']:
        if word in query.lower():
            action_words_found += 1
    score += min(action_words_found * 5, 25)  
    
    all_vague = set()
    for category in VAGUE_WORDS.values():
        all_vague.update(category)
    
    vague_count = sum(1 for token in tokens if token in all_vague)
    score = max(0, score - (vague_count * 5))  
    
    return min(score, max_score)

def calculate_question_clarity(query, tokens):
    if not tokens:
        return 0
    
    score = 50  
    
    is_question = query.strip().endswith('?')
    if is_question:
        score += 20
    else:
        score -= 10
    
    question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
    has_question_word = any(word in query.lower() for word in question_words)
    if has_question_word:
        score += 15
    
    question_patterns = [
        r'(what|how|why|when|where|who|which)\s+(is|are|do|does|did|can|could|will|would)',
        r'explain\s+',
        r'describe\s+',
        r'tell\s+me\s+about'
    ]
    
    for pattern in question_patterns:
        if re.search(pattern, query.lower()):
            score += 15
            break
    
    if len(tokens) < 4 and is_question:
        score -= 20
    
    if len(tokens) > 8 and is_question:
        score += 10
    
    return min(max(score, 0), 100)

def get_detailed_analysis(query, tokens, features):
    analysis = {
        'query': query,
        'token_count': len(tokens),
        'char_length': len(query),
        'is_question': query.strip().endswith('?'),
        'features': features,
        'vague_words_found': [],
        'specific_terms_found': []
    }
    
    all_vague = set()
    for category in VAGUE_WORDS.values():
        all_vague.update(category)
    
    for token in tokens:
        if token in all_vague:
            analysis['vague_words_found'].append(token)
    
    proper_nouns = re.findall(r'\b[A-Z][a-z]+\b', query)
    analysis['specific_terms_found'].extend(proper_nouns)
    
    for term in SPECIFIC_TERMS['technical_terms']:
        if term in query.lower():
            analysis['specific_terms_found'].append(term)
    
    return analysis