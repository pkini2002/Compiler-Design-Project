# Compiler-Design-Project

### 📌 Problem Statement:

Design a lexer and parser for the following i/p grammar

```
int main()
begin
int L[10];
int maxval=L[0]; 
for i=1 to n-1 do
if L[i]>maxval
maxval=L[i];
endif
endfor
return(maxval)
End
```

### Info

- Type of parsing used: `LL(1) parsing`
- A grammar whose parsing table has no multiply-defined en- tries is said to be LL(1) which stands for: scanning the input from Left to right producing a Leftmost derivation and using 1 input symbol of lookahead at each step to make parsing action decisions.

### Steps to run the file

- Navigate to the folder where the file `cdd.py` is present
- Make sure you have Python installed in your PC
- Run the file using the command

```
python cdd.py
```

### References

- <a href="https://pypi.org/project/tabulate/">Tabulate</a>
- <a href="https://docs.python.org/3/">Python Documentation</a>
- <a href="https://www.geeksforgeeks.org/construction-of-ll1-parsing-table/">Construction of LL(1) parsing table</a>
