FROM node:19

RUN useradd user -rm
USER user

WORKDIR /usr/src/app

COPY . .
RUN npm ci

CMD [ "node", "index.js" ]