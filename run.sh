#!/bin/bash

# Start the nodes in the background
python src/reki_agent/nodes.py &
NODES_PID=$!

# Start the load balancer in the background
python src/reki_agent/main.py &
MAIN_PID=$!

# Wait for the servers to start
sleep 5

# Run the k6 script
k6 run k6_script.js

# Kill the background processes
kill $NODES_PID
kill $MAIN_PID
