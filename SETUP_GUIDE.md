# Web3 Approval Revoker - Complete Setup Guide

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9+
- - Node.js 16+
  - - npm or yarn
    - - Git
     
      - ### Backend Setup
      - ```bash
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

        ## Environment Variables

        Create `.env` file in backend folder:
        ```
        RABBY_GAS_ACCOUNT_PRIVATE_KEY=0x[your_private_key]
        ALCHEMY_API_KEY=[your_alchemy_key]
        ETHEREUM_RPC=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
        POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
        ARBITRUM_RPC=https://arb-mainnet.g.alchemy.com/v2/YOUR_KEY
        OPTIMISM_RPC=https://opt-mainnet.g.alchemy.com/v2/YOUR_KEY
        BASE_RPC=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
        FLASHBOTS_RELAY=https://relay.flashbots.net
        ```

        ## Project Features

        ✅ OKX Wallet Integration (Transaction Signer)
        ✅ Rabby Gas Account (Gas Fee Sponsor)
        ✅ Flashbots MEV Protection
        ✅ Multi-chain Support (Ethereum, Polygon, Arbitrum, Optimism, Base)
        ✅ Beautiful React/Next.js GUI
        ✅ FastAPI Backend
        ✅ Real-time Bundle Status Monitoring

        ## API Endpoints

        ### POST /api/sponsored-tx
        Execute a sponsored token approval revocation

        **Request:**
        ```json
        {
          "tokenAddress": "0x...",
          "spenderAddress": "0x...",
          "signerAddress": "0x...",
          "signerPrivateKey": "0x...",
          "chain": "ethereum"
        }
        ```

        **Response:**
        ```json
        {
          "success": true,
          "bundleHash": "0x...",
          "targetBlock": 12345,
          "gasPayerAddress": "0x...",
          "signerAddress": "0x...",
          "status": "Pending",
          "method": "Flashbots"
        }
        ```

        ### POST /api/bundle-status
        Get the status of a submitted bundle

        **Request:**
        ```json
        {
          "bundleHash": "0x...",
          "chain": "ethereum"
        }
        ```

        ### GET /health
        Health check endpoint

        ## Supported Chains
        - Ethereum Mainnet
        - - Polygon
          - - Arbitrum One
            - - Optimism
              - - Base
               
                - ## Architecture
               
                - ### Frontend (React/Next.js)
                - - Wagmi for wallet connection
                  - - Viem for Web3 interactions
                    - - Beautiful UI with CSS styling
                      - - Real-time status updates
                       
                        - ### Backend (Python/FastAPI)
                        - - Web3.py for blockchain interactions
                          - - Flashbots SDK for MEV protection
                            - - Async/await for performance
                              - - CORS enabled for frontend communication
                               
                                - ## Transaction Flow
                               
                                - 1. User connects OKX Wallet
                                  2. 2. User selects Rabby Gas Account
                                     3. 3. User enters token and spender addresses
                                        4. 4. Backend builds revocation transaction
                                           5. 5. OKX Wallet signs the transaction
                                              6. 6. Flashbots simulates the bundle
                                                 7. 7. Bundle submitted to Flashbots relay
                                                    8. 8. Rabby Gas Account pays the fees
                                                       9. 9. Real-time status monitoring
                                                         
                                                          10. ## Troubleshooting
                                                         
                                                          11. ### Backend won't start
                                                          12. - Check Python version (3.9+)
                                                              - - Verify all dependencies installed: `pip install -r requirements.txt`
                                                                - - Check .env file has all required keys
                                                                 
                                                                  - ### Frontend won't load
                                                                  - - Check Node.js version (16+)
                                                                    - - Clear node_modules: `rm -rf node_modules && npm install`
                                                                      - - Check port 3000 is available
                                                                       
                                                                        - ### Wallet connection issues
                                                                        - - Ensure OKX Wallet extension is installed
                                                                          - - Check network is correct in wallet
                                                                            - - Try refreshing the page
                                                                             
                                                                              - ## Production Deployment
                                                                             
                                                                              - ### Backend
                                                                              - ```bash
                                                                                gunicorn -w 4 -b 0.0.0.0:8000 src.main:app
                                                                                ```

                                                                                ### Frontend
                                                                                ```bash
                                                                                npm run build
                                                                                npm run start
                                                                                ```

                                                                                ## Security Notes

                                                                                ⚠️ Never commit .env file
                                                                                ⚠️ Use environment variables for sensitive data
                                                                                ⚠️ In production, use wallet signing instead of private keys
                                                                                ⚠️ Always validate addresses before transactions
                                                                                ⚠️ Test on testnet first

                                                                                ## Support

                                                                                For issues or questions, please open an issue on GitHub.

                                                                                ## License

                                                                                MIT
