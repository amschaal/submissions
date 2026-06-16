FROM node:22-alpine as develop-stage
WORKDIR /app
COPY ./spa/package*.json ./
RUN yarn global add @quasar/cli
COPY ./spa .
# build stage
FROM develop-stage as build-stage
# Frontend build identity for the version.json refresh prompt (passed by
# buildspec.yml as --build-arg APP_COMMIT=<spa commit>).
ARG APP_COMMIT
ENV APP_COMMIT=$APP_COMMIT
RUN yarn
RUN quasar build

# production stage
FROM python:3.12

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql \
		postgresql-client \
		nginx \
	&& rm -rf /var/lib/apt/lists/*

#COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
COPY --from=build-stage /app/dist/spa /var/www/html/

RUN rm /etc/nginx/sites-enabled/default
COPY ./deployment/demo/nginx.conf /etc/nginx/sites-enabled/
COPY ./deployment/demo/startup.sh /tmp
RUN chmod 555 /tmp/startup.sh
RUN service nginx restart

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir -p /data/media /data/static
#RUN ln -s /data/media
#RUN ln -s /data/static
COPY . .

EXPOSE 80
ENTRYPOINT [ "/tmp/startup.sh" ] 
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
