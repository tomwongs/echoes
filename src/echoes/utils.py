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
    lines = output.split("\n")
    content = lines[0].split(":")[1][1:]
    metadata = lines[1].split(":")[1][1:]
    if metadata := eval(metadata):
        return {"content": content, "metadata": metadata}
    return {}