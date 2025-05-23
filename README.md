## Postup spuštění aplikace

### 1. Vytvoření projektu
Nejprve je nutné vytvořit kořenovou složku projektu a následně do ní přesunout všechny soubory (nebo naklonovat repozitář z GitHubu).
```bash
mkdir prezencni-system
cd prezencni-system
git clone https://github.com/Martin-Pop/prezence-rfid.git .
```

### 2. Virtuální prostředí a závislosti
V rámci této složky se vytvoří virtuální prostředí a následně aktivuje. Poté se nainstalují všechny požadované knihovny, které jsou uvedeny v souboru **requirements.txt.**
```bash
python3 -m venv venv
source venv/bin/activate 
python3 -m pip install -r requirements.txt
```
### 3. Konfigurace prostředí
V kořenové složce je nutné vytvořit soubor **.env**, do kterého se zadávají proměnné prostředí **DATABASE_NAME** a **FLASK_SECRET_KEY**, které aplikace vyžaduje pro bezpečný běh a připojení k databázi.
```bash
touch .env
```
do souboru napsat:
```bash
FLASK_SECRET_KEY=váš-klíč
DATABASE_NAME=váš-název-pro-databázi (název.db)
```
### 4. Inicializace databáze
Po správném nastavení prostředí je nutné spustit skript **setup_db.py**, který vytvoří potřebné databázové tabulky a připraví systém k provozu.
```bash
python3 setup_db.py
```
### 5. Automatické spouštění při startu systému
Pro zajištění automatického spuštění aplikace při startu zařízení je vhodné nakonfigurovat službu pomocí systemd. Vytvořím souborů s příponou .service, které budou spouštěny jako systémová služba na pozadí.

Příklad obsahu souboru /etc/systemd/system/rfid-reader.service (script na čtení karet):
```ini
[Unit]
Description=rfid reader script

[Service]
ExecStart=/home/martin/prezence/venv/bin/python /home/martin/prezence/rfid_reader.py
WorkingDirectory=/home/martin/prezence
User=martin
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
Příklad obsahu souboru /etc/systemd/system/prezence-web.service (script na webovou aplikaci):
```ini
[Unit]
Description=Flask Web App pro prezenci
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/home/martin/prezence/venv/bin/python3 /home/martin/prezence/app.py
WorkingDirectory=/home/martin/prezence
User=martin
Group=martin
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
aktivace:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nazev-sluzby.service
sudo systemctl start nazev-sluzby.service
```