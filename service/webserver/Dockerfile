# Use the nginx:1.24.0-perl base image
FROM nginx:1.24.0-perl

# Set the working directory
WORKDIR /etc/nginx

# Create sites-available and sites-enabled directories
RUN mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled

# Copy the Nginx configuration files
COPY myproject.conf /etc/nginx/sites-available/myproject.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Link the configuration file to the sites-enabled directory
RUN ln -s /etc/nginx/sites-available/myproject.conf /etc/nginx/sites-enabled/

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
