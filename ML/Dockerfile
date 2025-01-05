#Dockerfile (Building Docker Image for app)

#Specifying base image
FROM python:3.12.1

#Set ENV vars
# Set environment variables using the recommended format
ENV APP_HOME=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

#Set working directory and Copy local code to image
WORKDIR $APP_HOME 
COPY . $APP_HOME

RUN ls $APP_HOME/Data

#Update pip and Install necassary dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

#Command to run app 
CMD ["sh", "-c", "gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 0 app:app"]
