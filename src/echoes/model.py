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

        #top_memories = memories.get_top_memories(user_input)

        input = ""

        #if len(top_memories) != 0:
        #    input += "[MEMORY]\n"
        #    for memory in top_memories:
        #        input += memory["content"] + "\n"


        # The defaults instructions for handling memories [ Work still in progress to define the ideal defaults instructions ].
        #input += "\n[INSTRUCTIONS]\n"
        #input += "When the user asks a question about something factual (e.g., age, height, favorite things), look in the \"[MEMORY]\" section and use the exact information if available.\n"
        #input += "The content of the \"[MEMORY]\" section are your own memories, so refer to them in first person.\n"
        #input += "Sometimes the \"[MEMORY]\" might be feeding wrong inputs for the situation, use them only if relevant and appropriate to the situation.\n"
        #input += "When using the memories, don't copy paste them, reformulate them based on your character and only use the important informations."


        #if utils.fexist(model_data["path"] + "/instructions.txt"):
        #    input += utils.fread(model_data["path"] + "/instructions.txt") + "\n"
        #input += "\n"


        # Specifies to the AI that he can begin to generate it's output and not carry on to finish the user's sentence.
        if self.model_data.get("user"):
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