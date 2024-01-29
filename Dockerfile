# syntax=docker/dockerfile:1.4

FROM nginx:1.23.4-alpine-slim as nginx

WORKDIR /var/www/cam/

COPY webserver/ /

COPY nginx/default.conf /etc/nginx/conf.d/

EXPOSE 3000

ENTRYPOINT nginx -g "daemon off;"
