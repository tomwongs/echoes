import asyncio
import ollama

import echoes.utils as utils
import echoes.context as context
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
                input += "Your name is " + self.model_data['name'] + ". "

            input += "Here are your instructions to follow when generating a prompt, please follow them carefully: "
            input += self.model_data['instructions'] + "\n\n"


        # Specifies to the AI that he can begin to generate it's output and not carry on to finish the user's sentence.
        if self.model_data['user'] != '':
            input += f"\n{self.model_data['user']}: {user_input} \n"
        else:
            input += "\nUser: " + user_input + "\n\n"


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