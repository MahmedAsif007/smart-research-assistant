#mcp_server.py
from mcp.server.fastmcp import FastMCP
from datetime import date
 
mcp = FastMCP("ResearchTools")
 
 
@mcp.tool()
def calculator(expression: str) -> str:
    """Evaluate a simple math expression. Example: 120 * 0.85"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
 
 
@mcp.tool()
def get_current_date() -> str:
    """Return today's date"""
    return str(date.today())
 
 
if __name__ == "__main__":
    mcp.run(transport="stdio")