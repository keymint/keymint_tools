FROM ubuntu:xenial

# install system dependencies
RUN apt-get update -qq && apt-get install -qq -y \
      git \
      python3-pip \
    && rm -rf /var/lib/apt/lists/*

# install M2Crypto dependencies
RUN apt-get update -qq && apt-get install -qq -y \
      build-essential \
      python3-dev \
      libssl-dev \
      swig \
    && rm -rf /var/lib/apt/lists/*

# install keymint dependencies
COPY dependency_requirements.txt .
RUN pip3 install -r dependency_requirements.txt

# install keymint source
COPY source_requirements.txt .
RUN pip3 install -r dependency_source.txt

# setup keymint argcomplete
ENV KEYMINT_ARGCOMPLETE /usr/local/share/keymint_cli/environment/keymint-argcomplete.bash
RUN echo 'source ${KEYMINT_ARGCOMPLETE}' >> ~/.bashrc

# setup keymint workspace
ENV KEYMINT_WS /root/keymint_ws
RUN mkdir -p $KEYMINT_WS
WORKDIR $KEYMINT_WS
