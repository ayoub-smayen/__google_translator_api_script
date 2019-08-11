import execjs
import requests
import json
import tqdm
import time
import urllib.parse

class Translator():
	def __init__(self):
		self.illegal_signs = []
		self.headers = {'authority':'translate.google.cn', 'method':'GET', 'path':'', 'scheme':'https', 'accept':'*/*', 'accept-encoding':'gzip, deflate, br', 'accept-language' : 'zh-CN,zh;q=0.9', 'cookie':'', 'user-agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB;     rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)', 'x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='}
		self.ctx = execjs.compile("""function TL(a) { var k = ""; var b = 406644; var b1 = 3293161072; var jd = "."; var $b = "+-a^+6"; var Zb = "+-3^+b+-f"; for (var e = [], f = 0, g = 0; g < a.length; g++) { var m = a.charCodeAt(g); 128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), e[f++] = m >> 18 | 240, e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, e[f++] = m >> 6 & 63 | 128), e[f++] = m & 63 | 128) } a = b; for (f = 0; f < e.length; f++) a += e[f], a = RL(a, $b); a = RL(a, Zb); a ^= b1 || 0; 0 > a && (a = (a & 2147483647) + 2147483648); a %= 1E6; return a.toString() + jd + (a ^ b) }; function RL(a, b) { var t = "a"; var Yb = "+"; for (var c = 0; c < b.length - 2; c += 3) { var d = b.charAt(c + 2), d = d >= t ? d.charCodeAt(0) - 87 : Number(d), d = b.charAt(c + 1) == Yb ? a >>> d: a << d; a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d } return a } """)
	def __getToken(self, text):
		return self.ctx.call("TL",text)
	def __buildUrl(self, text, token):
		return 'https://translate.google.cn/translate_a/single?client=t&s1=auto&t1=zh-CN&h1=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&pc=1&ssel=0&tsel=0&kc=2&tk={token}&q={text}'.format(token = token, text = urllib.parse.quote(text))
	def sentence_translate(self, text):
		if len(text.strip()) == 0: return text # return empty sentences
		url = self.__buildUrl(text, self.__getToken(text))
		responde = requests.get(url, headers = self.headers).text
		try:
			result = json.loads(requests.get(url, headers = self.headers).text)[0][0][0] # Select translated sentence
		except json.decoder.JSONDecodeError as err:
			# text length exceeds the limitation
			# recursive solution
			middle_point = len(text)//2
			result_left = self.sentence_translate(text[:middle_point])
			result_right = self.sentence_translate(text[middle_point:])
			result = result_left + result_right
		return result
	def file_translate(self, source_file_path, target_file_path = None):
		translated_sentences = [self.sentence_translate(each_line) for each_line in tqdm.tqdm(open(source_file_path, 'r', encoding = 'utf-8'))]
		if target_file_path != None:
			with open(target_file_path, 'w', encoding = 'utf-8') as file:
				file.write(''.join(translated_sentences))
		return translated_sentences

def main():
	t = Translator()
	f = open('a.txt', 'w')
	translated_file = t.file_translate('C:/Users/Lenovo/Downloads/virtuoso/se/3sa_se_en.log', 'C:/Users/Lenovo/Downloads/virtuoso/se/3sa_se_ch.log')

if __name__ == '__main__':
	main()