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
# copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
# run front end thru nginx
CMD ["nginx", "-g", "daemon off;"]
