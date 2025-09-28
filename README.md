# Echoes
Set of tools to allow easy implementation of Ollama LLM on Python, with context and memories.\
The project is still in development, here are the aimed features;

✅ Model Init: Introduces the Model type that allows interaction with Ollama LLM.\
✅ Context: Able to follow the flow of the conversation and use previous elements used to evaluate the context and store it in a file in case of reboot.\
🛠️ Memory/Memories: Will be able to remember key elements of a conversation to re-use later.

All those features needs work/rework/upgrades, so far it's a very minimalistic version, a proof of concept.

### Tested Implementations

```
import echoes

user = {
    'name': "",                             # The user's name.
    'favorite': "",                         # What the user's love.
    'dislike': "",                          # What the user's hate.
    'relationship_lvl': "",                 # The relationship with the AI.
}

model_data = {
    'name': "LLama",                        # Attributing a name to the LLM (anything can be assigned).
    'model': "llama3.2:latest",             # Specify the LLM model.
    'persona': "",                          # Adds the persona of the model.
    'emotions': "",                         # The current emotion the AI is feeling (WORK IN PROGRESS NEED TO IMPLEMENT IN MODEL.PY).

    'user': user,                           # The user's information that are relevant to the generation.


    'context': [],                          # Store the conversation.
    'context_file': "context_file.json",    # Specify the file that should be created for remembering context, if the feature "is_remembering", None or '' values can be assigned.

    'memories': [],                         # Where the memories will be stored.

    'instructions': "",                     # Define the instructions the AI should follow when generating a prompt.
    'is_remembering': True,                 # Define if a file should be created containing the context for the LLM to remember when rebooted.

    'keywords_to_tag': {}                   # Future implementation for the memories feature that will use the keywords to identify the right memory.ies to select.
}

model = echoes.create_model(model_data)
model.talk()
```
Will allow the user to input in the console the prompt for the AI to reply, creating a back and forth conversation.\
You can also replace the last line with the tested function to generate the output of an input.

```
model = echoes.create_model(model_data)
output = asyncio.run(model.generate_response("Hello!"))
```
Will display in the console the LLM answer to "Hello!" and store it to the "output" variable as an 'str' for later uses.