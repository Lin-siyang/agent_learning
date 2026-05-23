from mcp import StdioServerParameters, stdio_client, ClientSession
from mcp.server.fastmcp import tools

from calculatorMCPServer import subtract

server_params = StdioServerParameters (
    #服务器执行的命令，这里是python
    command = "python",
    #启动命令的附加参数，这里是运行example_server.py
    args=["calculatorMCPServer.py"],
    #环境变量，默认为None,表示使用当前环境变量
    env=None
)


async def run():
    #创建与服务器的标准输入输出连接，并返回read和write流
    async with stdio_client(server_params) as (read, write):
        #创建一个客户端会话对象，通过read和write流于服务器进行通信交互
        async with ClientSession(read, write) as session:
            #向服务器发送初始化请求，确保连接准备就绪
            #建立初始状态，并让服务器返回其功能和版本信息
            capabilities = await session.initialize()
            print(f"Supported capabilities:{capabilities.capabilities}/n/n")

            tools = await session.list_tools()
            print(f"Supported tools:{tools}/n/n")

            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(str(tools))


            #文件相关功能测试
            add_result=await session.call_tool("add", arguments={"a": 6, "b": 3})
            subtract_result=await session.call_tool("subtract", arguments={"a": 6, "b": 3})
            multiply_result=await session.call_tool("multiply", arguments={"a": 6, "b": 3})
            divide_result=await session.call_tool("divide", arguments={"a": 6, "b": 3})
            print(f"add_result:{add_result}/n/n")
            print(f"subtract_result:{subtract_result}/n/n")
            print(f"multiply_result:{multiply_result}/n/n")
            print(f"divide_result:{divide_result}/n/n")




