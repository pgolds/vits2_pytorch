"""
### pinyinkit
文本转拼音的模块，依赖python-pinyin，jieba，phrase-pinyin-data模块。
"""
import re
from pypinyin import Style, lazy_pinyin

# 兼容0.1.0之前的版本。
# 音调：5为轻声
_diao_re = re.compile(r"^([a-z]{1,6})([12345])$")


def text2pinyin(text, errors=None, **kwargs):
    """
    汉语文本转为拼音列表
    :param text: str,汉语文本字符串
    :param errors: function,对转拼音失败的字符的处理函数，默认保留原样
    :return: list,拼音列表
    """
    if errors is None:
        errors = default_errors
    pin = lazy_pinyin(text, style=Style.TONE3, errors=errors, strict=True, neutral_tone_with_five=True, **kwargs)
    return pin


def default_errors(x):
    return list(x)


def split_pinyin(py):
    """
    单个拼音转为音素列表
    :param py: str,拼音字符串
    :param errors: function,对OOV拼音的处理函数，默认保留原样
    :return: list,音素列表
    """
    parts = _diao_re.match(py)
    if parts:
        return parts.groups()


def change_diao(src):
    """
    拼音变声调，连续上声声调的把前一个上声变为阳平。
    :param src: list,音素列表
    :return: list,变调后的音素列表
    """
    flag = -5
    out = []
    for i, w in enumerate(reversed(src)):
        if w == '3':
            if i - flag == 4:
                out.append('2')
            else:
                flag = i
                out.append(w)
        else:
            out.append(w)

    return list(reversed(out))


if __name__ == "__main__":
    print(__file__)
    assert text2pinyin("拼音") == ['pin1', 'yin1']
    assert text2pinyin("汉字,a1") == ['han4', 'zi4', ',', 'a', '1']