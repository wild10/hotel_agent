# this is an mcp client that use google map mpc server.
from mcp.client.fastmcp import MCPClient

client = MCPClient(
    host="http://localhost",
    port=8000
)

# client.find_nearby_restaurants("1600 Amphitheatre Parkway, Mountain View, CA")
mpc_tools = client.tools()

