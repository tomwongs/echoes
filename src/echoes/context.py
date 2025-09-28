from . import utils

# Contains the context handler (the context is stored inside the model_data, the context handler is only used to perform operation on the model_data, it doesn't store anything).

# Read the previous stored context.
def readContext(model_data: dict) -> list:

    if model_data['context_file'] == '' or model_data['context_file'] == None:
        return model_data['context'] 

    if utils.fexist(model_data['context_file']):
        print("\033[32mLoading previous context...\033[0m")
        context = eval(utils.fread(model_data['context_file']))
        if context != []:
            print("\033[32mPrevious context loaded!\033[0m")
            return context

    return model_data['context']


# Add in the stored context.
def add(model_data: dict, role: str, content: str):
    model_data['context'].append({"role": role, "content": content})

# Save the context in a file.
def save(model_data: dict) -> bool:
    return utils.fsave(model_data['context_file'], str(model_data['context']))


def content(model_data: dict):
    return model_data['context']