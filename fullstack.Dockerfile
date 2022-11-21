# FROM node:lts-alpine3.15 as develop-stage
FROM node:16-alpine as develop-stage
WORKDIR /app
COPY ./spa/package*.json ./
RUN yarn global add @quasar/cli
COPY ./spa .
# build stage
FROM develop-stage as build-stage
RUN yarn
RUN quasar build

# production stage
FROM python:3.9

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql \
		postgresql-client \
		nginx \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY --from=build-stage /app/dist/spa /var/www/html/

RUN rm /etc/nginx/sites-enabled/default
COPY ./deployment/fullstack/nginx.conf /etc/nginx/sites-enabled/
COPY ./deployment/fullstack/startup.sh /tmp
RUN chmod 555 /tmp/startup.sh

# RUN mkdir -p /data/media /data/static

# RUN service nginx restart


COPY . .
RUN ln -s /data/media media
# RUN ln -s /data/static static


EXPOSE 80
ENTRYPOINT [ "/tmp/startup.sh" ] 
