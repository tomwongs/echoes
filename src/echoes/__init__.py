from . import model

def create_model(model_data: dict) -> model.Model:
    LLM = model.Model(model_data)
    return LLM