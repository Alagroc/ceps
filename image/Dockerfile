from your_preferred_docker_registry/centos-7:latest

MAINTAINER Andres Martin <andreu.antonio@gmail.com> 

RUN yum install -y yum-plugin-ovl vim net-tools netcat-openbsd
RUN yum clean all
RUN yum install -y openssl uwsgi nginx python27 uwsgi-plugin-python27 supervisor python27-flask; yum clean all

ADD etc/  /etc
RUN mkdir /ceps

# Copy app
COPY ./ceps.py /ceps/ceps.py

# File creation and permissions
RUN mkdir -p /tmp/nginx
RUN chmod 777 /tmp/nginx
RUN mkdir -p /var/log/nginx
RUN chmod 777 /var/log/nginx
RUN rm -f /etc/nginx/sites-available/default.conf
RUN mkdir /nginx/cache -p
RUN mkdir /nginx/run -p
RUN chmod g+xrw -R /nginx

RUN chmod g+w /etc/nginx/nginx.conf
RUN chmod g+w /etc

RUN setcap 'cap_net_bind_service=+ep' /usr/sbin/nginx

STOPSIGNAL SIGQUIT
ADD ./services.sh /root/services.sh
CMD ["/bin/bash", "/root/services.sh"]

