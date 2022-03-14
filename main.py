# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import toomicsSpider


# Press the green button in the gutter to run the script.
def main():
    toomicsSpider.loginToomics()
    allComics = toomicsSpider.parseWeb()
    for i in range(3):
        picPageUrl = toomicsSpider.getInfoFromDetailPage(allComics[i][0])
        dire = allComics[i][1]
        for i in range(len(picPageUrl)):
            isFree = toomicsSpider.getPicsInfo(picPageUrl[i], dire)
            if isFree is False:
                break


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
