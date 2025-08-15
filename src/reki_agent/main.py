import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import xai_sdk

load_dotenv()

# Groq API setup
client = xai_sdk.Client()

# Node configuration
NODE_PORTS = [8001, 8002, 8003, 8004, 8005]

# Agent 1: Traffic Handler
def handle_traffic(request_data):
    # For simulation, we just pass the data through
    return request_data

# Agent 2: Node Status Checker
def check_node_status():
    node_statuses = {}
    for port in NODE_PORTS:
        try:
            response = requests.get(f'http://localhost:{port}/status', timeout=0.1)
            if response.status_code == 200:
                node_statuses[port] = response.json()['load']
            else:
                node_statuses[port] = 'unresponsive'
        except requests.exceptions.RequestException:
            node_statuses[port] = 'offline'
    return node_statuses

# Agent 3: XAI Recommender
def get_xai_recommendation(traffic_info, node_status):
    prompt = f"Given the current traffic: {traffic_info} and node statuses: {node_status}, which node should handle the request? Respond with the port number only."
    
    response = client.chat.create(
        model="grok-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content


# Agent 4: Execution Agent
def route_traffic(request_data, recommended_node):
    try:
        port = int(recommended_node)
        if port in NODE_PORTS:
            response = requests.post(f'http://localhost:{port}', json=request_data)
            return response.json()
        else:
            return {"error": "Invalid node recommended"}
    except (ValueError, requests.exceptions.RequestException) as e:
        return {"error": str(e)}

# CrewAI Setup
traffic_handler_agent = Agent(
    role='Traffic Handler',
    goal='Receive incoming traffic and pass it on for processing.',
    backstory='An efficient agent that sits at the entry point of the system.',
    verbose=True,
    allow_delegation=False,
    llm=client
)

node_status_agent = Agent(
    role='Node Status Checker',
    goal='Check the current status and load of all available nodes.',
    backstory='A vigilant agent that constantly monitors the health of the system.',
    verbose=True,
    allow_delegation=False,
    llm=client
)

groq_recommender_agent = Agent(
    role='Groq Recommender',
    goal='Get a recommendation from Groq on where to route the traffic.',
    backstory='A smart agent that leverages the power of Groq to make intelligent decisions.',
    verbose=True,
    allow_delegation=False,
    llm=client
)

execution_agent = Agent(
    role='Execution Agent',
    goal='Route the traffic to the node recommended by xai.',
    backstory='A reliable agent that executes the final decision.',
    verbose=True,
    allow_delegation=False,
    llm=client
)

class LoadBalancerHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)

        # Create tasks
        handle_traffic_task = Task(
            description=f'Handle incoming request: {request_data}',
            agent=traffic_handler_agent,
            expected_output="The request data as a dictionary."
        )

        check_status_task = Task(
            description='Check the status of all nodes.',
            agent=node_status_agent,
            expected_output="A dictionary of node statuses."
        )

        get_recommendation_task = Task(
            description='Get a routing recommendation from xai.',
            agent=groq_recommender_agent,
            expected_output="The recommended node port number."
        )

        route_traffic_task = Task(
            description='Route the traffic to the recommended node.',
            agent=execution_agent,
            expected_output="The response from the node."
        )

        # Create crew
        crew = Crew(
            agents=[traffic_handler_agent, node_status_agent, xai_recommender_agent, execution_agent],
            tasks=[handle_traffic_task, check_status_task, get_recommendation_task, route_traffic_task],
            process=Process.sequential,
            verbose=2
        )

        # Execute the crew
        result = crew.kickoff(inputs={'request_data': request_data})

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

def run_load_balancer():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, LoadBalancerHandler)
    print("Starting load balancer on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    # This main block is for running the load balancer.
    # The nodes should be started by running nodes.py in a separate terminal.
    run_load_balancer()