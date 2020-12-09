# -----------------------------------------------------------------------------
# ArielBM
# 03-12-2020
#
# Gramática Recursiva Por La Izquierda Para la Tarea 1
# -----------------------------------------------------------------------------


tokens = (
    'PARE_I',
    'PARE_D',
    'MAS',
    'MULTI',
    'DIGITO',
    'N'
)


#TOKENS
t_PARE_I = r'\('
t_PARE_D = r'\)'
t_MAS = r'\+'
t_MULTI = r'\*'
t_N = r'n'


#DEFINICIÓN 

def t_DIGITO(t):

    r'\d+'
    try:
        t.value = int(t.value)

    except ValueError:
        print('El valor ingresado es demasiado grande %d', t.value)
        t.value = 0
    
    return t


# CARACTERES IGNORADOS
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# CONSTRUCCIÓN DEL ANALIZADOR LÉXICO
import ply.lex as lex
lexer = lex.lex()



#DEFINIENDO LA PRECEDENCIA DE LOS OPERADORES
precedence = (
    ('left','MAS'),
    ('left','MULTI')
)


#IMPORTACIÓN DE GRAPHVIZ
from graphviz import Digraph
ast = Digraph('AST', filename='c:/source/ast.gv', node_attr={'color': 'white', 'fillcolor': 'white','style': 'filled', 'shape': 'record'})
ast.attr(rankdir='BT',ordering='in')
ast.edge_attr.update(arrowhead='none')
contador = 1
tag = 'N'


#GRAMÁTICA
def p_produccion0(t):
    ''' L   : E N'''

    global contador

    n1 = tag + str(contador)
    contador = contador + 1

    n2 = tag + str(contador)
    contador = contador + 1

    ast.node(n1, 'L.val = ' + str(t[1]['valor']) )
    ast.node(n2, '<<b>n</b>>' )

    ast.edge(t[1]['nombre'],n1)
    ast.edge(n2,n1)

    ast.render('grafo', format='png', view=True)


def p_produccion1(t):
    ''' E   : E MAS T
            | T '''

    global contador
    if len(t) == 2:
        
        n1 = tag + str(contador)
        contador = contador + 1

        ast.node(n1, 'E.val = ' + str(t[1]['valor']) )
        ast.edge(t[1]['nombre'],n1)

        t[0] = { 'valor' : t[1]['valor'], 'nombre' : n1 }

    else:

        n1 = tag + str(contador)
        contador = contador + 1
        n2 = tag + str(contador)
        contador = contador + 1

        ast.node(n1, '+' )
        ast.node(n2, 'E.val = ' + str(t[1]['valor']+t[3]['valor']) )

        ast.edge(t[1]['nombre'],n2)
        ast.edge(n1,n2)
        ast.edge(t[3]['nombre'],n2)

        t[0] = { 'valor' : t[1]['valor']+t[3]['valor'], 'nombre' : n2 }
    
    


def p_produccion2(t):
    ''' T   : T MULTI F
            | F '''

    global contador
    if len(t) == 2:
        
        n1 = tag + str(contador)
        contador = contador + 1

        ast.node(n1, 'T.val = ' + str(t[1]['valor']) )
        ast.edge(t[1]['nombre'],n1)

        t[0] = { 'valor' : t[1]['valor'], 'nombre' : n1 }

    else:

        n1 = tag + str(contador)
        contador = contador + 1
        n2 = tag + str(contador)
        contador = contador + 1

        ast.node(n1, '*' )
        ast.node(n2, 'T.val = ' + str(t[1]['valor']*t[3]['valor']) )

        ast.edge(t[1]['nombre'],n2)
        ast.edge(n1,n2)
        ast.edge(t[3]['nombre'],n2)

        t[0] = { 'valor' : t[1]['valor']*t[3]['valor'], 'nombre' : n2 }

 

def p_produccion3(t):
    ''' F   : PARE_I E PARE_D
            | DIGITO '''
    global contador
    if len(t) == 2:

        n1 = tag + str(contador)
        contador = contador + 1
        n2 = tag + str(contador)
        contador = contador + 1

        ast.node(n1, '<<b>digit</b>.lexval = ' + str(t[1]) + '>' )
        ast.node(n2, 'F.val = ' + str(t[1]) )
        ast.edge(n1,n2)

        t[0] = { 'valor' : t[1], 'nombre' : n2 }

    else:

        n1 = tag + str(contador)
        contador = contador + 1
        n2 = tag + str(contador)
        contador = contador + 1
        n3 = tag + str(contador)
        contador = contador + 1

        ast.node(n1, '(' )
        ast.node(n2, ')')
        ast.node(n3, 'F.val = ' + str(t[2]['valor']))

        ast.edge(n1,n3)
        ast.edge(t[2]['nombre'],n3)
        ast.edge(n2,n3)
        

        t[0] = { 'valor' : t[2]['valor'], 'nombre' : n3 }

        
        


def p_error(t):
    print("Error sintáctico en '%s'" % t.value)


import ply.yacc as yacc
parser = yacc.yacc()

parser.parse('(3+4)*(5+6)n')