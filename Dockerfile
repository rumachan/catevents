FROM jupyter/base-notebook:0c84b71d9f3d

MAINTAINER "Yannik Behr <y.behr@gns.cri.nz>"

USER root

ADD . /usr/local/bin

WORKDIR /usr/local/bin
# Install conda packages
RUN conda env create -f environment.yml && \
    conda clean --all -f -y

VOLUME ["/output"]

ENTRYPOINT ["conda", "run", "-n", "catevents"]
