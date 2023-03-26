def main():
    print("Number of messages:")
    n = int(input())
    print("Initial System cost:")
    sysP = int(input())
    print("Short-term memory vector cap:")
    vCap = int(input())
    #print("Current token number:")
    #tokens = int(input())

    stm_cost(n,sysP, vCap)

def stm_cost(n, sysP, vCap):
    cost = 0
    total_cost = 0
    tokens = 0
    k = 1
    memory_limit = vCap
    abV = []
    print(f"---------------------------------------------\
          \nCURRENT TOKENS PER MSG: {tokens}\
          \nCURRENT COST PER MSG: ${cost}\n")
    
    while n != 0:
        tokens += k*100
        tokens = tokens + sysP
        
        # Abstractions added to prompt
        for i in abV:
            tokens += abV[0][0]
            print(f"Abstraction added. +{abV[0][0]} tokens")

        cost = ((tokens/1000) * 0.002) + ((sysP/1000) * 0.002)
        total_cost += cost
        n -= 1
        memory_limit -= 1
        k += 1
        print(f"MESSAGE #{k-1} ********\
            \nCURRENT TOKENS PER MSG: {tokens}\
            \nCURRENT COST PER MSG: ${cost}\
            \nNUMBER OF ABSTRACTIONS: {len(abV)}")
        
        # Vector Cap limit hit:
        if memory_limit == 0 and n != 1:
            print("~Short-term memory limit, starting Abstraction...\
                  \n................................................")
            ab = abstraction(tokens)
            abV.append(ab)
            # Short-term memory vector cleared
            memory_limit = vCap
            tokens = 0
            # Abstraction processing cost added
            total_cost += ab[2]
        
    print(f"*****************************\
          \n*****END OF CONVERSATION*****\
          \n*****************************\
          \n* FINAL TOKENS PER MSG: {tokens}\
          \n* FINAL COST PER MSG: ${cost}\
          \n* TOTAL COST OF CONVERSATION: ${total_cost}")

# Simulation of abstraction process
def abstraction(tokens):
    # Abstraction represented as a list here, structure is as follows:
    # [{abstraction token count}, {abstraction process token count}, {abstraction process cost}]
    abstraction = []
    # Assume Abstraction itself has 250 tokens
    abstraction.append(250)
    # Abstraction process, uses short-term memory vector + some other words for prompt + the response itself
    abstraction.append(tokens + 30 + 250)
    # Finally the cost of the abstraction itself
    abstraction.append((abstraction[1]/1000) * 0.002)
    print(f"~Abstraction complete. Cost of Abstraction = ${abstraction[2]}")

    return abstraction

    
    
if __name__ == "__main__":   
    main()