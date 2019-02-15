# Generated from /home/biggenerals/PycharmProjects/mkmcheck/mkmcheck/wishlist/wish_grammar.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .wish_grammarParser import wish_grammarParser
else:
    from wish_grammarParser import wish_grammarParser

# This class defines a complete listener for a parse tree produced by wish_grammarParser.
class wish_grammarListener(ParseTreeListener):

    # Enter a parse tree produced by wish_grammarParser#start.
    def enterStart(self, ctx:wish_grammarParser.StartContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#start.
    def exitStart(self, ctx:wish_grammarParser.StartContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#WishNoMeta.
    def enterWishNoMeta(self, ctx:wish_grammarParser.WishNoMetaContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#WishNoMeta.
    def exitWishNoMeta(self, ctx:wish_grammarParser.WishNoMetaContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#WishWithMeta.
    def enterWishWithMeta(self, ctx:wish_grammarParser.WishWithMetaContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#WishWithMeta.
    def exitWishWithMeta(self, ctx:wish_grammarParser.WishWithMetaContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#meta.
    def enterMeta(self, ctx:wish_grammarParser.MetaContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#meta.
    def exitMeta(self, ctx:wish_grammarParser.MetaContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#ExcludePartiallyFulfilled.
    def enterExcludePartiallyFulfilled(self, ctx:wish_grammarParser.ExcludePartiallyFulfilledContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#ExcludePartiallyFulfilled.
    def exitExcludePartiallyFulfilled(self, ctx:wish_grammarParser.ExcludePartiallyFulfilledContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IncludePartiallyFulfilled.
    def enterIncludePartiallyFulfilled(self, ctx:wish_grammarParser.IncludePartiallyFulfilledContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IncludePartiallyFulfilled.
    def exitIncludePartiallyFulfilled(self, ctx:wish_grammarParser.IncludePartiallyFulfilledContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#CardboardWishBase.
    def enterCardboardWishBase(self, ctx:wish_grammarParser.CardboardWishBaseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#CardboardWishBase.
    def exitCardboardWishBase(self, ctx:wish_grammarParser.CardboardWishBaseContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#CardboardWishChain.
    def enterCardboardWishChain(self, ctx:wish_grammarParser.CardboardWishChainContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#CardboardWishChain.
    def exitCardboardWishChain(self, ctx:wish_grammarParser.CardboardWishChainContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#RequiredCardboardNoAmount.
    def enterRequiredCardboardNoAmount(self, ctx:wish_grammarParser.RequiredCardboardNoAmountContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#RequiredCardboardNoAmount.
    def exitRequiredCardboardNoAmount(self, ctx:wish_grammarParser.RequiredCardboardNoAmountContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#RequiredCardboardWithAmount.
    def enterRequiredCardboardWithAmount(self, ctx:wish_grammarParser.RequiredCardboardWithAmountContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#RequiredCardboardWithAmount.
    def exitRequiredCardboardWithAmount(self, ctx:wish_grammarParser.RequiredCardboardWithAmountContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#RequiredCardboardNoRequirements.
    def enterRequiredCardboardNoRequirements(self, ctx:wish_grammarParser.RequiredCardboardNoRequirementsContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#RequiredCardboardNoRequirements.
    def exitRequiredCardboardNoRequirements(self, ctx:wish_grammarParser.RequiredCardboardNoRequirementsContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#RequiredCardboardWithRequirements.
    def enterRequiredCardboardWithRequirements(self, ctx:wish_grammarParser.RequiredCardboardWithRequirementsContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#RequiredCardboardWithRequirements.
    def exitRequiredCardboardWithRequirements(self, ctx:wish_grammarParser.RequiredCardboardWithRequirementsContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#RequirementChain.
    def enterRequirementChain(self, ctx:wish_grammarParser.RequirementChainContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#RequirementChain.
    def exitRequirementChain(self, ctx:wish_grammarParser.RequirementChainContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#RequirementBase.
    def enterRequirementBase(self, ctx:wish_grammarParser.RequirementBaseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#RequirementBase.
    def exitRequirementBase(self, ctx:wish_grammarParser.RequirementBaseContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#FromExpansions.
    def enterFromExpansions(self, ctx:wish_grammarParser.FromExpansionsContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#FromExpansions.
    def exitFromExpansions(self, ctx:wish_grammarParser.FromExpansionsContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IsBorder.
    def enterIsBorder(self, ctx:wish_grammarParser.IsBorderContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IsBorder.
    def exitIsBorder(self, ctx:wish_grammarParser.IsBorderContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IsMinimumCondition.
    def enterIsMinimumCondition(self, ctx:wish_grammarParser.IsMinimumConditionContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IsMinimumCondition.
    def exitIsMinimumCondition(self, ctx:wish_grammarParser.IsMinimumConditionContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IsLanguage.
    def enterIsLanguage(self, ctx:wish_grammarParser.IsLanguageContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IsLanguage.
    def exitIsLanguage(self, ctx:wish_grammarParser.IsLanguageContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IsFoil.
    def enterIsFoil(self, ctx:wish_grammarParser.IsFoilContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IsFoil.
    def exitIsFoil(self, ctx:wish_grammarParser.IsFoilContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IsAltered.
    def enterIsAltered(self, ctx:wish_grammarParser.IsAlteredContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IsAltered.
    def exitIsAltered(self, ctx:wish_grammarParser.IsAlteredContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#IsSigned.
    def enterIsSigned(self, ctx:wish_grammarParser.IsSignedContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#IsSigned.
    def exitIsSigned(self, ctx:wish_grammarParser.IsSignedContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#AnyLanguage.
    def enterAnyLanguage(self, ctx:wish_grammarParser.AnyLanguageContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#AnyLanguage.
    def exitAnyLanguage(self, ctx:wish_grammarParser.AnyLanguageContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#CanBeFoil.
    def enterCanBeFoil(self, ctx:wish_grammarParser.CanBeFoilContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#CanBeFoil.
    def exitCanBeFoil(self, ctx:wish_grammarParser.CanBeFoilContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#CanBeAltered.
    def enterCanBeAltered(self, ctx:wish_grammarParser.CanBeAlteredContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#CanBeAltered.
    def exitCanBeAltered(self, ctx:wish_grammarParser.CanBeAlteredContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#CanBeSigned.
    def enterCanBeSigned(self, ctx:wish_grammarParser.CanBeSignedContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#CanBeSigned.
    def exitCanBeSigned(self, ctx:wish_grammarParser.CanBeSignedContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#ExpansionChain.
    def enterExpansionChain(self, ctx:wish_grammarParser.ExpansionChainContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#ExpansionChain.
    def exitExpansionChain(self, ctx:wish_grammarParser.ExpansionChainContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Expansion.
    def enterExpansion(self, ctx:wish_grammarParser.ExpansionContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Expansion.
    def exitExpansion(self, ctx:wish_grammarParser.ExpansionContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#BooleanTrue.
    def enterBooleanTrue(self, ctx:wish_grammarParser.BooleanTrueContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#BooleanTrue.
    def exitBooleanTrue(self, ctx:wish_grammarParser.BooleanTrueContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#BooleanFalse.
    def enterBooleanFalse(self, ctx:wish_grammarParser.BooleanFalseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#BooleanFalse.
    def exitBooleanFalse(self, ctx:wish_grammarParser.BooleanFalseContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#WhiteBorder.
    def enterWhiteBorder(self, ctx:wish_grammarParser.WhiteBorderContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#WhiteBorder.
    def exitWhiteBorder(self, ctx:wish_grammarParser.WhiteBorderContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#BlackBorder.
    def enterBlackBorder(self, ctx:wish_grammarParser.BlackBorderContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#BlackBorder.
    def exitBlackBorder(self, ctx:wish_grammarParser.BlackBorderContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#SilverBorder.
    def enterSilverBorder(self, ctx:wish_grammarParser.SilverBorderContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#SilverBorder.
    def exitSilverBorder(self, ctx:wish_grammarParser.SilverBorderContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#GoldBorder.
    def enterGoldBorder(self, ctx:wish_grammarParser.GoldBorderContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#GoldBorder.
    def exitGoldBorder(self, ctx:wish_grammarParser.GoldBorderContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Mint.
    def enterMint(self, ctx:wish_grammarParser.MintContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Mint.
    def exitMint(self, ctx:wish_grammarParser.MintContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#NearMint.
    def enterNearMint(self, ctx:wish_grammarParser.NearMintContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#NearMint.
    def exitNearMint(self, ctx:wish_grammarParser.NearMintContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Excellent.
    def enterExcellent(self, ctx:wish_grammarParser.ExcellentContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Excellent.
    def exitExcellent(self, ctx:wish_grammarParser.ExcellentContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Good.
    def enterGood(self, ctx:wish_grammarParser.GoodContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Good.
    def exitGood(self, ctx:wish_grammarParser.GoodContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#LightPlayed.
    def enterLightPlayed(self, ctx:wish_grammarParser.LightPlayedContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#LightPlayed.
    def exitLightPlayed(self, ctx:wish_grammarParser.LightPlayedContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Played.
    def enterPlayed(self, ctx:wish_grammarParser.PlayedContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Played.
    def exitPlayed(self, ctx:wish_grammarParser.PlayedContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Poor.
    def enterPoor(self, ctx:wish_grammarParser.PoorContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Poor.
    def exitPoor(self, ctx:wish_grammarParser.PoorContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#English.
    def enterEnglish(self, ctx:wish_grammarParser.EnglishContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#English.
    def exitEnglish(self, ctx:wish_grammarParser.EnglishContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#French.
    def enterFrench(self, ctx:wish_grammarParser.FrenchContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#French.
    def exitFrench(self, ctx:wish_grammarParser.FrenchContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#German.
    def enterGerman(self, ctx:wish_grammarParser.GermanContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#German.
    def exitGerman(self, ctx:wish_grammarParser.GermanContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Spanish.
    def enterSpanish(self, ctx:wish_grammarParser.SpanishContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Spanish.
    def exitSpanish(self, ctx:wish_grammarParser.SpanishContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Italian.
    def enterItalian(self, ctx:wish_grammarParser.ItalianContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Italian.
    def exitItalian(self, ctx:wish_grammarParser.ItalianContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#SimplifiedChinese.
    def enterSimplifiedChinese(self, ctx:wish_grammarParser.SimplifiedChineseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#SimplifiedChinese.
    def exitSimplifiedChinese(self, ctx:wish_grammarParser.SimplifiedChineseContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Japanese.
    def enterJapanese(self, ctx:wish_grammarParser.JapaneseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Japanese.
    def exitJapanese(self, ctx:wish_grammarParser.JapaneseContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Portuguese.
    def enterPortuguese(self, ctx:wish_grammarParser.PortugueseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Portuguese.
    def exitPortuguese(self, ctx:wish_grammarParser.PortugueseContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#Korean.
    def enterKorean(self, ctx:wish_grammarParser.KoreanContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#Korean.
    def exitKorean(self, ctx:wish_grammarParser.KoreanContext):
        pass


    # Enter a parse tree produced by wish_grammarParser#TraditionalChinese.
    def enterTraditionalChinese(self, ctx:wish_grammarParser.TraditionalChineseContext):
        pass

    # Exit a parse tree produced by wish_grammarParser#TraditionalChinese.
    def exitTraditionalChinese(self, ctx:wish_grammarParser.TraditionalChineseContext):
        pass


