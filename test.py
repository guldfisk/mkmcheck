from mkmcheck.wishload.fetch import WishListFetcher
from mtgorp.db.load import Loader

import mkmcheck

def test():

    wish_list_fetcher = WishListFetcher(
        db = mkmcheck.db,
        spreadsheet_id = mkmcheck.SHEET_ID,
        sheet_name = mkmcheck.INPUT_SHEET_NAME,
    )

    fetched_wish_list = wish_list_fetcher.fetch()

    print(fetched_wish_list)


if __name__ == '__main__':
    test()