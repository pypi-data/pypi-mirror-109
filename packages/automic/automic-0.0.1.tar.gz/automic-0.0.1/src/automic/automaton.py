from collections import defaultdict
from typing import List, Any, Set

import re

class Automaton:
    """
    Nondeterministic, with epsilon transitions (None)
    """
    
    def __init__(self, n_states: int, accepting: Set[int]):
        self.n_states = n_states
        self.transitions = [defaultdict(set) for _ in range(n_states)]
        self.accepting = set(accepting)
        self.pruned_depth = 0

    @property
    def alphabet(self):
        s = set()
        for transition in self.transitions:
            for k in transition:
                s.add(k)
        return frozenset(s - {None})

    def add_state(self):
        self.n_states += 1
        self.transitions.append(defaultdict(set))
    
    def epsilon_expand(self, states):
        while True:
            expanded = set(states)
            for state in states:
                if None in self.transitions[state]:
                    expanded |= self.transitions[state][None]
            if len(expanded) == len(states):
                return states
            states = expanded

    def epsilon_expand_paths(self, state_paths):
        # infinite loop if there are epsilon loops, so avoid that
        while True:
            expanded = set(state_paths)
            for state, path in state_paths:
                for successor in self.transitions[state][None]:
                    expanded.add((successor, state + (successor,)))
            if len(expanded) == len(state_paths):
                return state_paths
            state_paths = expanded
    
    
    def is_accessible(self, state):
        reachable = set()
        frontier = {0}
        while True:
            new_reachable = reachable | frontier
            if len(new_reachable) == len(reachable):
                return False
            reachable = new_reachable
            if state in reachable:
                return True
            new_frontier = set()
            for s in frontier:
                for token, successors in self.transitions[s].items():
                    new_frontier |= successors
            frontier = new_frontier
    
    def is_co_accessible(self, state):
        reachable = set()
        frontier = {state}
        while True:
            new_reachable = reachable | frontier
            if len(new_reachable) == len(reachable):
                return False
            reachable = new_reachable
            if len(reachable & self.accepting) > 0:
                return True
            new_frontier = set()
            for s in frontier:
                for token, successors in self.transitions[s].items():
                    new_frontier |= successors
            frontier = new_frontier
    
    def test(self, string: List[Any]):
        states = self.epsilon_expand({0})
        for token in string:
            assert token is not None
            if len(states) == 0:
                return False
            new_states = set()
            for state in states:
                new_states |= self.transitions[state][token]
            new_states = self.epsilon_expand(new_states)
            states = new_states
        return len(states & self.accepting) > 0

    def paths(self, string: List[Any]):
        state_paths = {(0, (0,))}
        state_paths = self.epsilon_expand_paths(state_paths)
        for token in string:
            assert token is not None
            if len(state_paths) == 0:
                return set()
            new_state_paths = set()
            for state, path in state_paths:
                for successor in self.transitions[state][token]:
                    new_state_paths.add((successor, path + (successor,)))
            new_state_paths = self.epsilon_expand_paths(new_state_paths)
            state_paths = new_state_paths
        return {path for state, path in state_paths if path[-1] in self.accepting}
        
    
    def __iter__(self):
        frontier = [(s, []) for s in self.epsilon_expand({0})]
        while len(frontier) > 0:
            for state, string in frontier:
                if state in self.accepting:
                    yield string

            new_frontier = []
            for state, string in frontier:
                for token, successors in self.transitions[state].items():
                    if token is not None:
                        for successor in self.epsilon_expand(successors):
                            new_frontier.append((successor, string + [token]))
            
            frontier = new_frontier

    def has_epsilons(self):
        for transition in self.transitions:
            if None in transition:
                if len(transition[None]) > 0:
                    return True
        return False
    
    def is_deterministic(self):
        if self.has_epsilons():
            return False
        for transition in self.transitions:
            for successors in transition.values():
                if len(successors) > 1:
                    return False
        return True
    
    
    def is_trim(self):
        for state in range(self.n_states):
            if not self.is_co_accessible(state):
                return False
            if not self.is_accessible(state):
                return False
            
        return True
    
    def is_ambiguous(self):
        A = epsilon_remove(self)
        A = trim(A)
        assert A.is_trim()
        assert not A.has_epsilons()
        
        AA = intersection(A, A)
        # (s, t) on an accepting path only if s == t
        for i in range(A.n_states):
            for j in range(i):
                # (s, t) is identical to (t, s), so only check one
                k = i*A.n_states + j
                if AA.is_accessible(k) and AA.is_co_accessible(k):
                    return True
        return False

    def copy(self):
        A = Automaton(self.n_nodes, {self.accepting})
        for i, transitions in enumerate(self.transitions):
            for token, successors in transitions.items():
                A.transitions[i][token] |= successors
        return A


    def prefix_language(self, state):
        A = self.copy()
        A.accepting = {state}
        
    def suffix_language(self, state):
        A = Automaton(self.n_states, set())
        # swap state and zero
        mapping = {s: s for s in range(A.n_states)}
        mapping[0] = state
        mapping[state] = 0
        A.accepting = {mapping[s] for s in self.accepting}
        
        for i, transitions in enumerate(self.transitions):
            ia = mapping[i]
            for token, successors in transitions.items():
                A.transitions[ia][token] = {mapping[s] for s in successors}
        return A
                
    def __add__(self, other):
        return prune(cat(self,other))
    
    def __or__(self, other):
        return prune(union(self, other))
    
    def __and__(self, other):
        return prune(intersection(self, other))
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return prune(repeat(self, key))
        elif isinstance(key, slice):
            if key.stop is None:
                if key.start is not None:
                    base = self[key.start]
                else:
                    base = Automaton(1, {0})

                if key.step is not None:
                    slope = self[key.step]
                else:
                    slope = self
            
                return base + star(slope)
            
            else:
                start = key.start
                if start is None:
                    start = 0
                stop = key.stop
                step = key.step
                if step is None:
                    step = 1
                
                # union of a bunch of automata; start with an empty language
                B = Automaton(1, set())
                for n in range(start, stop, step):
                    B |= repeat(self, n)

                return B

            
            

