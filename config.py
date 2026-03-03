import os
from dotenv import load_dotenv
load_dotenv()
 
class Config:
    def __init__(self):
        """
        Constructor for the class
        """
        self.ai_foundry_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")
        self.ai_agent_id = os.getenv("AI_AGENT_ID")
        self.model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")
        self.azure_function = os.getenv("AZURE_FUNCTION")
        # Validate configuration
        self.validate()
 
 
    def validate(self):
        """Validate that all required configuration properties are set."""
        missing_properties = []
        for attr, value in self.__dict__.items():
            if not value:  # Check if the property is None or an empty string
                missing_properties.append(attr)
 
        if missing_properties:
            raise ValueError(
                f"The following required configuration properties are missing or invalid: {', '.join(missing_properties)}"
            )
 