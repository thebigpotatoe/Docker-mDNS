# Import a python alpine image
FROM python:3.8-alpine

# Install python-zeroconf
RUN pip install --no-cache-dir zeroconf

# Set the workdir to the app dir
WORKDIR /app

# Copy across main python file
COPY mdns.py /app/mdns.py

# Run main file 
ENTRYPOINT ["python", "/app/mdns.py"]