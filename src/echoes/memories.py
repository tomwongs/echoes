from . import utils
from datetime import datetime
import hashlib
from mem4ai.mem4ai import Memtor



# WARNING THIS FEATURE IS STILL A WASTELAND!
#  This feature is not yet stable and implemented as all the code needs to be reviewed, tested and reworked.
#  Planning on using mem4ai library in the meantime of implementing a better system.


#def extract_keywords(text):
#        return set(re.findall(r'\b\w+\b', text.lower())) 
#
#
#def infer_tags_from_input(model_data: dict, user_input):
#    keywords = extract_keywords(user_input)
#    matched_tags = defaultdict(int)
#
#    for word in keywords:
#        for memory in model_data['memories']:
#            tags = memory["tags"]
#            for tag in tags:
#                if tag == word:
#                    matched_tags[tag] += 1
#
#        implicit_tag = model_data['keywords_to_tag'].get(word)
#        if implicit_tag:
#            matched_tags[implicit_tag] += 1
#
#
#    return matched_tags
#
#
#def score_memory_by_tags(memory, matched_tags):
#    score = 0
#    for tag in memory.get("tags", []):
#        score += matched_tags.get(tag, 0)
#    return score
#
#
#def memories_placeholder_convert(model_data: dict, memories):
#    for memory in memories:
#        memory["content"] = memory["content"].replace("{{char}}", model_data["name"])
#        if model_data.get("user"):
#            memory["content"] = memory["content"].replace("{{user}}", model_data["user"])
#
#    return memories
#
#
#def get_top_memories(memories, user_input, top_n=2):
#    matched_tags = infer_tags_from_input(user_input)
#
#    scored_memories = []
#    for memory in memories:
#       score = score_memory_by_tags(memory, matched_tags)
#       if score > 0:
#            print("\033[32mLoading", memory["title"], "memory card...\033[0m")
#            scored_memories.append([score, memory])
#
#    scored_memories.sort(reverse=True, key=lambda x: x[0])
#    return memories_placeholder_convert([mem for _, mem in scored_memories[:top_n]])


#def init_memory():
#    memtor = Memtor()
#    return memtor
#
#def add_memory(memory: mem4ai.Memtor, content: str, metadata: dict, user: str) -> str:
#    return memory.add_memory(content, metadata=metadata, user_id=user)
#
#def search_memory(memory: mem4ai.Memtor, content: str, user: str) -> list:
#    return memory.search_memories(content, user_id=user)
#
#def update_memory(memory: mem4ai.Memtor, memory_id, content: str, metadata: dict) -> bool:
#    return memory.update_memory(memory_id, content, metadata=metadata)
#
#def delete_memory(memory: mem4ai.Memtor, memory_id) -> bool:
#    return memory.delete_memory(memory_id)
#
#def save_memories(memory: mem4ai.Memtor) -> bool:
#    memories = memory.list_memories()
#    return utils.save('memories.json', str(memories))


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
        for memories in self.memory.get(user_id):
            for i in range(0, len(memories)):
                for word in content:
                    if word in self.memory[user_id][i]['content']:
                        memories.append(self.memory[user_id[i]])

        return relevant_memories


    def __str__(self):
        return str(self.memory)