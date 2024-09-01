#!/bin/sh
export TESTING=true

exec pytest --cov-report=xml
