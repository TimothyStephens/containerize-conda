#!/usr/bin/env bash

## Hard values
VERSION="0.2"
SIF_DIR="/scratch/singularity"
SINGULARITY_DEFAULT_ARGS="--no-home --bind /scratch:/scratch"


## Pre-run setup
set -euo pipefail
IFS=$'\n\t'

# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")

## Path to SIF files
SIF_DIR="/scratch/singularity"


## Useage information
usage() {
echo -e "
##
## Load containerize conda programs (v${VERSION})
##

Usage: 
## List all available conda programs 
$(basename $0) list

## List this help message
$(basename $0) help
## List help for a given program
$(basename $0) help program_name
  program_name     Name of program to get help for (shown by 'list')

## Run program
$(basename $0) run program_name program_command
  program_name     Name of program to run (shown by 'list')
  program_command  Commands of program that you are running (see 'help program_name' for an example of how this is done)


## To add arguments to singularity using the SINGULARITY_ARGS env
## Default singularity arguments: \"${SINGULARITY_DEFAULT_ARGS}\"



Options (all optional):
-v, --version              Script version (v${VERSION})
-h, --help                 This help message
--debug                    Run debug mode
" 1>&2
exit 1
}


## List available programs
available_programs() {
  echo -e "\n\n"
  echo -e "####################################"
  echo -e "#### List of available programs ####"
  echo -e "####################################"
  cat "${PROGRAM_LIST}" | column -ts$'\t'
  echo -e "\n"
}


## Function to check if the profided program_name can be resolved to a SIF file
check_sif() {
if [[ ! -e "${SIF}" ]]; then
  echo -e "\n\nERROR: ${PROGRAM} is not an available program!"
  available_programs
  exit 1
fi
}


## Print ERROR message
error() {
  echo -e "\nERROR: $@\n"
  exit 1
}


## Load arguments
for key in $1 $2; do
  case $key in
    -h|--help)
      usage
      exit 1;
      ;;
    -v|--version)
      echo "v${VERSION}"
      exit 0;
      ;;
    --debug)
      set -x
      ;;
  esac
done


## Load check and load list of programs
PROGRAM_LIST="${SIF_DIR}/manifest"
if [[ ! -e "${PROGRAM_LIST}" ]]; then
  error "${SIF_DIR}/manifest missing! This script might not be configured correctly."
fi


## Check singularity
set +eu
SINGULARITY=$(which singularity)
SINGULARITY_ARGS="${SINGULARITY_DEFAULT_ARGS} ${SINGULARITY_ARGS}"
set -eu
if [[ ! -e "${SINGULARITY}" ]]; then
  error -e "Can't fine singulairty in your PATH! Can't progress without it"
fi


## Check run type
set +eu
TYPE="${1}"
shift
PROGRAM="${1}"
SIF="${SIF_DIR}/${PROGRAM}.sif"
shift
COMMAND="$@"
set -eu

if   [[ "${TYPE}" == ""     ]]; then
  usage

elif [[ "${TYPE}" == "help" ]]; then
  if [[ "${PROGRAM}" == "" ]]; then
    usage
  else
    check_sif
    "${SINGULARITY}" run-help "${SIF}"
    echo -e ""
  fi

elif [[ "${TYPE}" == "list" ]]; then
  available_programs

elif [[ "${TYPE}" == "run" ]]; then
  if [[ -z "${COMMAND}" ]]; then
    error "You didnt provide any commands for singuality! Can't progress without some commands to run"
  fi
  check_sif
  CMD="${SINGULARITY} exec $SINGULARITY_ARGS ${SIF} ${COMMAND}"
  eval $CMD

elif [[ "${TYPE}" == "update-manifest" ]]; then
  echo -e "\n## Updating sif file manifest with the following programs:"
  ls "${SIF_DIR}/"*.sif | sed -e 's/.sif//' -e "s@${SIF_DIR}/@@" | grep -v "^rstudio" > "${PROGRAM_LIST}"
  cat "${PROGRAM_LIST}"
  echo -e ""

else
  error "Unrecognized option (${TYPE}) [allowed: list,help,run]"

fi












