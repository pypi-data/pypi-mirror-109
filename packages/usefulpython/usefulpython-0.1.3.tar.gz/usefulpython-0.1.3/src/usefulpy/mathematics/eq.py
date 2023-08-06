'''
File: eq.py
Version: 2.1.5
Author: Austin Garcia

This program stores the 'eq' class. It takes a string of an expression of a
function and returns an 'eq' object, which can be called with a number which
replaces the variable with a number.

Note: I originally created this for a specific sceneario in a graphing program
I created that used this to make a turtle graph an input equation. While I am
sure that there are other practical uses for this, some areas are only develope
as necessary within the original program, though I have attempted to broaden its
abilities.

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
0
 0.1
  Version 0.0.0
   eq is stored as a function with a list as a non-positional argument that
   defaults to the data, this equation is returned from a function 'make_eq'
  Version 0.0.1
   some bug fixes and whatnot.
 0.1
  Version 0.1.0
   Things moved around, a few new functions added
1
 1.0
  1.0.0
   Swiched to using a class for eq. Everything has been moved around. More
   efficient and elegant code
  1.0.1
   added 'prepare' and 'create' to avoid small bugs. added 'translations',
   'constants', and 'mathfuncs' for same reason 
  1.0.2
   eq class is now callable, a small bugfix or two.
   added to the usefulpy module
  1.0.3
   Really, really small bugfixes, and thus small improvements in quality.
  1.0.4
   Hopefully fixed a couple elusive bugs...
   Improvement with 'create' and involving function.
   Functions are addable.
  1.0.5
   Bugfixes... made to work with nmath > 2.1.1
   more functions
 1.1
  1.1.0
   Calculus foundations being laid... adding the 'derivate'
'''
##UPDATEME: Unreviewed for Usefulpy 1.2.1
##TODO: Update for use with eval.
##POSSIBLYOBSOLETE: Probably obsolete? May be removed later?
__author__ = 'Austin Garcia'
__version__ = '1.1.0'

import warnings
warnings.warn(DeprecationWarning('Module "eq" is out of date, and will soon be removed'))

from .nmath import *

from .. import validation as _validation
from .. import formatting
import copy

def derivate(eq, at):
    return (eq(at+1e-10)-eq(at))/1e-10

translations = {'cos':'\\cos ', 'sin':'\\sin ', 'tan':'\\tan ', 'sec':'\\sec ',
                'csc':'\\csc ', 'cot':'\\cot ', 'arc\\sec': '\\arcsec ', 'arc\\csc':'\\arccsc ',
                'arc\\cot':'\\arccot ', 'arc\\cos':'\\arccos ', 'arc\\sin':'\\arcsin ',
                'sqrt': '\\sqrt ', 'cbrt':'\\cbrt ', 'rt': '\\rt ',  'arc\\tan':'\\arctan ',
                'log':'\\log ', 'ln':'\\ln ', 'π':'\x0epi ', 'τ':'\x0etau ',
                'e':'\x0ee ', 'Φ': '\x0ephi ', 'φ':'\x0elphi ', 'ρ': '\x0erho ',
                'σ': '\x0esigma ', 'ς': '\x0elsigma ', 'κ': '\x0ekappa ',
                'ψ': '\x0epsi ', '**':'^', '\\sq\\rt':'\\sqrt', '\\cb\\rt':'\\cbrt',
                'floor':'\\floor ', 'c\x0ee il':'\\ceil ', 'd\x0ee rivat\x0ee ':'\\derivate ',
                '\\s\x0ee c':'\\sec ', '\\arcsec ':'\\arcs\x0ee c '}

constants = {'\x0epi': π, '\x0etau': τ, '\x0ee': e, '\x0ephi': φ, '\x0elphi': φ_,
             '\x0erho': ρ, '\x0ekappa': κ,
             '\x0epsi': ψ}
