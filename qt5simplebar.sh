#!/bin/bash

thisdir=$(dirname "$0")
cd $thisdir
python3 qt5simplebar.py &
cd $HOME
