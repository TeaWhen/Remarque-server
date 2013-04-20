# kill previous gunicorn process

kill -9 `more ~/remarque.pid`

# start new gunicorn process

gunicorn -w 4 -b 0.0.0.0:8123 remarque:app -D --pid ~/remarque.pid