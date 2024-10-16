#!/bin/bash

function find_entry_path() {
    # echo "@i@ --> find dir: ${0}"
    this_script_dir=$( dirname -- "$0"; )
    pwd_dir=$( pwd; )
    if [ "${this_script_dir:0:1}" = "/" ]
    then
        # echo "get absolute path ${this_script_dir}" > /dev/tty
        entry_path=${this_script_dir}""
    else
        # echo "get relative path ${this_script_dir}" > /dev/tty
        entry_path=${pwd_dir}"/"${this_script_dir}
    fi
    echo "${entry_path}"
}

ENTRY_PATH=$( find_entry_path )
# echo "ENTRY_PATH: ${ENTRY_PATH}"
# echo "input command line: $@"
# python3 ${ENTRY_PATH}/wolfes_cg_main.py "$@"

### calling example
INPUT_ARGS="--input ~/tmp/cg/input.json"
OUTPUT_ARGS="--output ~/tmp/cg"
LOG_LEVEL="--loglevel 10"
python3 ${ENTRY_PATH}/wolfes_cg_main.py ${INPUT_ARGS} ${OUTPUT_ARGS} ${LOG_LEVEL}