def literal(string: List[Any]):
    A = Automaton(len(string)+1, {len(string)})
    for i, token in enumerate(string):
        A.transitions[i][token].add(i+1)
    return A


def union(A, B):
    C = Automaton(A.n_states + B.n_states+1, set())
    # state 0 is a new starting state with some epsilon transitions
    # A's and B's state indices change
    a_offset = 1
    b_offset = A.n_states + 1
    
    # starting state
    C.transitions[0][None] = {a_offset, b_offset}
   
    
    for i, transitions in enumerate(A.transitions):
        for token, successors in transitions.items():
            C.transitions[i+a_offset][token] |= {s+a_offset for s in successors}

    for i, transitions in enumerate(B.transitions):
        for token, successors in transitions.items():
            C.transitions[i+b_offset][token] |= {s+b_offset for s in successors}

    
    C.accepting = {s + a_offset for s in A.accepting}
    C.accepting |= {s + b_offset for s in B.accepting}
    
    return C

def intersection(A, B):
    C = Automaton(A.n_states * B.n_states, set())
    for i in range(A.n_states):
        for j in range(B.n_states):
            k = i*A.n_states + j
            for a_token, a_successors in A.transitions[i].items():
                for b_token, b_successors in B.transitions[j].items():
                    if a_token == b_token:
                        c_successors = set()
                        for a_successor in a_successors:
                            for b_successor in b_successors:
                                c_successors.add(a_successor * A.n_states + b_successor)
                        C.transitions[k][a_token] |= c_successors
    for a_accepting in A.accepting:
        for b_accepting in B.accepting:
            C.accepting.add(a_accepting*A.n_states + b_accepting)
    
    return C
    
