def get_llm_response(query, is_clear=False):
    if is_clear:
        return f"**Direct Answer:** Based on your clear query '{query}', here's a concise response..."
    else:
        return f"**General Response:** I'll help you with '{query}'. Let me provide some useful information..."

def get_suggestions_for_ambiguous():
    return [
        "Be more specific - instead of 'things', name what you're asking about",
        "Add context - mention the domain/topic explicitly",
        "Use proper nouns - name specific people, places, or things",
        "Ask complete questions - include who, what, when, where, why",
        "Avoid vague pronouns - use specific nouns instead of 'it', 'they', 'that'"
    ]