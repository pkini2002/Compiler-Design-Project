import re
import warnings
from tabulate import tabulate
import copy

warnings.filterwarnings("ignore")

def removeLeftRecursion(rulesDiction):
    store = {}
    for lhs in rulesDiction:
        alphaRules = []
        betaRules = []
        allrhs = rulesDiction[lhs]
        for subrhs in allrhs:
            if subrhs[0] == lhs:
                alphaRules.append(subrhs[1:])
            else:
                betaRules.append(subrhs)
        if len(alphaRules) != 0:
            lhs_ = lhs + "'"
            while lhs_ in rulesDiction.keys() or lhs_ in store.keys():
                lhs_ += "'"
            for b in range(0, len(betaRules)):
                betaRules[b].append(lhs_)
            rulesDiction[lhs] = betaRules
            for a in range(0, len(alphaRules)):
                alphaRules[a].append(lhs_)
            alphaRules.append(['#'])
            store[lhs_] = alphaRules
    for left in store:
        rulesDiction[left] = store[left]
    return rulesDiction

def LeftFactoring(rulesDiction):
    newDict = {}
    for lhs in rulesDiction:
        allrhs = rulesDiction[lhs]
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        new_rule = []
        tempo_dict = {}
        for term_key in temp:
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                lhs_ = lhs + "'"
                while lhs_ in rulesDiction.keys() or lhs_ in tempo_dict.keys():
                    lhs_ += "'"
                new_rule.append([term_key, lhs_])
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                new_rule.append(allStartingWithTermKey[0])
        newDict[lhs] = new_rule
        for key in tempo_dict:
         newDict[key] = tempo_dict[key]
    return newDict

def first(rule):
    global rules, nonterm_userdef, term_userdef, diction, firsts
    if len(rule) != 0 and (rule is not None):
        if rule[0] in term_userdef:
            return rule[0]
        elif rule[0] == '#':
            return '#'
    if len(rule) != 0:
            if rule[0] in list(diction.keys()):
                fres = []
                rhs_rules = diction[rule[0]]
                for itr in rhs_rules:
                    indivRes = first(itr)
                    if type(indivRes) is list:
                        for i in indivRes:
                            fres.append(i)
                    else:
                        fres.append(indivRes)
                if '#' not in fres:
                        return fres
                else:
                        newList = []
                        fres.remove('#')
                        if len(rule) > 1:
                            ansNew = first(rule[1:])
                            if ansNew != None:
                                if type(ansNew) is list:
                                    newList = fres + ansNew
                                else:
                                    newList = fres + [ansNew]
                            else:
                                newList = fres
                        fres.append('#')
                        return newList

def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    solset = set()
    if nt == start_symbol:
        solset.add('$')
    for curNT in diction:
        rhs = diction[curNT]
        for subrule in rhs:
            if nt in subrule:
                while nt in subrule:
                    index_nt = subrule.index(nt)
                    subrule = subrule[index_nt + 1:]
                    if len(subrule) != 0:
                     res = first(subrule)
                     if '#' in res:
                        newList = []
                        res.remove('#')
                        ansNew = follow(curNT)
                        if ansNew != None:
                            if type(ansNew) is list:
                                newList = res + ansNew
                            else:
                                newList = res + [ansNew]
                        else:
                            newList = res
                        res = newList

                    else:
                     if nt != curNT:
                        res = follow(curNT)

                    if res is not None:
                            if type(res) is list:
                                for g in res:
                                    solset.add(g)
                            else:
                                solset.add(res)

    return list(solset)


def computeAllFirsts():
    global rules, nonterm_userdef, term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs
    # Open a file named rules.txt in write mode
    with open('rules.txt', 'w') as file:
        file.write("Rules:\n")
        for y in diction:
            file.write(f"{y} -> {diction[y]}\n") 
    diction = removeLeftRecursion(diction)
    diction = LeftFactoring(diction)
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        firsts[y] = t

    print("============================================================================================")
    print("\nCalculated firsts: ")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
     print(f"first({key_list[index]}) "f"=> {firsts.get(gg)}")
     index += 1    

def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset
    print("\nCalculated follows: ")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
     print(f"follow({key_list[index]})"f" => {follows[gg]}")
     index += 1    

def createParseTable():
    global diction, firsts, follows, term_userdef
    print("\n")
    print("============================================================================================")
    print("Firsts and Follow Result table")
    mx_len_first = 0
    mx_len_fol = 0
    for u in diction:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2
    print(tabulate([["Non-T", "FIRST", "FOLLOW"]] + [[u, str(firsts[u]), str(follows[u])] for u in diction], headers='firstrow', tablefmt='fancy_grid'))

    print("\n")
    print("============================================================================================")

    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    terminals.remove('(')
    terminals.remove(')')
    terminals.remove('+')
    terminals.remove('-')
    terminals.remove('=')
    terminals.remove('1')
    terminals.append('$')
    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        mat.append(row)
    grammar_is_LL = True
    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
            if '#' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('#')
                    res = list(res) + list(follows[lhs])
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = f"{lhs}->{' '.join(y)}"
                else:
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] \
                            + f",{lhs}->{' '.join(y)}"

    with open('parsingtable.txt', 'w', encoding='utf-8') as file:
        file.write("Generated parsing table:\n")
        headers = [""] + terminals
        rows = [[ntlist[j]] + y for j, y in enumerate(mat)]
        file.write(tabulate(rows, headers, tablefmt='fancy_grid'))


    return (mat, grammar_is_LL, terminals)


