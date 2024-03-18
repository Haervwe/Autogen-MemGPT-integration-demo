# Autogen-MemGPT-integration-demo
simple scritps for Integration of Autogen and memGPT to test differnt outcomes of LLM agents cooperation


HOW TO USE:

Hook up your API in the scripts config
modify the agents promts (using memgpt you should delete the agents if they will have different sistem promts and the same name since they are stored in a database when created)
modify the task promt

run! and see if the hallucinate 

results using 7B and 13B models with a token context size of 8192 

natural-functions-Q8_0.gguf:
  Function Calling: Really good at function calling , few errors with memGPT
  Coding: can write simple scripts and single document python code, prone to hallucinations
  Story-Telling: prone to halucinate 

llama-2-13b-chat.Q5_K_M.gguf
  Function Calling: Bad at function calling, cant be effectibly used with memGPT, works with Autogen alone
  Coding: Not good, can write REALLY simple code
  Story-Telling: Can produce good results if prompted with specifics about the story, loose track when memGPT kicks off managing context

dolphin-2.6-mistral-7b-dpo-laser.Q8_0.gguf
  Function Calling: The best model for memGPT, prone to errors formating autoGEN functions some times specially closing the SH tags for CLI execution
  Coding: Average, can be used to revise code with VScode plugins (Copilot clones like twinny)
  Story-Telling: prone to loose track and give really short statements instead of a story

airoboros-l2-13b-3.1.1.Q6_K.gguf
  Function Calling: works for memGPT, prone to forget autogen functions
  Coding: can write simple scripts , cant be tested further since it does not format correctly tags for autogen
  Stor-Telling: prone to loose trak, prone to respond empty (may be a VRAM limitation)

deepseek-coder-6.7B-instruct-GGUF
  Function Calling: not usable for memGPT, prone to forget autogen functions
  Coding: can write simple scripts the best, can modify documents, and kinda undesrtand the code, prone to halluciante nonsensical code when asked to resolve a complex task.
  Stor-Telling: incoherent
