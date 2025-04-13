# Use official Node.js image
#FROM node:20

# Create app directory
#WORKDIR /usr/src/app

# Copy and install dependencies
#COPY package*.json ./
#RUN npm install

# Copy source files
#COPY . .

# Expose port and start app
#EXPOSE 3000
#CMD [ "npm", "start" ]

FROM node:18
WORKDIR /app

# Copy package.json and package-lock.json first (this allows Docker to cache the dependencies)
COPY frontend/package.json frontend/package-lock.json ./

# Copy the rest of the frontend application code
COPY frontend/src ./src
COPY frontend/public ./public

RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "start"]