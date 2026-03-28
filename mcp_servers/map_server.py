## MCP Server for using google maps and api.

from mcp.server.fastmcp import FastMCP

# create the mcp server
mcp = FastMCP()

@mcp.tool
def find_nearby_restaurants(location:str):
    return [
        {"name": "Luigi's Bistro", "distance": "100m", "rating": "4.5"},
        {"name": "Pasta Palace", "distance": "200m", "rating": "4.0"},
        {"name": "Pizza Place", "distance": "300m", "rating": "3.5"},
    ]

if __name__ == "__main__":
    mcp.run()