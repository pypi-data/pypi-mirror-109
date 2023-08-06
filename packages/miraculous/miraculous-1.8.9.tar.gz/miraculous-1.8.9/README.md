[![CodeFactor](https://www.codefactor.io/repository/github/I-make-python-module-and-bots-stuff/D.py-M/badge)](https://www.codefactor.io/repository/github/I-make-python-module-and-bots-stuff/D.py-M)
[![Pypi Download Stats](https://img.shields.io/pypi/dm/miraculous)](https://pypistats.org/packages/miraculous)
[![Latest version](https://badge.fury.io/py/miraculous.svg)](https://pypi.org/project/miraculous/)
[![Languages](https://img.shields.io/github/languages/count/I-make-python-module-and-bots-stuff/D.py-M)]()
[![Size of code](https://img.shields.io/github/languages/code-size/I-make-python-module-and-bots-stuff/D.py-M)]()
[![All download in pypi](https://img.shields.io/pypi/dd/miraculous)](https://pypi.org/project/miraculous)
[![Latest release](https://img.shields.io/github/v/release/I-make-python-module-and-bots-stuff/D.py-M)]()
[![Activity](https://img.shields.io/github/commit-activity/w/I-make-python-module-and-bots-stuff/D.py-M)]()
[![Commit](https://img.shields.io/github/last-commit/I-make-python-module-and-bots-stuff/D.py-M)]()
[![Contributor](https://img.shields.io/github/contributors-anon/I-make-python-module-and-bots-stuff/D.py-M)]()
[![Documentation Status](https://readthedocs.org/projects/miraculous/badge/?version=latest)](https://miraculous.readthedocs.io/en/latest/?badge=latest)
[![CIRCLE CI STATUS](https://circleci.com/gh/I-make-python-module-and-bots-stuff/D.py-M.svg?style=svg)](https://app.circleci.com/pipelines/github/I-make-python-module-and-bots-stuff/D.py-M)
*So many fucking badge*
# D.py-M
Greeting! Welcome to my miraculous bot repository!
Here's how to setup!
# Setup process
1. If you gonna host on your pc edit last line to be bot.run("token"). If you're gonna host on  repl add .env file and add TO=token. If you're gonna to host with heroku I have file ready for you just edit config var to be KEY TO VALUE bot token
2. Then fire it up it should show your bot name id and stuff
Default prefix is "m." you can change at bot variable

# But I just download this from pypi
Just use 

```py
from miraculous import login

login(token="bot token",needwebserver=False)

```
needwebserver You can just pass it with bool or leave it if you don't use replit
```
```
Or if you use enviroment variable
```py
from miraculous import login
from os import getenv

login(token=getenv("your enviroment variable!"))
```
## What I just fixed?
- Not realtime volume changing
- Loop don't work
- Pausing and Resuming is not work
- Changed how it play music without downloading
## What I just don't fixed yet?
- Sound doesn't change when looping
# Errors?
Please ensure you have all module by do
```bash
pip install -r requirements.txt
```
And check your token is not none if you are using enviroment variable method
```bash
python yourscriptname.py
Removing cache dir /home/runner/.cache/youtube-dl ..
* Serving Flask app "miraculous" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
Loaded cog.globalchat!
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
Loaded cog.globalchat!
 * Serving Flask app "" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
Traceback (most recent call last):
  File "main.py", line 519, in <module>
    bot.run(os.getenv("TOr"))
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 723, in run
    return future.result()
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 702, in runner
    await self.start(*args, **kwargs)
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 665, in start
    await self.login(*args, bot=bot)
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 511, in login
await self.http.static_login(token.strip(), bot=bot)
AttributeError: 'NoneType' object has no attribute 'strip'
```
also check your token is not exposed
```bash
python main.py
Removing cache dir /home/runner/.cache/youtube-dl ..
 * Serving Flask app "miraculous" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
Loaded cog.globalchat!
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
Loaded cog.globalchat!
 * Serving Flask app "" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
Traceback (most recent call last):
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/http.py", line 293, in static_login
    data = await self.request(Route('GET', '/users/@me'))
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/http.py", line 247, in request
    raise HTTPException(r, data)
discord.errors.HTTPException: 401 Unauthorized (error code: 0): 401: Unauthorized

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "main.py", line 584, in <module>
    bot.run("ksdajfhkhasdkfj")
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 718, in run
    return future.result()
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 697, in runner
    await self.start(*args, **kwargs)
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 660, in start
    await self.login(*args, bot=bot)
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/client.py", line 509, in login
    await self.http.static_login(token.strip(), bot=bot)
  File "/opt/virtualenvs/python3/lib/python3.8/site-packages/discord/http.py", line 297, in static_login
    raise LoginFailure('Improper token has been passed.') from exc
discord.errors.LoginFailure: Improper token has been passed.
```
# Links
[Pypi Link (*plz download*)](https://pypi.org/project/miraculous/)  [Github link](https://github.com/I-make-python-module-and-bots-stuff/Music-bot)  [Discord server](https://discord.gg/sHprKhGwg8) [READ THE DOCS REEEEE](https://miraculous.rtfd.io)
# Love!
# What I update in module today?
Change doc url
