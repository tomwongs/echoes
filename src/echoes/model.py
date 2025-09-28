import asyncio
import ollama

from . import utils
from . import context
#import echoes.memories as memories     # Unstable features, to be used when properly implemented.


# Contains the tools for initializing the model and to make it work as intended.

#memory = memories.init_memory()

class Model:
    
    def __init__(self, model_data: dict):
        self.model_data = model_data
        self.model_data['context'] = context.readContext(model_data)                                                            # The context is a list of dictionaries.

    
    
    # Adds the memories and the instructions to the user prompt.
    def format_input(self, user_input: str) -> str:

        input = ""

        # Feed the instructions into the LLM if there are.
        if self.model_data['instructions'] != '':

            if self.model_data['name'] != '':
                input += "Your name is " + self.model_data['name'] + ".\n"

            if self.model_data['persona'] != '':
                input += "The following is your persona, use it to generate your output: "
                input += self.model_data['persona'] + "\n\n"

            input += "Here are your instructions to follow when generating a prompt, please follow them carefully: "
            input += self.model_data['instructions'] + "\n\n"

        
        if (user := self.model_data['user']) != {}:
            input += "Informations about the user:\n"
            
            if user['favorite'] != '':
                input += "The user's favorites are " + user['favorite'] + ".\n"

            if user['dislike'] != '':
                input += "The user doesn't like " + user['dislike'] + ".\n"

            if user['relationship_lvl'] != '':
                input += "The relationship you have with the user is: " + user['relationship_lvl'] + ".\n"
                
            if user['name'] != '':
                input += "The user's name is " + user['name'] + " be sure to reference it if needed.\n"






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
    


    # Generate a response while writing live it's generation in async with 'print'.
    async def generate_response(self, prompt: str) -> str:
        output = ""

        formated_prompt = [{"role": "user", "content": self.format_input(prompt)}]

        async for part in await ollama.AsyncClient().chat(model=self.model_data["model"], messages=context.content(self.model_data) + formated_prompt, stream=True):
            print(part["message"]["content"], end='', flush=True)
            output += part["message"]["content"]
        

        context.add(self.model_data, "user", prompt)
        context.add(self.model_data, "assistant", output)

        # Store the user and assistant prompt in the context.
        if self.model_data["is_remembering"]:
            context.save(self.model_data)

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