FROM nginx:1.19.2-alpine

RUN apk add --no-cache curl

COPY ./nginx.conf /etc/nginx/
COPY ./healthcheck /
