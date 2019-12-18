from __future__ import annotations

import typing as t

import datetime

from lazy_property import LazyProperty

from mtgorp.models.persistent.attributes.borders import Border

from mkmcheck.values.values import Condition, Language

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Enum, Float, DateTime, UnicodeText
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.engine.base import Engine
from sqlalchemy.dialects.mysql.types import MEDIUMTEXT

from mkmcheck import db


Base = declarative_base()

_UT = UnicodeText()
_UT.with_variant(MEDIUMTEXT, 'mysql')


class RequestCache(Base):
    __tablename__ = 'request_cache'

    request = Column(String(127), primary_key=True)
    response = Column(_UT)

    time_stamp = Column(
        DateTime,
        default = datetime.datetime.utcnow,
        onupdate = datetime.datetime.utcnow,
    )

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.request,
        )


class Requirement(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True)

    cardboard_wish_id = Column(
        Integer,
        ForeignKey('cardboard_wishes.id'),
        nullable = False,
    )
    cardboard_wish = relationship(
        'CardboardWish',
        back_populates = 'requirements',
    )

    requirement_type = Column(String(31))

    __mapper_args__ = {
        'polymorphic_on': requirement_type,
        'polymorphic_identity': 'requirement',
    }

    def fulfilled(self, article: Article) -> bool:
        pass

    def __repr__(self):
        return '{}'.format(
            self.__class__.__name__,
        )


class ExpansionCode(Base):
    __tablename__ = 'expansion_codes'

    id = Column(Integer, primary_key=True)

    from_expansions_id = Column(
        Integer,
        ForeignKey('requirements.id'),
        nullable = False,
    )
    from_expansions = relationship(
        'FromExpansions',
        back_populates = '_expansion_codes'
    )

    code = Column(String(7))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.code == other.code
        )

    def __hash__(self):
        return hash(self.code)


class FromExpansions(Requirement):

    _expansion_codes: t.List[ExpansionCode] = relationship(
        'ExpansionCode',
        back_populates = 'from_expansions',
        cascade = 'all, delete-orphan',
    )

    @property
    def expansion_codes(self) -> t.List[str]:
        return [expansion_code.code for expansion_code in self._expansion_codes]

    __mapper_args__ = {
        'polymorphic_identity': 'from_expansions',
    }

    def fulfilled(self, article: Article) -> bool:
        return article.expansion_code in self.expansion_codes

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.expansion_codes == other.expansion_codes
        )

    def __hash__(self):
        return hash(frozenset(self.expansion_codes))

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.expansion_codes,
        )


class IsBorder(Requirement):

    border = Column(Enum(Border))

    __mapper_args__ = {
        'polymorphic_identity': 'is_border',
    }

    def fulfilled(self, article: Article) -> bool:
        expansion = db.expansions.get(article.expansion_code, None)
        return expansion is not None and expansion.border is not None and expansion.border == self.border

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.border == other.border
        )

    def __hash__(self):
        return hash(self.border)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.border,
        )


class IsMinimumCondition(Requirement):

    condition = Column(Enum(Condition))

    __mapper_args__ = {
        'polymorphic_identity': 'is_minimum_condition',
    }

    def fulfilled(self, article: Article) -> bool:
        return article.condition >= self.condition

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.condition == other.condition
        )

    def __hash__(self):
        return hash(self.condition)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.condition,
        )


class IsLanguage(Requirement):

    language = Column(Enum(Language))

    __mapper_args__ = {
        'polymorphic_identity': 'is_language',
    }

    def fulfilled(self, article: Article) -> bool:
        return article.language == self.language

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.language == other.language
        )

    def __hash__(self):
        return hash(self.language)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.language,
        )


class IsFoil(Requirement):

    is_foil = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'is_foil',
    }

    def fulfilled(self, article: Article) -> bool:
        return article.is_foil == self.is_foil

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.is_foil == other.is_foil
        )

    def __hash__(self):
        return hash(self.is_foil)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.is_foil,
        )


class IsAltered(Requirement):

    is_altered = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'is_altered',
    }

    def fulfilled(self, article: Article) -> bool:
        return article.is_altered == self.is_altered

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.is_altered == other.is_altered
        )

    def __hash__(self):
        return hash(self.is_altered)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.is_altered,
        )


class IsSigned(Requirement):

    is_signed = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'is_signed',
    }

    def fulfilled(self, article: Article) -> bool:
        return article.is_signed == self.is_signed

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.is_signed == other.is_signed
        )

    def __hash__(self):
        return hash(self.is_signed)

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.is_signed,
        )


