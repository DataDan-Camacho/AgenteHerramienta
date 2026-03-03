import os
import json
import requests
from config import Config
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
 
config = Config()
load_dotenv()
 
project_client = AIProjectClient(
    endpoint=config.ai_foundry_endpoint,
    credential=DefaultAzureCredential(),
)
 
agent_name = config.ai_agent_id
openai_client = project_client.get_openai_client()
 
# Crear conversación opcional
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")
 
telefono = "2224445559" #Variable Fictica de prueba
conversation_id = conversation.id
url_az_function = config.azure_function
 
# Primer mensaje
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
    input="Hola",
)
 
# Segundo mensaje
response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
    input="Mi nombre es Angel, me apellido Cortez con correo cortez@gmail.com, con empresa ATP Solutions y quiero cotizar equipos de surface",
)
 
# Procesar posibles llamadas a funciones
input_list: ResponseInputParam = []
for item in response.output:
    if item.type == "function_call" and item.name == "save_data":
        args = json.loads(item.arguments)
 
        # Inyectar parametros internos que no están en la especificación del portal
        args["phone_number"] = telefono
        args["conversation_id"] = conversation_id
 
        # Llamada a la Azure Function con los extras
        response_post = requests.post(
            url=url_az_function,
            json=args
        )
        try:
            result = response_post.json()
        except ValueError:
            print("Datos Enviados", response_post.text)
            result = None
 
        # Devolver resultado al modelo
        input_list.append(
            FunctionCallOutput(
                type="function_call_output",
                call_id=item.call_id,
                output=json.dumps(result),
            )
        )
 
# Enviar la salida de la función al modelo
if input_list:
    response = openai_client.responses.create(
        input=input_list,
        conversation=conversation_id,
        extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
    )
    print(f"Final response: {response.output_text}")
 