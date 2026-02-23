FROM node:18-alpine

WORKDIR /app

# Copier les fichiers de dependances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code
COPY . .

# Build
RUN npm run build

# Exposer le port
EXPOSE 3000

# Lancer l'application
CMD ["npm", "start"]
