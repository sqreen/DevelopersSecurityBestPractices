FROM ubuntu:latest
MAINTAINER boris@sqreen.io

# Install john the ripper
RUN apt-get -y update && apt-get -y install gcc build-essential libssl-dev john git-core
RUN rm `which john`
RUN git clone git://github.com/magnumripper/JohnTheRipper -b bleeding-jumbo john
RUN cd john/src && ./configure && make -s clean && make -sj4
RUN /john/run/john --test=0
ENV PATH /john/run:$PATH
ADD ./john.ini /john.ini
ADD ./password.list /password.list

# Install enough python to generate passwords
RUN apt-get -y update && apt-get -y install python python-pip
RUN pip install -U pip
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD generate_data.py /
