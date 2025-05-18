#!/bin/bash
set -e

APP_DIR="/home/boba/Mainframe"
SERVICE_NAME="navi-dashboard"
DOMAIN="_"  # Optional — use "_" if not using a domain

echo "🔧 Updating system..."
sudo apt update && sudo apt install -y python3 python3-venv python3-pip nginx git

echo "📂 Ensuring app directory exists..."
cd "$APP_DIR"

echo "🐍 Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt || pip install flask gunicorn

echo "💡 Creating systemd service..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=Gunicorn for Navi Dashboard
After=network.target

[Service]
User=boba
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/.venv/bin"
ExecStart=$APP_DIR/.venv/bin/gunicorn -w 3 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}

echo "🌐 Creating NGINX config..."
sudo tee /etc/nginx/sites-available/navi > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location /static/ {
        alias $APP_DIR/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/navi /etc/nginx/sites-enabled/navi
sudo nginx -t && sudo systemctl reload nginx

echo "🎉 Deployment complete! Navi is online."
