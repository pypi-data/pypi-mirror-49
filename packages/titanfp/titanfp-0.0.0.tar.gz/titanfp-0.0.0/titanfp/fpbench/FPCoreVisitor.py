# Generated from FPCore.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FPCoreParser import FPCoreParser
else:
    from FPCoreParser import FPCoreParser

# This class defines a complete generic visitor for a parse tree produced by FPCoreParser.

class FPCoreVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FPCoreParser#parse_fpcore.
    def visitParse_fpcore(self, ctx:FPCoreParser.Parse_fpcoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#parse_exprs.
    def visitParse_exprs(self, ctx:FPCoreParser.Parse_exprsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#fpcore.
    def visitFpcore(self, ctx:FPCoreParser.FpcoreContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#argument.
    def visitArgument(self, ctx:FPCoreParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprNum.
    def visitExprNum(self, ctx:FPCoreParser.ExprNumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprSym.
    def visitExprSym(self, ctx:FPCoreParser.ExprSymContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprCtx.
    def visitExprCtx(self, ctx:FPCoreParser.ExprCtxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprCast.
    def visitExprCast(self, ctx:FPCoreParser.ExprCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprIf.
    def visitExprIf(self, ctx:FPCoreParser.ExprIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprLet.
    def visitExprLet(self, ctx:FPCoreParser.ExprLetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprLetStar.
    def visitExprLetStar(self, ctx:FPCoreParser.ExprLetStarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprWhile.
    def visitExprWhile(self, ctx:FPCoreParser.ExprWhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprWhileStar.
    def visitExprWhileStar(self, ctx:FPCoreParser.ExprWhileStarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#ExprOp.
    def visitExprOp(self, ctx:FPCoreParser.ExprOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#NumberDec.
    def visitNumberDec(self, ctx:FPCoreParser.NumberDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#NumberHex.
    def visitNumberHex(self, ctx:FPCoreParser.NumberHexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#NumberRational.
    def visitNumberRational(self, ctx:FPCoreParser.NumberRationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#NumberDigits.
    def visitNumberDigits(self, ctx:FPCoreParser.NumberDigitsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#prop.
    def visitProp(self, ctx:FPCoreParser.PropContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#DatumNum.
    def visitDatumNum(self, ctx:FPCoreParser.DatumNumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#DatumSym.
    def visitDatumSym(self, ctx:FPCoreParser.DatumSymContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#DatumStr.
    def visitDatumStr(self, ctx:FPCoreParser.DatumStrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FPCoreParser#DatumList.
    def visitDatumList(self, ctx:FPCoreParser.DatumListContext):
        return self.visitChildren(ctx)



del FPCoreParser