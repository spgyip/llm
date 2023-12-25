#from langchain.prompts import PromptTemplate
#from langchain.chat_models import ChatOpenAI
#from langchain.chains import LLMChain, SimpleSequentialChain
import langchain.prompts
import langchain.chat_models
import langchain.chains 

llm = langchain.chat_models.ChatOpenAI(base_url="http://localhost:1234/v1", model_name="local_model")

description_prompt = langchain.prompts.PromptTemplate.from_template("Write me a description for TikTok about {topic}")
description_chain = langchain.chains.LLMChain(llm=llm, prompt=description_prompt, verbose=True)
#script_prompt = langchain.prompts.PromptTemplate.from_template("Write me a script for a TikTok given the following description: {description}")
#script_chain = langchain.chains.LLMChain(llm=llm, prompt=script_prompt)

#tiktok_chain = langchain.chains.SimpleSequentialChain(chains=[description_chain, script_chain])
#script = tiktok_chain.run("Cats are cool")
#print(script)

#output = description_chain.predict(topic="Cats are cool")
output = description_chain.run(topic="Cats are cool")
print(output)
#script = script_chain.predict(description=output, verbose=True)
#print(script)

