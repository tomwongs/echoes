from . import utils
from datetime import datetime
import hashlib



# WARNING THIS FEATURE IS STILL A WASTELAND!
#  This feature is not yet stable and implemented as all the code needs to be reviewed, tested and reworked.
#  Planning on using mem4ai library in the meantime of implementing a better system.


class Memory:
    
    def __init__(self, memory:dict={} ):
        self.memory = memory 

        
    def init_user(self, user):
        self.user = user
        # Check if there's an id provided in the user data.
        if not self.user.get('id'):
            self.user['id'] = self.gen_user_id()


        # Check if there's a memory initiated with the user id.
        if self.memory == {}: 
            if not self.user['id'] in self.memory:
                self.memory[self.user['id']] = []

        return self.user['id']



    def gen_user_id(self):
        now = datetime.now()
        id = utils.sha256(now)

        return id 


    def add_memory(self, content: str, metadata: list, user: str):
        memory_id = utils.sha256(content)
        user_id = user['id']
        self.memory[user_id].append({'id': memory_id, 'content': content, 'metadata': metadata})


    def delete_memory(self, memory_id):
        for user, memories in self.memory.values():
            for i in range(0, len(memories)):
                if self[user][i]['id'] == memory_id:
                    del self.memory[user][i]
                    return


    def search_memory(self, content: str, user_id: str) -> list:
        relevant_memories = []
        for usr_memories in self.memory[user_id]:
            for i in range(0, len(usr_memories)):

                if i > len(self.memory[user_id])-1:
                    break

                for word in content.split():
                    if word in self.memory[user_id][i]['content']:
                        relevant_memories.append(self.memory[user_id][i])
                        break

        return relevant_memories

    def save_memories(self):
        utils.fsave(self.memory)


    def __str__(self):
        return str(self.memory)