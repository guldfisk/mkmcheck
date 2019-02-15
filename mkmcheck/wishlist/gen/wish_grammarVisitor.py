# Generated from /home/biggenerals/PycharmProjects/mkmcheck/mkmcheck/wishlist/wish_grammar.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .wish_grammarParser import wish_grammarParser
else:
    from wish_grammarParser import wish_grammarParser

# This class defines a complete generic visitor for a parse tree produced by wish_grammarParser.

class wish_grammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by wish_grammarParser#start.
    def visitStart(self, ctx:wish_grammarParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#WishNoMeta.
    def visitWishNoMeta(self, ctx:wish_grammarParser.WishNoMetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#WishWithMeta.
    def visitWishWithMeta(self, ctx:wish_grammarParser.WishWithMetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#meta.
    def visitMeta(self, ctx:wish_grammarParser.MetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#ExcludePartiallyFulfilled.
    def visitExcludePartiallyFulfilled(self, ctx:wish_grammarParser.ExcludePartiallyFulfilledContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IncludePartiallyFulfilled.
    def visitIncludePartiallyFulfilled(self, ctx:wish_grammarParser.IncludePartiallyFulfilledContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#CardboardWishBase.
    def visitCardboardWishBase(self, ctx:wish_grammarParser.CardboardWishBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#CardboardWishChain.
    def visitCardboardWishChain(self, ctx:wish_grammarParser.CardboardWishChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#RequiredCardboardNoAmount.
    def visitRequiredCardboardNoAmount(self, ctx:wish_grammarParser.RequiredCardboardNoAmountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#RequiredCardboardWithAmount.
    def visitRequiredCardboardWithAmount(self, ctx:wish_grammarParser.RequiredCardboardWithAmountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#RequiredCardboardNoRequirements.
    def visitRequiredCardboardNoRequirements(self, ctx:wish_grammarParser.RequiredCardboardNoRequirementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#RequiredCardboardWithRequirements.
    def visitRequiredCardboardWithRequirements(self, ctx:wish_grammarParser.RequiredCardboardWithRequirementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#RequirementChain.
    def visitRequirementChain(self, ctx:wish_grammarParser.RequirementChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#RequirementBase.
    def visitRequirementBase(self, ctx:wish_grammarParser.RequirementBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#FromExpansions.
    def visitFromExpansions(self, ctx:wish_grammarParser.FromExpansionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IsBorder.
    def visitIsBorder(self, ctx:wish_grammarParser.IsBorderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IsMinimumCondition.
    def visitIsMinimumCondition(self, ctx:wish_grammarParser.IsMinimumConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IsLanguage.
    def visitIsLanguage(self, ctx:wish_grammarParser.IsLanguageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IsFoil.
    def visitIsFoil(self, ctx:wish_grammarParser.IsFoilContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IsAltered.
    def visitIsAltered(self, ctx:wish_grammarParser.IsAlteredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#IsSigned.
    def visitIsSigned(self, ctx:wish_grammarParser.IsSignedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#AnyLanguage.
    def visitAnyLanguage(self, ctx:wish_grammarParser.AnyLanguageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#CanBeFoil.
    def visitCanBeFoil(self, ctx:wish_grammarParser.CanBeFoilContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#CanBeAltered.
    def visitCanBeAltered(self, ctx:wish_grammarParser.CanBeAlteredContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#CanBeSigned.
    def visitCanBeSigned(self, ctx:wish_grammarParser.CanBeSignedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#ExpansionChain.
    def visitExpansionChain(self, ctx:wish_grammarParser.ExpansionChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Expansion.
    def visitExpansion(self, ctx:wish_grammarParser.ExpansionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#BooleanTrue.
    def visitBooleanTrue(self, ctx:wish_grammarParser.BooleanTrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#BooleanFalse.
    def visitBooleanFalse(self, ctx:wish_grammarParser.BooleanFalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#WhiteBorder.
    def visitWhiteBorder(self, ctx:wish_grammarParser.WhiteBorderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#BlackBorder.
    def visitBlackBorder(self, ctx:wish_grammarParser.BlackBorderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#SilverBorder.
    def visitSilverBorder(self, ctx:wish_grammarParser.SilverBorderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#GoldBorder.
    def visitGoldBorder(self, ctx:wish_grammarParser.GoldBorderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Mint.
    def visitMint(self, ctx:wish_grammarParser.MintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#NearMint.
    def visitNearMint(self, ctx:wish_grammarParser.NearMintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Excellent.
    def visitExcellent(self, ctx:wish_grammarParser.ExcellentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Good.
    def visitGood(self, ctx:wish_grammarParser.GoodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#LightPlayed.
    def visitLightPlayed(self, ctx:wish_grammarParser.LightPlayedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Played.
    def visitPlayed(self, ctx:wish_grammarParser.PlayedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Poor.
    def visitPoor(self, ctx:wish_grammarParser.PoorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#English.
    def visitEnglish(self, ctx:wish_grammarParser.EnglishContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#French.
    def visitFrench(self, ctx:wish_grammarParser.FrenchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#German.
    def visitGerman(self, ctx:wish_grammarParser.GermanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Spanish.
    def visitSpanish(self, ctx:wish_grammarParser.SpanishContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Italian.
    def visitItalian(self, ctx:wish_grammarParser.ItalianContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#SimplifiedChinese.
    def visitSimplifiedChinese(self, ctx:wish_grammarParser.SimplifiedChineseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Japanese.
    def visitJapanese(self, ctx:wish_grammarParser.JapaneseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Portuguese.
    def visitPortuguese(self, ctx:wish_grammarParser.PortugueseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#Korean.
    def visitKorean(self, ctx:wish_grammarParser.KoreanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by wish_grammarParser#TraditionalChinese.
    def visitTraditionalChinese(self, ctx:wish_grammarParser.TraditionalChineseContext):
        return self.visitChildren(ctx)



del wish_grammarParser