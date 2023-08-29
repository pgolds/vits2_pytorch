import re

numDict = {
    '0': '零',
    '1': '幺',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '七',
    '8': '八',
    '9': '九',
}
wordDict = {
    'A': '诶',
    'B': '必',
    'C': '西',
    'D': '滴',
    'E': '亿',
    'F': '哎辅',
    'G': '计',
    'H': '哎尺',
    'I': '哀',
    'J': '戒',
    'K': '楷',
    'L': '哎欧',
    'M': '兆',
    'N': '嗯',
    'O': '欧',
    'P': '批',
    'Q': '扣',
    'R': '啊',
    'S': '哎死',
    'T': '踢',
    'U': '优',
    'V': '微',
    'W': '达不溜',
    'X': '爱克斯',
    'Y': '歪',
    'Z': '则诶',
    '+': '加',
}

# 数字匹配
textPattern = '#(.*?)#'
textPatternPat = re.compile(textPattern)

# 数字文本提取替换
def textformat(text):
    result = re.sub(textPatternPat, replace_text_value_func, text)
    result = result.replace("@", "")
    # 过滤通用英文转汉字谐音
    # for word in wordDict:
    #     result = result.replace(word, wordDict[word])
    #     result = result.replace(word.lower(), wordDict[word])
    return result

# 数字转化
def replace_text_value_func(matched):
    if matched:
        text = matched.group(1)
        result = ''
        for char in text:
            result += numDict.get(char, '零')
        return result