mathfuncs = {'\\cos': (cos, (1,)), '\\sin': (sin, (1,)), '\\tan': (tan, (1,)),
             '\\arccos': (acos, (1,)), '\\arcsin': (asin, (1,)),
             '\\arctan' : (atan, (1,)), '\\log': (log, (1, (2, ))),
             '\\ln': (ln, (1,)), '\\sqrt': (sqrt, (1,)), '\\cbrt':(cbrt, (1,)),
             '\\rt':(rt, (-2, 1)), '\\floor':(floor, (1, )), '\\ceil':(ceil, (1,)),
             '\\sec': (sec, (1,)), '\\csc': (csc, (1,)), '\\cot': (cot, (1,)),
             '\\arcsec': (asec, (1,)), '\\arccsc': (acsc, (1,)),
             '\\arccot' : (acot, (1,)), '\\derivate':(derivate, (1, 'var'))}
parenthesis = '()'
digits = '0.123456789'
operations = '^+-*/'
implied = 'im*'

fns = {}

def create(text):
    if type(text) == eq:
        return copy.deepcopy(text)
    text = text.replace(' ', '')
    while '--' in text: text = text.replace('--', '+')
    while '++' in text: text = text.replace('++', '+')
    while '+-' in text: text = text.replace('+-', '-')
    while '-+' in text: text = text.replace('-+', '-')
    text = text.replace('**', '^')
    var = None
    try:
        if text[1] == '(' and text[3:5] == ')=':
            var = text[2]
            fnnm = text[0]
            text = text[5:]
    except: pass
    text = formatting.translate(text, translations)
    ntext = ''
    fn = False
    for x in text:
        if fn:
            if x == ' ': fn = False
            if x in digits: ntext += ' ' + x
            else: ntext += x
        else:
            if x in ('\\', '\x0e'):
                ntext += x
                fn = True
            elif x not in digits: ntext += ' '+x+' '
            else: ntext+= x
    if text.startswith('-'): text+='0 '
    text = (ntext+' ').replace('  ', ' ')
    neq = eq(text, var)
    try: fns[fnnm] = neq
    except: pass
    return neq

