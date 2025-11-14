# Stage 1: build Angular application
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies first to leverage layer caching
COPY package*.json ./
RUN npm ci

# Copy the rest of the source and build
COPY . .
RUN npm run build -- --configuration production

# Stage 2: serve compiled assets with Nginx
FROM nginx:1.27-alpine AS runtime

# Copy custom Nginx configuration for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the Angular build output from the previous stage
COPY --from=build /app/dist/redum-app/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
