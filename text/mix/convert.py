"""
#### convert
文本转换。
全角半角转换
"""

# 半角转全角映射表
ban2quan_dict = {i: i + 65248 for i in range(33, 127)}
ban2quan_dict.update({32: 12288})

# 全角转半角映射表
quan2ban_dict = {v: k for k, v in ban2quan_dict.items()}


def ban2quan(text: str):
    """
    半角转全角
    :param text:
    :return:
    """
    return text.translate(ban2quan_dict)


def quan2ban(text: str):
    """
    全角转半角
    :param text:
    :return:
    """
    return text.translate(quan2ban_dict)


if __name__ == "__main__":
    assert ban2quan("aA1 ,:$。、") == "ａＡ１　，：＄。、"
    assert quan2ban("ａＡ１　，：＄。、") == "aA1 ,:$。、"
