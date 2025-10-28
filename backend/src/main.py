from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
import logging
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Web3 Approval Revoker")

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


CHAIN_CONFIG = {
    "ethereum": {
        "rpc": os.getenv(
            "ETHEREUM_RPC", "https://eth-mainnet.g.alchemy.com/v2/demo"
        ),
        "chain_id": 1,
    },
    # … polygon / arbitrum / optimism / base …
}

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
    def __init__(self, chain: str = "ethereum") -> None:
        self.chain = chain
        self.cfg = CHAIN_CONFIG.get(chain, CHAIN_CONFIG["ethereum"])
        self.w3 = Web3(Web3.HTTPProvider(self.cfg["rpc"]))
        self.chain_id = self.cfg["chain_id"]
        self.gas_account_key = os.getenv("RABBY_GAS_ACCOUNT_PRIVATE_KEY")
        self.flashbots_relay = os.getenv(
            "FLASHBOTS_RELAY", "https://relay.flashbots.net"
        )

    async def execute_sponsored_revocation_via_flashbots(
        self,
        token_address: str,
        spender_address: str,
        signer_address: str,
        signer_private_key: str,
    ):
        try:
            logger.info("Executing revocation on %s", self.chain)

            # ─── validation ───────────────────────────────────────────
            for label, addr in [
                ("token", token_address),
                ("spender", spender_address),
                ("signer", signer_address),
            ]:
                if not Web3.is_address(addr):
                    raise ValueError(f"Invalid {label} address: {addr}")

            signer = Account.from_key(signer_private_key)
            gas_account = Account.from_key(self.gas_account_key)

            nonce = self.w3.eth.get_transaction_count(signer.address)

            token = self.w3.eth.contract(
                address=Web3.to_checksum_address(token_address), abi=ERC20_ABI
            )

            tx = token.functions.approve(
                Web3.to_checksum_address(spender_address), 0
            ).build_transaction(
                {
                    "from": signer.address,
                    "nonce": nonce,
                    "gas": 100_000,
                    "gasPrice": self.w3.eth.gas_price,
                    "chainId": self.chain_id,
                }
            )

            signed = signer.sign_transaction(tx)
            logger.info("Signed tx %s", signed.hash.hex())

            # In a real Flashbots flow you would build and send a bundle here.
            return {
                "status": "success",
                "txHash": signed.hash.hex(),
                "chain": self.chain,
            }

        except Exception as exc:
            logger.exception("execute_sponsored_revocation failed")
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    async def get_bundle_status(self, bundle_hash: str):
        # Stub implementation
        return {"status": "pending", "bundleHash": bundle_hash, "chain": self.chain}


@app.post("/api/sponsored-tx")
async def sponsored_tx_endpoint(req: SponsoredTxRequest):
    service = SponsoredTransactionService(req.chain)
    return await service.execute_sponsored_revocation_via_flashbots(
        req.tokenAddress,
        req.spenderAddress,
        req.signerAddress,
        req.signerPrivateKey,
    )


@app.post("/api/bundle-status")
async def bundle_status_endpoint(req: BundleStatusRequest):
    service = SponsoredTransactionService(req.chain)
    return await service.get_bundle_status(req.bundleHash)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
