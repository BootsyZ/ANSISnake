class EscSeq:
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'

    CWORKING = '\33[1;30;45m'
    CFAILED = '\33[1;5;30;41m'
    CSUCCES = '\33[1;30;42m'
    CBASE = '\33[1;37;100m'
    CBORDER = '\33[1;37;40m'

    CBLACKONWHITE = '\33[1;30;47m'
    CWHITEONBLACK = '\33[1;37;40m'

    LWRAPOFF = "\33[?7l"
    LWRAPON = "\33[?7h"

    TRESET = "\33c"

    DHEIGHTT = "\33#3"
    DHEIGHTB = "\33#4"
    SWIDTH = "\33#5"
    DWIDTH = "\33#6"


    @staticmethod
    def GetColourValue(colour):
        if colour == EscSeq.CBLACK \
                or colour == EscSeq.CBLACKBG \
                or colour == EscSeq.CWHITEONBLACK:
            return 0, 0, 0
        elif colour == EscSeq.CWHITE \
                or colour == EscSeq.CWHITE2 \
                or colour == EscSeq.CWHITEBG \
                or colour == EscSeq.CWHITEBG2 \
                or colour == EscSeq.CBLACKONWHITE:
            return 255, 255, 255
        elif colour == EscSeq.CGREY \
                or colour == EscSeq.CGREYBG:
            return 63, 63, 63
        elif colour == EscSeq.CRED \
                or colour == EscSeq.CRED2 \
                or colour == EscSeq.CREDBG \
                or colour == EscSeq.CREDBG2:
            return 255, 0, 0
        elif colour == EscSeq.CGREEN \
                or colour == EscSeq.CGREEN2 \
                or colour == EscSeq.CGREENBG \
                or colour == EscSeq.CGREENBG2:
            return 0, 255, 0
        elif colour == EscSeq.CYELLOW \
                or colour == EscSeq.CYELLOW2 \
                or colour == EscSeq.CYELLOWBG \
                or colour == EscSeq.CYELLOWBG2:
            return 255, 255, 0
        elif colour == EscSeq.CBLUE \
                or colour == EscSeq.CBLUE2 \
                or colour == EscSeq.CBLUEBG \
                or colour == EscSeq.CBLUEBG2:
            return 0, 0, 255
        elif colour == EscSeq.CVIOLET \
                or colour == EscSeq.CVIOLET2 \
                or colour == EscSeq.CVIOLETBG \
                or colour == EscSeq.CVIOLETBG2:
            return 255, 0, 255
        elif colour == EscSeq.CBEIGE \
                or colour == EscSeq.CBEIGE2 \
                or colour == EscSeq.CBEIGEBG \
                or colour == EscSeq.CBEIGEBG2:
            return 255, 255, 127
        elif colour == EscSeq.CEND:
            return 0, 0, 0
        else:
            return 0, 0, 0

    @staticmethod
    def GetColourValueBackground(colour):
        if colour == EscSeq.CBLACKBG \
                or colour == EscSeq.CWHITEONBLACK:
            return 0, 0, 0
        elif colour == EscSeq.CWHITEBG \
                or colour == EscSeq.CWHITEBG2 \
                or colour == EscSeq.CBLACKONWHITE:
            return 255, 255, 255
        elif colour == EscSeq.CGREYBG:
            return 63, 63, 63
        elif colour == EscSeq.CREDBG:
            return 192, 0, 0
        elif colour == EscSeq.CREDBG2:
            return 255, 0, 0
        elif colour == EscSeq.CGREENBG:
            return 0, 192, 0
        elif colour == EscSeq.CGREENBG2:
            return 0, 255, 0
        elif colour == EscSeq.CYELLOWBG:
            return 192, 192, 0
        elif colour == EscSeq.CYELLOWBG2:
            return 255, 255, 0
        elif colour == EscSeq.CBLUEBG:
            return 0, 0, 192
        elif colour == EscSeq.CBLUEBG2:
            return 0, 0, 255
        elif colour == EscSeq.CVIOLETBG:
            return 192, 0, 192
        elif colour == EscSeq.CVIOLETBG2:
            return 255, 0, 255
        elif colour == EscSeq.CBEIGEBG:
            return 192, 192, 95
        elif colour == EscSeq.CBEIGEBG2:
            return 255, 255, 127
        elif colour == EscSeq.CEND:
            return 0, 0, 0
        else:
            return 0, 0, 0

    @staticmethod
    def GetColourValueForeground(colour):
        if colour == EscSeq.CBLACK \
                or colour == EscSeq.CBLACKONWHITE:
            return 0, 0, 0
        elif colour == EscSeq.CWHITE \
                or colour == EscSeq.CWHITE2 \
                or colour == EscSeq.CWHITEONBLACK:
            return 255, 255, 255
        elif colour == EscSeq.CGREY:
            return 63, 63, 63
        elif colour == EscSeq.CRED \
                or colour == EscSeq.CRED2:
            return 255, 0, 0
        elif colour == EscSeq.CGREEN \
                or colour == EscSeq.CGREEN2:
            return 0, 255, 0
        elif colour == EscSeq.CYELLOW \
                or colour == EscSeq.CYELLOW2:
            return 255, 255, 0
        elif colour == EscSeq.CBLUE \
                or colour == EscSeq.CBLUE2:
            return 0, 0, 255
        elif colour == EscSeq.CVIOLET \
                or colour == EscSeq.CVIOLET2:
            return 255, 0, 255
        elif colour == EscSeq.CBEIGE \
                or colour == EscSeq.CBEIGE2:
            return 255, 255, 127
        elif colour == EscSeq.CEND:
            return 255, 255, 255
        else:
            return 255, 255, 255
