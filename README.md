# newsroom

### run locally
* run a mongo database named `newsroom`
* install python 3
* create virtualenv `virtualenv -p python3 venv`
* run the virtualenv `source ven/bin/activate`
* install dependencies `pip3 install -r requirements.txt`
* run the server `python3 main.py`

### deploying
* clone [ecs-deploy](https://github.com/silinternational/ecs-deploy) into a ~/src folder
* `bash deploy.sh testing | production`


### TODO:
* integrate nlp api: https://github.com/codelucas/newspaper
* integrate news article search api: https://newsapi.org/
