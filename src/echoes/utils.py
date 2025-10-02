import hashlib

# Basic utils for Echoes, contains boring code that I don't want to rewrite.

def fsave(filename: str, content: str) -> bool:
    file = open(filename, 'w', encoding="utf-8")
    state = file.write(content)
    file.close()
    return state

def fread(filename: str) -> str:
    file = open(filename, 'r')
    content = file.read()
    file.close()
    return content

def fexist(filename: str) -> bool:
    try:
        open(filename, 'r')
        return True
    except:
        return False

def extract_ai_memory_format(output: str) -> dict:
    lines = output.split('\n')
    words = []
    for line in lines:
        words += line.split(' ')
    print(words)

    content_start = False
    metadata_start = False

    content = ''
    metadata = ''

    for word in words:
        if word.lower() == "content:":
            content_start = True
            metadata_start = False

        elif word.lower() == "metadata:":
            content_start = False
            metadata_start = True


        if content_start == True:
            if word.lower() == "content:":
                continue
            content += word + ' '

        elif metadata_start == True:
            if word.lower() == "metadata:":
                continue
            metadata += word


    if metadata := eval(metadata):
        return {"content": content, "metadata": metadata}
    return {}


def sha256(input: str):
    input = str(input).encode('utf-8')
    raw_hash = hashlib.sha256(input)
    hash = raw_hash.hexdigest()

    return hash