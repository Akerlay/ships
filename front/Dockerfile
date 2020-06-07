FROM nginx:latest
COPY ./dist /var/www/ships
RUN chmod -R a+x /var/www
COPY ./nginx.conf /etc/nginx/nginx.conf
#COPY .//run_nginx.sh /etc/nginx/run_nginx.sh
#RUN chmod -R a+x /var/www
#RUN chmod -R a+x /etc/nginx/run_nginx.sh
#ENTRYPOINT /etc/nginx/run_nginx.sh
#RUN apt-get update && apt-get install -y gettext-base
#RUN envsubst < /etc/nginx/nginx.temp.conf > /etc/nginx/nginx.con