import logging
from asyncio import timeout
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

#创建一个MCP Server对象，命名为calculator
mcp=FastMCP("calculator")

#定义加法工具函数
@mcp.tool()
async def add(a:float,b:float) -> list[TextContent]:
    """执行加法运算
    Args:
         a:第一个数字
         b:第二个数字
    """
    result=a+b
    return [TextContent(type="text",text=str(result))]

#定义减法工具函数
@mcp.tool()
async def subtract(a:float,b:float) -> list[TextContent]:
    """执行减法运算
     Args:
         a:第一个数字
         b:第二个数字
    """
    result=a-b
    return [TextContent(type="text",text=str(result))]

#定义乘法工具函数
@mcp.tool()
async def multiply(a:float,b:float) -> list[TextContent]:
    """执行乘法运算
     Args:
         a:第一个数字
         b:第二个数字
    """
    result=a*b
    return [TextContent(type="text",text=str(result))]

#定义除法工具函数
@mcp.tool()
async def divide(a:float,b:float) -> list[TextContent]:
    """执行除法运算
     Args:
         a:第一个数字
         b:第二个数字
    """
    if b==0:
        raise ValueError("除数不能为零")
    result=a/b
    return [TextContent(type="text",text=str(result))]

if __name__ == "__main__":
    #启动MCP Server,使用标准输入输出作为传输方式
    mcp.run(transport='stdio')