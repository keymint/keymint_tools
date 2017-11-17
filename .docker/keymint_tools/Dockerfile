FROM ubuntu:xenial

# install system dependencies
RUN apt-get update && apt-get install -y \
      git \
      python3-pip \
    && rm -rf /var/lib/apt/lists/*

# install keymint dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# setup keymint argcomplete
ENV KEYMINT_ARGCOMPLETE /usr/local/share/keymint_cli/environment/keymint-argcomplete.bash
RUN echo 'source ${KEYMINT_ARGCOMPLETE}' >> ~/.bashrc

# setup keymint workspace
ENV KEYMINT_WS /root/keymint_ws
RUN mkdir -p $KEYMINT_WS
WORKDIR $KEYMINT_WS