def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, input_string, term_userdef, start_symbol):
    with open('parsing.txt', 'w') as file:
        # file.write(f"Validate String:\n{input_string}\n")
        print(f"Validate String:\n\n{input_string}\n")
        print("Look into the parsing.txt file for the parsing steps")
        print("\n")
        if grammarll1 == False:
            file.write(f"Input String = \"{input_string}\"\nGrammar is not LL(1)\n")
        stack = [start_symbol, '$']
        buffer = []
        input_string = input_string.split()
        input_string.reverse()
        buffer = ['$'] + input_string
        file.write("{:>70} {:>10} {:>20}\n".format("Input\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", "Stack\t\t", "Action"))
        while True:
            if stack == ['$'] and buffer == ['$']:
                file.write("{:>100} | {:>25} | {:>30}\n".format(' '.join(buffer), ' '.join(stack), "Valid"))
                return "Valid String!"
            elif stack[0] not in term_userdef:
                x = list(diction.keys()).index(stack[0])
                y = table_term_list.index(buffer[-1])
                if parsing_table[x][y] != '':
                    entry = parsing_table[x][y]
                    file.write("{:>100} | {:>25} | {:>30}\n".format(' '.join(buffer), ' '.join(stack), f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                    lhs_rhs = entry.split("->")
                    lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                    entryrhs = lhs_rhs[1].split()
                    stack = entryrhs + stack[1:]
                else:
                    file.write(f"Invalid String! No rule at Table[{stack[0]}][{buffer[-1]}]\n")
                    return "Invalid String! No rule at Table[{stack[0]}][{buffer[-1]}]"
            else:
                if stack[0] == buffer[-1]:
                    file.write("{:>100} | {:>25} | {:>30}\n".format(' '.join(buffer), ' '.join(stack), f"Matched1:{stack[0]}"))
                    buffer = buffer[:-1]
                    stack = stack[1:]
                else:
                    file.write("Invalid String! Unmatched terminal symbols\n")
                    return "Invalid String! Unmatched terminal symbols"

sample_input_string = None
inps = ''
with open('input.txt', 'r+') as f:
    for line in f.readlines():
        inps += line
sample_input_string = inps
arr1 = inps.split()[4]
id = inps.split()[7]
arr2 = inps.split()[9]
arr3 = inps.split()[21]
print(inps.split())
x = re.search("^[a-zA-Z][a-zA-Z0-9_]*", id)
if not x:
    print("Invalid identifier")
    exit(1)
y = re.search("^[a-zA-Z][a-zA-Z0-9_]*[[0-9]+]", arr1)
if not y:
    print("Invalid array name")
    exit(1)
z = re.search("^[a-zA-Z][a-zA-Z0-9_]*[[0-9]+]", arr2)
if not z:
    print("Invalid initialization")
    exit(1)
zz = re.search("^[a-zA-Z][a-zA-Z0-9_]*[[a-z]+]", arr3)
if not zz:
    print("Invalid index")
    exit(1)
rules = [
    "S -> T M B A D",
    "T -> int",
    "M -> main()",
    "B -> begin",
    "D -> End",
    "A -> E F G W X",
    "E -> T " + arr1 + " ;",
    "F -> T " + id + " = " + arr2 + " ;",
    "G -> for C do",
    "C -> i = 1 to n - 1",
    "W -> if " + arr3 + " > " + id + " P Q R",
    "P -> " + id + " = " + arr3 + " ;",
    "Q -> endif",
    "R -> endfor",
    "X -> return ( " + id + " )"
]
nonterm_userdef = ['S', 'T', 'M', 'B', 'D', 'A', 'E', 'F', 'K', 'Z', 'G', 'W', 'P', 'Q', 'R', 'X', 'C']
term_userdef = [id, arr1, arr2, arr3, 'n', 'int', 'main()', 'End', 'for', 'if', 'begin', 'do', 'i', 'to', '(', ')', '+', '-', 'endif', 'endfor', 'return', '>', '=', '1', ',', ';']
diction = {}
firsts = {}
follows = {}

computeAllFirsts()
start_symbol = list(diction.keys())[0]
computeAllFollows()

(parsing_table, result, tabTerm) = createParseTable()
if sample_input_string != None:
  validity = validateStringUsingStackBuffer(parsing_table, result,
  tabTerm, sample_input_string,term_userdef, start_symbol)
  print(validity)
else:
    print("No input String detected")
