FROM ubuntu:20.04

# So we dont have to interactivly configure tzdata
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install \
      build-essential \
      curl \
      bzip2 \
      ca-certificates \
      libglib2.0-0 \
      libxext6 \
      libsm6 \
      libxrender1 \
      git
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get clean

COPY mmseqs.tar.gz /
RUN tar -zxvf mmseqs.tar.gz && rm -f mmseqs.tar.gz
RUN chmod +x /mmseqs/bin/*

ENV PATH="/mmseqs/bin:$PATH"

