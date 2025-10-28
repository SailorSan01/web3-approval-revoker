# 🚀 QUICK START GUIDE - Web3 Approval Revoker

## ⚡ 5-Minute Setup

This guide will get you up and running in minutes!

### Prerequisites
- Python 3.10+ installed
- - Node.js 16+ installed
  - - Git installed
    - - Your Alchemy API Key (already configured)
      - - Your Rabby Gas Account Private Key (already configured)
       
        - ### Step 1: Clone the Repository
       
        - ```bash
          git clone https://github.com/SailorSan01/web3-approval-revoker.git
          cd web3-approval-revoker
          ```

          ### Step 2: Setup Backend

          ```bash
          cd backend

          # Create virtual environment
          python -m venv venv

          # Activate virtual environment
          # On Windows:
          venv\Scripts\activate
          # On macOS/Linux:
          source venv/bin/activate

          # Install dependencies
          pip install -r requirements.txt

          # Copy .env.example to .env (credentials already included)
          cp .env.example .env

          # Start the backend server
          python src/main.py
          ```

          ✅ Backend will start at: **http://localhost:8000**
          ✅ API Documentation: **http://localhost:8000/docs**

          ### Step 3: Setup Frontend (New Terminal)

          ```bash
          cd frontend

          # Install dependencies
          npm install

          # Start the development server
          npm run dev
          ```

          ✅ Frontend will start at: **http://localhost:3000**

          ### Step 4: Access the Application

          1. Open your browser and go to: **http://localhost:3000**
          2. 2. Connect your OKX Wallet
             3. 3. Select the chain (Ethereum, Polygon, Arbitrum, Optimism, or Base)
                4. 4. Enter the token address and spender address
                   5. 5. Click "Revoke Approval"
                      6. 6. Sign the transaction with your OKX Wallet
                         7. 7. Done! ✅
                           
                            8. ---
                           
                            9. ## 📋 Environment Variables (Already Configured)
                           
                            10. Your `.env` file already contains:
                           
                            11. ```
                                RABBY_GAS_ACCOUNT_PRIVATE_KEY=0x35d071217fdca7a26000d55388891ae00b44ef4ce782e78bff6edf350f677122
                                ALCHEMY_API_KEY=U9wwKHhyvwxly94UgjWgy
                                ETHEREUM_RPC=https://eth-mainnet.g.alchemy.com/v2/U9wwKHhyvwxly94UgjWgy
                                POLYGON_RPC=https://polygon-mainnet.g.alchemy.com/v2/U9wwKHhyvwxly94UgjWgy
                                ARBITRUM_RPC=https://arb-mainnet.g.alchemy.com/v2/U9wwKHhyvwxly94UgjWgy
                                OPTIMISM_RPC=https://opt-mainnet.g.alchemy.com/v2/U9wwKHhyvwxly94UgjWgy
                                BASE_RPC=https://base-mainnet.g.alchemy.com/v2/U9wwKHhyvwxly94UgjWgy
                                FLASHBOTS_RELAY=https://relay.flashbots.net
                                ```

                                ---

                                ## 🔧 Troubleshooting

                                ### Backend won't start?

                                ```bash
                                # Make sure you're in the backend directory
                                cd backend

                                # Verify Python version
                                python --version  # Should be 3.10+

                                # Reinstall dependencies
                                pip install --upgrade -r requirements.txt

                                # Try running again
                                python src/main.py
                                ```

                                ### Frontend won't start?

                                ```bash
                                # Make sure you're in the frontend directory
                                cd frontend

                                # Clear npm cache
                                npm cache clean --force

                                # Reinstall dependencies
                                rm -rf node_modules package-lock.json
                                npm install

                                # Try running again
                                npm run dev
                                ```

                                ### Port already in use?

                                ```bash
                                # Backend (change port)
                                python src/main.py --port 8001

                                # Frontend (change port)
                                npm run dev -- --port 3001
                                ```

                                ---

                                ## 📚 API Endpoints

                                ### 1. Execute Sponsored Transaction

                                **POST** `/api/sponsored-tx`

                                ```json
                                {
                                  "tokenAddress": "0x...",
                                  "spenderAddress": "0x...",
                                  "signerAddress": "0x...",
                                  "signerPrivateKey": "0x...",
                                  "chain": "ethereum"
                                }
                                ```

                                ### 2. Get Bundle Status

                                **POST** `/api/bundle-status`

                                ```json
                                {
                                  "bundleHash": "0x...",
                                  "chain": "ethereum"
                                }
                                ```

                                ### 3. Health Check

                                **GET** `/health`

                                ---

                                ## ✨ Features

                                ✅ **Multi-Chain Support**
                                - Ethereum
                                - - Polygon
                                  - - Arbitrum
                                    - - Optimism
                                      - - Base
                                       
                                        - ✅ **Security Features**
                                        - - OKX Wallet Integration
                                          - - Rabby Gas Account Sponsorship
                                            - - Flashbots MEV Protection
                                              - - Private Pool Submission
                                               
                                                - ✅ **User-Friendly Interface**
                                                - - Beautiful React/Next.js GUI
                                                  - - Real-time Transaction Monitoring
                                                    - - Chain Selection
                                                      - - Easy Wallet Connection
                                                       
                                                        - ---

                                                        ## 🎯 Next Steps

                                                        1. ✅ Backend is running at http://localhost:8000
                                                        2. 2. ✅ Frontend is running at http://localhost:3000
                                                           3. 3. ✅ All credentials are configured
                                                              4. 4. ✅ Ready to revoke token approvals!
                                                                
                                                                 5. ---
                                                                
                                                                 6. ## 📞 Support
                                                                
                                                                 7. For issues or questions:
                                                                 8. 1. Check the [README.md](README.md) for detailed documentation
                                                                    2. 2. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for advanced setup
                                                                       3. 3. Check the [PROJECT_FILES.md](PROJECT_FILES.md) for file structure
                                                                         
                                                                          4. ---
                                                                         
                                                                          5. ## 🚀 You're All Set!
                                                                         
                                                                          6. Your Web3 Approval Revoker is now ready to use! Start revoking token approvals safely and securely with Flashbots MEV protection.
                                                                         
                                                                          7. Happy revoking! 🎉
