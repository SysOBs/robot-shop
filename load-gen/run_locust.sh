#!/bin/bash
locust -f robot-shop.py --host http://194.210.120.176:32205 --headless -u 1 -r 1