class eq(object):
    def __init__(self, text, var = None):
        ''' creates a function from text that can be solved for a single
variable while slower compared to a regular function, it has the ability to
create this from *input* which is what makes it useful'''
        parameter = None
        if type(text) == self.__class__:
            self = copy.deepcopy(text)
            return
        if '"' in text:
            index = text.index('"')
            text = text[:index]
            del index
        if '{' in text:
            index = text.index('{')
            text, parameter = text[:index], text[index:]
            del index
        self.text = text+' '
        self.ParameterText = parameter
        self.parameter = self.makeParameter()
        self.var = var
        self.neq = self.makeEq()
        self.solved = False
        self.value = None
        if self.var is None:
            self.value = self.solve(0)
            self.solved = True

    def makeParameter(self): return NotImplemented #Working on it

    def __eq__(self, other):
        if type(other) != self.__class__: return False
        return self.neq == other.neq

    def makeEq(self):
        text = self.text
        if text.count('(') != text.count(')'):
            raise SyntaxError('Parenthesis nesting error occured')
        nlist = []
        runstr = ''
        depth = 0
        var = self.var
        fn = False
        na = 'na' #To avoid errors regarding '-' placed first
        prevtype = na #To avoid 'implied multiplication' leading to errors
        num = 'num' #support for prevtype
        oper = 'oper'#support for prevtype
        va = 'var' #support for prevtype
        f = 'fn'#support for prevtype
        c = 'special'#support for prevtype
        p = '()'
        for char in text:
            if depth == 0:
                if char == ')':
                    raise SyntaxError('Parenthesis nesting error occured')
                elif char == '(':
                    depth += 1
                    if runstr != '':
                        if runstr == '-':
                            nlist.append(-1)
                            prevtype = num
                        else:
                            nlist.append(runstr)
                            if _validation.is_float(runstr): curtype = num
                            elif runstr in operations: curtype = oper
                            elif runstr.startswith('\\'): curtype = f
                            elif runstr.startswith('\x0e'): curtype = c
                            else:
                                if var == None:
                                    if runstr.startswith('-'):
                                        var = runstr[1:]
                                    else:
                                        var = runstr
                                    curtype = va
                                elif runstr == var or (runstr == '-'+var): curtype = va
                                else: raise SyntaxError(runstr + ' seems to be an invalid character')
                            prevtype = curtype
                    if prevtype in (va, num, c, p):
                        nlist.append(implied)
                    nlist.append(_validation.trynumber(runstr))
                    runstr = '('
                elif char == ' ':
                    if runstr != '':
                        if _validation.is_float(runstr): curtype = num
                        elif runstr in operations: curtype = oper
                        elif runstr.startswith('\\'): curtype = f
                        elif runstr.startswith('\x0e'): curtype = c
                        else:
                            if var == None:
                                if runstr.startswith('-'):
                                    var = runstr[1:]
                                else:
                                    var = runstr
                                curtype = va
                            elif runstr == var or (runstr == '-'+var): curtype = va
                            else: raise SyntaxError(runstr + ' seems to be an invalid character')
                        if prevtype in (va, num, c, p):
                            if curtype == oper: pass
                            else: nlist.append(implied)
                        if runstr == '-' and prevtype == na: pass
                        elif runstr == '-' and prevtype == oper: pass
                        else: nlist.append(_validation.trynumber(runstr)); runstr = ''
                        prevtype = curtype
                        if fn: fn = False
                elif char == '\\' or char == '\x0e':
                    fn = True
                    if runstr != '':
                        if _validation.is_float(runstr): curtype = num
                        elif runstr in operations: curtype = oper
                        elif runstr.startswith('\\'): curtype = f
                        elif runstr.startswith('\x0e'): curtype = c
                        else:
                            if var == None:
                                if runstr.startswith('-'):
                                    var = runstr[1:]
                                else:
                                    var = runstr
                                curtype = va
                            elif runstr == var or (runstr == '-'+var): curtype = va
                            else: raise SyntaxError(runstr + ' seems to be an invalid character')
                        if prevtype in (va, num, c, p):
                            if curtype == oper: pass
                            else: nlist.append(implied)
                        prevtype = curtype
                    nlist.append(_validation.trynumber(runstr))
                    runstr = char
                elif fn:
                    runstr += char
                elif char in operations:
                    runstr = char
                else:
                    if runstr == '':
                        runstr += char
                    elif _validation.is_float(runstr) or runstr == '-' or runstr == '.' or runstr == '-.':
                        if _validation.is_float(char) or char == '.':
                            runstr += char
                        elif runstr == '-':
                            runstr += char
                        else:
                            nlist.append(_validation.trynumber(runstr))
                            nlist.append(implied)
                            runstr = char
                    elif _validation.is_float(char):
                        nlist.append(_validation.trynumber(runstr))
                        nlist.append(implied)
                        runstr = char
                    else: runstr += char
            else:
                runstr += char
                if char == ')': depth -= 1
                elif char == '(': depth += 1
                if depth == 0:
                    ceq = eq(runstr[1:-1])
                    if ceq.solved: ceq = ceq.value
                    elif var == None: var = ceq.var
                    else:
                        if ceq.var != var: raise SyntaxError(ceq.var + ' seems to be an invalid character')
                    nlist.append(ceq)
                    prevtype = p
                    runstr = ''
        self.var = var
        if nlist[0] == '+': nlist = nlist[1:]
        nlist = formatting.scour(nlist)
        if len(nlist) == 1 and (type(nlist[0]) is self.__class__):
            nlist = nlist[0].neq
        return nlist

    def __repr__(self):
        if self.solved:
            return '('+str(self.value)+')'
        nneq = []
        for n in self.neq:
            if _validation.is_float(n) and ('e' in str(n)):
                n = str(n)
                negative = n.startswith('-')
                if negative: n = n[1:]
                power = n[n.index('-')+1:]
                fnm = n[:n.index('-')-1]
                qlen = len(fnm)
                nneq.append('0.'+('0'*(int(power)-qlen))+fnm)
            else: nneq.append(n)
        reprtranslate = {'[':'(', ']':')', ',':'', "'":'', '\\':'', ' im* ':''}
        nrepr = formatting.translate(str(nneq), reprtranslate)
        return nrepr

    def solve(self, value):
        if self.solved: return self.value
        Nlist = self.neq.copy()
        def d(Nlist):
            while '\\derivate' in Nlist:
                count = 1
                for x in Nlist.copy():
                    if x == '\\derivate':
                        if type(Nlist[count]) is self.__class__:
                            Nlist[count-1:count+1] = [derivate(Nlist[count], value)]
                        elif Nlist[count]== self.var:
                            Nlist[count-1:count+1] = 1
                        else: Nlist[count-1:count+1] = 0
                        break
                    count += 1
            return Nlist
                    
        def s(Nlist):
            count = 0
            for x in Nlist.copy():
                if self.var != None:
                    if x == self.var:
                        Nlist[count] = value
                    if x == ('-'+self.var):
                        Nlist[count] = 0-value
                if type(x) == str:
                    if x in constants:
                        Nlist[count] = constants[x]
                count += 1
            return Nlist
        def p(Nlist):
            count = 0
            for x in Nlist.copy():
                if type(x) is self.__class__:
                    Nlist[count] = x.solve(value)
                count +=1
            return Nlist
        def e(Nlist):
            while '^' in Nlist:
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    try:
                        if prev1 == '^':
                            Nlist[count-3:count] = [prev2**x]
                            break
                    except: pass
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def imp(Nlist):
            while (implied in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == implied:
                        if _validation.is_float(prev2) and _validation.is_float(x):
                            Nlist[count-3:count] = [prev2*x]
                            break
                        else: pass
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def f(Nlist):
            #see mathfuncs
            def done(Nlist):
                for x in Nlist:
                    if (type(x) is str) and (x.startswith('\\')):
                        return False
            while not done(Nlist):
                index = 0
                for x in Nlist.copy():
                    if (type(x) is str) and (x.startswith('\\')):
                        if Nlist[index+1] == '^':
                            Nlist.pop(index+1)
                            power = Nlist.pop(index+1)
                        else: power = 1
                        funcdata = mathfuncs[x]
                        fx = funcdata[0]
                        pardata = funcdata[1]
                        args = []
                        
                        for datum in pardata:
                            if datum == 'var': args.append(value)
                            else: args.append(Nlist[index+datum])
                        
                        nvalue = fx(*args)
                        pardata = list(pardata)
                        pardata.append(0)
                        spacer = (min(pardata), max(pardata))
                        Nlist[index+spacer[0]:1+index+spacer[1]] = [nvalue**power]
                    index +=1
                else: break
            return Nlist
        
        def m(Nlist):
            while ('*' in Nlist) or ('/' in Nlist) or (implied in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '*' or prev1 == implied:
                        Nlist[count-3:count] = [prev2*x]
                        break
                    elif prev1 == '/':
                        Nlist[count-3:count] = [prev2/x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def a(Nlist):
            while ('+' in Nlist) or ('-' in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '+':
                        Nlist[count-3:count] = [prev2+x]
                        break
                    elif prev1 == '-':
                        Nlist[count-3:count] = [prev2-x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def b(Nlist):
            while len(Nlist) != 1:
                prev = ''
                count = 0
                for x in Nlist.copy():
                    if _validation.is_float(x) and _validation.is_float(prev):
                        if x < 0:
                            Nlist[count-1:count+1] = [prev+x]
                            break
                        else:
                            Nlist[count-1:count+1] = [prev*x]
                            break
                    elif prev == '-' and _validation.is_float(x):
                        Nlist[count-1, count] = [-x]
                        break
                    count += 1
                    prev = x
                else: break
            return Nlist
        OOP = 'dspifemab'
        oop = {'d':d, 's': s, 'p':p, 'f':f, 'i': imp, 'e':e, 'm': m, 'a':a, 'b':b}
        for op in OOP:
            Nlist = oop[op](Nlist)
        if len(Nlist)==1:
            return _validation.trynumber(Nlist[0])
        else:
            raise ValueError(Nlist)

    def derivate(self):
        return (self(create('x+0.000000000000000000000000000001'))-self(create('x')))/create('0.000000000000000000000000000001')
    
    def __call__(self, num):
        if _validation.is_float(num):
            return self.solve(num)
        if type(num) == self.__class__:
            nstr = formatting.translate(repr(self), {self.var: repr(num), ('-'+self.var):repr(0-num)})
            return create(nstr)

    def __str__(self):
        return repr(self)

    def __add__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self)[1:-1])+' + '+(repr(other)[1:-1]))

    def __radd__(self, other):
        return self+other

    def __mul__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self))+(repr(other)))

    def __rmul__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(other))+(repr(self)))

    def __sub__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self))+'-'+(repr(other)))

    def __truediv__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self))+'/'+(repr(other)))

    def __rsub__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(other))+'-'+(repr(self)))

    def __rtruediv__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(other))+'/'+(repr(self)))

#eof
