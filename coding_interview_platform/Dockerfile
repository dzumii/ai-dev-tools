FROM node:20-alpine AS builder
WORKDIR /app

# copy server and client
COPY server ./server
COPY client ./client

# install server deps
WORKDIR /app/server
RUN npm install --production

# install client deps (http-server only)
WORKDIR /app/client
RUN npm install --production

# Final image
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/server ./server
COPY --from=builder /app/client ./client

EXPOSE 3000
# Start server which also serves client static files (client files are at /app/client)
WORKDIR /app/server
CMD ["node", "src/server.js"]
