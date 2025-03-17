FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY matrix_rain.py /app/
COPY requirements.txt /app/
COPY setup.py /app/

# Install dependencies (though there are no external dependencies)
RUN pip install --no-cache-dir -r requirements.txt

# Install the application
RUN pip install -e .

# Make sure the terminal is interactive and supports colors
ENV TERM=xterm-256color
ENV PYTHONUNBUFFERED=1

# Run the application
ENTRYPOINT ["python", "matrix_rain.py"]
