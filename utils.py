import os

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Due to the network, function of getting extra information from Wikipedia cannot use
#from langchain_community.utilities import WikipediaAPIWrapper

# Only if title == 'Sora模型'
WIKI_INFO = """
Sora是一个能以文本描述生成视频的人工智能模型，由美国人工智能研究机构OpenAI开发。

Sora这一名称源于日文“空”（そら sora），即天空之意，以示其无限的创造潜力。其背后的技术是在OpenAI的文本到图像生成模型DALL-E基础上开发而成的。模型的训练数据既包含公开可用的视频，也包括了专为训练目的而获授权的著作权视频，但OpenAI没有公开训练数据的具体数量与确切来源。

OpenAI于2024年2月15日向公众展示了由Sora生成的多个高清视频，称该模型能够生成长达一分钟的视频。同时，OpenAI也承认了该技术的一些缺点，包括在模拟复杂物理现象方面的困难。《麻省理工科技评论》的报道称演示视频令人印象深刻，但指出它们可能是经精心挑选的，并不一定能代表Sora生成视频的普遍水准。

由于担心Sora可能被滥用，OpenAI表示目前没有计划向公众发布该模型，而是给予小部分研究人员有限的访问权限，以理解模型的潜在危害。Sora生成的视频带有C2PA元数据标签，以表示它们是由人工智能模型生成的。OpenAI还与一小群创意专业人士分享了Sora，以获取对其实用性的反馈。
"""

def generate_script(subject, temperature, time, api_keys, base_url=""):
    title_prompt = ChatPromptTemplate.from_messages([
        ("human", "请你以{title}为关键词，想出一个短视频的标题，不超过10个字")
    ])

    text = """你是一位短视频博主，现在需要你根据以下内容，为你的短视频频道生成一份短视频脚本。
    视频标题：{title}，视频时长：{time}分钟。生成的脚本长度请尽可能遵循视频时长。
    内容上，请按照【开头、中间、结尾】分隔，开头尽可能吸引观众的注意力，中间提供干货，结尾尽可能有惊喜。
    整体风格偏科普，氛围上以轻松为主，主要观众为年轻群体。
    """
    if subject == 'Sora模型':
        text += """
        你可以使用以下维基百科查询结果中的内容作为参考，但请仅参考相关的部分'''{wiki_info}'''"""
    video_prompt = ChatPromptTemplate.from_messages([
        ("human", text)
    ])

    if base_url:
        client = ChatOpenAI(temperature=temperature, openai_api_key=api_keys, openai_api_base=base_url)
    else:
        client = ChatOpenAI(temperature=temperature, openai_api_key=api_keys)

    title_chain = title_prompt | client
    video_chain = video_prompt | client

    title = title_chain.invoke({"title": subject}).content

    # Due to network, function of getting extra info from Wikipedia cannot use
    #search = WikipediaAPIWrapper(lang='zh')
    #search_result = search.run(subject)

    if subject == 'Sora模型':
        script = video_chain.invoke({
            "title": title,
            "time": time,
            "wiki_info": WIKI_INFO
        })
    else:
        script = video_chain.invoke({
            "title": title,
            "time": time
        })

    return title, script.content

if __name__ == '__main__':
    result = generate_script('Sora模型', 0.7, 1, os.getenv("OPENAI_API_KEY"))
    print(result)

