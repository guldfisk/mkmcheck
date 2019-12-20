import json

from sqlalchemy.orm import joinedload

from mkmcheck.model import models
from mkmcheck.model.models import IsFoil
from mkmcheck.schemas.schemas import WishListSchema, RequirementSchema, CardboardWishSchema, WishSchema
from mkmcheck.wishload.fetch import WishListFetcher
from mtgorp.db.load import Loader

import mkmcheck


def test():
    session = mkmcheck.ScopedSession()

    data = {
        "include_partially_fulfilled": False,
        "cardboard_wishes": [
            {
                "requirements": [
                    {
                        "requirement_type": "is_language",
                        "language": 1,
                    },
                    {
                        "requirement_type": "is_foil",
                        "is_foil": False,
                    },
                    {
                        "requirement_type": "is_altered",
                        "is_altered": False,
                    },
                    {
                        "requirement_type": "is_signed",
                        "is_signed": False,
                    }
                ],
                "cardboard_name": "Yuriko, the Tiger's Shadow",
                "minimum_amount": 1,
            }
        ],
        "weight": 0,
    }
    obj = WishSchema().load(data, session = session)

    print(obj)

    print(json.dumps(WishSchema().dump(obj)))

    import time

    st = time.time()
    wish_list = (
        session.query(models.WishList)
            .options(
                joinedload(models.WishList.wishes)
                    .joinedload(models.Wish.cardboard_wishes)
                        .joinedload(models.CardboardWish.requirements)
            )
            .order_by(models.WishList.created_date.desc())
            .first()
    )
    print('done', time.time() - st)

    # for wish in wish_list.wishes:
    #     for cardboard_wish in wish.cardboard_wishes:
    #         for requirement in cardboard_wish.requirements:
    #             if isinstance(requirement, IsFoil):
    #                 print(requirement, requirement.cardboard_wish)
    st = time.time()
    data = WishListSchema().dump(wish_list)
    wish_list_again = WishListSchema().load(data, session = session)
    print('done', time.time() - st)

    # print(wish_list)


if __name__ == '__main__':
    test()
