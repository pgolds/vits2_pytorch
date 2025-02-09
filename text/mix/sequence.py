"""
#### sequence
转为序列的方法，文本转为音素列表，文本转为ID列表。
拼音变调，拼音转音素。
"""
from .phoneme import shengyun2ph_dict, diao2ph_dict, char2ph_dict, pinyin2ph_dict, ph2pinyin_dict, ph2char_dict
from .pinyin import text2pinyin, change_diao
from .symbol import _chain, _eos, _pad, _oov, symbol_chinese
from .convert import quan2ban
import re

# 分隔英文字母
_en_re = re.compile(r"([a-zA-Z]+)")

# phs = ({w for p in shengyun2ph_dict.values() for w in p.split()}
#        | set(diao2ph_dict.values()) | set(char2ph_dict.values()))

phs = ({p.split()[0] for p in shengyun2ph_dict.values()}) | ({p.split()[1] + j for p in shengyun2ph_dict.values() for j in set(diao2ph_dict.values())}
       | set(char2ph_dict.values()))

assert bool(phs - set(symbol_chinese)) is False

ph2id_dict = {p: i for i, p in enumerate(symbol_chinese)}
id2ph_dict = {i: p for i, p in enumerate(symbol_chinese)}

assert len(ph2id_dict) == len(id2ph_dict)

def chartext2phoneme(text):
    """
    文本转为音素，用中文音素方案。
    中文转为拼音，按照清华大学方案转为音素，分为辅音、元音、音调。
    英文全部大写，转为字母读音。
    英文非全部大写，转为英文读音。
    标点映射为音素。
    :param text: str,正则化后的文本。
    :return: list,音素列表
    """
    text = normalize_chinese(text)
    text = normalize_english(text)
    pys = text2pinyin(text, errors=lambda x: [(w,) for w in x])
    phs = charpinyin2phoneme(pys)
    # phs = change_diao(phs)
    return phs

def text2phoneme(text):
    """
    文本转为音素，用中文音素方案。
    中文转为拼音，按照清华大学方案转为音素，分为辅音、元音、音调。
    英文全部大写，转为字母读音。
    英文非全部大写，转为英文读音。
    标点映射为音素。
    :param text: str,正则化后的文本。
    :return: list,音素列表
    """
    text = normalize_chinese(text)
    text = normalize_english(text)
    pys = text2pinyin(text, errors=lambda x: [(w,) for w in x])
    phs = pinyin2phoneme(pys)
    phs = change_diao(phs)
    return phs


def text2sequence(text):
    """
    文本转为ID序列。
    :param text:
    :return:
    """
    phs = text2phoneme(text)
    seq = phoneme2sequence(phs)
    return seq

def charpinyin2phoneme(src):
    out = []
    for py in src:
        phs = []
        if py in pinyin2ph_dict:
            ph = pinyin2ph_dict[py].split()
            phs.extend(ph)
        else:
            for w in py:
                ph = py_errors(w)
                phs.extend(ph)
        # phs.append(_chain)  # 一个字符对应一个chain符号
        out.extend(phs)
    return out

def pinyin2phoneme(src):
    """
    拼音或其他字符转音素。
    :param src: list,拼音用str格式，其他用tuple格式。
    :return: list
    """
    out = [_pad]
    for py in src:
        phs = []
        if py in pinyin2ph_dict:
            ph = pinyin2ph_dict[py].split()
            phs.extend(ph)
        else:
            for w in py:
                ph = py_errors(w)
                phs.extend(ph)
        # phs.append(_chain)  # 一个字符对应一个chain符号
        out.extend(phs)
    out.append(_eos)
    out.append(_pad)
    return out


def phoneme2sequence(src):
    out = []
    for w in src:
        if w in ph2id_dict:
            out.append(ph2id_dict[w])
    return out


def sequence2phoneme(src):
    out = []
    for w in src:
        if w in id2ph_dict:
            out.append(id2ph_dict[w])
    return out


def phoneme2pinyin(src, with_eos=False):
    tmp = []
    out = []
    for ph in src:
        if ph == _chain:
            phs = ' '.join(tmp)
            if phs in ph2pinyin_dict:
                out.append(ph2pinyin_dict[phs])
            elif phs in ph2char_dict:
                out.append(ph2char_dict[phs])
            else:
                out.append(_oov)
            tmp = []
        else:
            tmp.append(ph)
    else:
        if with_eos:
            for ph in tmp:
                if ph in {_eos, _pad}:
                    out.append(ph)
                else:
                    out.append(_oov)
    return out


def py_errors(text):
    out = []
    for p in text:
        if p in char2ph_dict:
            out.append(char2ph_dict[p])
    return out


def normalize_chinese(text):
    text = quan2ban(text)
    return text


def normalize_english(text):
    out = []
    parts = _en_re.split(text)
    for part in parts:
        if not part.isupper():
            out.append(part.lower())
        else:
            out.append(part)
    return "".join(out)


if __name__ == "__main__":
    print(__file__)