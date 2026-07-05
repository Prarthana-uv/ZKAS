FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD npm run health || exit 1

# Run application
CMD ["npm", "start"]
