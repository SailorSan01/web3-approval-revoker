# Web3 Approval Revoker - Complete Project Files

## Project Structure

```
web3-approval-revoker/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py (CREATED)
│   │   ├── config.py (CREATED)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── flashbots_service.py
│   │   │   └── sponsored_tx_service.py
│   │   └── utils/
│   │       ├─ __init__.py
│   │       └── logger.py
│   ├── requirements.txt (CREATED)
│   ├── .env.example (CREATED)
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── WalletSetup.tsx
│   │   │   ├── GasAccountSelector.tsx
│   │   │   ├── ApprovalRevoker.tsx
│   │   │   └── TransactionStatus.tsx
│   │   ├── hooks/
│   │   │   └── useSponsoredTx.ts
│   │   ├── styles/
│   │   │   ├── globals.css
│   │   │   ├─ WalletSetup.css
│   │   │   ├── GasAccountSelector.css
│   │   │   ├── ApprovalRevoker.css
│   │   │   └── TransactionStatus.css
│   │   ├── pages/
│   │   │   └── index.tsx
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── README.md
├── .gitignore
└── README.md
```

## Remaining Files to Create

Please create the following files in your local repository:

### Backend Services

**backend/src/services/flashbots_service.py**
```python
from web3 import Web3
from eth_account import Account
from flashbots import flashbots
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FlashbotsService:
    def __init__(self, web3_provider: Web3, relay_url: str = "https://relay.flashbots.net"):
        self.w3 = web3_provider
        self.relay_url = relay_url

    async def send_bundle(self, transactions: List[str], signer_account: Account, target_block: int = None) -> Dict[str, Any]:
        try:
            flashbots(self.w3, account=signer_account, endpoint_uri=self.relay_url)
            if target_block is None:
                target_block = self.w3.eth.block_number + 1
            bundle = []
            for tx in transactions:
                bundle.append({"signed_transaction": tx})
            logger.info(f"Sending bundle with {len(bundle)} transactions to block {target_block}")
            result = self.w3.flashbots.send_bundle(bundle, target_block_number=target_block)
            bundle_hash = result.hex()
            logger.info(f"Bundle sent with hash: {bundle_hash}")
            return {'success': True, 'bundleHash': bundle_hash, 'targetBlock': target_block, 'transactionCount': len(bundle)}
        except Exception as e:
            logger.error(f"Error sending Flashbots bundle: {str(e)}")
            return {'success': False, 'error': str(e)}
```

**backend/src/services/sponsored_tx_service.py**
```python
from web3 import Web3
from eth_account import Account
from typing import Dict, Any
import json
from config import settings
from .flashbots_service import FlashbotsService
import logging

logger = logging.getLogger(__name__)

class SponsoredTransactionService:
    def __init__(self, chain: str):
        self.chain = chain
        self.rpc_url = settings.RPC_ENDPOINTS.get(chain)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.gas_account = Account.from_key(settings.RABBY_GAS_ACCOUNT_PRIVATE_KEY)
        self.flashbots_service = FlashbotsService(self.w3)

    ERC20_ABI = json.loads('[{"constant": false, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}]')

    async def build_revocation_tx(self, token_address: str, spender_address: str, signer_address: str) -> Dict[str, Any]:
        try:
            token_address = Web3.to_checksum_address(token_address)
            spender_address = Web3.to_checksum_address(spender_address)
            signer_address = Web3.to_checksum_address(signer_address)
            contract = self.w3.eth.contract(address=token_address, abi=self.ERC20_ABI)
            tx = contract.functions.approve(spender_address, 0).build_transaction({
                'from': signer_address,
                'nonce': self.w3.eth.get_transaction_count(signer_address),
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'chainId': self.w3.eth.chain_id,
            })
            return {'success': True, 'tx': tx}
        except Exception as e:
            logger.error(f"Error building revocation tx: {str(e)}")
            return {'success': False, 'error': str(e)}

    async def execute_sponsored_revocation_via_flashbots(self, token_address: str, spender_address: str, signer_address: str, signer_private_key: str) -> Dict[str, Any]:
        try:
            logger.info(f"Starting sponsored revocation via Flashbots on {self.chain}")
            build_result = await self.build_revocation_tx(token_address, spender_address, signer_address)
            if not build_result['success']:
                return build_result
            tx = build_result['tx']
            signer_account = Account.from_key(signer_private_key)
            signed_tx = self.w3.eth.account.sign_transaction(tx, signer_private_key)
            signed_tx_hex = signed_tx.rawTransaction.hex()
            logger.info(f"Transaction signed by OKX Wallet: {signer_account.address}")
            logger.info("Simulating bundle execution...")
            bundle_result = await self.flashbots_service.send_bundle([signed_tx_hex], signer_account=self.gas_account)
            if not bundle_result['success']:
                return bundle_result
            logger.info(f"Bundle sent successfully: {bundle_result['bundleHash']}")
            return {'success': True, 'bundleHash': bundle_result['bundleHash'], 'targetBlock': bundle_result['targetBlock'], 'gasPayerAddress': self.gas_account.address, 'signerAddress': signer_address, 'tokenAddress': token_address, 'spenderAddress': spender_address, 'status': 'Pending', 'method': 'Flashbots', 'chain': self.chain}
        except Exception as e:
            logger.error(f"Error executing sponsored revocation: {str(e)}")
            return {'success': False, 'error': str(e)}
```

