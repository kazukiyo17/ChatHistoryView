import jieba
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_wordcloud(text_list, suffix=""):
    '''
    生成词云
    '''
    with open("WechatHisAnalyse/data/CNstopwords.txt",'r',encoding='utf-8') as f:
        lines = f.readlines()
        stopwords = [line.strip().replace("\ufeff","") for line in lines]

    # 分词
    emoji_pattern = re.compile("(\[.+?\])")
    norm_texts = []
    for text in text_list:
        text = emoji_pattern.sub("", text) # 去除表情
        text = text.replace('\n', '') # 去除换行符
        words = jieba.lcut(text) # 分词
        # 去除停用词
        res = [word for word in words if word not in stopwords and word.replace(" ","")!="" and len(word)>1]
        if res!=[]:
            norm_texts.extend(res)
    
    # 词频统计
    count_dict = dict(Counter(norm_texts))
    print(count_dict)
    wc = WordCloud(font_path="WechatHisAnalyse/data/simhei.ttf", background_color='white', include_numbers=False, random_state=0)
    wc = wc.fit_words(count_dict)
    # wc 转为list
    wc_list = [{'name': k, 'value': v} for k, v in wc.words_.items()]
    print(wc_list)
    # plt.figure(figsize=(10, 6))  # Increase the figure size for better clarity
    # plt.imshow(wc)
    # plt.axis("off")  # Remove the axis
    # plt.tight_layout()  # Adjust the layout
    # plt.show()
    # wc.to_file('WechatHisAnalyse/data/wordcloud' + suffix + '.png')
