# Prompt Memory Lab
Set of scripts experimenting with various methods of prompt memory for LLMs and the finding lowest token cost per prompt whilst retaining memory of conversational sessions.

## Short-Term Memory Algoirthms

### Inclusive Short-Term Memory (ISM)

In ISM, all tokens from all messages (prompt + response) in each conversation are appended to the prompt after each message. The entirity of all appended tokens can be represented as a vector. The short-term memory vector included in every prompt is thus inclusive of all tokens of all messages in each conversation.

ISM is expensive, its cost represented as:

![Cost formula for I-SM](https://user-images.githubusercontent.com/123819841/227754883-f471ba01-6947-4db4-9306-45631fc7ac12.png)

Where n is the number of messages in the conversation, m is the token count for each message, and S is a System prompt that isn't appended to the short-term memory vector, but is included at the start of each prompt.

ISM becomes cost prohibitive as costs rises exponentially.

To reduce cost, we can cap the number of elements in the shot-term memory vector. Then we can abstract the entire conversation in the short-term vector by prompting the LLM to create a summary with t tokens. By adding this abstraction to the prompt and 'emptying' the short-term memory vector, we can taper the exponential cost increase.

We can call this new algorithm Abstraction Inclusive Short-Term Memory (A-ISM)

### Abstraction Inclusive Short-Term Memory

Using A-ISM, the composition of each prompt or prompt 'stack' would be:
1. System Prompt
2. Abstraction Vector
3. Short-Term Memory Vector

The process goes like this:
1. After every message, append prompt and response tokens in short-term memory vector
2. If number of elements in short-term memory vector == the memory limit, go to 3 else go to 1
3. Abstract short-term memory by summarizing the contents of the short-term memory vector; use the entire vector as the prompt
4. Empty short-term memory vector
5. Append abstraction vector with abstraction

The cost will still grow exponential as the Abstraction vector is uncapped and all abstractions are inclusive. There is no second-order abstractions. Let's compare the cost of A-ISM with ISM.

The results are fruitful (using the short-term-memory-calc.py):
Inclusive STM - 100 msgs:
FINAL TOKENS PER MSG: 545000          
FINAL COST PER MSG: $1.0908          
TOTAL COST OF CONVERSATION: $38.45

Abstracted Inclusive STM - 100 msgs, 51 cap, 1 abstraction
FINAL TOKENS PER MSG: 404250          
FINAL COST PER MSG: $0.8093          
TOTAL COST OF CONVERSATION: $24.38
37% cost reduction from ISM^

Abstracted Inclusive STM - 100 msgs, 11 cap, 9 abstractions
FINAL TOKENS PER MSG: 142200          
FINAL COST PER MSG: $0.2852          
TOTAL COST OF CONVERSATION: $8.78
78% cost reduction from ISM^


### 1. Inclusive Tensor Memory (ITM)

All tokens are appended to the prompt after each message (prompt + response). At the end of a conversation with n messages, every message added to the prompt  during the conversation is added to a long-term memory tensor. The long-term memory tensor is appended to the prompt initialization at the start of the next conversation.

Prompt Stack:
- System Prompt
- Long-Term Memory Tensor
- Short-Term Memory Vector

Advantages: Recall of every message of every prompt.
Cons: High cost, token cost per message increases linearly with every message. The cost shown is I = Initial prompt cost, C = cost per message, n = number of messages per conversation.

In the case with ITM:

![Summation notation of LTM cost](https://user-images.githubusercontent.com/123819841/227696954-fb40a2e2-c67b-4825-859d-6858911625fd.png)



### 2. Abstracted Linear Memory

Short-term memory functions similarly to LTM in that every message is appended to the prompt initialization. However at the end of a conversation, the memory undergoes a compression process whereby the short-term memory is summarized by an LLM into an Abstraction. The Abstraction(s) are collected into a long-term memory vector and appended at the start of the next conversation.

In Abstracted Linear Memory, the cost still increases linearly per prompt as every Abstraction is added to every Initial prompt cost. Plus there is the added cost Abstraction compression.

Prompt Stack:
- Initial Prompt
- Abstraction Vector
- Short-Term Memory Vector

Advantages: Hypothetically cheaper than LTM despite added Abstraction compression
Cons: Costs may still be high due to linearly increased per prompt cost. There may also be memory loss as some features may be forgotten over many conversations, however this could simulate a more natural memory.



### 3. Fully Abstracted Memory

Short-term memory also functions the same as Absolute and Abstracted memory, the difference here is that there is only 1 Abstraction in every prompt. The end of a conversation means that the short-term memory vector is abstracted, but in a new conversation the newest abstraction is used. Abstractions do not stack. Therefore per prompt cost is hypothetically the lowest, but memory loss possibly the highest.

Prompt Stack:
- Initial Prompt
- Abstraction
- Short-Term Memory Vector

Advantages: Hypothetically the cheapest of all 3 forms of memory. 
Cons: There is still an added abstraction compression cost, and memory loss may be greatest
