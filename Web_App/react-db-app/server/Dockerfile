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

# Expose port 4000 for the server
EXPOSE 4000

# Start the server when the container starts
CMD ["npm", "start"]
