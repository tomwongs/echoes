import asyncio
import ollama

from . import utils
from . import context
from . import memories


# Contains the tools for initializing the model and to make it work as intended.

#memory = memories.init_memory()

class Model:
    
    def __init__(self, model_data: dict):
        self.model_data = model_data
        self.model_data['context'] = context.readContext(model_data)                                                            # The context is a list of dictionaries.

    
    
    # Adds the memories and the instructions to the user prompt.
    def format_input(self, user_input: str, create_memory=False) -> str:

        input = ""

        
        
        if (user := self.model_data['user']) != {}:
            input += "Information about the user:\n"
            
            if user['favorite'] != '':
                input += "The user's favorites are " + user['favorite'] + ".\n"

            if user['dislike'] != '':
                input += "The user doesn't like " + user['dislike'] + ".\n"

            if user['relationship_lvl'] != '':
                input += "This the relationship you have with the user, precisely who the user is to you: " + user['relationship_lvl'] + ".\n"
                
            if user['name'] != '':
                input += "The user's name is " + user['name'] + " be sure to reference it if needed.\n\n"


        # Feed the instructions into the LLM if there are.
        if self.model_data['instructions'] != '':

            if self.model_data['name'] != '':
                input += "Your name is " + self.model_data['name'] + ".\n"

            if self.model_data['persona'] != '':
                input += "The following is your persona, use it to generate your output: "
                input += self.model_data['persona'] + "\n\n"

            input += "Here are your instructions to follow when generating a prompt, please follow them carefully: "
            input += self.model_data['instructions'] + "\n\n"



        if create_memory:
            input += "How to generate your output: Extract the important information in the following user message in order to generate a memory. And do NOT use the <think> flag\n\n"

            input += "Message:\n"
            input += user_input + "\n\n" 

            input += "Write only two lines for the memory in this format:\n"

            input += "Content: [short neutral fact about the user, in third person, present tense if possible, and why it is relevant]\n"
            input += "Metadata: [python dict containing a key and a value (all in lowercase) that would describe the content with short tags about topics, themes, or emotions]\n\n"

            input += "Output ONLY the Content and Metadata, nothing less, nothing more.\n"
            input += "IMPORTANT NOTE: If the information is not relevant output ONLY a dot\n"
            print(input) # Debug
            return input


        


        # Specifies to the AI that he can begin to generate it's output and not carry on to finish the user's sentence.
        if (user_name := self.model_data['user']['name']) != '':
            input += f"\n{user_name}: {user_input} \n"
        else:
            input += "\nUser: " + user_input + "\n\n"


        if (llm_name := self.model_data['name']) != '':
            input += f"\n{llm_name}: "
        else:
            input += "Assistant: "
        

        print(input) # Debug
        return input
    


    # Generate the memory
    async def generate_memory(self, prompt: str):
        output = ""
        thinking = False
        formated_prompt = [{"role": "system", "content": self.format_input(prompt, create_memory=True)}]

        async for part in await ollama.AsyncClient().chat(model=self.model_data["model"], messages=context.content(self.model_data) + formated_prompt, stream=True):
            word = part["message"]["content"]
            print(word, end='', flush=True)
            if word == "<think>":
                thinking = True
            elif word == "</think>":
                thinking = False
            
            if not thinking:
                output += part["message"]["content"]


        return output



    # Generate a response while writing live it's generation in async with 'print'.
    async def generate_response(self, prompt: str) -> str:
        output = ""
        thinking = False

        formated_prompt = [{"role": "user", "content": self.format_input(prompt)}]

        async for part in await ollama.AsyncClient().chat(model=self.model_data["model"], messages=context.content(self.model_data) + formated_prompt, stream=True):
            word = part["message"]["content"]
            print(word, end='', flush=True)
            if word == "<think>":
                thinking = True
            elif word == "</think>":
                thinking = False
            
            if not thinking:
                output += part["message"]["content"]
        

        context.add(self.model_data, "user", prompt)
        context.add(self.model_data, "assistant", output)

        # Store the user and assistant prompt in the context.
        if self.model_data["is_remembering"]:
            context.save(self.model_data)

        #memory_output = await self.generate_memory(prompt)
        #memory_content = utils.extract_ai_memory_format(memory_output)

        #memories.add_memory(memory, memory_content['content'], memory_content['metadata'], self.model_data['user']['name']) # NOT WORKING

        return output

    


    def talk(self):
        while True:
            print("\n")
            user_input = input("> ")
            if (user_input == "exit"):
                break
            if (user_input == "[context]"):
                print(self.model_data['context']) # Debug
                continue

            asyncio.run(self.generate_response(user_input))