# Pulling from base docker image
FROM continuumio/anaconda3:2021.11

# Install apt packages
RUN apt-get update \
    && apt-get install -y \
    unzip \
    vim 

# Setting up filesystem
RUN mkdir -p /assemble \
    && mkdir -p /assemble/input \
    && mkdir -p /assemble/output \
    && mkdir -p /assemble/checkv-db-v1.5 \
    && mkdir -p /assemble/build \
    && mkdir -p /assemble/bin

# Setting up software
WORKDIR /assemble/build
RUN wget http://cab.spbu.ru/files/release3.15.4/SPAdes-3.15.4-Linux.tar.gz \
    && tar -xzf SPAdes-3.15.4-Linux.tar.gz \
    && rm SPAdes-3.15.4-Linux.tar.gz

ENV PATH="/assemble/build/SPAdes-3.15.4-Linux/bin:${PATH}"

# Building environments and inputting script
COPY ./assemble.txt /assemble/build
RUN conda create --name assemble --file /assemble/build/assemble.txt \
    && conda init bash
RUN echo "conda activate" >> ~/.bashrc

# Adding scripts
COPY ./docker_lib/* /assemble/bin/
RUN echo 'export PATH="/assemble/bin:$PATH"' >> ~/.bashrc

# Copying database over
COPY ./database/checkv-db-v1.5 /assemble/checkv-db-v1.5/

# Setting entry
WORKDIR /assemble
CMD [ "echo avengers assemble" ]
