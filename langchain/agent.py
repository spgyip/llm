import requests
import bs4
import langchain.tools
import langchain.prompts
import langchain.chat_models
import langchain.chains
import langchain.agents

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
}

def parse_html(content) -> str:
    soup = bs4.BeautifulSoup(content, "html.parser")
    text_content_with_link = soup.get_text()
    return text_content_with_link

def fetch_web_page(url: str) -> str:
    print("===============RUN fetch_web_page")
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)

ddg_search = langchain.tools.DuckDuckGoSearchResults()

web_fetch_tool = langchain.tools.Tool.from_function(
                    func=fetch_web_page,
                    name="WebFetcher",
                    description="Fetch content of a web page"
                )

prompt_template = "Summarize the following content: {content}"
llm = langchain.chat_models.ChatOpenAI(
        #base_url="http://localhost:1234/v1", 
        model="gpt-3.5-turbo-16k",
        #model="gpt-3.5-turbo-1106",
      )
llm_chain = langchain.chains.LLMChain(
            llm=llm, 
            prompt=langchain.prompts.PromptTemplate.from_template(prompt_template)
        )

summarize_tool = langchain.tools.Tool.from_function(
            func=llm_chain.run,
            name="Summarizer",
            description="Summarize a web page"
        )

tools = [ddg_search, web_fetch_tool, summarize_tool]

agent = langchain.agents.initialize_agent(
            tools=tools,
            #agent_type=langchain.agents.AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent_type=langchain.agents.AgentType.OPENAI_FUNCTIONS,
            llm=llm,
            verbose=True
        )

prompt = "Research how to use the requests library in Python. Use your tools to search and summarize content into a guide on how to use the requests library."
print(agent.run(prompt))




