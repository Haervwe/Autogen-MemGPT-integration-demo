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
        "context_window": 32768,
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
    human_input_mode="TERMINATE",  # needed?
    default_auto_reply="...",  # Set a default auto-reply message here (non-empty auto-reply is required for LM Studio)
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", "").rstrip(),
)

# MemGpt Agent that acts as a sci fy writer
try:
    writer = create_memgpt_autogen_agent_from_config(
        "MemGPT_Writer_pro",
        llm_config=llm_config_memgpt,
        system_message=f"You a proffesional theater play writter, I make long and detailed paragraphs full of descriptions, the least you write is around 1000 words, you write in the style of Isaac Asimov, you dont tell anything but the story when you are writing",
        interface_kwargs=interface_kwargs,
        default_auto_reply="...",
        skip_verify=False,  # NOTE: you should set this to True if you expect your MemGPT AutoGen agent to call a function other than send_message on the first turn
        auto_save=False,  # NOTE: set this to True if you want the MemGPT AutoGen agent to save its internal state after each reply - you can also save manually with .save()
    )
except ValueError:
    writer = load_autogen_memgpt_agent(agent_config={"name": "MemGPT_Writer_pro"})


# MemGpt Agent that acts as a sci fy critic

try:
    critic = create_memgpt_autogen_agent_from_config(
        "MemGPT_Critic_pro",
        llm_config=llm_config_memgpt,
        system_message=f"you are a theater critic obsessed with perfection(which I make sure to tell everyone I work with). you are trying to help make the best sci-fy story, your job is to critized the histiry and make sure it is consistent\n"
            f"You are participating in a group chat with a user ({user_proxy.name}) "
            f"and a writer who you will help by giving advice in how to improve the story if its satisfactory you will tell him to continue it ({writer.name}).",
        interface_kwargs=interface_kwargs,
        default_auto_reply="...",
        skip_verify=False,  # NOTE: you should set this to True if you expect your MemGPT AutoGen agent to call a function other than send_message on the first turn
        auto_save=False,  # NOTE: set this to True if you want the MemGPT AutoGen agent to save its internal state after each reply - you can also save manually with .save()
    ) 
except ValueError:
    critic = load_autogen_memgpt_agent(agent_config={"name": "MemGPT_Critic_pro"})


# The assitant agent
    
##assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})

# Initialize the group chat between the user and two LLM agents (writer and critic)
groupchat = autogen.GroupChat(agents=[user_proxy, writer, critic], messages=[], max_round=100, speaker_selection_method="round_robin")
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="I want you to write a really good short play script for theaters about vampires story that follow the hero journey, and is outputed completed in the last respose. following the completion of the task,output the final story version to a txt, also you can only finish after a full narrative arc is resolved",
)