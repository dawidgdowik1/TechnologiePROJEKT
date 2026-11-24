#!/bin/bash
# Konfiguracja bazowej instancji EC2 (voting-web-base)

# 1. Instalacja bibliotek aplikacji
sudo pip3 install flask pymysql gunicorn

# 2. Utworzenie katalogu roboczego i skopiowanie kodu aplikacji
sudo mkdir -p /opt/voting-app
sudo cp ../app/app.py /opt/voting-app/app.py

# 3. Utworzenie tabeli candidates i dodanie zawodnikow w Amazon RDS
python3 -c "import sys; sys.path.append('/opt/voting-app'); import app; app.init_db()"

# 4. Konfiguracja uslugi systemowej systemd (Gunicorn na porcie 80)
cat << 'EOF' | sudo tee /etc/systemd/system/voting.service
[Unit]
Description=Voting App
After=network.target

[Service]
User=root
WorkingDirectory=/opt/voting-app
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:80 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 5. Uruchomienie i wlaczenie autostartu uslugi
sudo systemctl daemon-reload
sudo systemctl enable --now voting
sudo systemctl status voting --no-pager