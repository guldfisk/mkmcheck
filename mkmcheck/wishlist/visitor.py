import typing as t

from mtgorp.db.database import CardDatabase
from mtgorp.models.persistent.attributes.borders import Border

from mkmcheck.values.values import Condition, Language

from mkmcheck.model.models import Wish, CardboardWish, Requirement
from mkmcheck.model import models
from mkmcheck.wishlist.exceptions import WishParseException

from mkmcheck.wishlist.gen.wish_grammarParser import wish_grammarParser
from mkmcheck.wishlist.gen.wish_grammarVisitor import wish_grammarVisitor


class WishVisitor(wish_grammarVisitor):

    def __init__(self, db: CardDatabase):
        self._db = db

    def visitStart(self, context: wish_grammarParser.StartContext):
        return self.visit(context.wish())

    def visitWishNoMeta(self, context: wish_grammarParser.WishNoMetaContext):
        return Wish(
            cardboard_wishes = self.visit(context.cardboard_wishes()),
            include_partially_fulfilled = False,
        )

    def visitWishWithMeta(self, context: wish_grammarParser.WishWithMetaContext):
        return Wish(
            cardboard_wishes = self.visit(context.cardboard_wishes()),
            include_partially_fulfilled = self.visit(context.meta())
        )

    def visitMeta(self, context: wish_grammarParser.MetaContext):
        return self.visit(context.inclution_strategy())

    def visitExcludePartiallyFulfilled(self, ctx: wish_grammarParser.ExcludePartiallyFulfilledContext):
        return False

    def visitIncludePartiallyFulfilled(self, ctx: wish_grammarParser.IncludePartiallyFulfilledContext):
        return True

    def visitCardboardWishBase(self, context: wish_grammarParser.CardboardWishBaseContext):
        return [self.visit(context.cardboard_wish())]

    def visitCardboardWishChain(self, context: wish_grammarParser.CardboardWishChainContext):
        cardboard_wishes = self.visit(context.cardboard_wishes())
        cardboard_wishes.append(self.visit(context.cardboard_wish()))
        return cardboard_wishes

    def _build_cardboard_wish(
        self,
        cardboard_name: str,
        required_amount: int,
        requirements_options: t.List[t.Union[str, Requirement]]
    ) -> CardboardWish:
        if not cardboard_name in self._db.cardboards:
            raise WishParseException(f'"{cardboard_name}" not a valid cardboard name')

        if required_amount == 0:
            raise WishParseException(f'0 is not a valid required amount for cardboard "{cardboard_name}"')

        requirements = [option for option in requirements_options if isinstance(option, Requirement)]
        options = [option for option in requirements_options if isinstance(option, str)]

        if (
            not 'any_language' in options
            and not any(
            isinstance(requirement, models.IsLanguage)
            for requirement in
            requirements
        )
        ):
            requirements.append(
                models.IsLanguage(
                    language = Language.ENGLISH,
                )
            )

        if (
            not 'can_be_foil' in options
            and not any(
            isinstance(requirement, models.IsFoil)
            for requirement in
            requirements
        )
        ):
            requirements.append(
                models.IsFoil(
                    is_foil = False,
                )
            )

        if (
            not 'can_be_altered' in options
            and not any(
            isinstance(requirement, models.IsAltered)
            for requirement in
            requirements
        )
        ):
            requirements.append(
                models.IsAltered(
                    is_altered = False,
                )
            )

        if (
            not 'can_be_signed' in options
            and not any(
            isinstance(requirement, models.IsSigned)
            for requirement in
            requirements
        )
        ):
            requirements.append(
                models.IsSigned(
                    is_signed = False,
                )
            )

        return CardboardWish(
            cardboard_name = cardboard_name,
            minimum_amount = required_amount,
            requirements = requirements,
        )

    def visitRequiredCardboardNoAmount(self, context: wish_grammarParser.RequiredCardboardNoAmountContext):
        cardboard_name, requirements = self.visit(context.required_cardboard())
        return self._build_cardboard_wish(cardboard_name, 1, requirements)

    def visitRequiredCardboardWithAmount(self, context: wish_grammarParser.RequiredCardboardWithAmountContext):
        cardboard_name, requirements = self.visit(context.required_cardboard())
        required_amount = int(str(context.INTEGER()))
        return self._build_cardboard_wish(cardboard_name, required_amount, requirements)

    def visitRequiredCardboardNoRequirements(self, context: wish_grammarParser.RequiredCardboardNoRequirementsContext):
        return str(context.VALUE()), []

    def visitRequiredCardboardWithRequirements(self, context: wish_grammarParser.RequiredCardboardWithRequirementsContext):
        return str(context.VALUE()), self.visit(context.requirements())

    def visitRequirementChain(self, context: wish_grammarParser.RequirementChainContext):
        requirements = self.visit(context.requirements()) #type: t.List[Requirement]
        requirements.append(self.visit(context.requirement()))
        return requirements

    def visitRequirementBase(self, context: wish_grammarParser.RequirementBaseContext):
        return [self.visit(context.requirement())]

    def visitFromExpansions(self, context: wish_grammarParser.FromExpansionsContext):
        return models.FromExpansions(
            _expansion_codes = self.visit(context.expansions())
        )

    def visitIsBorder(self, context: wish_grammarParser.IsBorderContext):
        return models.IsBorder(
            border = self.visit(context.border())
        )

    def visitIsMinimumCondition(self, context: wish_grammarParser.IsMinimumConditionContext):
        return models.IsMinimumCondition(
            condition = self.visit(context.condition())
        )

    def visitIsLanguage(self, context: wish_grammarParser.IsLanguageContext):
        return models.IsLanguage(
            language = self.visit(context.language())
        )

    def visitIsFoil(self, context: wish_grammarParser.IsFoilContext):
        return models.IsFoil(
            is_foil = self.visit(context.boolean())
        )

    def visitIsAltered(self, context: wish_grammarParser.IsAlteredContext):
        return models.IsAltered(
            is_altered = self.visit(context.boolean())
        )

    def visitIsSigned(self, context: wish_grammarParser.IsSignedContext):
        return models.IsSigned(
            is_signed = self.visit(context.boolean())
        )

    def visitAnyLanguage(self, context: wish_grammarParser.AnyLanguageContext):
        return 'any_language'

    def visitCanBeFoil(self, context: wish_grammarParser.CanBeFoilContext):
        return 'can_be_foil'

    def visitCanBeAltered(self, context: wish_grammarParser.CanBeAlteredContext):
        return 'can_be_altered'

    def visitCanBeSigned(self, context: wish_grammarParser.CanBeSignedContext):
        return 'can_be_signed'

    def visitBooleanTrue(self, context: wish_grammarParser.BooleanTrueContext):
        return True

    def visitBooleanFalse(self, context: wish_grammarParser.BooleanFalseContext):
        return False

    def visitWhiteBorder(self, context: wish_grammarParser.WhiteBorderContext):
        return Border.WHITE

    def visitBlackBorder(self, context: wish_grammarParser.BlackBorderContext):
        return Border.BLACK

    def visitSilverBorder(self, context: wish_grammarParser.SilverBorderContext):
        return Border.SILVER

    def visitGoldBorder(self, context: wish_grammarParser.GoldBorderContext):
        return Border.GOLD

    def visitMint(self, context: wish_grammarParser.MintContext):
        return Condition.MINT

    def visitNearMint(self, context: wish_grammarParser.NearMintContext):
        return Condition.NEAR_MINT

    def visitExcellent(self, context: wish_grammarParser.ExcellentContext):
        return Condition.EXCELLENT

    def visitGood(self, context: wish_grammarParser.GoodContext):
        return Condition.GOOD

    def visitLightPlayed(self, context: wish_grammarParser.LightPlayedContext):
        return Condition.LIGHT_PLAYED

    def visitPlayed(self, context: wish_grammarParser.PlayedContext):
        return Condition.PLAYED

    def visitPoor(self, context: wish_grammarParser.PoorContext):
        return Condition.POOR

    def visitEnglish(self, context: wish_grammarParser.EnglishContext):
        return Language.ENGLISH

    def visitFrench(self, context: wish_grammarParser.FrenchContext):
        return Language.SPANISH

    def visitGerman(self, context: wish_grammarParser.GermanContext):
        return Language.GERMAN

    def visitSpanish(self, context: wish_grammarParser.SpanishContext):
        return Language.SPANISH

    def visitItalian(self, context: wish_grammarParser.ItalianContext):
        return Language.ITALIAN

    def visitSimplifiedChinese(self, context: wish_grammarParser.SimplifiedChineseContext):
        return Language.SIMPLIFIED_CHINESE

    def visitJapanese(self, context: wish_grammarParser.JapaneseContext):
        return Language.JAPANESE

    def visitPortuguese(self, context: wish_grammarParser.PortugueseContext):
        return Language.PORTUGUESE

    def visitKorean(self, context: wish_grammarParser.KoreanContext):
        return Language.KOREAN

    def visitTraditionalChinese(self, context: wish_grammarParser.TraditionalChineseContext):
        return Language.TRADITIONAL_CHINESE

    def _check_expansion(self, code: str):
        if not code in self._db.expansions:
            raise WishParseException(f'"{code}" is not a valid expansion code')

    def visitExpansionChain(self, context: wish_grammarParser.ExpansionChainContext):
        expansion_code = str(context.EXPANSION_CODE_VALUE())

        self._check_expansion(expansion_code)

        expansions = self.visit(context.expansions())
        expansions.append(
            models.ExpansionCode(code=expansion_code)
        )

        return expansions

    def visitExpansion(self, context: wish_grammarParser.ExpansionContext):
        expansion_code = str(context.EXPANSION_CODE_VALUE())
        self._check_expansion(expansion_code)
        return [
            models.ExpansionCode(code=expansion_code)
        ]

