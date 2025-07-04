import sys
import json
import requests
import time

HTTP_BASE_URL = "http://localhost:8000"

def wait_for_server():
    """Wait for the HTTP server to be available"""
    max_retries = 30
    for i in range(max_retries):
        try:
            resp = requests.get(f"{HTTP_BASE_URL}/tools", timeout=2)
            if resp.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    return False

def main():
    print("MCP Proxy started", file=sys.stderr, flush=True)
    
    # Wait for server to be ready
    if not wait_for_server():
        print("Failed to connect to HTTP server", file=sys.stderr, flush=True)
        return
    
    try:
        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                method = request.get("method")
                request_id = request.get("id", 0)

                if method == "initialize":
                    # Handle initialization
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "outlook-email-mcp-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response), flush=True)

                elif method == "tools/list":
                    # Get tools from HTTP server and format properly
                    try:
                        resp = requests.get(f"{HTTP_BASE_URL}/tools?id={request_id}", timeout=5)
                        if resp.status_code == 200:
                            server_response = resp.json()
                            # Extract tools from server response and format for MCP
                            tools = server_response.get("result", {}).get("tools", [])
                            response = {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "result": {
                                    "tools": tools
                                }
                            }
                        else:
                            response = {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "error": {"code": -32000, "message": "Failed to get tools from server"}
                            }
                    except requests.exceptions.RequestException as e:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32000, "message": f"Server connection error: {str(e)}"}
                        }
                    print(json.dumps(response), flush=True)

                elif method == "tools/call":
                    # Forward tool calls to HTTP server
                    try:
                        payload = {**request["params"], "id": request_id}
                        resp = requests.post(f"{HTTP_BASE_URL}/tool_call", json=payload, timeout=30)
                        if resp.status_code == 200:
                            response_data = resp.json()
                        else:
                            response_data = {
                                "jsonrpc": "2.0",
                                "id": request_id,
                                "error": {"code": -32000, "message": f"HTTP {resp.status_code}: {resp.text}"}
                            }
                    except requests.exceptions.RequestException as e:
                        response_data = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {"code": -32000, "message": f"Request failed: {str(e)}"}
                        }
                    print(json.dumps(response_data), flush=True)

                elif method == "resources/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "resources": []
                        }
                    }
                    print(json.dumps(response), flush=True)

                elif method == "prompts/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "prompts": []
                        }
                    }
                    print(json.dumps(response), flush=True)

                elif method == "notifications/initialized":
                    # Acknowledge without result
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {}
                    }
                    print(json.dumps(response), flush=True)

                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32601, "message": f"Method '{method}' not found"}
                    }
                    print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr, flush=True)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr, flush=True)
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id", 0) if 'request' in locals() else 0,
                    "error": {"code": -32000, "message": f"Internal error: {str(e)}"}
                }
                print(json.dumps(response), flush=True)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr, flush=True)

if __name__ == "__main__":
    main()
