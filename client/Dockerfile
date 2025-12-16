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
# Default backend URL for local docker-compose (overridden by Render env var)
ENV BACKEND_URL=http://server:8000
# Use envsubst to substitute environment variable, then start nginx
CMD ["/bin/sh", "-c", "envsubst '${BACKEND_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
