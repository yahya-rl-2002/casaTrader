# Multi-stage build pour optimiser la taille de l'image

# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copier les fichiers de dépendances (depuis la racine du projet)
COPY package*.json ./
COPY vite.config.ts tsconfig*.json ./
COPY postcss.config.js tailwind.config.ts ./

# Installer les dépendances
RUN npm ci

# Copier le code source
COPY src ./src
COPY public ./public
COPY index.html .

# Build
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copier les fichiers buildés
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration Nginx
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
