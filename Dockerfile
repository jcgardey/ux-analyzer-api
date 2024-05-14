FROM python:3.10-slim

ENV USER=backend
ENV HOME=/usr/src/app
WORKDIR ${HOME}

RUN apt-get update \
 && apt-get install git pkg-config gcc default-libmysqlclient-dev -y --no-install-recommends

# Create a group and user
RUN addgroup --system ${USER} --gid 1000 && adduser -u 1000 --gid 1000 --system ${USER} 
RUN usermod -aG sudo ${USER}

RUN git clone https://github.com/jcgardey/ux-analyzer-api.git
WORKDIR ${HOME}/ux-analyzer-api

RUN pip install -r src/requirements.txt
RUN chown -R ${USER}:${USER} /usr/src/app
RUN chmod 777 start.sh
USER ${USER} 

EXPOSE 8000
CMD ["./start.sh"] 