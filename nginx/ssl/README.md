# SSL Certificate Placeholder
# 
# In production, replace these with real SSL certificates from Let's Encrypt
# or your certificate provider.
#
# To generate Let's Encrypt certificates:
# 1. Install certbot on your VPS
# 2. Run: certbot certonly --webroot -w /var/www/certbot -d yourdomain.com
# 3. Certificates will be placed in /etc/letsencrypt/live/yourdomain.com/
# 4. Copy them to this directory or mount them in docker-compose.prod.yml
#
# For development/testing, you can generate self-signed certificates:
# openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
#   -keyout privkey.pem -out fullchain.pem \
#   -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
