import json

from mkmcheck.model import models
from mkmcheck.wishload.fetch import WishListFetcher
from mtgorp.db.load import Loader

import mkmcheck

def test():
    session = mkmcheck.ScopedSession()

    wish_list = session.query(models.WishList).order_by(models.WishList.created_date.desc()).first()

    print(json.dumps(wish_list.to_dict()))


if __name__ == '__main__':
    test()