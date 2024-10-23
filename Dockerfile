FROM node:20-alpine

WORKDIR /usr/app/

COPY ./package.json ./package-lock.json ./
COPY ./gulpfile.js ./
COPY ./src ./src

RUN mkdir -p ./static

RUN npm ci