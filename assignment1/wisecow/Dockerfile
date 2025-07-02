# Use a minimal base image with bash and required tools
FROM debian:stable-slim

# Install dependencies
RUN apt-get update \
    && apt-get install -y cowsay fortune fortune-mod netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/games:${PATH}"

# Set working directory
WORKDIR /app

# Copy the script
COPY wisecow.sh ./

# Make the script executable
RUN chmod +x wisecow.sh

# Expose the port used by the app
EXPOSE 4499

# Run the script
CMD ["./wisecow.sh"] 