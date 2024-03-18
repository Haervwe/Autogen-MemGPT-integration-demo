import os
import autogen
from autogen import AssistantAgent, UserProxyAgent

# create a config for the MemGPT AutoGen agent
config_list = [
    {
        "model": "Dolphin 2.6 Mistral 7b q8",
        "base_url": "http://localhost:1234/v1",  # port 1234 for LM Studio
        "api_key": "NULL",
    },
]




llm_config = {"config_list": config_list, "seed": 42}


# The user agent
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list},default_auto_reply="...",)

user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker":False},
    human_input_mode="TERMINATE",  # needed?
    default_auto_reply="...",
    )


# Initialize


user_proxy.initiate_chat(
    
    user_proxy.initiate_chat(assistant, message="make a Cmd script to delete all files in ./outputs folder")
)