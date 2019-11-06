

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from mtgorp.db.database import CardDatabase

from mkmcheck.wishlist.visitor import WishVisitor
from mkmcheck.model.models import Wish
from mkmcheck.wishlist.exceptions import WishParseException

from mkmcheck.wishlist.gen.wish_grammarParser import wish_grammarParser
from mkmcheck.wishlist.gen.wish_grammarLexer import wish_grammarLexer


class WIshParseListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise WishParseException('Syntax error')

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise WishParseException('Conetext sensitivity')


class WishParser(object):

    def __init__(self, db: CardDatabase):
        self._visitor = WishVisitor(db)

    def parse(self, s: str) -> Wish:
        parser = wish_grammarParser(
            CommonTokenStream(
                wish_grammarLexer(
                    InputStream(s)
                )
            )
        )

        parser._listeners = [WIshParseListener()]

        return self._visitor.visit(parser.start())