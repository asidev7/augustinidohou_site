#!/bin/bash
# Script de déploiement — augustinidohou.site
# Usage : bash deploy.sh
set -e

APP_DIR="/var/www/portfolio"
DOMAIN="augustinidohou.site"
USER="www-data"
PYTHON="python3"

echo "=============================="
echo "  DÉPLOIEMENT augustinidohou.site"
echo "=============================="

# 1. Mise à jour du code
echo "[1/8] Pull GitHub..."
cd $APP_DIR
git pull origin main

# 2. Virtualenv & dépendances
echo "[2/8] Dépendances Python..."
$PYTHON -m venv env
source env/bin/activate
pip install -r requirements.txt --quiet

# 3. Migrations
echo "[3/8] Migrations..."
DJANGO_SETTINGS_MODULE=portfolio.settings_prod python manage.py migrate --noinput

# 4. Static files
echo "[4/8] Collectstatic..."
DJANGO_SETTINGS_MODULE=portfolio.settings_prod python manage.py collectstatic --noinput --clear

# 5. Permissions
echo "[5/8] Permissions..."
chown -R $USER:$USER $APP_DIR
chmod -R 755 $APP_DIR
mkdir -p $APP_DIR/media $APP_DIR/staticfiles
chown -R $USER:$USER $APP_DIR/media $APP_DIR/staticfiles

# 6. Gunicorn
echo "[6/8] Redémarrage Gunicorn..."
systemctl restart portfolio-gunicorn

# 7. Nginx
echo "[7/8] Reload Nginx..."
nginx -t && systemctl reload nginx

# 8. Statut
echo "[8/8] Statut..."
systemctl status portfolio-gunicorn --no-pager -l

echo ""
echo "✅ Déploiement terminé → https://$DOMAIN"
