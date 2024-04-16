import numpy as np
import random
import math

def state2num(state): # given binary list, convert to its base-10 form
    # state is 1-D numpy array
    state=np.array(state)
    if(len(state)==state.size):
        n=0
        for i in range(len(state)-1,-1,-1):
            #print(state[i],i)
            n+=state[i]*2**(len(state)-1-i)
        return n
    else:
        print("not 1D array!")
        return 0

def num2state(value,bits):
    # basically turning a base 10 number to a binary string
    # bits would define how much space we reserve
    state=[]
    #m=int(math.log(value,2))
    m=bits-1
    for i in range(m,-1,-1):
        c=2**i
        state.append(value//c)
        value=value%c
    state=np.array(state)
    return state
    


class Cellular():
    def __init__(self,n_hood=3):
        self.n_hood=n_hood # neighberhood level
        self.Rule=np.array(random.choices([0,1],k=2**n_hood))
        self.RuleNum=state2num(self.Rule)

    def _randomizeRule(self):
        self.Rule=np.array(random.choices([0,1],k=2**self.n_hood))
        return self.Rule
    
    def getInitial(self,world_size):
        initial=np.array(random.choices([0,1],k=world_size))
        return initial
        

    def _setRulebyNum(self,n): # choose a rule
        if(n<=2**(2**self.n_hood)):
            self.Rule=np.array(num2state(n,2**self.n_hood))
            return self.Rule
        else:
            print('rule number out of range!')
            print(f'max: {2**(2**self.n_hood)}, min: 0;')

    def _setRulebyArray(self,rule): #customize the rule
        rule=np.array(rule)
        # pass in numpy array 1-D or a list in binary
        if(len(rule)==rule.size and len(rule)==2**self.n_hood):
            self.Rule=np.array(rule)
        else:
            print('invalid rule')
            return False
        return self.Rule

    def update(self,state): #pass in a state, return the next state based on Rule
        new_state=[]
        # loop through each cell
        for i in range(0,len(state)):
            rang=int((self.n_hood-1)/2)
            env=[]
            for v in range(-rang,rang+1):
                env.append(state[(i+v)%len(state)])
            # convert the env into a binary to pair with the rule
            n=state2num(env)
            # the rule list has 0th mapping at the end
            rule_n=(2**self.n_hood)-1-n # reverse the index
            new_cell=self.Rule[rule_n]
            #print(new_cell,n)
            new_state.append(new_cell)
        new_state=np.array(new_state)
        return new_state

    def _info(self):
        self.RuleNum=state2num(self.Rule)
        print('-'*10)
        print(f'This is Rule {self.RuleNum};')
        print(f'Rule: {self.Rule};')
        print(f'Using {self.n_hood}-hood;')
        print('-'*10)
        return self.RuleNum
        
# Testing the code
def Test1():
    n=5
    x=Cellular(n)
    x._info()
    x._randomizeRule()
    x._info()
    rule=random.choices([0,1],k=2**n)
    print(f'new Rule: {rule}')
    x._setRule(rule)
    x._info()

    s1=x.getInitial()
    print(s1)
    s2=x.update(s1)
    print(s2)

def Test2():
    n=3
    world_size=35
    rule_n=218
    iterations=30
    x=Cellular(n)
    x._setRulebyNum(rule_n)
    x._info()
    #s=x.getInitial(world_size)
    s=np.array([0]*12+[1]+[0]*12)
    print(s)
    for i in range(iterations):
        s=x.update(s.copy())
        print(s)
Test2()

