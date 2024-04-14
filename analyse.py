import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
# from msg_wordcloud import generate_wordcloud
from sentiment_analysis import generate_sentiment_chart
import json
import jieba
import re
from collections import Counter
from wordcloud import WordCloud

# Index(['mesLocalID', 'mesSvrID', 'msgCreateTime', 'msgContent', 'msgStatus',
#        'msgImgStatus', 'messageType', 'mesDes', 'msgSource', 'IntRes1',
#        'IntRes2', 'StrRes1', 'StrRes2', 'msgVoiceText', 'msgSeq',
#        'CompressContent', 'ConBlob'],
#       dtype='object')

history_file = './WechatHisAnalyse/dbFiles/history.csv'
font = FontProperties(fname='./WechatHisAnalyse/data/simhei.ttf')

def read_csv():
    # encoding = detect_encoding(history_file)
    df = pd.read_csv(history_file, encoding= 'utf-8')
    # 第一行是列名
    print(df.columns)
    # print(df.head())
    return df

def filter_text_message(df):
    '''过滤文字类型的消息'''
    df = df[df['messageType'] == 1]
    return df

def preprocess(df):
    '''数据预处理'''
    df = filter_text_message(df)
    # 过滤2018年之前的数据
    df = df[pd.to_datetime(df['msgCreateTime'], unit='s').dt.year >= 2020]
    # 按时间排序
    df = df.sort_values('msgCreateTime')
    return df

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
    update_js(wc_list, 'wordCloud' + suffix)

def calculate_word_freq(df):
    '''统计词频'''
    # 去掉“哈”
    df['msgContent'] = df['msgContent'].str.replace('哈', '')
    # sender 的词云
    sender_text = df[df['mesDes'] == 0]['msgContent']
    generate_wordcloud(sender_text, 'sender')

    # receiver 的词云
    receiver_text = df[df['mesDes'] == 1]['msgContent']
    generate_wordcloud(receiver_text, 'receiver')

    # 总的词云
    generate_wordcloud(df['msgContent'], 'all')



def calculate_msg_count(df):
    '''统计消息数量'''
    # 每个月的消息数量，msgCreateTime是时间戳，如1656741155
    df['msgCreateTime'] = pd.to_datetime(df['msgCreateTime'], unit='s')
    df['month'] = df['msgCreateTime'].dt.strftime('%Y/%m')
    msg_count = df.groupby(['month', 'mesDes']).size().unstack(fill_value=0)
    # 修改json 文件 WechatHisAnalyse/pages/data.json
    # 读json ，如果没有msgCount字段，就创建一个,有就更新
    msg_count_json = {
        'tooltip': {
        'trigger': 'axis',
        'axisPointer': {
            'type': 'shadow'
        },
        },
        'legend': {
            'data': ['kazu', '西瓜']
        },
        'xAxis': {
            'data': df['month'].unique().tolist()
        },
        'yAxis': {},
        'series': [
            {
                'name': 'kazu',
                'type': 'bar',
                'stack': '消息量',
                'data': msg_count.loc[:, 0].fillna(0).tolist()
            },
            {
                'name': '西瓜',
                'type': 'bar',
                'stack': '消息量',
                'data': msg_count.loc[:, 1].fillna(0).tolist()
            }
        ]
    }

    update_js(msg_count_json, 'msgCount')
    # with open('./WechatHisAnalyse/pages/data.json', 'r') as f:
    #     data = json.load(f)
    #     if 'msgCount' in data:
    #         data['msgCount'] = msg_count_json
    #     else:
    #         data['msgCount'] = msg_count_json
    # with open('./WechatHisAnalyse/pages/data.json', 'w') as f:
    #     json.dump(data, f)
    # 生成柱状图
    # msg_count.unstack(level='mesDes').plot(kind='bar', figsize=(20, 6), stacked=True)  # Set the figure size to (20, 6)
    # plt.xlabel('时间', fontproperties=font)
    # plt.ylabel('消息', fontproperties=font)
    # plt.title('消息数量', fontproperties=font)
    # plt.legend(['kazu', '西瓜'], prop=font)
    # plt.show()
    # # 保存在本地
    # plt.savefig('./WechatHisAnalyse/data/message_count.png')


def sentiment_analysis(df):
    '''情感分析'''
    # sender 的情感分析,按年划分
    sender_text = df[df['mesDes'] == 0]
    receiver_text = df[df['mesDes'] == 1]
    for year in range(2021, 2025):
        tmp = sender_text[pd.to_datetime(df['msgCreateTime'], unit='s').dt.year == year]
        generate_sentiment_chart(sender_text[pd.to_datetime(df['msgCreateTime'], unit='s').dt.year == year]['msgContent'], 'sender' + str(year))
        generate_sentiment_chart(receiver_text[pd.to_datetime(df['msgCreateTime'], unit='s').dt.year == year]['msgContent'], 'receiver' + str(year))

def update_js(json_data, key):
    '''更新js文件'''
    with open('./WechatHisAnalyse/pages/data.js', 'r+') as f:
        data = f.read()
        f.write(f"let {key} = {json.dumps(json_data)};\n" )
        f.close()
    


# main
if __name__ == '__main__':
    df = read_csv()
    df = preprocess(df)
    calculate_msg_count(df)
    calculate_word_freq(df)