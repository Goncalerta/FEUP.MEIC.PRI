# syntax=docker/dockerfile:1
FROM node:16.13.1-alpine3.15
WORKDIR /app/frontend
COPY ./src /app/frontend/src
COPY ./public /app/frontend/public
COPY ./package-lock.json /app/frontend/package-lock.json
COPY ./package.json /app/frontend/package.json
COPY ./.eslintrc.json /app/frontend/.eslintrc.json
COPY ./.prettierrc.json /app/frontend/.prettierrc.json
COPY ./jsconfig.json /app/frontend/jsconfig.json
RUN npm ci
