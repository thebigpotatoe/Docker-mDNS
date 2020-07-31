# Import a python alpine image
FROM python:3.8-alpine

# Install python-zeroconf
RUN pip install zeroconf

# Copy across main python file
WORKDIR /
RUN mkdir /data
COPY app/* /app/
RUN chmod +x /app/mdns.py

# Run main file 
ENTRYPOINT ["python", "/app/mdns.py"]