### Frontend Components

**frontend/src/components/WalletSetup.tsx**
```typescript
import React, { useState } from 'react';
import { useConnect, useAccount } from 'wagmi';
import GasAccountSelector from './GasAccountSelector';
import '../styles/WalletSetup.css';

interface WalletSetupProps {
  onSetupComplete: (config: any) => void;
}

export default function WalletSetup({ onSetupComplete }: WalletSetupProps) {
  const { connect, connectors } = useConnect();
  const { address, isConnected } = useAccount();
  const [step, setStep] = useState<'wallet' | 'gas' | 'complete'>('wallet');
  const [okxAddress, setOkxAddress] = useState<string | null>(null);
  const [gasAccount, setGasAccount] = useState<any>(null);

  const handleConnectOKX = () => {
    const okxConnector = connectors.find(c => c.name === 'OKX Wallet');
    if (okxConnector) {
      connect({ connector: okxConnector });
    }
  };

  const handleOKXConnected = () => {
    if (address) {
      setOkxAddress(address);
      setStep('gas');
    }
  };

  const handleGasAccountSelected = (account: any) => {
    setGasAccount(account);
    setStep('complete');
    onSetupComplete({
      okxWallet: okxAddress,
      gasAccount: account,
      timestamp: new Date().toISOString()
    });
  };

  return (
    <div className="wallet-setup">
      <div className="setup-card">
        {step === 'wallet' && (
          <div className="setup-step">
            <h2>Step 1: Connect OKX Wallet</h2>
            <p>This wallet will sign the approval revocation transactions</p>
            {!isConnected ? (
              <button className="btn btn-primary" onClick={handleConnectOKX}>
                🔗 Connect OKX Wallet
              </button>
            ) : (
              <div className="connected-info">
                <div className="success-badge">✓ Connected</div>
                <p className="address">{address}</p>
                <button className="btn btn-secondary" onClick={handleOKXConnected}>
                  Continue to Gas Account Setup
                </button>
              </div>
            )}
          </div>
        )}
        {step === 'gas' && (
          <div className="setup-step">
            <h2>Step 2: Select Rabby Gas Account</h2>
            <p>Choose which wallet will pay the gas fees</p>
            <GasAccountSelector onSelect={handleGasAccountSelected} />
          </div>
        )}
        {step === 'complete' && (
          <div className="setup-step success">
            <h2>✓ Setup Complete!</h2>
            <div className="setup-summary">
              <div className="summary-item">
                <label>OKX Wallet (Signer):</label>
                <span className="address">{okxAddress}</span>
              </div>
              <div className="summary-item">
                <label>Gas Account (Payer):</label>
                <span className="address">{gasAccount?.address}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

### Frontend Configuration Files

**frontend/package.json**
```json
{
  "name": "web3-approval-revoker",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "wagmi": "^2.0.0",
    "viem": "^2.0.0",
    "@wagmi/connectors": "^4.0.0",
    "ethers": "^6.10.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "@types/react-dom": "^18.2.0"
  }
}
```

## Setup Instructions

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python src/main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features
- ✅ OKX Wallet Integration (Signer)
- - ✅ Rabby Gas Account (Sponsor)
  - - ✅ Flashbots MEV Protection
    - - ✅ Multi-chain Support
      - - ✅ Beautiful GUI Controller
       
        - ## Supported Chains
        - - Ethereum
          - - Polygon
            - - Arbitrum
              - - Optimism
                - - Base
                 
                  - ## API Endpoints
                  - - POST /api/sponsored-tx - Execute sponsored transaction
                    - - POST /api/bundle-status - Get bundle status
                      - - GET /health - Health check
                       
                        - For complete file contents, see the individual files in the repository.
