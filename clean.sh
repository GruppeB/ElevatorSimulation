#!/bin/bash

rm -f data/*.data
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
