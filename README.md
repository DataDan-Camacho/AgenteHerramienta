# AgenteHerramienta

Este repositorio contiene un ejemplo sencillo de cómo invocar una herramienta (función) desde un agente hospedado en Microsoft Foundry y procesar la llamada en una función de Azure. El código está escrito en Python y demuestra el flujo básico de:

1. Crear una conversación con el cliente de OpenAI de Foundry.
2. Enviar mensajes al agente configurado en el portal de Foundry.
3. Capturar respuestas que incluyen llamadas a funciones desde el portal de MS Foundry (`function_call`).
4. Invocar una Azure Function para procesar los datos y devolver el resultado al modelo.

---

## Estructura del proyecto

- `agent.py` – Ejemplo de código que interactúa con el agente, maneja el ciclo de conversación y la llamada a la función.
- `config.py` – Clase de configuración que carga variables de entorno y valida su presencia.
- `openapi.json` – Archivo de Especifación OpenAI para la herramienta en el portal.
- `pyproject.toml` – Archivo de configuración de Python (poetry, dependencias, etc.).

---

## Requisitos

- Python 3.9+ (se recomienda usar un entorno virtual).
- Paquetes listados en `pyproject.toml`.
- Cuenta con acceso a Microsoft Foundry y configuración de un agente con herramienta que acepte la función `save_data`.
- Una Azure Function desplegada para recibir los datos y procesarlos.

---

## Configuración

Guarda las variables de entorno en un archivo `.env` en la raíz del proyecto o expórtalas en el entorno. Las siguientes variables son obligatorias:

```text
AI_FOUNDRY_ENDPOINT=<URL de tu instancia de AI Foundry>
AI_AGENT_ID=<ID del agente configurado en Foundry>
MODEL_DEPLOYMENT_NAME=<Nombre del despliegue del modelo (opcional si se usa agent_reference)>
AZURE_FUNCTION=<URL de la Azure Function que procesa la llamada>
```

---

## Uso

Ejecuta `agent.py` para iniciar el flujo de ejemplo. El script:

1. Crea una conversación en Foundry.
2. Envía un saludo y un mensaje de ejemplo que dispara la llamada a la función `save_data`.
3. Enrutará los argumentos a la Azure Function indicada y enviará la respuesta de vuelta al modelo.
4. Imprime en consola la respuesta final del agente.

