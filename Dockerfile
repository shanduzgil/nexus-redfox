FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --no-cache-dir --no-deps .
USER 10001
EXPOSE 8765
ENTRYPOINT ["nexus"]
CMD ["serve","/app","--host","0.0.0.0"]
