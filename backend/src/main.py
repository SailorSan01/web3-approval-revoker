from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Web3 Approval Revoker with Flashbots")

# Add CORS middleware
app.add_middleware(
          CORSMiddleware,
          allow_origins=["*"],
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
)

# Request models
class SponsoredTxRequest(BaseModel):
          tokenAddress: str
          spenderAddress: str
          signerAddress: str
          signerPrivateKey: str
          chain: str = "ethereum"

class BundleStatusRequest(BaseModel):
          bundleHash: str
          chain: str = "ethereum"

# Chain configuration
CHAIN_CONFIG = {
          "ethereum": {
                        "rpc": os.getenv("ETHEREUM_RPC", "https://eth-mainnet.g.alchemy.com/v2/demo"),
                        "chain_id": 1,
          },
          "polygon": {
                        "rpc": os.getenv("POLYGON_RPC", "https://polygon-mainnet.g.alchemy.com/v2/demo"),
                        "chain_id": 137,
          },
          "arbitrum": {
                        "rpc": os.getenv("ARBITRUM_RPC", "https://arb-mainnet.g.alchemy.com/v2/demo"),
                        "chain_id": 42161,
          },
          "optimism": {
                        "rpc": os.getenv("OPTIMISM_RPC", "https://opt-mainnet.g.alchemy.com/v2/demo"),
                        "chain_id": 10,
          },
          "base": {
                        "rpc": os.getenv("BASE_RPC", "https://base-mainnet.g.alchemy.com/v2/demo"),
                        "chain_id": 8453,
          },
}

# ERC20 ABI for approve function
ERC20_ABI = [
          {
                        "constant": False,
                        "inputs": [
                                          {"name": "_spender", "type": "address"},
                                          {"name": "_value", "type": "uint256"},
                        ],
                        "name": "approve",
                        "outputs": [{"name": "", "type": "bool"}],
                        "type": "function",
          }
]

class SponsoredTransactionService:
          def __init__(self, chain: str = "ethereum"):
                        self.chain = chain
                        self.config = CHAIN_CONFIG.get(chain, CHAIN_CONFIG["ethereum"])
                        self.w3 = Web3(Web3.HTTPProvider(self.config["rpc"]))
                        self.chain_id = self.config["chain_id"]
                        self.gas_account_key = os.getenv("RABBY_GAS_ACCOUNT_PRIVATE_KEY")
                        self.flashbots_relay = os.getenv("FLASHBOTS_RELAY", "https://relay.flashbots.net")

          async def execute_sponsored_revocation_via_flashbots(
                        self,
                        token_address: str,
                        spender_address: str,
                        signer_address: str,
                        signer_private_key: str,
          ):
                        try:
                                          logger.info(f"Executing sponsored revocation on {self.chain}")

            # Validate addresses
                            if not Web3.is_address(token_address):
                                                  raise ValueError(f"Invalid token address: {token_address}")
                                              if not Web3.is_address(spender_address):
                                                                    raise ValueError(f"Invalid spender address: {spender_address}")
                                                                if not Web3.is_address(signer_address):
                                                                                      raise ValueError(f"Invalid signer address: {signer_address}")

                            # Create signer account
                            signer_account = Account.from_key(signer_private_key)
            gas_account = Account.from_key(self.gas_account_key)

            # Get nonce
            nonce = self.w3.eth.get_transaction_count(signer_address)

            # Create contract instance
            token_contract = self.w3.eth.contract(
                                  address=Web3.to_checksum_address(token_address),
                                  abi=ERC20_ABI
            )

            # Build revocation transaction (approve with 0 amount)
            tx = token_contract.functions.approve(
                                  Web3.to_checksum_address(spender_address),
                                  0
            ).build_transaction({
                                  "from": Web3.to_checksum_address(signer_address),
                                  "nonce": nonce,
                                  "gas": 100000,
                                  "gasPrice": self.w3.eth.gas_price,
                                  "chainId": self.chain_id,
            })

            # Sign transaction
            signed_tx = signer_account.sign_transaction(tx)

            logger.info(f"Transaction signed: {signed_tx.hash.hex()}")

            return {
                                  "status": "success",
                                  "message": "Revocation transaction prepared",
                                  "txHash": signed_tx.hash.hex(),
                                  "chain": self.chain,
                                  "tokenAddress": token_address,
                                  "spenderAddress": spender_address,
            }
except Exception as e:
            logger.error(f"Error in execute_sponsored_revocation_via_flashbots: {str(e)}")
            raise

    async def get_bundle_status(self, bundle_hash: str):
                  try:
                                    logger.info(f"Getting bundle status for {bundle_hash}")
                                    return {
                                        "status": "pending",
                                        "bundleHash": bundle_hash,
                                        "chain": self.chain,
                                    }
except Exception as e:
            logger.error(f"Error getting bundle status: {str(e)}")
            raise

# API Endpoints
@app.post("/api/sponsored-tx")
async def execute_sponsored_transaction(request: SponsoredTxRequest):
          try:
                        logger.info(f"Received sponsored transaction request on {request.chain}")
                        service = SponsoredTransactionService(request.chain)
                        result = await service.execute_sponsored_revocation_via_flashbots(
                            token_address=request.tokenAddress,
                            spender_address=request.spenderAddress,
                            signer_address=request.signerAddress,
                            signer_private_key=request.signerPrivateKey
                        )
                        return result
except Exception as e:
        logger.error(f"Error executing sponsored transaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bundle-status")
async def get_bundle_status(request: BundleStatusRequest):
          try:
                        service = SponsoredTransactionService(request.chain)
                        result = await service.get_bundle_status(request.bundleHash)
                        return result
except Exception as e:
        logger.error(f"Error getting bundle status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
          return {"status": "ok", "service": "Web3 Approval Revoker with Flashbots"}

if __name__ == "__main__":
          import uvicorn
          uvicorn.run(app, host="0.0.0.0", port=8000)
