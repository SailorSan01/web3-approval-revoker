from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.sponsored_tx_service import SponsoredTransactionService
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Web3 Approval Revoker with Flashbots")

app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

class SponsoredTxRequest(BaseModel):
      tokenAddress: str
      spenderAddress: str
      signerAddress: str
      signerPrivateKey: str
      chain: str = "ethereum"

class BundleStatusRequest(BaseModel):
      bundleHash: str
      chain: str = "ethereum"

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
