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
#C0MD [ "npm", "start" ]

FROM node:18
WORKDIR /app
# Copy package.json and package-lock.json for backend dependencies
COPY ./backend/package.json ./backend/package-lock.json ./
# Copy the backend source code into the container
COPY ./backend /app
RUN npm install
EXPOSE 5000
CMD ["node", "app.js"]