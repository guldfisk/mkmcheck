from marshmallow import fields
from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy import fields as alchemy_fields

from mkmcheck.model import models
from mkmcheck.values.values import Language
from mtgorp.models.persistent.attributes.borders import Border


class FromExpansionsSchema(ModelSchema):

    class Meta:
        model = models.FromExpansions
        exclude = ('cardboard_wish',)


class IsBorderSchema(ModelSchema):
    border = EnumField(Border, by_value = True)

    class Meta:
        model = models.IsBorder
        exclude = ('cardboard_wish',)


class IsMinimumConditionSchema(ModelSchema):

    class Meta:
        model = models.IsMinimumCondition
        exclude = ('cardboard_wish',)


class IsLanguageSchema(ModelSchema):
    language = EnumField(Language, by_value = True)

    class Meta:
        model = models.IsLanguage
        exclude = ('cardboard_wish',)


class IsFoilSchema(ModelSchema):

    class Meta:
        model = models.IsFoil
        exclude = ('cardboard_wish',)


class IsAlteredSchema(ModelSchema):

    class Meta:
        model = models.IsAltered
        exclude = ('cardboard_wish',)


class IsSignedSchema(ModelSchema):

    class Meta:
        model = models.IsSigned
        exclude = ('cardboard_wish',)


class RequirementSchema(OneOfSchema):
    type_field = 'requirement_type'

    type_schemas = {
        'from_expansions': FromExpansionsSchema,
        'is_border': IsBorderSchema,
        'is_minimum_condition': IsMinimumConditionSchema,
        'is_language': IsLanguageSchema,
        'is_foil': IsFoilSchema,
        'is_altered': IsAlteredSchema,
        'is_signed': IsSignedSchema,
    }

    def get_obj_type(self, obj) -> str:
        if isinstance(obj, models.FromExpansions):
            return 'from_expansions'

        if isinstance(obj, models.IsBorder):
            return 'is_border'

        if isinstance(obj, models.IsMinimumCondition):
            return 'is_minimum_condition'

        if isinstance(obj, models.IsLanguage):
            return 'is_language'

        if isinstance(obj, models.IsFoil):
            return 'is_foil'

        if isinstance(obj, models.IsAltered):
            return 'is_altered'

        if isinstance(obj, models.IsSigned):
            return 'is_signed'


class CardboardWishSchema(ModelSchema):
    requirements = fields.List(alchemy_fields.Nested(RequirementSchema))

    class Meta:
        model = models.CardboardWish
        exclude = ('wish',)


class WishSchema(ModelSchema):
    cardboard_wishes = fields.List(alchemy_fields.Nested(CardboardWishSchema))

    class Meta:
        model = models.Wish
        exclude = ('wish_list',)


class WishListSchema(ModelSchema):
    wishes = fields.List(alchemy_fields.Nested(WishSchema))

    class Meta:
        model = models.WishList
