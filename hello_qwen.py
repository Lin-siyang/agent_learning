import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
import langchain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

#
# try:
#     client = OpenAI(
#         # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
#         api_key=os.getenv("DASHSCOPE_API_KEY"),
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     )
#
#     completion = client.chat.completions.create(
#         model="qwen-plus",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
#         messages=[
#             {'role': 'system', 'content': 'You are a helpful assistant.'},
#             {'role': 'user', 'content': '你是谁？'}
#         ]
#     )
#     print(completion.choices[0].message.content)
# except Exception as e:
#     print(f"错误信息：{e}")
#     print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")



"""
使用LangChain调用
"""

llm=ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0,
    model="deepseek-chat",
)
# response=llm.invoke("介绍一下你自己")
# print(langchain.__version__)
# print(response)#AImessage对象会打印content,addtional_kwargs,tool_calls等等
# print("###############################################################")
# print(response.content)#纯文本
#



#需要注意的一点是，这里需要指明具体的role，比如system、user
# prompt=ChatPromptTemplate.from_messages( [
#     ("system", "你是世界级的技术文档编写者"),
#     ("user", "{input}"),
# ])
#
# chain=prompt | llm
# response=chain.invoke({"input":"写一首情诗"})
# print(response.content)


##################################################################
prompt=ChatPromptTemplate.from_messages( [
    ("system", "你是世界级的技术文档编写者"),
    ("user", "{input}"),
])
#使用输出解析器
output_praser=JsonOutputParser()

chain=prompt | llm | output_praser

response=chain.invoke({"input":"写一首情诗,用JSON格式回复，问题用question，回答用answer"})
print(response)

