FROM debian:bullseye-slim
RUN apt-get update && apt-get install -y keepassxc python3
WORKDIR /app
COPY ./src ./src
CMD ./src/main.py
