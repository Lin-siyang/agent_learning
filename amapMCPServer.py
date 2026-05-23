import os
import asyncio
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import SystemMessage,HumanMessage
from langchain.chat_models import init_chat_model
from typing import Dict,List,Any

"""
用 LangGraph + LangChain + MCP 工具，搭一个“会调用高德地图工具的 ReAct 智能体”。
也就是：
先初始化大模型
再连接远程 MCP Server，拿到地图相关工具
用 create_react_agent(...) 把“模型 + 工具 + 记忆 + 系统提示词”组装成 Agent
给 Agent 一个用户问题
Agent 自己判断要不要调用工具
工具返回结果后，Agent 再组织最终答案
所以这段代码已经不是“单纯调用模型”，而是在学 真正的 Agent 工作流。
LLM
Tools
Prompt
Memory
Agent
Async 异步调用
"""
#从环境变量中获取密钥key
AMAP_MAPS_API_KEY=os.getenv('AMAP_MAPS_API_KEY')
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# 初始化LLM，创建大模型对象
#model：这是模型标识 model_provider：指定模型提供商
llm=init_chat_model(
    model="deepseek-chat",
    temperature=0,
    model_provider="deepseek",
)


def parse_message(message:Dict[str,Any]) -> None:...

def save_graph_visualization(graph_visualization:Dict[str,Any]) -> None:...

#定义一个异步函数，配合await使用
async def run_agent():
    # 实例化MCP Server客户端，连接MCP Server拿到工具
    client = MultiServerMCPClient(
        {
            #高德地图MCP
            "map-sse": {
                "url":"https://mcp.amap.com/sse?key="+AMAP_MAPS_API_KEY,
                "transport":"sse",
            },
            #自定义MCP Server
            "calculator":{
                "command":"python",
                "args":["calculatorMCPServer.py"],
                "transport":"stdio",
            }
        })
    #过 client 这个 MCP 客户端，去远程拿到这个服务提供的工具列表、
    # await
    # 因为这个请求要访问网络，不会立刻返回，所以要“等待”,等远程服务返回工具后再继续
    tools=await client.get_tools()
    # print(f"tools:{tools}\n")

    #基于内存存储的short-term memory,给agent提供短期记忆
    checkpointer = InMemorySaver()

    #定义系统消息，指导如何使用工具，给模型设定身份、任务和行为规则。SystemMessage(...) 是一个类/构造方式
    system_message = SystemMessage(content="你是一个地图查询助手，请根据用户输入的查询内容，返回查询结果。")


    #创建React Agent对象 把模型和工具组装成一个agent
    # system_message系统提示给agent 你是一个地图查询助手，请根据用户输入的查询内容，返回查询结果。
    #把模型、工具、记忆、角色设定，组装成一个可工作的智能体。
    #LangGraph提供的ReAct架构的智能体，基于 LangGraph 的 MCP 架构
    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpointer,
        prompt=system_message,
    )

    #使用了checkpointer，agent需要知道线程ID
    config = {"configurable":{"thread_id":"1"}}


    # # 1.同步处理查询（非流式）
    # # invoke可以理解成“执行一次调用”
    # # ainvoke前面的a表示 async，也就是异步版，传入的是一个字典，里面包含一个messages字段，这个字段是一个列表，列表中包含一个HumanMessage对象，这个对象包含一个content字段，这个字段包含用户输入的查询内容。
    # #这行执行完后，agent_response 里保存的是 agent 的完整响应结果
    # agent_response = await agent.ainvoke({"messages": [HumanMessage(content="从青岛中国石油大学华东古镇口校区开车到唐岛湾校区怎么走，大概需要多久？")]}, config=config)
    #
    # #将返回的message进行格式化输出
    # parse_message(agent_response['messages'])
    # agent_response_content= agent_response["messages"][-1].content
    # print(f"agent_response_content:{agent_response_content}\n")#把变量插入到字符串中

    """
    async for
    因为流式输出会不断返回片段，所以要异步迭代。
    message_chunk
    每次返回的一小段消息。
    metadata
    这一段消息对应的元信息，比如来自哪个节点。
    """

    #2.流式处理查询
    async for message_chunk,metadata in agent.astream(
            input={"messages": [HumanMessage(content="现在要购买一批货，单价是1034.32423，数量是235326，商家说可以在这个基础上打95折，折后总价是多少？")]},
            config=config,
            stream_mode="messages"
    ):
        # #测试原始输出
        # print(f"Token:{message_chunk}\n")
        # print(f"Metadata:{metadata}\n")

        if metadata["langgraph_node"]=="tools":
            continue

        #输出最终结果
        if message_chunk.content:
            print(message_chunk.content,end="",flush=True)


#控制“只在直接运行当前文件时执行”，被导入时不自动执行。
if __name__ == "__main__":
    asyncio.run(run_agent())

#当你直接运行一个文件时，这个文件里的 __name__ 会被设为：__main__.所以条件成立，下面的代码就会执行。
#当这个文件被导入时，这个文件里的 __name__ 会被设为：模块名.比如"amapMCPServer"
#asyncio.run(...) 就是在做这件事：创建并启动一个事件循环，把异步函数 run_agent() 真正跑起来。异步函数加asyncio.
