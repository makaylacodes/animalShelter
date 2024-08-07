# Dockerfile for animalShelter
# Author: Makayla Anderson-Tucker

# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Create app directory
# WORKDIR /usr , if next line doesnt work
WORKDIR /animalShelter

# Bundle app source
COPY . .

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 3000 outside container
EXPOSE 3000

# Command used to start application 
CMD ["python", "animalShelter"]