def cat(A, B):
    A = epsilon_remove(A)
    B = epsilon_remove(B)
    C = Automaton(A.n_states + B.n_states, set())
    # all of A's states keep their indices, B's indices change
    b_offset = A.n_states
    
    # Duplicate A exactly in C
    for i, transitions in enumerate(A.transitions):
        for token, successors in transitions.items():
            C.transitions[i][token] |= successors
    
    # Duplicate B into C with changed indices
    for i, transitions in enumerate(B.transitions):
        for token, successors in transitions.items():
            C.transitions[i+b_offset][token] |= {s + b_offset for s in successors}
            
    # add epsilon transitions from A's accepting states to B's start state
    for state in A.accepting:
        C.transitions[state][None].add(b_offset)
    
    # make the accepting states B's accepting states
    C.accepting = {s + b_offset for s in B.accepting}
    return C

def star(A):
    B = Automaton(A.n_states, {0})
    for i, transitions in enumerate(A.transitions):
        for token, successors in transitions.items():
            B.transitions[i][token] |= successors
    
    for state in A.accepting:
        B.transitions[state][None].add(0)
    return B

def repeat(A, n):
    B = Automaton(1, {0})
    for _ in range(n):
        B = cat(B, A)
    return B


def trim(A):
    state_mapping = {0: 0}
    for state in range(1, A.n_states):
          if A.is_accessible(state) and A.is_co_accessible(state):
              state_mapping[state] = len(state_mapping)
    B = Automaton(len(state_mapping), set())
    for a, b in state_mapping.items():
        for token, successors in A.transitions[a].items():
            for successor in successors:
                if successor in state_mapping:
                    B.transitions[b][token].add(state_mapping[successor])
    for state in A.accepting:
        if state in state_mapping:
            B.accepting.add(state_mapping[state])
    return B
    
def epsilon_remove(A):
    epsilon_closures = [
        A.epsilon_expand({i}) for i in range(A.n_states)
    ]
    B = Automaton(A.n_states, set())
    for i in range(B.n_states):
        for closure_state in epsilon_closures[i]:
            for token, successors in A.transitions[closure_state].items():
                if token is not None:
                    B.transitions[i][token] |= A.transitions[closure_state][token]
    for state in range(B.n_states):
        if len(epsilon_closures[state] & A.accepting) > 0:
            B.accepting.add(state)
    return B

def determinize(A):
    """
    Powerset construction, probably not practical for large automata
    """
    A = epsilon_remove(A)
    B = Automaton(2**A.n_states - 1, set())
    # B's state n corresponds to the set of states defined in (n+1)'s binary representation
    accepting_mask = 0
    for state in A.accepting:
        accepting_mask |= (1<<state)
    for state in range(B.n_states):
        bitset = state + 1
        if bitset & accepting_mask:
            B.accepting.add(state)

    for i, transitions in enumerate(B.transitions):
        nondeterministic_transitions = defaultdict(set)
        bitset = i + 1
        for j in range(A.n_states):
            if bitset & (1<<j):
                for token, successors in A.transitions[j].items():
                    nondeterministic_transitions[token] |= successors
        for token, successors in nondeterministic_transitions.items():
            successor_set = 0
            for successor in successors:
                successor_set |= (1<<successor)
            transitions[token] = {successor_set - 1}
    return B
            

    
def merge(A, i, j):
    B = Automaton(A.n_states - 1, set())
    if i > j:
        i, j = j, i
    assert i != j

    a_to_b = {}

    for s_a in range(A.n_states):
        if s_a < j:
            a_to_b[s_a] = s_a
        elif s_a == j:
            a_to_b[s_a] = i
        else:
            a_to_b[s_a] = s_a - 1

    for s_a in range(A.n_states):
        s_b = a_to_b[s_a]
        if s_a in A.accepting:
            B.accepting.add(s_b)
        for token, successors_a in A.transitions[s_a].items():
            successors_b = {a_to_b[successor] for successor in successors_a}
            B.transitions[s_b][token] |= successors_b

    return B

