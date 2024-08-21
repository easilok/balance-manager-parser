set shell := ["bash", "-uc"]

coverflex file:
    .venv/bin/python main.py -b coverflex {{file}}

revolut file:
    .venv/bin/python main.py -b revolut {{file}}
