# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import threading
from threading import Thread

import toomicsSpider


# def test():
#     allComics = toomicsSpider.parseWeb()
#     for i in range(2, len(allComics)):
#         picPageUrl = toomicsSpider.getInfoFromDetailPage(allComics[i][0])
#         dire = allComics[i][1]
#         for j in range(len(picPageUrl)):
#             isFree = toomicsSpider.getPicsInfo(picPageUrl[j], dire)
#             if isFree is False:
#                 break

# Press the green button in the gutter to run the script.
def main():
    toomicsSpider.loginToomics()
    allComics = toomicsSpider.parseWeb()
    print(len(allComics))
    for i in range(len(allComics)):
        picPageUrl = toomicsSpider.getInfoFromDetailPage(allComics[i][0])
        dire = allComics[i][1]
        for j in range(len(picPageUrl)):
            isFree = toomicsSpider.getPicsInfo(picPageUrl[j], dire)
            if isFree is False:
                break


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
