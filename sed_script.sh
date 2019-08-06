#!/bin/bash

sed -i "s/6669/61${HOSTNAME#*-0}/" ~/autossh.service
