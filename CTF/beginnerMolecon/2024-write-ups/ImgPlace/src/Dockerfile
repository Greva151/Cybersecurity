FROM node:22 AS installer

WORKDIR /tmp/build

COPY ./package.json .
COPY ./pnpm-lock.yaml .

RUN npm install -g pnpm
RUN pnpm install

FROM node:22-slim AS runner

WORKDIR /app

COPY --from=installer /tmp/build/node_modules/ /app/node_modules
COPY ./package.json .
COPY ./src/ ./src/
COPY ./static/ ./static
COPY ./views/ ./views

CMD [ "node", "src/server.js" ]