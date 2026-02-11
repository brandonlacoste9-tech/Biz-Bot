#!/bin/bash

# SSL certificate setup script using Let's Encrypt
# Run this on your VPS before deploying to production

set -e

DOMAIN="${DOMAIN:-yourdomain.com}"
EMAIL="${SSL_EMAIL:-admin@yourdomain.com}"
WEBROOT="/var/www/certbot"

echo "🔒 Setting up SSL certificates for $DOMAIN"

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    echo "Installing certbot..."
    apt-get update
    apt-get install -y certbot
fi

# Create webroot directory
mkdir -p "$WEBROOT"

# Start nginx temporarily for certificate validation
echo "Starting nginx for certificate validation..."
docker-compose up -d nginx

# Wait for nginx to start
sleep 5

# Obtain certificate
echo "Obtaining SSL certificate..."
certbot certonly --webroot \
    -w "$WEBROOT" \
    -d "$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --non-interactive \
    --keep-until-expiring

# Copy certificates to nginx ssl directory
echo "Copying certificates..."
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem nginx/ssl/

# Set proper permissions
chmod 644 nginx/ssl/fullchain.pem
chmod 600 nginx/ssl/privkey.pem

# Restart nginx to apply certificates
echo "Restarting nginx..."
docker-compose restart nginx

echo "✓ SSL certificates setup complete!"
echo
echo "Certificate details:"
certbot certificates

# Setup auto-renewal
echo
echo "Setting up automatic renewal..."
cat > /etc/cron.d/certbot-renew << CRON
0 0,12 * * * root certbot renew --quiet --deploy-hook "cd $(pwd) && docker-compose restart nginx"
CRON

echo "✓ Auto-renewal configured (runs twice daily)"
