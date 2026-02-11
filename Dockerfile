# Multi-stage build for production
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Development stage
FROM base AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Production builder
FROM base AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production runner
FROM base AS production
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 bizbot

# Copy necessary files
COPY --from=deps --chown=bizbot:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=bizbot:nodejs /app/src ./src
COPY --from=builder --chown=bizbot:nodejs /app/package*.json ./

USER bizbot

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["npm", "start"]
