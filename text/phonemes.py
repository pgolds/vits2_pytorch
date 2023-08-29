import re
from pypinyin import Style
from pypinyin.contrib.neutral_tone import NeutralToneWith5Mixin
from pypinyin.converter import DefaultConverter
from pypinyin.core import Pinyin

from text import pinyin_dict

class MyConverter(NeutralToneWith5Mixin, DefaultConverter):
    pass

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def clean_chinese(text: str):
    text = text.strip()
    text_clean = []
    for char in text:
        if (is_chinese(char)):
            text_clean.append(char)
        else:
            if len(text_clean) > 1 and is_chinese(text_clean[-1]):
                text_clean.append(',')
    text_clean = ''.join(text_clean).strip(',')
    return text_clean

def get_phoneme4pinyin(pinyins):
    result = []
    count_phone = []
    for pinyin in pinyins:
        if pinyin[:-1] in pinyin_dict:
            tone = pinyin[-1]
            a = pinyin[:-1]
            a1, a2 = pinyin_dict[a]
            result += [a1, a2 + tone]
            count_phone.append(2)
    return result, count_phone

def correct_pinyin_tone3(text):
    pinyin_list = [p[0] for p in Pinyin(MyConverter()).pinyin(
        text, style=Style.TONE3, strict=False, neutral_tone_with_five=True)]
    if len(pinyin_list) >= 2:
        for i in range(1, len(pinyin_list)):
            try:
                if re.findall(r'\d', pinyin_list[i-1])[0] == '3' and re.findall(r'\d', pinyin_list[i])[0] == '3':
                    pinyin_list[i-1] = pinyin_list[i-1].replace('3', '2')
            except IndexError:
                pass
    return pinyin_list

def get_phonemes(text):
    text = text.replace("——", "...") \
        .replace("—", "...") \
        .replace("……", "...") \
        .replace("…", "...") \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace("\n", "")
    text = clean_chinese(text)
    phonemes = ["sil"]
    for subtext in text.split(","):
        if (len(subtext) == 0):
            continue
        pinyins = correct_pinyin_tone3(subtext)
        sub_p, sub_c = get_phoneme4pinyin(pinyins)
        phonemes.extend(sub_p)
        # 延长停顿时间
        phonemes.append("sp sp sp sp sp")
    # 句尾去除延长
    phonemes[-1] = "sp"
    phonemes.append("sil")
    return " ".join(phonemes)