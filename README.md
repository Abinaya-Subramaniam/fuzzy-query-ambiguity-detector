# Fuzzy Logic Ambiguity Detector for LLM Queries

## Overview

A fuzzy logic based system that detects ambiguity in user queries. The system analyzes queries using multiple linguistic features and provides intelligent suggestions for how LLMs should respond based on the detected ambiguity level.

---

## Problem Statement

LLMs often struggle with ambiguous queries that contain vague pronouns, insufficient context, or incomplete questions. This system helps.

- Detect ambiguous queries before sending to LLMs
- Classify queries into clear, moderate, or ambiguous categories
- Suggest optimal response strategies for LLMs
- Guide users to improve their queries

---

## System Architecture

```
fuzzy_ambiguity_llm/
├── app.py                
├── ambiguity.py           
├── nlp_utils.py         
├── llm_stub.py           
└── requirements.txt      
```

---

##  Methodology

### 1. NLP Preprocessing (`nlp_utils.py`)

#### Feature Extraction Pipeline:

```python
1. Tokenization → word_tokenize(query)
2. Stopword Removal → Remove common English stopwords
3. Vague Word Detection → Identify ambiguous terms
4. Specificity Calculation → Count technical/proper terms
5. Question Analysis → Detect question structure
```

#### Linguistic Features Calculated:

| Feature | Description | Calculation | Range |
|---------|-------------|-------------|-------|
| **Length** | Query character length | `len(query)` | 0-100 |
| **Vague Ratio** | Percentage of vague words | `(vague_words / total_words) × 100` | 0-100% |
| **Specificity** | Technical/specific term score | Weighted sum of specific terms | 0-100 |
| **Question Clarity** | Question structure quality | Based on question patterns | 0-100 |

#### Vague Word Categories:

- **Pronouns**: `['it', 'they', 'them', 'their', 'this', 'that', 'these', 'those']`
- **General Terms**: `['something', 'anything', 'everything', 'nothing', 'thing', 'things', 'stuff']`
- **Vague Verbs**: `['do', 'make', 'get', 'have', 'work', 'happen', 'go', 'use']`
- **Ambiguous Nouns**: `['way', 'method', 'process', 'kind', 'sort', 'type']`

---

### 2. Fuzzy Logic System (`ambiguity.py`)

#### Input Variables (Antecedents):

##### 1. Query Length (0-100 characters)

```
Membership Functions:
- very_short: [0, 0, 20] → Triangular MF
- short:      [10, 30, 50] → Triangular MF  
- medium:     [40, 60, 80] → Triangular MF
- long:       [70, 90, 100] → Triangular MF
```

##### 2. Vague Word Ratio (0-100%)

```
Membership Functions:
- low:    [0, 0, 30] → Triangular MF
- medium: [20, 50, 80] → Triangular MF
- high:   [70, 100, 100] → Triangular MF
```

##### 3. Specificity Score (0-100)

```
Membership Functions:
- low:    [0, 0, 40] → Triangular MF
- medium: [30, 50, 70] → Triangular MF
- high:   [60, 100, 100] → Triangular MF
```

##### 4. Question Clarity (0-100)

```
Membership Functions:
- poor: [0, 0, 40] → Triangular MF
- fair: [30, 50, 70] → Triangular MF
- good: [60, 100, 100] → Triangular MF
```

#### Output Variable (Consequent):

##### Ambiguity Score (0-100)

```
Membership Functions:
- low:    [0, 0, 30] → Triangular MF
- medium: [20, 50, 80] → Triangular MF
- high:   [70, 100, 100] → Triangular MF
```

---

### 3. Fuzzy Rules System

#### Rule Base (10 Comprehensive Rules):

```
Rule 1:  IF length is very_short AND vague_ratio is high 
         THEN ambiguity is high

Rule 2:  IF length is very_short AND specificity is low 
         THEN ambiguity is high

Rule 3:  IF length is long AND specificity is high 
         THEN ambiguity is low

Rule 4:  IF question_clarity is good 
         THEN ambiguity is low

Rule 5:  IF question_clarity is poor 
         THEN ambiguity is high

Rule 6:  IF vague_ratio is high 
         THEN ambiguity is high

Rule 7:  IF length is medium AND specificity is medium AND vague_ratio is medium 
         THEN ambiguity is medium

Rule 8:  IF length is short AND specificity is high AND question_clarity is good 
         THEN ambiguity is medium

Rule 9:  IF length is long AND vague_ratio is high 
         THEN ambiguity is high

Rule 10: IF specificity is high AND question_clarity is good 
         THEN ambiguity is low
```

#### Inference Process:

1. **Fuzzification**: Convert crisp inputs to fuzzy membership values
2. **Rule Evaluation**: Apply fuzzy rules using AND/OR operators
3. **Aggregation**: Combine rule outputs using MAX operator
4. **Defuzzification**: Convert fuzzy output to crisp value using centroid method

---

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

```bash
git clone https://github.com/Abinaya-Subramaniam/fuzzy-ambiguity-detector.git
cd fuzzy-ambiguity-detector

python -m venv venv
source venv/bin/activate  

pip install -r requirements.txt
```

### Requirements

```
streamlit==1.28.0
scikit-fuzzy==0.4.2
nltk==3.8.1
```

---

### Testing Example Queries

#### Low Ambiguity:
```
"What is the capital of Sri Lanka?"
"Explain Python's list comprehension with examples"
```

#### Medium Ambiguity:
```
"How do I fix this?"
"Can you help me with that thing?"
```

#### High Ambiguity:
```
"It doesn't work"
"Make it better"
```

---

## Decision Logic

| Ambiguity Score | Category | LLM Action | Example Response |
|----------------|----------|------------|------------------|
| 0-30 | **Low** | Direct Answer | "Here's the answer to your question..." |
| 30-70 | **Medium** | Clarifying Question | "Could you specify whether you mean X or Y?" |
| 70-100 | **High** | Request Details | "I need more information. Please provide..." |

---
