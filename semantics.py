#Robert Parry

#Code runs - fri 12 Nov 8:25
# TODO  #Change incorrect tree navigation - Semantic checks work but some of the information it uses isn't correct because the wrong location is used.
        #Part 1VI
        #Part 3I

import antlr4 as antlr
from CoffeeLexer import CoffeeLexer
from CoffeeVisitor import CoffeeVisitor
from CoffeeParser import CoffeeParser
from CoffeeUtil import Var, Method, Import, Loop, SymbolTable

class CoffeeTreeVisitor(CoffeeVisitor):
    
    #Global variable for transferring data between methods.
    transfer_var = ""
    
    def __init__(self):
        self.stbl = SymbolTable()
        
    def visitProgram(self, ctx):
        method =  Method('main', 'int', ctx.start.line)
        self.stbl.pushFrame(method)
        self.visitChildren(ctx)
        self.stbl.popFrame()
        
    def visitBlock(self, ctx):
        if (ctx.LCURLY() != None):
            self.stbl.pushScope()
        
        self.visitChildren(ctx)
        
        if (ctx.LCURLY() != None):
            self.stbl.popScope()
    
    def visitGlobal_decl(self, ctx):
        line = ctx.start.line
        var_type = ctx.var_decl().data_type().getText()
        for i in range(len(ctx.var_decl().var_assign())):
            var_id = ctx.var_decl().var_assign(i).var().ID().getText()
            var_size = 8
            var_array = False
            
            var = self.stbl.peek(var_id)
            if (var != None):
                print('error')
            
            #Checking for arrays
            if (ctx.var_decl().var_assign(i).var().INT_LIT() != None):
                print(ctx.var_decl().var_assign(i).var().INT_LIT().getText())
            
            var = Var(var_id,
                      var_type,
                      var_size,
                      Var.LOCAL,
                      var_array,
                      line)
            self.stbl.pushVar(var)
           
#3III    #n is of type BOOL not INT
        var_step = ctx.var_decl().data_type().getText()
        
        if(ctx.statement().limit().step() != None):
            if(var_step != "int"):
                raise Exception("error on line ", line, "the variable ", var_step , " should be of type INT.")
        
        
    def visitVar_decl(self, ctx):
        line = ctx.start.line
        var_type = ctx.data_type().getText()
        for i in range(len(ctx.var_assign())):
            var_id = ctx.var_assign(i).var().ID().getText()
            var_size = 8
            var_array = False
            
            var = self.stbl.peek(var_id)
            if (var != None):
                print('error')
            
            var = Var(var_id,
                      var_type,
                      var_size,
                      Var.GLOBAL,
                      var_array,
                      line)
            self.stbl.pushVar(var)
            
#1III-ii
        global transfer_var #Modify/use global variable
        transfer_var = ctx.var_assign().method_call().ID().getText()
        
        print(transfer_var)   
            
        
    def visitMethod_decl(self, ctx):
        line = ctx.start.line
        method_id = ctx.ID().getText()
        method_type = ctx.return_type().getText()
        method = self.stbl.peek(method_id)
        if (method != None):
            print('error...')
        method = Method(method_id, method_type, line)
        self.stbl.pushMethod(method)
        self.stbl.pushFrame(method)
        for i in range(len(ctx.param())):
            var_id = ctx.param(i).ID().getText()
        var_type = ctx.param(i).data_type().getText()
        var_size = 8
        var_array = False
        # TODO: check table, catch errors, create var, add to table
        method.pushParam(var_type)
        self.visit(ctx.block())
        # TODO: additional checks for methods expecting return values
        self.stbl.popFrame()
        
#1II  #Check void methods don't return any values     #error on line 3: void method 'foo' returning (int)   
        line = ctx.start.line
        rtrn = ctx.return_type().getText()
        rtrn_value = ctx.block().statement()
            
        print(rtrn)
        print(rtrn_value)
                
        if (rtrn == "void" ):
            if(rtrn_value == None):
               raise Exception('error on line ', line, rtrn, ' methods cannot return a value.')
                   

#1III-i #Check that all methods used have been declared     #error on line 5 reference to undeclared method 'food'
        #Needs putting in a while loop and iterating through 'ctx.ID()'.
        line = ctx.start.line
        method_id2 = ctx.ID().getText()
        
        global transfer_var #modify global variable
        
        if(method_id2 != transfer_var):
               raise Exception("Undeclared method ", line, var_id, " must be declared before use.")
              

    def visitReturn(self, ctx):
        method_ctx = self.stbl.getMethodContext()
        method_ctx.has_return = True
        if (ctx.expr() != None):
            expr_type = self.visit(ctx.expr())
   
            
    def visitImport_stmt(self, ctx):
        line = ctx.start.line
        var_type = ctx.getText()
        for i in range(len(ctx.ID())):
            method_id = ctx.ID(2)
            var_size = 8
            var_array = False
            
            print(method_id)
      
            
#1I    #Check for duplicate methods IDs     #error on line 1 :imported method 'printf' already in use
       #Needs putting in a while loop and iterating through 'ctx.ID()'.

            var = self.stbl.peek(method_id)
            if (var != None):
                raise Exception('error on line', line, 'method id', method_id, 'already declared in scope on line', var.line, ".")
                
            var = Var(method_id, var_type, var_size, Var.GLOBAL, var_array, line)
            self.stbl.pushVar(var)  
         
            
    def visitMetLoop(self, ctx):
        line = ctx.start.line
        var_type = ctx.var_decl().data_type().getText()
        for i in range(len(ctx.var_decl().var_assign())):
            var_id = ctx.var_decl().var_assign(i).var().ID().getText()
            var_size = 8
            var_array = False


#3II    #Loop has a return statement so the method cannot
        #'statement() & statement().block()' are incorrect but the rest is of the semantic check is correct
        loop_rtrn = False
        method_rtrn = False
        
        if(ctx.statement().block() != None):
            loop_rtrn = True 
        
        if(ctx.statement() != None):
            method_rtrn = True
        
        if(loop_rtrn == False):
            if(method_rtrn == True):
                raise Exception("error on line ", line, "there are duplicate return statements.")


##IV    #Check statements are in the correct place

        loop_cont = False
        method_cont = False
        
        if(ctx.statement().block() != None):
            loop_cont = True 
        
        if(ctx.statement() != None):
            method_cont = True
        
        if(loop_cont == True):
            if(method_cont):
                raise Exception("error on line ", line, "the method continue statement is outside of the loop.")




#1IV #check if the correct number of arguments are given     #three arguments given when there are meant to be two


        #raise Exception("error on line ", line, "the method ", var , " requires ", var , "arguments")

#3I    #Check if code returns INT value
                    
                
        #raise Exception("error on line ", line, "the method ", var , " requires ", var , "arguments")
              
              
    def visitLocation(self, ctx):
        var_id = ctx.ID().getText()
        
    def visitLiteral(self, ctx):
        if (ctx.INT_LIT() != None):
            return 'int'
        elif (ctx.STRING_LIT() != None):
            return 'string'
        elif (ctx.bool_lit() != None):
            return 'bool'
        
    def visitExpr(self, ctx):
        if (ctx.literal() != None):
            return self.visit(ctx.literal())
        elif (ctx.location() != None):
            return self.visit(ctx.location())
        else:
            return self.visitChildren(ctx)
        
        
#### Loading files etc... ##########################################################################
       
       
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





