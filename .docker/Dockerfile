FROM ubuntu:20.04

MAINTAINER Terradue S.r.l
USER root

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    SHELL=/bin/bash \
    PATH=/srv/conda/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive \
    NB_USER=jovyan \
    NB_UID=1002 \
    NB_GID=1002

    
ENV USER=${NB_USER} \ 
    HOME=/home/${NB_USER}
    
RUN groupadd --gid ${NB_GID} ${NB_USER}                                                                                             && \
    useradd --comment "Default user" --create-home --gid ${NB_GID} --no-log-init --shell /bin/bash --uid ${NB_UID} ${NB_USER}       && \
    apt-get -qq update                                                                                                              && \
    apt-get -qq install --yes apt-utils                                                                                             && \
    apt-get -qq install --yes --no-install-recommends ttf-dejavu wget make g++ sudo vim less unzip tree file  locales > /dev/null   && \
    apt-get -qq purge                                                                                                               && \
    apt-get -qq clean                                                                                                               && \
    rm -rf /var/lib/apt/lists/*                                                                                                     && \
    echo "LC_ALL=en_US.UTF-8" >> /etc/environment                                                                                   && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen                                                                                     && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf                                                                                      && \
    locale-gen en_US.UTF-8

ENV APP_BASE=/srv \
    CONDA_DIR=/srv/conda 

# conda installation via miniforge
ADD .docker/install-miniforge.bash /tmp/install-miniforge.bash

RUN chmod 755 /tmp/install-miniforge.bash                                                                                           && \
    /tmp/install-miniforge.bash                                                                                                     && \
    rm -f /tmp/install-*.bash                                                                                                       && \
    chown -R $NB_USER:$NB_GID ${HOME} 

USER ${NB_USER}

ENV NB_PYTHON_PREFIX=${CONDA_DIR}/envs/env_sar_calibration 

ENV PATH=$NB_PYTHON_PREFIX/bin:$CONDA_DIR/bin:$PATH \
    KERNEL_PYTHON_PREFIX=${NB_PYTHON_PREFIX} \
    PREFIX=${NB_PYTHON_PREFIX}

# create the conda environment
ADD environment.yml /tmp/environment.yml

RUN mamba env create -p ${NB_PYTHON_PREFIX} -f /tmp/environment.yml                                                                 && \
    mamba clean --all -f -y                                                                                                         && \
    rm -fr /tmp/environment.yml 

# install project
COPY --chown=jovyan:100 . ${HOME}

RUN cd ${HOME}                                                                                                                      && \
    ${NB_PYTHON_PREFIX}/bin/python setup.py install

WORKDIR ${HOME}
