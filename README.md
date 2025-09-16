# AI-Powered Load Balancer

This project implements an intelligent load balancer that uses AI agents to dynamically distribute incoming traffic across a set of backend nodes. The agents, built with `crewai` and `xai-sdk`, analyze the current traffic and node health to make smart routing decisions.

## Features

- **Intelligent Traffic Distribution:** Uses AI agents to decide the best node for each request.
- **Node Health Monitoring:** Actively checks the status of each backend node.
- **Scalable Agent-based Architecture:** Built with `crewai` for a modular and extensible agent design.
- **Load Testing:** Includes a `k6` script to simulate traffic and test the load balancer's performance.

## Getting Started

### Prerequisites

- Python 3.10+
- [k6](https://k6.io/docs/getting-started/installation/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd load_ai2
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your XAI API key:**
   - Create a `.env` file in the root directory.
   - Add your XAI API key to the `.env` file:
     ```
     XAI_API_KEY="your-api-key"
     ```

## Usage

1. **Start the backend nodes and the load balancer:**
   ```bash
   ./run.sh
   ```
   This will:
   - Start the backend nodes on ports 8001-8005.
   - Start the main load balancer on port 8000.
   - Run a k6 load test.

2. **Send requests to the load balancer:**
   You can use the provided `k6_script.js` or send your own requests to `http://localhost:8000/`.

## Load Testing

The `k6_script.js` file is configured to simulate a load test with the following stages:

- **Ramp-up:** 100 virtual users over 1 minute.
- **Sustain:** 100 virtual users for 3 minutes.
- **Ramp-down:** 0 virtual users over 1 minute.

To run the load test, simply execute the `run.sh` script.
