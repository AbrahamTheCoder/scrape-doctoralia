import re

def quote_json(text):
    # Add double quotes around unquoted keys and string values
    text = re.sub(r'(\w+):', r'"\1":', text)
    # text = re.sub(r': ([^,{}]+)(,|$)', r': "\1"\2', text)
    
    # Remove trailing commas
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*\]', ']', text)
    
    return text

def validate_url(url: str):
    # Check if the URL is valid
    pattern = r'^(https?:\/\/)(\w+\.)*doctoralia\.com\.mx(/.*)?$'
    return re.match(pattern, url) is not None