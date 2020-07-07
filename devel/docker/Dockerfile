FROM python:3.8.3-slim-buster
WORKDIR /usr/src/app
RUN apt-get update && \
apt-get install -y enchant git make nano && \
git clone https://github.com/Valparaiso-Data-Science/general-course-relevance-discovery && cd general-course-relevance-discovery && make setup \