class CardboardWish(Base):
    __tablename__ = 'cardboard_wishes'

    id = Column(Integer, primary_key=True)

    wish_id = Column(
        Integer,
        ForeignKey('wishes.id'),
        nullable = False,
    )
    wish = relationship(
        'Wish',
        back_populates = 'cardboard_wishes',
    )

    cardboard_name = Column(String(127))
    minimum_amount = Column(Integer)

    requirements: t.List[Requirement] = relationship(
        'Requirement',
        back_populates = 'cardboard_wish',
        cascade = 'all, delete-orphan',
    )

    def validate_article(self, article: 'Article') -> bool:
        return all(
            requirement.fulfilled(article)
            for requirement in
            self.requirements
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.cardboard_name == other.cardboard_name
            and self.minimum_amount == other.minimum_amount
            and self.requirements == other.requirements
        )

    def __hash__(self):
        return hash(
            (
                self.cardboard_name,
                self.minimum_amount,
                frozenset(self.requirements),
            )
        )

    def __repr__(self):
        return '({}, {}, {})'.format(
            self.cardboard_name,
            self.minimum_amount,
            self.requirements,
        )


class Wish(Base):
    __tablename__ = 'wishes'

    id = Column(Integer, primary_key=True)

    wish_list_id = Column(
        Integer,
        ForeignKey('wish_lists.id'),
        nullable = False,
    )
    wish_list = relationship(
        'WishList',
        back_populates = 'wishes',
    )

    weight = Column(Integer)
    include_partially_fulfilled = Column(Boolean)

    cardboard_wishes: t.List[CardboardWish] = relationship(
        'CardboardWish',
        back_populates = 'wish',
        cascade = 'all, delete-orphan',
    )

    @property
    def cardboard_names(self) -> t.Iterable[str]:
        return (
            cardboard_wish.cardboard_name
            for cardboard_wish in
            self.cardboard_wishes
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.weight == other.weight
            and self.include_partially_fulfilled == other.include_partially_fulfilled
            and self.cardboard_wishes == other.cardboard_wishes
        )

    def __hash__(self):
        return hash(
            (
                self.weight,
                self.include_partially_fulfilled,
                frozenset(self.cardboard_wishes),
            )
        )

    def __repr__(self):
        return '({}, {})'.format(
            self.weight,
            self.cardboard_wishes,
        )


class WishList(Base):
    __tablename__ = 'wish_lists'

    id = Column(Integer, primary_key=True)

    created_date = Column(
        DateTime,
        default = datetime.datetime.utcnow,
    )

    wishes: t.List[Wish] = relationship(
        'Wish',
        back_populates = 'wish_list',
        cascade = 'all, delete-orphan',
    )

    @property
    def cardboard_names(self) -> t.Iterable[str]:
        for wish in self.wishes:
            for cardboard_name in wish.cardboard_names:
                yield cardboard_name

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.wishes == other.wishes
        )

    def __hash__(self):
        return hash(frozenset(self.wishes))

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.wishes,
        )


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)

    cardboard_name = Column(String(63))
    expansion_code = Column(String(7))
    price = Column(Float)
    amount = Column(Integer)
    condition = Column(Enum(Condition))
    language = Column(Enum(Language))
    is_foil = Column(Boolean)
    is_signed = Column(Boolean)
    is_altered = Column(Boolean)
    is_playset = Column(Boolean)

    @property
    def adjusted_price(self):
        return self.price / 4 if self.is_playset else self.price

    seller_id = Column(
        Integer,
        ForeignKey('sellers.id'),
        nullable = False,
    )
    seller = relationship(
        'Seller',
        back_populates = 'articles',
    )

    def __repr__(self):
        base = f'{self.amount}x {self.cardboard_name}|{self.expansion_code}'
        base += f'({self.condition.name}'
        if self.language != Language.ENGLISH:
            base += f', {self.language}'
        if self.is_foil:
            base += ', FOIL'
        if self.is_signed:
            base += ', SIGNED'
        if self.is_altered:
            base += ', ALTERED'
        if self.is_playset:
            base += ', PLAYSET'
        base += f'): {self.price}'
        return base


class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True)

    name = Column(String(63))

    articles: t.List[Article] = relationship(
        'Article',
        back_populates = 'seller',
        cascade = 'all, delete-orphan',
    )

    market_id = Column(
        Integer,
        ForeignKey('markets.id'),
        nullable = False,
    )
    market = relationship(
        'Market',
        back_populates = 'sellers',
    )

    @LazyProperty
    def article_map(self) -> t.Dict[str, t.Collection[Article]]:
        _map: t.Dict[str, t.List[Article]] = {}

        for article in self.articles:
            try:
                _map[article.cardboard_name].append(article)
            except KeyError:
                _map[article.cardboard_name] = [article]

        return _map

    def get_articles_for_cardboard(self, cardboard_name: str) -> t.List[Article]:
        return self.article_map.get(cardboard_name, [])

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.name,
        )


class Market(Base):
    __tablename__ = 'markets'

    id = Column(Integer, primary_key=True)

    created_date = Column(
        DateTime,
        default = datetime.datetime.utcnow,
    )

    sellers: t.List[Seller] = relationship(
        'Seller',
        back_populates = 'market',
        cascade = 'all, delete-orphan',
    )

    wish_list_id = Column(
        Integer,
        ForeignKey('wish_lists.id'),
    )
    wish_list = relationship('WishList')


def create(engine: Engine):
    Base.metadata.create_all(engine)
