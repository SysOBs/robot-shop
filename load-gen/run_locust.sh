#!/bin/bash
locust -f robot-shop.py --host http://194.210.120.176:31167 --headless -u 1 -r 1
