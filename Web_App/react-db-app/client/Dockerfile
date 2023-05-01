# Use an official Node.js runtime as a parent image
FROM node:14-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to /app
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the app files to /app
COPY . .

# Build the client code
RUN npm run build

# Expose port 3000 for the client
EXPOSE 3000

# Start the client server
CMD ["npm", "start"]
