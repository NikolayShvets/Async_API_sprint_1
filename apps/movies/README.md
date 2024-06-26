# Async movies api
***
## Python version
3.12
## Local
***
### Installation
* create a virtual environment
```bash
python -m venv .venv
```
* activate .venv
```bash
source .venv/bin/activate
```
* install requirements
```bash
pip install -r ./requirements/local.txt
```
* create an .env file from the .env.example file
```bash
cp ./app/.env.example ./app/.env
```
* change variable values as needed

### Deploy
* use shortcut script
```bash
cd ../../ &&  make local
```

## Production
***
### Deploy
* use shortcut script:
```bash
cd ../../ &&  make
```

## Test and Lint

* run linters(ruff) and mypy
```bash
make plint 
```
