import os
import autogen
from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config, load_autogen_memgpt_agent
from memgpt.constants import LLM_MAX_TOKENS, DEFAULT_PRESET
from autogen import AssistantAgent, UserProxyAgent

# create a config for the MemGPT AutoGen agent
config_list = [
    {
        "model": "NULL",
        "base_url": "http://localhost:1234/v1",  # port 1234 for LM Studio
        "api_key": "NULL",
    },
]

# MemGPT-powered agents will also use local LLMs, but they need additional setup (also they use the Completions endpoint)
config_list_memgpt = [
    {
        "preset": DEFAULT_PRESET,
        "model": None,
        "model_wrapper": "chatml" , #"airoboros-l2-70b-2.1"
        "model_endpoint_type": "lmstudio",
        "model_endpoint": "http://localhost:1234",  # port 1234 for LM Studio
        "context_window": 16384,
    },
]

llm_config = {"config_list": config_list, "seed": 42}
llm_config_memgpt = {"config_list": config_list_memgpt, "seed": 42}



# there are some additional options to do with how you want the interface to look (more info below)
interface_kwargs = {
    "debug": False,
    "show_inner_thoughts": True,
    "show_function_outputs": True,
}

# The user agent
user_proxy = autogen.UserProxyAgent(
    name="Haervwe",
    system_message="you are a curator of the story made so far, you need to parse it to a .txt ",
    code_execution_config={"last_n_messages": 2, "work_dir": "Outputs", "use_docker":False},
    human_input_mode="NEVER",  # needed?
    default_auto_reply="...",  # Set a default auto-reply message here (non-empty auto-reply is required for LM Studio)
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),
)



# The Coder agent
    
coder = AssistantAgent(
    "assistant", 
    llm_config={"config_list": config_list},
    system_message=f"""You are a skilled full-stack developer tasked with building a complete web application from scratch. Design a responsive front-end using modern frameworks like React, handling UI, routing, and state management. Implement a suitable back-end framework like Node.js, handling APIs, database models, and business logic. Set up a database and write queries. Implement authentication and authorization. Write tests and deploy to a cloud platform. Document your process and provide setup instructions."""

)
#  Agent that acts as Product Manager

pm = AssistantAgent(
    "assistant", 
    llm_config={"config_list": config_list},
    system_message=f"""You are the product manager leading the development of a new full-stack web application. Conduct market research and competitive analysis. Define the product vision and strategy aligned with business goals. Gather requirements from stakeholders and create user stories. Collaborate with designers on UI/UX. Work closely with the development team. Manage the product roadmap and feature prioritization. Coordinate with cross-functional teams for launches. Analyze metrics and user feedback. Communicate updates to stakeholders. Iterate and improve the product over time."
               f"You are participating in a group chat with a user ({user_proxy.name}) "
               f"and a coder who you will be managing ({coder.name})."""
)


# try:
#     pm = create_memgpt_autogen_agent_from_config(
#         "MemGPT_Product_Manager1",
#         llm_config=llm_config_memgpt,
#         system_message=f"""You are the product manager leading the development of a new full-stack web application. Conduct market research and competitive analysis. Define the product vision and strategy aligned with business goals. Gather requirements from stakeholders and create user stories. Collaborate with designers on UI/UX. Work closely with the development team. Manage the product roadmap and feature prioritization. Coordinate with cross-functional teams for launches. Analyze metrics and user feedback. Communicate updates to stakeholders. Iterate and improve the product over time."
#             f"You are participating in a group chat with a user ({user_proxy.name}) "
#             f"and a coder who you will be managing ({coder.name}).""",
#         interface_kwargs=interface_kwargs,
#         default_auto_reply="...",
#         skip_verify=False,  # NOTE: you should set this to True if you expect your MemGPT AutoGen agent to call a function other than send_message on the first turn
#         auto_save=False,  # NOTE: set this to True if you want the MemGPT AutoGen agent to save its internal state after each reply - you can also save manually with .save()
#     ) 
# except ValueError:
#     pm = load_autogen_memgpt_agent(agent_config={"name": "MemGPT_Product_Manager1"})




# Initialize the group chat between the user and two LLM agents (writer and critic)
groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder], messages=[], max_round=100, speaker_selection_method="round_robin")
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message=f"""Create a really simple single page aplication that allow two players in the same pc to play chess, you are forbiden to try to use an ai agent opponent"""
)