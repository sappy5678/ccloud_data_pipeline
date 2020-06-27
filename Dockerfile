# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8-slim

# Copy local code to the container image.
COPY . ./ccloud


ENV APP_HOME ccloud
WORKDIR $APP_HOME/.


# Install production dependencies.
# RUN apt-get update
# RUN apt-get install ping
# RUN echo $(ping 8.8.8.8 -c 3 )
# RUN echo $(ping google.com -c 3 )
# RUN echo $(ls -lha )

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements
RUN python -m spacy download en_core_web_md && python -m spacy download en_core_web_sm
RUN apt-get update && apt-get install -y openssh-client
# RUN apt-get update
# RUN cd /var/lib/dpkg/
#RUN mv /var/lib/dpkg/info/ /var/lib/dpkg/info.bak
#RUN mkdir /var/lib/dpkg/info/
#RUN ls /var/lib/dpkg
#RUN apt-get update
#RUN apt-get -f install
#RUN ls /var/lib/dpkg/
#RUN mv /var/lib/dpkg/info/* /var/lib/dpkg/info.bak/
#RUN rm -rf /var/lib/dpkg/info
#RUN mv /var/lib/dpkg/info.bak /var/lib/dpkg/info
# RUN apt-get update && \
#     apt-get install -y openjdk-11-jdk && \
#     apt-get install -y ant && \
#     apt-get clean
# RUN apt-get update && \
#     aot-get install ca-certificates-java && \
#     apt-get clean && \
#     update-ca-certificates -f
RUN apt-get update
RUN mkdir -p /usr/share/man/man1
# ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
# RUN export JAVA_HOME

RUN apt-get install -y default-jre
RUN apt-get install -y default-jdk
# RUN java --version
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
RUN chmod +x run.sh
CMD ["./run.sh"]
# ENTRYPOINT ["run.sh"]

