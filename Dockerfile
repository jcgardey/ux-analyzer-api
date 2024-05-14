FROM python:3.10-slim

ENV USER=backend
ENV HOME=/usr/src/app
WORKDIR ${HOME}

RUN apt-get update \
 && apt-get install git pkg-config gcc default-libmysqlclient-dev -y --no-install-recommends

# Create a group and user
RUN addgroup --system ${USER} --gid 1000 && adduser -u 1000 --gid 1000 --system ${USER} 
RUN usermod -aG sudo ${USER}


COPY ./backend/ux_analyzer/* ${HOME}

RUN pip install -r requirements.txt
RUN chown -R ${USER}:${USER} /usr/src/app
USER ${USER} 

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 