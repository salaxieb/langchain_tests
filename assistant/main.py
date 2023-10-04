from langchain.llms import CTransformers
# from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.agents.agent_toolkits import GmailToolkit
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.agents import initialize_agent, AgentType
from langchain.chains.summarize import load_summarize_chain

from langchain.chat_models import ChatOpenAI



if __name__ == '__main__':
    llama_llm = CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML", model_file = 'llama-2-7b-chat.ggmlv3.q2_K.bin', callbacks=[StreamingStdOutCallbackHandler()])
    chat_gpt_llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')


    template = """[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
Your answer are brief and usually not more thatn 10 words long.
Always answer as helpfully as possible, while being safe.
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.
If you don't know the answer to a question, please don't share false information.
<</SYS>>
{text}[/INST]"""

    toolkit = GmailToolkit()

    # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
    # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
    credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="credentials.json",
    )
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    prompt = PromptTemplate(template=template, input_variables=["text"])

    # llm_chain = LLMChain(prompt=prompt, llm=llm)
    # # text = input("Write question:")
    text = "What is my conversation in my gmail with Lucy.Chan@fragomen.com is about?"
    # response = llm_chain.run(text)
    agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=chat_gpt_llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    # chain = load_summarize_chain(llm, chain_type="refine")
    # help(chain)
    agent.run(text)
    #     prompt.format(text=text)
    # )
