#!/bin/bash

pdm install

eval "$(pdm --pep582)"

tail -f /dev/null