import echoes
import asyncio

model_data = {
    'name': 'LLama',
    'model': 'llama3.2:latest',
    'context': [],
    'context_file': 'context_file.json',
    'memories': [],
    'is_remembering': True,
    'keywords_to_tag': {}
}

model = echoes.create_model(model_data)
output = asyncio.run(model.generate_response("Hello!"))