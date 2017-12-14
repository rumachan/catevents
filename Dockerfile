FROM ubuntu:16.04

MAINTAINER Yannik Behr <y.behr@gns.cri.nz>

# Can fail on occasion.
RUN apt-get update && \ 
    apt-get -y install \
    bzip2 \
    ca-certificates \
    wget \
    && apt-get clean

# Install conda and check the md5 sum provided on the download site
ENV MINICONDA_VERSION 4.3.30 
ENV CONDA_DIR /opt/conda
ENV PATH=$CONDA_DIR/envs/python2/bin:$CONDA_DIR/bin:$PATH

RUN cd /tmp && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "0b80a152332a4ce5250f3c09589c7a81 *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda config --system --prepend channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    $CONDA_DIR/bin/conda config --system --set show_channel_urls true && \
    $CONDA_DIR/bin/conda update --all --quiet --yes && \
    conda clean -tipsy

RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 \
    'matplotlib=1.5*' \
    'pandas=0.17*' && \
    conda clean -tipsy

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

CMD ["catevents.py","catevents.cfg"]

