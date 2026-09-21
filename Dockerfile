FROM python:3.12-slim

#set working dir 

WORKDIR /app

#copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy rest of application
COPY . .

#expose the appilication port
EXPOSE 8000

#run command
CMD [ "uvicorn" , "app:app" , "--host" ,"0.0.0.0" ,"--port" , "8000" ]
