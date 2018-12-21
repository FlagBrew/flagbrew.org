import markdown2 as md
import base64

def markdown(text):
    x = [
        'tables', 'footnotes', #'metadata',
        'fenced-code-blocks', 'header-ids',
        'wiki-tables', 'cuddled-lists', 'code-friendly'
    ]
    html = md.markdown(base64.b64decode(text), extras=x)
    return html