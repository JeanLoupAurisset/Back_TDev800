# syntax=docker/dockerfile:1
FROM ubuntu:18.04
RUN apt-get update 
RUN apt-get install -y postgresql
# RUN apt-get install -y screen
RUN apt-get install -y python3-pip
RUN apt-get install -y python-psycopg2
RUN apt-get install -y libpq-dev
# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``
# Django rest install
RUN mkdir BackEnd
RUN cd BackEnd 
COPY . .
RUN pip3 install psycopg2
RUN pip3 install django
RUN pip3 install djangorestframework

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/10/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/10/main/postgresql.conf

# Expose the DjangoRest port
EXPOSE 8000

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/10/bin/postgres", "-D", "/var/lib/postgresql/10/main", "-c", "config_file=/etc/postgresql/10/main/postgresql.conf"]
CMD ["python3", "BackEnd/manage.py", "migrate"]
CMD ["python3", "BackEnd/manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
