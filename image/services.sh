#!/bin/bash
echo "Starting nginx and uwsgi"
if [ ! -d /var/log/nginx ]; then mkdir -p /var/log/nginx; fi

/usr/sbin/uwsgi --logto /nginx/uwsgi.log --logfile-chmod 644 --logfile-chown --pidfile2 /nginx/uwsgi.pid --stats /nginx/uwsgi.stats --zerg-server /nginx/uwsgi.zerg --need-app --ini /etc/uwsgi/uwsgi.ini --ftok /nginx/uwsgi.ftok.2 &
nginx -c /etc/nginx/nginx.conf 
echo "Did i just crash?"
while (true); do sleep 5; done

