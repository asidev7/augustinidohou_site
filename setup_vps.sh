#!/bin/bash
# Configuration initiale VPS — augustinidohou.site
# Lancer en root : bash setup_vps.sh
set -e

DOMAIN="augustinidohou.site"
APP_DIR="/var/www/portfolio"
REPO="https://github.com/asidev7/augustinidohou_site.git"
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")

echo "=============================="
echo "  SETUP VPS augustinidohou.site"
echo "=============================="

# 1. Paquets système
echo "[1] Installation des paquets..."
apt update -qq
apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git curl

# 2. Cloner le repo
echo "[2] Clonage du repo..."
mkdir -p $APP_DIR
git clone $REPO $APP_DIR || (cd $APP_DIR && git pull)

# 3. Python env
echo "[3] Environnement Python..."
cd $APP_DIR
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt --quiet

# 4. Variables d'environnement
echo "[4] Fichier .env..."
cat > $APP_DIR/.env << EOF
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_SETTINGS_MODULE=portfolio.settings_prod
EOF

# 5. Migrations & static
echo "[5] Migrations & static..."
DJANGO_SETTINGS_MODULE=portfolio.settings_prod python manage.py migrate --noinput
DJANGO_SETTINGS_MODULE=portfolio.settings_prod python manage.py collectstatic --noinput

# 6. Créer superuser admin (interactif)
echo "[6] Créer le superuser admin..."
DJANGO_SETTINGS_MODULE=portfolio.settings_prod python manage.py createsuperuser

# 7. Permissions
echo "[7] Permissions..."
mkdir -p $APP_DIR/media $APP_DIR/staticfiles
chown -R www-data:www-data $APP_DIR

# 8. Service Gunicorn systemd
echo "[8] Service Gunicorn..."
cat > /etc/systemd/system/portfolio-gunicorn.service << EOF
[Unit]
Description=Portfolio Gunicorn — augustinidohou.site
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/env/bin/gunicorn \\
    --workers 3 \\
    --bind unix:$APP_DIR/gunicorn.sock \\
    --access-logfile $APP_DIR/access.log \\
    --error-logfile $APP_DIR/error.log \\
    portfolio.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable portfolio-gunicorn
systemctl start portfolio-gunicorn

# 9. Nginx config
echo "[9] Configuration Nginx..."
cat > /etc/nginx/sites-available/portfolio << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $APP_DIR/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/gunicorn.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# 10. SSL Let's Encrypt
echo "[10] Certificat SSL..."
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m sandeaugustinidohou@gmail.com --redirect

# 11. Renouvellement auto SSL
echo "[11] Renouvellement SSL automatique..."
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && systemctl reload nginx") | crontab -

echo ""
echo "==============================="
echo "✅ Setup terminé !"
echo "   https://$DOMAIN"
echo "   Admin : https://$DOMAIN/admin"
echo "==============================="
