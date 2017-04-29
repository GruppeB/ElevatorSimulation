#!/bin/bash

rm -f data/*.data
rm -f arrivaldata/*.txt
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
