#!/bin/bash

while true; do
    python3 product_getter.py
    if [ $? -eq 0 ]; then
        break
    fi
    echo "product_getter.py failed, retrying..."
    sleep 1
done