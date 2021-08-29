import zlib; 

class LineConst:

    #LINE Limitation
    maxQuickReply = 13
    maxCarouselColumn = 12
    maxActionPerColumn = 3

    #Channel Credentials
    pengoAccessToken = b"x\x9c\r\xcb\xdf\x0e\x81P\x1c\x00\xe0'2.\xb2\xda\xfc\x19:t\xea\xa8\xa5\xa1\xe9\x88\xcaP\xa3\x90\x92\x8aF\\\xb8\xf1R\xbf'\xe3\xfe\xfb\\\x85\x1a\xb3\x10\xdb\x0b(\xcfh~\xcb\xbb}\x82wne\xe0\xcd9l\x92<X\x1a\x82\x13\xa1\x18^Pf\xbc\xea\x17\xf8\xa2\x8d\xe3\xcea\x06\x8f\xcb\x9dw=\xcaD\x81Z\xa4\t<\x03\x19\x99\x0e\xfa\xbbw&${\xe5\xc8\x8e\xb8\xe2z\xd6\xa6\xb2\xf9\x9f\xf6\x1a\x9e\x03}\xc9\xd0u\xb5NS\xd6O-_\x0f'\xf0\xce\xf9)|5\x9de1\xe5\x1a\xcd\x04\xcaM\xd6\xba\xddM\x02\x1f\xdf \x86t\x92\x86\xed\x84\x1c\x94V\x0f^X\xea\xa2U-e\xb6b\x04\x8fS\xacZ\xe2\x0f\x80\xb3J}"
    pengoSecret = b'x\x9c32\xcd4\xcbJ1K\xcb\xb2H\xb56\xb1676\xb5\xb24M\xb5\xb4\xb4\xb0\xb3455\xb71\xb1\x04\x00\x90\xd9\x089'

    def decode(text,n):
        deText = zlib.decompress(text).decode("utf-8")
        index = 0;
        result = ""
        for c in deText:
            result += chr(ord(c) - (index%n)-1)
            index += 1
        return result

