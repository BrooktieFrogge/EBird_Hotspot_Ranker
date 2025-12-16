# build stage
# node base image
FROM node:22-alpine as build-stage
# set work dir
WORKDIR /app
# copy package files
COPY package*.json ./
# install dependencies
RUN npm install
# copy source files to work dir
COPY . .
# build app
RUN npm run build

# prod stage
# nginx base image (proxy manager)
FROM nginx:alpine as production-stage
# copy built front end to nginx so it can serve the pages
COPY --from=build-stage /app/dist /usr/share/nginx/html
# copy nginx config template
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
# copy static nginx for local docker-compose use
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
# default backend host for local docker-compose 
ENV BACKEND_HOST=server:8000
# for render: need to add https://
# for local: we use http://server:8000
# this script handles both cases
CMD ["/bin/sh", "-c", "if echo $BACKEND_HOST | grep -q 'onrender.com'; then export BACKEND_URL=https://$BACKEND_HOST; else export BACKEND_URL=http://$BACKEND_HOST; fi && envsubst '${BACKEND_URL} ${BACKEND_HOST}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
