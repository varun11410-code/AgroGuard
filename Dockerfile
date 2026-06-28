FROM python:3.11-slim

# Install system dependencies for OpenCV and other ML tools
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user named "user" with user ID 1000
# (Hugging Face Spaces requires this for security)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy requirements first to leverage Docker cache
COPY --chown=user backend/requirements.txt .

# Install Python dependencies
# (We upgrade pip, setuptools, and wheel first to ensure ML packages build correctly)
RUN pip install --no-cache-dir -U pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files
COPY --chown=user backend/ .

# Expose port 7860 (Hugging Face Spaces default port)
EXPOSE 7860

# Run database migrations and start the Gunicorn server
CMD flask db upgrade && gunicorn run:app --workers 2 --threads 4 --timeout 120 --bind 0.0.0.0:7860
