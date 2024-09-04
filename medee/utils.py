import re

def remove_parentheses(text: str) -> str:
    return re.sub(r'\(.*?\)', '', text).strip()

def remove_prefix(text: str) -> str:
    return re.sub(r'^\d+\. ', '', text)

def remove_extra_dots(text: str) -> str:
    return re.sub(r'\.{2,}', '', text)

def remove_bracketed_content(text: str) -> str:
    return re.sub(r'\s*\[\s*.*?\s*\]\s*', ' ', text)
