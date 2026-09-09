from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ProviderConfig:
    africa_talking_api_key: str = os.getenv("AFRICAS_TALKING_API_KEY", "")
    africa_talking_username: str = os.getenv("AFRICAS_TALKING_USERNAME", "")
    whatsapp_token: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    whatsapp_phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    daraja_consumer_key: str = os.getenv("DARAJA_CONSUMER_KEY", "")
    daraja_consumer_secret: str = os.getenv("DARAJA_CONSUMER_SECRET", "")
    r2_endpoint_url: str = os.getenv("R2_ENDPOINT_URL", "")
    r2_bucket_name: str = os.getenv("R2_BUCKET_NAME", "")


providers = ProviderConfig()
