mkdir test-flask

cd test-flask

sudo apt install python3.8-venv

python3 -m venv myenv

source myenv/bin/activate

pip install Flask

pip install urllib3

pip freeze > requirements.txt