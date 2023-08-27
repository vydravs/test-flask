### Why?
The API accepts a POST request at /json, transforms the incoming json in some way, using a dynamically loaded module and its functions, the names of which are specified in the incoming request, and returns it back (client with sample json file in the client project folder).

Receives a GET request at /html and displays a table of dynamically loaded modules with function names, function Docstring and functions themselves.

### Install
```
mkdir test-flask
cd test-flask
sudo apt install python3.8-venv
python3 -m venv myenv
source myenv/bin/activate
pip install Flask
pip install urllib3
pip freeze > requirements.txt
python app.py
```

### Build Docker image, run and stop it
```
docker duild .
docker images
docker run --rm -d -p 5000:80 <IMAGE_ID>
docker stop <IMAGE_ID>
```