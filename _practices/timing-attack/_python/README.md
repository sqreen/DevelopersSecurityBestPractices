We have provided a sample python web application coded in Flask that check authorization token in a timing attack vulnerable way. You can also find a script that will exploit this vulnerability to retrieve the expected token.

### Run the web application

In order to run the web application, create a virtualenv:

```bash
python -m virtualenv -p $(which python3) venv
source venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

You can then run the web application this way:

```bash
gunicorn -w 1 app:app
```


The web application expects to receive the token named `SECRET_TOKEN` in `app.py` in the header named `X-TOKEN`. If the header match the hardcoded one, it returns a `200 OK` status code, else it returns a `403 Forbidden`.

### Hack the web application

In order to run the script to hack the web application, create a virtualenv:

```bash
python -m virtualenv -p $(which python3) venv
source venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

Finally, launch it with:

```bash
python hack.py
```

### Customize

You can change the hardcoded token in `app.py` to validate that the script is effectively working.

If you change the expected token size, also change the variable `TOKEN_SIZE` in `hack.py`. The hacking script was not made smart enough to try to find the right token size.
