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