# SimpleTrack
A bare-bones issue tracker intended for nontechnical users.

In dev,

1. `$ virtualenv SimpleTrack`
2. `$ pip install -r requirements.txt`
3. `$ python simpletrack.py`

Otherwise this runs on Docker behind nginx on my server. Docker
runs the container, which runs gunicorn, which binds to a socket
on the host, to which nginx proxies requests.