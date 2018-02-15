#!/bin/bash

# WS=${HOME}/ws/docker/keymint
# mkdir -p ${WS}
#
# IMAGE="keymint/keymint_tools"

USER_UID=$(id -u)
USER_GID=$(id -g)

# do we need to use sudo to start docker containers?
( id -Gn | grep -q docker ) || SUDO=sudo

DOCKER_CLI="docker"

prepare_docker_user_parameters() {
  USER_SET=" --user=${USER_UID}:${USER_UID}"
}

prepare_docker_env_parameters() {
  ENV_VARS+=""
  ENV_VARS+=" --env=USER_UID=${USER_UID}"
  ENV_VARS+=" --env=USER_GID=${USER_GID}"
  ENV_VARS+=" --env=TZ=$(date +%Z)"
  ENV_VARS+=" --env=LANG=C.UTF-8"
  ENV_VARS+=" --env=LC_ALL=C"
}

prepare_docker_volume_parameters() {

  VOLUMES+=""
  VOLUMES+=" --volume=${WS}:${WS}"
  VOLUMES+=" --volume=/run/user/${USER_UID}/pulse:/run/pulse"
  VOLUMES+=" --volume=/etc/group:/etc/group:ro"
  VOLUMES+=" --volume=/etc/passwd:/etc/passwd:ro"
  VOLUMES+=" --volume=/etc/shadow:/etc/shadow:ro"
  VOLUMES+=" --volume=/etc/sudoers.d:/etc/sudoers.d:ro"
}

prepare_docker_network_parameters() {
  NETWORKS+=""
  NETWORKS+=" --net=host"
}

prepare_docker_miscellaneous_parameters() {
  MISCELLANEOUS+=""
  MISCELLANEOUS+=" --interactive"
  MISCELLANEOUS+=" --tty"
  MISCELLANEOUS+=" --workdir=${HOME}"
}

prepare_docker_user_parameters
prepare_docker_env_parameters
prepare_docker_volume_parameters
prepare_docker_network_parameters
prepare_docker_miscellaneous_parameters

echo "Starting ${prog}..."
${SUDO} ${DOCKER_CLI} run \
  ${MISCELLANEOUS} \
  ${USER_SET} \
  ${ENV_VARS} \
  ${VOLUMES} \
  ${NETWORKS} \
  ${IMAGE} $@
