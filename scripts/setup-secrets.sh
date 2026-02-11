#!/bin/bash

# Script to set up Docker secrets for production deployment
# Run this on your VPS before starting the production stack

set -e

SECRETS_DIR="./secrets"

echo "Setting up Docker secrets for Biz-Bot..."

# Create secrets directory if it doesn't exist
mkdir -p "$SECRETS_DIR"

# Function to create secret file
create_secret() {
    local secret_name=$1
    local secret_file="$SECRETS_DIR/${secret_name}.txt"
    
    if [ -f "$secret_file" ]; then
        echo "✓ Secret $secret_name already exists"
    else
        echo -n "Enter value for $secret_name: "
        read -s secret_value
        echo
        echo "$secret_value" > "$secret_file"
        chmod 600 "$secret_file"
        echo "✓ Created secret $secret_name"
    fi
}

# Required secrets
echo "Creating required secrets..."
echo

create_secret "twilio_account_sid"
create_secret "twilio_auth_token"
create_secret "elevenlabs_api_key"
create_secret "openai_api_key"
create_secret "jwt_secret"
create_secret "encryption_key"
create_secret "postgres_password"

echo
echo "✓ All secrets created successfully!"
echo
echo "Secrets are stored in: $SECRETS_DIR"
echo "Make sure to keep these files secure and never commit them to git!"
echo
echo "Next steps:"
echo "1. Update your .env file with non-secret configuration"
echo "2. Run: docker-compose -f docker-compose.prod.yml up -d"
