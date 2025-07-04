from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request
from server.mcp_email_server import create_email_mcp_server

mcp_app = create_email_mcp_server()

async def tools(request: Request):
    request_id = request.query_params.get("id", 0)
    
    try:
        tools_list = await mcp_app.list_tools()
        
        # Convert tools to proper MCP format
        formatted_tools = []
        for tool in tools_list:
            tool_dict = tool.model_dump() if hasattr(tool, 'model_dump') else tool
            
            # Ensure proper structure for MCP
            formatted_tool = {
                "name": tool_dict.get("name"),
                "description": tool_dict.get("description"),
                "inputSchema": tool_dict.get("inputSchema", {
                    "type": "object",
                    "properties": {},
                    "required": []
                })
            }
            formatted_tools.append(formatted_tool)
        
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": int(request_id),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "tools": formatted_tools,
                "serverInfo": {
                    "name": "outlook-email-mcp-server",
                    "version": "1.0.0"
                }
            }
        })
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": int(request_id),
            "error": {
                "code": -32000,
                "message": f"Failed to list tools: {str(e)}"
            }
        })

async def tool_call(request: Request):
    data = await request.json()
    try:
        result = await mcp_app.call_tool(
            name=data["name"], 
            arguments=data.get("arguments", data.get("input", {}))  # Handle both field names
        )
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": data.get("id", 1),
            "result": {
                "content": [  # MCP expects content array format
                    {
                        "type": "text",
                        "text": str(result)
                    }
                ]
            }
        })
    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": data.get("id", 1),
            "error": {
                "code": -32000,
                "message": f"Tool execution failed: {str(e)}"
            }
        })

tool_routes = [
    Route("/tools", tools, methods=["GET"]),
    Route("/tool_call", tool_call, methods=["POST"]),
]
