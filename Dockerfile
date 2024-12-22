# Step 1: Use an official Python runtime as a base image
FROM python:3.8-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file to the container
COPY requirements.txt /app/

# Step 4: Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . /app/

# Step 6: Expose port 8000 for FastAPI (default port)
EXPOSE 8000

# Step 7: Set the default command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
