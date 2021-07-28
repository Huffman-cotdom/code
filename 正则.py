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

# HTML处理
def filterHtmlTag(htmlstr):
		
	'''
	过滤html中的标签
	'''
	# 兼容换行
	s = htmlstr.replace('\r\n','\n')
	s = htmlstr.replace('\r','\n')
	
	# 规则
	re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) # 匹配CDATA
	re_script = re.compile('<\s*script[^>]*>[\S\s]*?<\s*/\s*script\s*>',re.I)# script
	re_style = re.compile('<\s*style[^>]*>[\S\s]*?<\s*/\s*style\s*>',re.I)# style
	re_br = re.compile('<br\\s*?\/??>',re.I)# br标签换行
	re_p = re.compile('<\/p>',re.I)# p标签换行
	re_h = re.compile('<[\!|/]?\w+[^>]*>',re.I)# HTML标签
	re_comment = re.compile('<!--[^>]*-->')# HTML注释
	re_hendstr = re.compile('^\s*|\s*$')# 头尾空白字符
	re_lineblank = re.compile('[\t\f\v ]*')# 空白字符
	re_linenum = re.compile('\n+')# 连续换行保留1个
	
	# 处理
	s = re_cdata.sub('',s)# 去CDATA
	s = re_script.sub('',s) # 去script
	s = re_style.sub('',s)# 去style
	s = re_br.sub('\n',s)# br标签换行
	s = re_p.sub('\n',s)# p标签换行
	s = re_h.sub('',s) # 去HTML标签
	s = re_comment.sub('',s)# 去HTML注释
	s = re_lineblank.sub('',s)# 去空白字符
	s = re_linenum.sub('\n',s)# 连续换行保留1个
	s = re_hendstr.sub('',s)# 去头尾空白字符
	
	# 替换实体
	s = replaceCharEntity(s)
	
	return s

def replaceCharEntity(htmlStr):
	
	'''
	  替换html中常用的字符实体
	  使用正常的字符替换html中特殊的字符实体
	  可以添加新的字符实体到CHAR_ENTITIES 中
	  CHAR_ENTITIES是一个字典前面是特殊字符实体  后面是其对应的正常字符
	  :param htmlStr:
	'''
	CHAR_ENTITIES={'nbsp':' ','160':' ',
			'lt':'<','60':'<',
			'gt':'>','62':'>',
			'amp':'&','38':'&',
			'quot':'"','34':'"',}
	re_charEntity=re.compile(r'&#?(?P<name>\w+);')
	sz=re_charEntity.search(htmlStr)
	while sz:
		entity=sz.group()#entity全称，如>
		key=sz.group('name')#去除&;后的字符如（" "--->key = "nbsp"）    去除&;后entity,如>为gt
		try:
			htmlStr= re_charEntity.sub(CHAR_ENTITIES[key],htmlStr,1)
			sz=re_charEntity.search(htmlStr)
		except KeyError:
			#以空串代替
			htmlStr=re_charEntity.sub('',htmlStr,1)
			sz=re_charEntity.search(htmlStr)
	return htmlStr
