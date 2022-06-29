

#### ABSTRACT
In the field of compiling, how to justfy the validability and parse a CFG language is often of great concern. Applying forward chaining during inferencing and backward chaining in explaination, the rule-based expert system "LL-1 Helper" introduced here serves the purpose of checking whether a CFG language is LL(1) parsable, and presenting its parsing table and other side products accordingly. "LL-1 helper" features easy usage and concise output, while perserving key information inferenced along the process in a process logging window. Detailed back-chained explanation facility is also a highlight which applys to literally every single rule logged. With both back-end and UI written in Python, the system is cross-platform with dependency on python environment only. When fed with varying scale test sets, "LL-1 helper" consistently gives out accrate results with a satisfying responding time. 


#### 1. BACKGROUND 
Before we start, here are some key concepts for your reference concerning grammar. Take a look if you are not familiar with compiler theory.
* terminal symbol & non-terminal symbol
From Wikipedea: "Terminal symbols are literal symbols that may appear in the outputs of the production rules of a formal grammar and which cannot be changed using the rules of the grammar."
and:
"Nonterminal symbols are those symbols that can be replaced. They may also be called simply syntactic variables. A formal grammar includes a start symbol, a designated member of the set of nonterminals from which all the strings in the language may be derived by successive applications of the production rules."

* LL grammar
From wikipedea:"In formal language theory, an LL grammar is a context-free grammar that can be parsed by an LL parser, which parses the input from left to right, and constructs a leftmost derivation of the sentence. "

* LL(1) grammar
During the above parsing process, if a grammar can be uniquely parsed by peeking one symbol ahead, then this grammar is called LL(1) grammar.

* LL parsing table
A two-dimensional table derived from a LL grammar where each table entry (X,y) indicate the available rule to choose from for non-terminal symbol X on encountering terminal y.

* LL grammar rule
A common grammar rule is often in the form $A$ -> $a$ where $a$ is a combination of terminal and non-terminal. It indicates that if the current left-hand-side symbol is A, it can be replaced by $a$.

* reduce
The process of replacing non-terminals with the right-hand-side of their grammar rule, causing fewer non-terminals in the resulting production formula is called reduce. This step in primarily used in the inference section(see part)

* left-recursion
From Wikipedea: "left recursion is a special case of recursion where a string is recognized as part of a language by the fact that it decomposes into a string from that same language and a suffix."
Simply put, left-recursion occurs when grammar rules as "A -> A$\alpha$" exists. This is bound to introduce duplicity to the parsing table, thus grammar with commin prefix is not LL(1).


* common prefix
Common prefix occurs when two grammar rules of the same non-terminal share the same prefix. This is bound to introduce duplicity in the parsing table, thus grammar with commin prefix is not LL(1).


#### 2. INCENTIVE

While learning compiler theory, I found myself constantly checking the LL(1) status of a grammar by hand. This checking routine is highly repetitive and notably suitable for automization. Moreover the rule reducing process very much simulates the inferencing mechanism in expert system. So why not build a helper expert system on LL(1) grammar to make my life easier? And here it comes "LL-1 helper".

#### 3. FUNCTIONALITY
To summarize, "LL-1 helper" works as:
1. LL(1) grammar checker on CFG language
2. LL(1) parsing table generator

In other words, on the target grammar, "LL-1 helper" will first tell you whether it is a LL(1) grammar, then generate its parsing table.(Exceptions may apply in cases as left-recursion and common prefix)


#### 4. SYSTEM STRUCTURE (USER's PERSPECTIVE)
"LL-1 helper" mainly consists of three parts:
1. input section
2. inference section
3. explaination section

##### 4.1 INPUT SECTION
User need to input a CFG grammar as object. The format for the input is specified and displayed by the system. 
On wrong input format, the input will not be accepted and an error message indicating detailed error type will be displayed.
If the input grammar passes the format checking, the grammar will be read and interpreted.
The grammar consists of three parts: start symbol, grammar rules and terminal-symbols. For a grammar rule $A$ -> $\alpha$, it is represented in the system as:

IF left is $A$   
THEN right produces $\alpha$


##### 4.2 INFERENCE SECTION
Once the grammar is interpreted, the inferencing chain starts.

The inference stage consists of 7 parts:

###### 4.2.1. check left-recursion and common prefix

When either of these two special cases occurs, the grammar is definitely not LL(1) because both of them introduces duplicity (and eventually conflict when doing actual parsing) to the parsing table. In the case the system terminates here, no further inferenceing progress will be issued.
Otherwise the control flows to the nexts section.

###### 4.2.2. rule reducing

This is the part where the reducing techique is used. Each time a different non-terminal being picked out for launching reducing is called an iteration. Reduce is available if:
* There exits a non-terminal, say X, with only terminal symbols as the first symbol on the right hand-side all of its latest grammar rules. Here latest means(possibly) having been applied with other reduction.
* $X$ has a production like:

IF left is $X$  
THEN right produces $x$

* There exits a grammar rule in the latest rule base, say:

IF left is $A$ 
THEN right produces $\alpha$ $X$ $\theta$

where $\alpha$ and $\theta$ can be any combination of symbols

Then we can replace the $B$ in the grammar rule with the production of $X$, resulting in new rule:

IF left is A   
THEN right produces $\alpha$ $x$ $\theta$


Rule inferencing terminates if there is no new rule fired in the last round of iteration.

###### 4.2.3. construct first sets

In this section we collect all the first right-hand-side terminal-symbol from all rules fired for each non-terminal repectively.

###### 4.2.4. construct nullable 

A symbol is said to be nullable if it has empty symbol in its first set. All terminal symbols except empty symbol itself are not nullable.

