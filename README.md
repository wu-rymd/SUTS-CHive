## To run app

* install virtualenv, pip


```bash
virtualenv venv
source venv/bin/active
pip install -r req.txt
python ./app.py
```


## Make requests from terminal to running app

```bash
# create school
curl -H 'Content-Type: application/json' -d '{"name":"some school","address":"123 park","email":"","phone":""}' -X POST http://localhost:5000/schools

# get schools
curl http://localhost:5000/schools
```
