FROM ubuntu:16.04

MAINTAINER Yannik Behr <y.behr@gns.cri.nz>

# Can fail on occasion.
RUN apt-get update && apt-get upgrade || true
RUN apt-get -y install \
    python-pandas \
    python-matplotlib \
    git \
    wget \
 	&& apt-get clean

# Init mpl fonts
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot"

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.10.0/tini && \
    echo "1361527f39190a7338a0b434bd8c88ff7233ce7b9a4876f3315c22fce7eca1b0 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
chmod +x /usr/local/bin/tini


# Configure container startup
ENTRYPOINT ["tini", "--"]

VOLUME ["/output"]
COPY catevents.py /usr/local/bin/
COPY catevents.cfg /usr/local/bin/
WORKDIR /usr/local/bin

CMD ["/usr/bin/python", "catevents.py","catevents.cfg"]