def from_xfst(spec):
    node_ids = {}
    node_transitions = {}
    lines = []
    for line in spec.split("\n"):
        if len(lines) > 0 and line.startswith(' '):
            lines[-1] += line
        else:
            lines.append(line)
            
    for line in lines:
        if match := re.match(r"(f?s[0-9]+): *(.*)", line):
            state = match.group(1)
            node_ids[state] = len(node_ids)
            node_transitions[state] = []
            rhs = match.group(2)
            token_re = r"([^ ])*"
            for match in re.finditer("(" + token_re + ")" + r" -> (f?s[0-9]+)(, |\.)", rhs):
                token = match.group(1)
                token = token.replace('"', '')
                successor = match.group(3)
                node_transitions[state].append((token, successor))
    A = Automaton(len(node_ids), set())
    for node, transitions in node_transitions.items():
        node_id = node_ids[node]
        if node.startswith('f'):
            A.accepting.add(node_id)
        for token, successor in transitions:
            successor_id = node_ids[successor]
            A.transitions[node_id][token].add(successor_id)
    return A



def shallow_suffixes(A, state, k):
    frontier = [(state, [])]
    frontier = [(s, []) for s in A.epsilon_expand({state})]

    suffixes = set()
    
    for hop in range(k):
        for state, string in frontier:
                if state in A.accepting:
                    suffixes.add(tuple(string))

        new_frontier = []
        for state, string in frontier:
            for token, successors in A.transitions[state].items():
                if token is not None:
                    for successor in A.epsilon_expand(successors):
                        new_frontier.append((successor, string + [token]))    
        frontier = new_frontier
    for state2, string in frontier:
        string = string + [('state', state2)]
        suffixes.add(tuple(string))
    return suffixes


def shallow_prefixes(A, state, k):
    reversed_transitions = [defaultdict(set) for _ in range(A.n_states)]
    for i, transitions in enumerate(A.transitions):
        for token, successors in transitions.items():
            for successor in successors:
                reversed_transitions[successor][token].add(i)

    AT = Automaton(A.n_states, {0})
    AT.transitions = reversed_transitions

    return shallow_suffixes(AT, state, k)


def shallow_match(A, i, j, k):
    def normalize(s):
        n = []
        for token in s:
            if token == ('state', i) or token == ('state', j):
                n.append(('state', 'self'))
            else:
                n.append(token)
        return tuple(n)
    
    i_suffixes = shallow_suffixes(A, i, k)
    j_suffixes = shallow_suffixes(A, j, k)

    if {normalize(s) for s in i_suffixes} == {normalize(s) for s in j_suffixes}:
        return True
    
    i_prefixes = shallow_prefixes(A, i, k)
    j_prefixes = shallow_prefixes(A, j, k)

    return {normalize(s) for s in i_prefixes} == {normalize(s) for s in j_prefixes}

    

    
def prune(A, max_depth=4):
    if A.pruned_depth >= max_depth:
        return A
    A = epsilon_remove(A)
    A = trim(A)
    merged = True
    while merged:
        merged = False
        for k in range(1, max_depth+1):
            if merged: break
            # reverse the iteration order; in practical cases we often merge
            # high-index states first 
            for i in reversed(range(A.n_states)):
                if merged: break
                for j in reversed(range(i)):
                    if shallow_match(A, i, j, k):
                        A = merge(A, i, j)
                        merged = True
                        break
    A.pruned_depth = max_depth
    return A
        

def show(A):
    for i, t in enumerate(A.transitions):
        if i in A.accepting:
            print("*", end="")
        else:
            print(" ", end="")
        print(i, dict(t))

