from collections import defaultdict
from collections import deque
def fix(reg):
  r=list()
  n=len(reg)
  for i in range(n):
    c=reg[i]
    if c=="." or c=="(" or c=="|":
      r.append(c)
    elif (i+1<n) and reg[i+1]!=")" and reg[i+1]!="|" and reg[i+1]!="*":
      r.append(c)
      r.append(".")
    else:
      r.append(c)
  return r
      
def pre_reg(reg):
  s=list()
  reg=fix(reg)
  stack=list()
  n=len(reg)
  for i in range(n-1,-1,-1):
    c=reg[i]
    if c=="*" or c==")":
      stack.append(c)
    elif c==".":
      while(len(stack) and stack[-1]=="*"):
        r=stack.pop()
        s=[r]+s
      stack.append(c)
    elif c=="|":
      while(len(stack) and (stack[-1]=="*" or stack[-1]==".")):
        r=stack.pop()
        s=[r]+s
      stack.append(c)
    elif c=="(":
      while stack[-1]!=")":
        r=stack.pop()
        s=[r]+s
      stack.pop()
      if len(stack) and stack[-1]=="*":
        r=stack.pop()
        s=[r]+s
    else:
      s=[c]+s
  while stack:
    s=[stack.pop()]+s
  return s
def make_NFA(reg):
  reg=pre_reg(reg)
  NFA=defaultdict(set)
  stack=list()
  state=0
  n=len(reg)
  for i in range(n-1,-1,-1):
    c=reg[i]
    if c=="|":
      s1,leaf1=stack.pop()
      s2,leaf2=stack.pop()
      state+=1
      NFA[(state,"eps")].add(s1)
      NFA[(state,"eps")].add(s2)
      leaf=leaf1.union(leaf2)
      stack.append((state,leaf))
    elif c==".":
      s1,leaf1=stack.pop()
      s2,leaf2=stack.pop()
      for nd in leaf1:
         NFA[(nd,"eps")].add(s2)
      stack.append((s1,leaf2))
    elif c=="*":
      s1,leaf=stack.pop()
      state+=1
      s2=state
      state+=1
      s3=state    
      for lfs in leaf:
        NFA[(lfs,"eps")].add(s3)
      state+=1
      s4=state
      NFA[(s3,"eps")].add(s4)
      NFA[(s3,"eps")].add(s1)
      NFA[(s2,"eps")].add(s1)
      NFA[(s2,"eps")].add(s4)
      stack.append((s2,{s4}))
    else:
      state+=1
      s1=state
      state+=1
      s2=state
      NFA[(s1,c)].add(s2)
      stack.append((s1,{s2}))
  return NFA,stack[-1]  
#keep track of leaf
#fix c=="." case in NFA
#implement bfs based regex matcher
def eval_NFA(NFA, start, end, string):
    def epsilon_closure(states):
        stack = list(states)
        closure = set(states)
        while stack:
            s = stack.pop()
            for nxt in NFA[(s, "eps")]:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure
    current = epsilon_closure({start})
    for ch in string:
        next_states = set()
        for s in current:
            next_states.update(NFA[(s, ch)])
        if not next_states:
            return False
        current = epsilon_closure(next_states)
    return len(current.intersection(end)) > 0

    

reg=input("ENTER REGEX:")
print("-------------------")
nfa,states=make_NFA(reg)
print(fix(reg))
print(pre_reg(reg))
print(nfa)
print(states)
print("----------------------")
while(True):
  chk=input("ENTER STRING: ")
  print(eval_NFA(nfa,states[0],states[1],chk))


