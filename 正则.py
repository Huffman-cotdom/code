import re


sentence = ''

# 1. 删除两侧带有括号的汉字
sentence = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", sentence)

# 2. 用中文输入法下的，！？来替换英文输入法下的,!?
sentence = sentence.replace(",", "，")
sentence = sentence.replace("!", "！")
sentence = sentence.replace("?", "？")

# 3. 删除emojy表情
emojy_pattern = re.compile('["\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0'
                            '-\U0001F1FF"]')

sentence = emojy_pattern.sub('', sentence)

# 4. 删除@+昵称
r = re.compile("@.*?\\s")
sentence = r.sub('', sentence)

# 5. 删除链接
r = re.compile("(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)")
sentence = r.sub('', sentence)

# 6. 删除换行符和回车符
r = re.compile("\n|\r")
sentence = r.sub('', sentence)

#  7. 删除特殊符号
r = re.compile(r"[\W]")
sentence = r.sub('', sentence)
