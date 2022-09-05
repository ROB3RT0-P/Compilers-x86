#Robert Parry

#Code runs with errors below - Fri 12 Nov 8:15
#TODO   #Fix visit block - visit_block can stop all the other functions running.
        #Duplication - Code runs correctly but is running multiple times and the assembly code is duplicated multiple times
        #Part 2 - Methods

import antlr4 as antlr
from CoffeeLexer import CoffeeLexer
from CoffeeParser import CoffeeParser
from CoffeeVisitor import CoffeeVisitor
from CoffeeUtil import Var, Method, Import, Loop, SymbolTable

class CoffeeTreeVisitor(CoffeeVisitor):
    def __init__(self):
        self.stbl = SymbolTable()
        self.data = '.data\n'
        self.body = '.text\n.global main\n'

    def visitProgram(self, ctx):
        
        #print('test visit program')
        line = ctx.start.line

        method = Method('main', 'int', line)

        self.stbl.pushFrame(method)
        
        self.stbl.pushMethod(method)

        method.body += method.id + ':\n'
        method.body += 'push %rbp\n'
        method.body += 'movq %rsp, %rbp\n'

        self.visitChildren(ctx)

        if method.has_return == False:
            method.body += 'pop %rbp\n'
            method.body += 'ret\n'

        self.data += method.data
        self.body += method.body

        self.stbl.popFrame()
        
        
     
    def visitMethod_decl(self,ctx):
        #print('test visit method')
        
        line = ctx.start.line
        
        method_id = ctx.method_decl().get_Text()#
        return_type = ctx.return_type().data_type().getText()#
        
        method = Method(method_id, return_type, line)
        self.stbl.pushMethod()
        
        self.stbl.pushFrame(method)
        
        self.data += method.data
        self.body += method.body    
        
        self.stbl.popFrame()
        
        method.body += 'movq %rsp, %rbp'#?
        
        
        if (ctx.block() != None):#?
            self.visit(ctx.block())
        else:
            self.visit(ctx.expr())


    def visitLiteral(self, ctx):
        method_ctx = self.stbl.getMethodContext()
        if (ctx.INT_LIT() != None):
            method_ctx.body += 'movq $' + \
            ctx.INT_LIT().getText() + ', %rax\n'
            
            print('test visit literal')

    def visitExpr(self, ctx):
        
        #print('test visit expression')
        
        if(ctx.literal()!= None):
            print('literal')
            pass
        elif(ctx.location() != None):
            pass
        elif (len(ctx.expr()) == 2):
            print('binop')
            method_ctx = self.stbl.getMethodContext()
            self.visit(ctx.expr(0))
            method_ctx.body += 'movq %rax, %r10\n'
            self.visit(ctx.expr(1))
            method_ctx.body += 'movq %rax, %r11\n'
        
        
#1)Expressions - Arithmetic
    #Modulus '%' operator to be implemented
    
        if(len(ctx.expr()) == 1):#guess
            method_ctx = self.stbl.getMethodContext()#placeholder
        elif (len(ctx.expr()) == 2):
            method_ctx = self.stbl.getMethodContext()
            self.visit(ctx.expr(0))
            method_ctx.body += 'movq %rax, %r10\n'
            self.visit(ctx.expr(1))
            method_ctx.body += 'movq %rax, %r11\n'
            
        if (ctx.ADD() != None):
            method_ctx.body += 'addq %r10, %r11\n'
            method_ctx.body += 'movq %r11, %rax\n'
        
        if (ctx.SUB() != None):
            method_ctx.body += 'subq %r11, %r10\n'
            method_ctx.body += 'movq %r10, %rax\n'
            
        if (ctx.DIV() != None):
            method_ctx.body += 'movq %r10, %rbx\n'
            method_ctx.body += 'idiv %rbx\n'
            
        if (ctx.MUL() != None):
            method_ctx.body += 'imul %r10, %r11\n'
            method_ctx.body += 'movq %r11, %rax\n'
        
        else:
            return self.visitChildren(ctx)\
        
      
        
    def visitMethod_call(self, ctx):
        method_ctx = self.stbl.getMethodContext()
        method_id = ctx.ID().getText()
        for i in range(len(ctx.expr())):
            self.visit(ctx.expr(i))
        method_ctx.body += 'movq %rax, ' + \
        self.stbl.param_reg[i] + '\n'
        method_ctx.body += 'addq $' + \
        str(self.stbl.getStackPtr()) + ', %rsp\n'
        method_ctx.body += 'call ' + method_id + '\n'
        method_ctx.body += 'subq $' + \
        str(self.stbl.getStackPtr()) + ', %rsp\n'

####################################################################################################
#Problematic section
#VisitBlock stops all other functions running properly, but when removed causes visitLocation to throw an exception.
#Therefore, commenting out these two sections temporarily is needed to run the other code as normal.
#The code here is all correct from my understanding

    #def visitBlock(self, ctx):#causes other functions to not run - program possibly gets stuck here
    #    if (ctx.LCURLY() != None):
    #        method_ctx = self.stbl.getMethodContext()
    #        method_ctx.body += 'movq %rdi, -8(%rbp)'
    #        self.visitChildren(ctx)    
    #    print('test visit block')
    

    #def visitLocation(self, ctx):
    #    method_ctx = self.stbl.getMethodContext()
    #    var_id = ctx.ID().getText()
    #    var = self.stbl.find(var_id)
    #    method_ctx.body += 'movq ' + \
    #    str(var.addr) + '(%rbp), %rax\n'#causes problems when visit block removed
        
    #    print('test visit location')



####################################################################################################

#load source code
filein = open('./test.coffee', 'r')
source_code = filein.read();
filein.close()

#create a token stream from source code
lexer = CoffeeLexer(antlr.InputStream(source_code))
stream = antlr.CommonTokenStream(lexer)

#parse token stream
parser = CoffeeParser(stream)
tree = parser.program()

#create Coffee Visitor object
visitor = CoffeeTreeVisitor()

#visit nodes from tree root
visitor.visit(tree)

#assembly output code
code = visitor.data + visitor.body
print(code)

#save the assembly file
fileout = open('a.s', 'w')
fileout.write(code)
fileout.close()

#assemble and link
import os
os.system("gcc a.s -lm ; ./a.out ; echo $?")
