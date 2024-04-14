import pandas as pd
import matplotlib.pyplot as plt
import jieba
from matplotlib.font_manager import FontProperties

font = FontProperties(fname='./WechatHisAnalyse/data/simhei.ttf')

def get_sentiment_dict():
    '''从excel 中读取情感词典，并整理成列表'''
    df = pd.read_excel('WechatHisAnalyse/data/大连理工大学中文情感词汇本体.xlsx')

    # 整理情绪列表
    Joy = []
    Like = []
    Surprise = []
    Anger = []
    Depress = []
    Fear = []
    Dislike = []
    for idx, row in df.iterrows():
        if row['情感分类'] in ['PA', 'PE']:
            Joy.append(row['词语'])
        if row['情感分类'] in ['PD', 'PH', 'PG', 'PB', 'PK']:
            Like.append(row['词语'])
        if row['情感分类'] in ['PC']:
            Surprise.append(row['词语'])
        if row['情感分类'] in ['NA']:
            Anger.append(row['词语'])
        if row['情感分类'] in ['NB', 'NJ', 'NH', 'PF']:
            Depress.append(row['词语'])
        if row['情感分类'] in ['NI', 'NC', 'NG']:
            Fear.append(row['词语'])
        if row['情感分类'] in ['NE', 'ND', 'NN', 'NK', 'NL']:
            Dislike.append(row['词语'])
    Positive = Joy + Like + Surprise
    Negative = Anger + Depress + Fear + Dislike
    print('情绪词语列表整理完成')


    return Joy , Like , Surprise,Anger , Depress , Fear , Dislike,Positive,Negative

Joy , Like , Surprise,Anger , Depress , Fear , Dislike,Positive,Negative = get_sentiment_dict()

def emotion_caculate(text):
    content = jieba.lcut(text)

    positive = 0
    negative = 0
    for word in content:
        if word in Positive:
            positive += 1
        elif word in Negative:
            negative += 1
    if positive>negative:
        polarity = 1
    elif positive<negative:
        polarity = -1
    else:
        polarity = 0
    return polarity

# 计算情感百分比饼图
def generate_sentiment_chart(text_list, suffix):
    '''计算情感百分比'''
    positive = 0
    negative = 0
    # 中立
    neutral = 0
    for text in text_list:
        polarity = emotion_caculate(text)
        if polarity == 1:
            positive += 1
        elif polarity == -1:
            negative += 1
        else:
            neutral += 1
    # 生成饼图
    # labels = ['正面', '负面', '中立']
    # sizes = [positive, negative, neutral]
    # explode = (0, 0, 0)
    # colors = ['#82AEB1', '#C93756', '#C0C5C1']
    # plt.figure()  # Create a new figure
    # plt.pie(sizes, explode=explode, autopct='%1.1f%%', startangle=140, colors=colors)
    # plt.axis('equal')
    # # plt.title('情感分析' + suffix, fontproperties=font)
    # plt.legend(labels, loc='upper right', prop=font)
    # # 保存在本地
    # plt.savefig('./WechatHisAnalyse/data/sentiment' + suffix + '.png')
    # plt.show()
