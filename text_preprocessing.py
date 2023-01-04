import re,html


def clean(text):
    # lower
    text = text.lower()
    # tags like <tag>
    text = re.sub(r'<[^<>]*>', ' ',text)
    # Markdown Urls
    text = re.sub(r'\[([^\[\]]*)\]\([^\(\)]*\)',r'\1',text)
    # Remove Punctuation
    text = re.sub(r'([!?,])\1+', r'\1', text)
    # Remove all URL's
    text = re.sub(r'http.*', ' ', text)
    # Remove @
    text = re.sub(r'@\w*', ' ', text)
    # text or code in brackets
    text = re.sub(r'\[[^\[\]]*\]',' ',text)
    # remove b"
    text = text.replace('b\"',' ')
    # remove b'
    text = text.replace("b\'",' ')
    # remove \\n
    text = text.replace('\\n',' ')
    # Remove &amp
    text = text.replace('&amp',' ')
    # remove UTF-8 code like \\xe2
    text = re.sub(r'(\\x(.){2})', ' ',text)
    # Standalone sequences for specials
    text = re.sub(r'(?:^|\s)[;.\'\"&#<>{}\[\]+|\\:-]{1,}(?:\s|$)', ' ',text)
    # stand alone sequence of hyphens
    text= re.sub(r'(?:^|\s)[\-=\+]{2,}(?:\s|$)', ' ',text)
    # Sequence of white spaces
    text = re.sub(r'\s+',' ',text)
    return text.strip()