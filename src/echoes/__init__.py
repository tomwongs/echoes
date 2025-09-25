import echoes.model as model

#model_data = {}

#model_data["name"] = "Monika"
#model_data["model"] = "Monika"
#model["path"] = "models/"+model["name"]
#model["is_remembering"] = False             # Define wether or not the model will register the inputs/outputs in the context.

#model = core.Model()
#model.talk()


def create_model(model_data: dict) -> model.Model:
    LLM = model.Model(model_data)
    return LLM