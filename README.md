# Prompt Memory Lab
Set of scripts experimenting with various methods of prompt memory for LLMs and the finding lowest token cost per prompt whilst retaining memory of conversational sessions.

This readme is under construction. It will be cleaned up and completed once all testing is done. Scripts for calculators and simulations will all be uploaded. Further experimentation is still underway.

## Short-Term Memory Algoirthms

### Inclusive Short-Term Memory (ISM)

In ISM, all tokens from all messages (prompt + response) in each conversation are appended to the prompt after each message. The entirity of all appended tokens can be represented as a vector. The short-term memory vector included in every prompt is thus inclusive of all tokens of all messages in each conversation.

ISM is expensive, its cost represented as:

![Cost formula for I-SM](https://user-images.githubusercontent.com/123819841/227754883-f471ba01-6947-4db4-9306-45631fc7ac12.png)

Where n is the number of messages in the conversation, m is the token count for each message, and S is a System prompt that isn't appended to the short-term memory vector, but is included at the start of each prompt.

ISM becomes cost prohibitive as costs rises exponentially.

To reduce cost, we can cap the number of elements in the shot-term memory vector. Then we can abstract the entire conversation in the short-term vector by prompting the LLM to create a summary with t tokens. By adding this abstraction to the prompt and 'clearing' the short-term memory vector, we can taper the exponential cost increase.

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


Inclusive STM - 30 msgs:

* FINAL TOKENS PER MSG: 58500          
* FINAL COST PER MSG: $0.1178          
* TOTAL COST OF CONVERSATION: $1.38

Abstracted Inclusive STM - 30 msgs, 16 cap:

* FINAL TOKENS PER MSG: 18200          
* FINAL COST PER MSG: $0.037          
* TOTAL COST OF CONVERSATION: $0.56
59% cost reduction from ISM^

Abstracted Inclusive STM - 30 msgs, 10 cap:

* FINAL TOKENS PER MSG: 0          
* FINAL COST PER MSG: $0.0278          
* TOTAL COST OF CONVERSATION: $0.41
70% cost reduction of ISM ^

Abstracted Inclusive STM - 30 msgs, 5 cap:

* FINAL TOKENS PER MSG: 0          
* FINAL COST PER MSG: $0.019         
* TOTAL COST OF CONVERSATION: $0.313
24% cost reduction from 10 cap ^
77% cost reduction from ISM ^


### Fully Abstracted Short-Term Memory (FASM)

In a Fully Abstracted Memory, there is no Abstraction Vector, there is only a single Abstraction cell. When the short-term memory vector is cleared, an abstraction is created from all the tokens in the vector, just like with A-ISM. However upon subsequent memory clearing, the content of the Abstraction cell is used as a prompt in the Abstraction process in conjunction with the memory vector and then the content of the Abstraction cell is replaced with the new Abstraction. Thus FASM is not inclusive of all messages nor of Abstractions.

Testing this with the fasm-calc.py has shown that FASM is negligably more cost effective for normal message volume (~30 messages):

Fully Abstracted STM (FASM) - 30 msgs, 10 cap
* FINAL TOKENS PER MSG: 0          
* FINAL COST PER MSG: $0.0227       
* TOTAL COST OF CONVERSATION: $0.386
5% cost reduction from A-ISM^

However in high message volume (~100 messages), the results are more noticeable:


Inclusive STM (ISM)- 100 msgs:

* FINAL TOKENS PER MSG: 545000          
* FINAL COST PER MSG: $1.0908          
* TOTAL COST OF CONVERSATION: $38.45

Abstracted Inclusive STM - 100 msgs, 51 cap, 1 abstraction:

* FINAL TOKENS PER MSG: 149450          
* FINAL COST PER MSG: $0.2997          
* TOTAL COST OF CONVERSATION: $11.64
70% cost reduction from ISM^

Abstracted Inclusive STM - 100 msgs, 21 cap, 4 abstractions:

* FINAL TOKENS PER MSG: 34400          
* FINAL COST PER MSG: $0.0696          
* TOTAL COST OF CONVERSATION: $3.61
91% cost reduction from ISM^

Abstracted Inclusive STM - 100 msgs, 11 cap, 9 abstractions:

* FINAL TOKENS PER MSG: 35400          
* FINAL COST PER MSG: $0.0716          
* TOTAL COST OF CONVERSATION: $2.54
94% cost reduction from ISM^

Fully Abstracted STM (FASM) - 100 msgs, 11 cap, 9 abstractions:

* FINAL TOKENS PER MSG: 14400          
* FINAL COST PER MSG: $0.0296          
* TOTAL COST OF CONVERSATION: $1.46
96% cost reduction from ISM^
43% cost reduction from A-ISM^


43% cost reduction from A-ISM is substantial, but A-ISM already demonstrates >90% cost reduction from ISM, so the real cost reduction in high message volume is small even though the percentage is relatively high. A-ISM however can still have exponential cost increases in massive message volume (1000 msgs). A quick test demonstrates FASM being significantly more cost effective in massive message volume:

Abstracted Inclusive STM - 1000 msgs, 11 cap, 90 abstractions:

* FINAL TOKENS PER MSG: 233500          
* FINAL COST PER MSG: $0.467        
* TOTAL COST OF CONVERSATION: $168.10

Fully Abstracted STM - 1000 msgs, 11 cap, 90 abstractions:

* FINAL TOKENS PER MSG: 7400          
* FINAL COST PER MSG: $0.01488          
* TOTAL COST OF CONVERSATION: $9.14
95% cost reduction from A-ISM^

FASM is the most cost-effective choice for massive message volume. 

### Conclusion

While more investigation is needed, as well as setting restrictive token caps to fit with GPT-3.5 4k token limit, there seems to be promising results:

* Abstraction significantly reduces cost of per-msg prompt while retaining memory.
* ISM allows for total recall of conversational content but is extremely expensive and impractical. Inclusive memory can be used in a limited way within a data vector for working memory in conjunction with Abstractions as is the case with A-ISM.
* A-ISM works well and is quite cheap for normal-high message volumes, making it a strong candidate for an algorithm for working memory. However it becomes cost prohibitve in massive message volume, therefore Abstraction vector has to be capped and cleared.
* FASM is by far the cheapest option, however hypothetically it has the highest chance for memory loss and decrease in quality for conversational recall. Because of this, FASM may be best suited for a long-term memory setup.

Further investigation and experimentation is needed. Some current issues:

* Greater optimization needed so that the number of tokens in each prompt stack lies within a 4k token limit. Consider chaining with other LLMs for abstraction process.
* Investigation into optimal short-term memory vector cap number. Local minima for cost, local maxima for quality.
* Consider short-term memory vector to have tapered clearing, with the oldest messages in the vector loaded into abstraction while newest messages remain inclusive. This should hypothetically increase quality.

# OLD - ignore

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
