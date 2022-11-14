FROM python:3.8-slim

WORKDIR /TCP_TEST_SERVER

COPY py_lib.txt .
RUN pip install --upgrade pip
RUN pip install -r py_lib.txt

COPY server.py .

EXPOSE 30000


#CMD ["python3", "./server.py", " --port 30000"]
CMD ["./server.py","--port","30000"]