###### 4.2.5. construct follow sets

In this section we collect all the terminal-symbols immediately after the target non-terminal from all rules fired for each non-terminal repectively.

###### 4.2.6. construct parsing table

The constructing process assigns the basic rules(the original grammar rules, not the inferenced rules) to the designated block. For each block entry $(A,a)$(where $A$ is non-terminal symbol and $a$ terminal symbol), assign basic rule $A$ -> $\theta$ to it if:
* a is in the first set of $\theta$
or 
* $\theta$ is nullable and $a$ is in $A$'s follow set

###### 4.2.7. result of validation

Based on whether duplicity exists in the parsing table, the final rule of inference tell whether this grammar is LL(1) parsable.



Throughout this section, all the new inferenced rules will be:

* logged on the progess window for user's quick reference
* written into an external file for further usage

##### 4.3 EXPLANATION SECTION

As the progress window only contain key points during inference, user might expect more detailed and targeted explanation for the rules fired. Futhermore the progress window tends to present hundred or thousands of logging information so it's basically hard to follow the logic chain of the rule under query. So here's why explanation facility come into being.
Each time a rule number is entered, the explanation facility travels backward, tracing every rule number on the logic inference chain until a self-explanable rule is met. For each rule number encountered along the chain, a brief explanation sentence is presented accounting for the relation between the current rule and its antecedent(s).
Considering the user group of "LL-1 helper" should to some extent be familiar with the basic LL grammar inference tricks, the "brief introduction" at each rule along with logic chain output should suffice to do the explanation.


#### 5. SYSTEM STRUCTURE (MAINTAINER's PERSPECTIVE)

This section gives a brief introduction to the essential back-end structure and coding logic of the system for developer and maintainer's reference.
According to the structure specified by Newell and Simon, a rule-based expert system consists of five parts:rule base, fact, inference engine, explanation facility and user interface. 

* rule base: In the case of "LL-1 helper", the rule base is orginally just a set of reducing and checking rules. No detailed grammar resides in the original rule base. Only after reading facts(user's grammar input) does the actual grammar symbols come into rule base.
The whole inferencing process is built upon the rule base and the content of the progress window comes exclusively from the rule base.

* fact: For convenience here "fact" has two forms: the raw user input form, and the interpreted form presented as "basic rules". The interpreted form conforms to the standard rule format of the rule base(IF THEN format), while the raw user input meets the grammar checking critiques only. Seperating these two forms have the following benefits:

1. Easy user experience. User don't need to meet the strict format restrictions during input(the grammar checking is much more friendlier)
2. Stand alone formatting. Developer control the output format of rules independent of the user input.
3. Convenient input restore. On editing, the system simplicty switch back the original user input for modification.
4. Quick reference. The formated basic rules are displayed along side the progress window for user's handy reference.

* inference engine: As is already explained upon in part 4.2. One more thing to clarify is that in order to parse rules of unknow characters in the rule base(where the symbol characters are primarily defined by user), the python regex library is used and unified rule formatting is hence a must.

* explanation facility: To achieve the effect of quick logic chain tracing, a special data structure is build and maintained during previous courses, name it "explanation tree". Each node on the tree consists of: the rule number this node represents, the message string explaining the firing logic of the current node, and a list of "pointers" to the rules producing this rule. Every time a new rule is fired, whatever section it is in, the data structure creates a new node binding the currently fired rule number with a brief explanation message and a list of logicaly antecedent rules numbers. 
The method of constructing explanation message string and finding antecedent rule numbers are slighty different for each part in the inference section. For example: during rule reducing part each new fired rule has two antecedents: a grammar rule being replaced and a grammar rule used for replacing. And the explanation message would be something like "Reducing rule a with rule b resulting in c". While in first set construction part the explanation tree node would need to record every grammar rule number which gives out the first symbol, and build a message string similar to "Member of rule X's first set found in rules a,b,c,d accordingly."
To generate explanation for a specified rule number, the work is done recursively: first output the message on the current node, then one by one recurse on its antecedents in a depth-first manner. The recursion terminates on self-explanable rules, whose antecedent rule number is "-1". Code snippet as below:

```
def recurse_explain(self,num):
    # -1 as num means reaching end of recursion(self-explanable rules)
    if num == -1:
        return

    # read content of rule indicated by rule num from rule base
    rule_content = self.get_rule_from_base(num)

    # write to explanation section
    self.explain_text.insert(tkinter.END,"\n\n"+str(num)+". "+rule_content+"\n"+self.short_break_line+self.explain_rules[num][1])

    # recurse on num on logic recursion path
    for n in self.explain_rules[num][0]:
        self.recurse_explain(n)
```


* user interface: see section 6.

#### 6. USER INTERFACE

The GUI of "LL-1 helper" is build with the python CustomtKinter library.




#### 7. OTHER STATEMENTS

##### 7.1 INPUT ACCURACY

One thing that makes expert systems special is that it allows for inaccurate input: even with fuzzy input it goes on. However that's not the case with "LL-1 helper" where the input must satisfy grammar checking before being accepted. While seems like a violation of convention, the necessity of grammar checking is bound to the system's purpose: deal with grammar, which itself resides on accrate symbol and semantic representation. Considering the scope of usage, I think most users would rather be caught by grammar checking at the first place than getting a false judgement or mal parsing result.

##### 7.2 FILE OUTPUT 

The parsing table and inferencing results will be found in a file in the system folder, default name "rules.txt"



#### REFERENCES
1. Wikipedea
2. CustomtKinter doc at:https://github.com/TomSchimansky/CustomTkinter
3. Artificial Intelligence: a Guide to Intelligent Systems by Michael Negnevitsky
