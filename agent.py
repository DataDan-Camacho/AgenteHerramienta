import os
import json
import requests
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

agent_name = os.environ["AGENT_NAME"]
openai_client = project_client.get_openai_client()

# Crear conversación opcional
conversation = openai_client.conversations.create()
print(f"Created conversation (id: {conversation.id})")

telefono = "2224445559"
conversation_id = conversation.id

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
    input="Angel Cortez cortez@precitool.com precitool2 Slicenciamiento de surface en la nube",
)

# Procesar posibles llamadas a funciones
input_list: ResponseInputParam = []
for item in response.output:
    if item.type == "function_call" and item.name == "save_data":
        args = json.loads(item.arguments)

        # Inyectar parámetros internos que no están en el schema del portal
        args["phone_number"] = telefono
        args["conversation_id"] = conversation_id

        # Llamada real a tu Azure Function con los extras
        result = requests.post(
            "https://precitool-agent-skills.azurewebsites.net/api",
            json=args
        ).json()

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
        previous_response_id=response.id,
        extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
    )
    print(f"Final response: {response.output_text}")