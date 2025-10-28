from pydantic_settings import BaseSettings
from typing import Dict
import os

class Settings(BaseSettings):
      RPC_ENDPOINTS: Dict[str, str] = {
                "ethereum": os.getenv("ETHEREUM_RPC", "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"),
                "polygon": os.getenv("POLYGON_RPC", "https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY"),
                "arbitrum": os.getenv("ARBITRUM_RPC", "https://arb-mainnet.g.alchemy.com/v2/YOUR_KEY"),
                "optimism": os.getenv("OPTIMISM_RPC", "https://opt-mainnet.g.alchemy.com/v2/YOUR_KEY"),
                "base": os.getenv("BASE_RPC", "https://base-mainnet.g.alchemy.com/v2/YOUR_KEY"),
      }

    RABBY_GAS_ACCOUNT_PRIVATE_KEY: str = os.getenv("RABBY_GAS_ACCOUNT_PRIVATE_KEY", "")
    FLASHBOTS_RELAY: str = os.getenv("FLASHBOTS_RELAY", "https://relay.flashbots.net")
    ALCHEMY_API_KEY: str = os.getenv("ALCHEMY_API_KEY", "")

    class Config:
              env_file = ".env"
              case_sensitive = True

settings = Settings()
