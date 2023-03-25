# prompt-memory-lab
Set of scripts experimenting with various methods of prompt memory for LLMs and the finding lowest token cost per prompt whilst retaining memory of conversational sessions.

1. Linear Tensor Memory
Every message (prompt + response) is appended to the prompt initialization. At the end of a conversation with n messages, every message added to the initial prompt initialization during the conversation is added to a long-term memory tensor. The long-term memory tensor is appended to the prompt initialization at the start of the next conversation.

Prompt Stack:
Initial Prompt
Long-Term Memory Tensor
Short-Term Memory Vector

Advantages: Recall of every message of every prompt.
Cons: High cost, token cost per message increases linearly with every message. The cost shown is I = Initial prompt cost, C = cost per message, n = number of messages per conversation.

In the case with Linear Tensor Memory I += 



2. Abstracted Linear Memory
Short-term memory functions similarly to LTM in that every message is appended to the prompt initialization. However at the end of a conversation, the memory undergoes a compression process whereby the short-term memory is summarized by an LLM into an Abstraction. The Abstraction(s) are collected into a long-term memory vector and appended at the start of the next conversation.

In Abstracted Linear Memory, the cost still increases linearly per prompt as every Abstraction is added to every Initial prompt cost. Plus there is the added cost Abstraction compression.

Prompt Stack:
Initial Prompt
Abstraction Vector
Short-Term Memory Vector

Advantages: Hypothetically cheaper than LTM despite added Abstraction compression
Cons: Costs may still be high due to linearly increased per prompt cost. There may also be memory loss as some features may be forgotten over many conversations, however this could simulate a more natural memory.



3. Fully Abstracted Memory
Short-term memory also functions the same as Absolute and Abstracted memory, the difference here is that there is only 1 Abstraction in every prompt. The end of a conversation means that the short-term memory vector is abstracted, but in a new conversation the newest abstraction is used. Abstractions do not stack. Therefore per prompt cost is hypothetically the lowest, but memory loss possibly the highest.

Prompt Stack:
Initial Prompt
Abstraction
Short-Term Memory Vector

Advantages: Hypothetically the cheapest of all 3 forms of memory. 
Cons: There is still an added abstraction compression cost, and memory loss may be greatest
