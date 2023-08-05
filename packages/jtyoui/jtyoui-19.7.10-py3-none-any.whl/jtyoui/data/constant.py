#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time : 2019/2/19
# @Email : jtyoui@qq.com


# 常见的照片格式
Photo_Format = (
    'bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps',
    'ai', 'raw', 'WMF', 'webp'
)

# 常见的文字编码格式
Decode = ('Unicode', 'ASCII', 'GBK', 'GB2312', 'UTF-8', 'ISO-8859-1', 'UTF-16', 'GB18030', 'ISO-8859-2')


# 数学符号
class MathSymbols:
    """‖‰℃℉←↑→↓∈∏∑°√∝∞∟∠∣∧∨∩∪∫∮～≈≌≒≠≡"""
    vector_value = '‖'  # ‖A‖ 表示A向量的值
    one_thousand = '‰'  # 千分号
    celsius_scale = '℃'  # 摄氏温标的温度计量单位
    fahrenheit_scale = '℉'  # 华氏温标
    right = '→'  # 向右
    left = '←'  # 向左
    up = '↑'  # 向上
    down = '↓'  # 向下
    belong_to = '∈'  # 属于
    product = '∏'  # 求乘积
    summation = '∑'  # 求累加
    one_degrees = '°'  # 1度,度角单位
    check_mark = '√'  # 对钩
    positive_proportion = '∝'
    infinity = '∞'
    slope = '∠'
    intersection = '∩'  # 交集
    and_ = '∧'  # 逻辑和
    condition = '∣'  # 条件概率P(A∣B)
    union = '∪'  # 并集
    integral = '∫'  # 积分
    or_ = '∨'  # 逻辑或
    closed_curve = '∮'  # 闭合曲线
    asymptotically_equal = '～'  # 逐渐相等,f(x)～g(x),表示lim f(x)=lim g(x)
    approximately_equal = '≈'  # 约等于
    identically_equal = '≌'  # 全等
    reversible = '≒'  # 可逆
    not_equal = '≠'  # 不等于
    identity = '≡'  # 恒等于
    ls = list('‖‰℃℉←↑→↓∈∏∑°√∝∞∟∠∣∧∨∩∪∫∮～≈≌≒≠≡')


# 将英文的星期转为中文
week_to_chinese = {
    'Monday': '星期一',
    'Mon': '星期一',
    'Mon.': '星期一',
    'Tuesday': '星期二',
    'Tues': '星期二',
    'Tues.': '星期二',
    'Tue': '星期二',
    'Wednesday': '星期三',
    'Wed': '星期三',
    'Wed.': '星期三',
    'Thursday': '星期四',
    'Thur': '星期四',
    'Thu': '星期四',
    'Thur.': '星期四',
    'Thurs': '星期四',
    'Thurs.': '星期四',
    'Friday': '星期五',
    'Fri': '星期五',
    'Fri.': '星期五',
    'Saturday': '星期六',
    'Sat': '星期六',
    'Sat.': '星期六',
    'Sunday': '星期日',
    'Sun': '星期日',
    'Sun.': '星期日',
}

# 将中文的星期转为英文
week_to_english = {
    '星期一': 'Monday',
    '星期二': 'Tuesday',
    '星期三': 'Wednesday',
    '星期四': 'Thursday',
    '星期五': 'Friday',
    '星期六': 'Saturday',
    '星期日': 'Sunday',
}

# 将英文的月份转为中文
month_to_chinese = {
    'January': '一月',
    'Jan': '一月',
    'Jan.': '一月',
    'February': '二月',
    'Feb': '二月',
    'Feb.': '二月',
    'March': '三月',
    'Mar': '三月',
    'Mar.': '三月',
    'April': '四月',
    'Apr': '四月',
    'Apr.': '四月',
    'May': '五月',
    'May.': '五月',
    'June': '六月',
    'Jun': '六月',
    'Jun.': '六月',
    'July': '七月',
    'Jul': '七月',
    'Jul.': '七月',
    'August': '八月',
    'Aug': '八月',
    'Aug.': '八月',
    'September': '九月',
    'Sept': '九月',
    'Sept.': '九月',
    'October': '十月',
    'Oct': '十月',
    'Oct.': '十月',
    'November': '十一月',
    'Nov': '十一月',
    'Nov.': '十一月',
    'December': '十二月',
    'Dec': '十二月',
    'Dec.': '十二月'
}

# 将中文的月份转为英文
month_to_english = {
    '一月': 'January',
    '二月': 'February',
    '三月': 'March',
    '四月': 'April',
    '五月': 'May',
    '六月': 'June',
    '七月': 'July',
    '八月': 'August',
    '九月': 'September',
    '十月': 'October',
    '十一月': 'November',
    '十二月': 'December'
}

# 翻译http转态码的含义
http_status_code = {
    '100': "请求者应当继续提出请求。服务器返回此代码表示已收到请求的第一部分，正在等待其余部分",
    '101': "请求者已要求服务器切换协议，服务器已确认并准备切换",
    '300': "针对请求，服务器可执行多种操作。服务器可根据请求者选择一项操作，或提供操作列表供请求者选择",
    '301': "请求的网页已永久移动到新位置。服务器返回此响应（对GET或HEAD请求的响应）时，会自动将请求者转到新位置",
    '302': "服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求",
    '303': "请求者应当对不同的位置使用单独的GET请求来检索响应时，服务器返回此代码",
    '304': "自从上次请求后，请求的网页未修改过。服务器返回此响应时，不会返回网页内容",
    '305': "请求者只能使用代理访问请求的网页。如果服务器返回此响应，还表示请求者应使用代理",
    '307': "服务器目前从不同位置的网页响应请求，但请求者应继续使用原有位置来进行以后的请求",
    '400': "服务器不理解请求的语法",
    '401': "请求要求身份验证。对于需要登录的网页，服务器可能返回此响应",
    '403': "服务器拒绝请求",
    '404': "服务器找不到请求的网页",
    '405': "禁用请求中指定的方法",
    '406': "无法使用请求的内容特性响应请求的网页",
    '407': "请求者应当授权使用代理",
    '408': "服务器等候请求时发生超时",
    '409': "服务器在完成请求时发生冲突。服务器必须在响应中包含有关冲突的信息",
    '410': "如果请求的资源已永久删除，服务器就会返回此响应",
    '411': "服务器不接受不含有效内容长度标头字段的请求",
    '412': "服务器未满足请求者在请求中设置的其中一个前提条件",
    '413': "服务器无法处理请求，因为请求实体过大，超出服务器的处理能力",
    '414': "请求的URI过长，服务器无法处理",
    '415': "请求的格式不受请求页面的支持",
    '416': "如果页面无法提供请求的范围，则服务器会返回此状态代码",
    '417': "服务器未满足期望':请求标头字段的要求",
    '500': "服务器遇到错误，无法完成请求",
    '501': "服务器不具备完成请求的功能。例如，服务器无法识别请求方法时可能会返回此代码",
    '502': "服务器作为网关或代理，从上游服务器收到无效响应",
    '503': "服务器目前无法使用（由于超载或停机维护）。通常这只是暂时状态",
    '504': "服务器作为网关或代理，但是没有及时从上游服务器收到请求",
    '505': "服务器不支持请求中所用的HTTP协议版本",
}

# 将拼音声调去掉
letter_maps = {'ā': 'a',
               'á': 'a',
               'a': 'a',
               'ǎ': 'a',
               'à': 'a',
               'e': 'e',
               'ē': 'e',
               'é': 'e',
               'ě': 'e',
               'è': 'e',
               'o': 'o',
               'ō': 'o',
               'ó': 'o',
               'ǒ': 'o',
               'ò': 'o',
               'm': 'm',
               'ǹ': 'n',
               'ň': 'n',
               'ǚ': 'u',
               'g': 'g',
               'ī': 'i',
               'k': 'k',
               'ń': 'n',
               'ǘ': 'u',
               'y': 'y',
               'ǔ': 'u',
               'ū': 'u',
               'ǜ': 'u',
               'x': 'x',
               'n': 'n',
               'd': 'd',
               'ú': 'u',
               'r': 'r',
               'c': 'c',
               'j': 'j',
               'i': 'i',
               'ü': 'u',
               'w': 'w',
               's': 's',
               'b': 'b',
               'l': 'l',
               'h': 'h',
               'ǐ': 'i',
               'í': 'i',
               'ḿ': 'm',
               'p': 'p',
               'f': 'f',
               'u': 'u',
               'q': 'q',
               'z': 'z',
               'ì': 'i',
               'ù': 'u',
               't': 't'
               }

# 节日
holiday = {
    "01-01": "元旦节",
    "腊月卅十": "除夕",
    "正月除一": "春节",
    "正月十五": "元宵节",
    "02-14": "情人节",
    "03-08": "妇女节",
    "03-12": "植树节",
    "04-01": "愚人节",
    "04-05": "清明节",
    "五月除五": "端午节",
    "05-01": "劳动节",
    "05-04": "青年节",
    "06-01": "儿童节",
    "07-01": "建党节",
    "七月除七": "七夕节",
    "08-01": "建军节",
    "七月十五": "中元节",
    "八月十五": "中秋节",
    "九月除九": "重阳节",
    "09-10": "教师节",
    "10-01": "国庆节",
    "11-01": "万圣节",
    "12-24": "平安夜",
    "12-25": "圣诞节"
}

# 中国的月份
chinese_mon = ["零", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]

# 中国的月份对应数字
chinese_mon_number = {
    '零': '0',
    '正': '1',
    '一': '1',
    '二': '2',
    '两': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
    '十': '10',
    '冬': '11',
    '腊': '12',
}

# 增加时间
add_time = {
    '天': 1,
    '前天': -2,
    '昨天': -1,
    '今天': 0,
    '明天': 1,
    '后天': 2,
    '去年': -1 * 365,
    '前年': -2 * 365,
    '昨年': -1 * 365,
    '今年': 0,
    '明年': 1 * 365,
    '后年': 2 * 365,
    '上个月': -1 * 31,
    '这个月': 0,
    '下个月': 1 * 31,
    '上月': -1 * 31,
    '这月': 0,
    '下月': 1 * 31,
    '下周': 7,
    '上周': -7,
    '下个周': 7,
    '上个周': -7,
    '这周': 0,
    '这个周': 0,
}

# 中文数字
num_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十']
more_num_symbol = ['零', '百', '千', '万', '亿', '兆'] + num_symbol

# 模糊音
fuzzy_tone = {
    'z': 'zh',
    'l': 'n',
    'c': 'ch',
    'f': 'h',
    's': 'sh',
    'r': 'l',
    'en': 'eng',
    'in': 'ing',
    'an': 'ang',
    'ei': 'ui'
}

# 中文空格
chinese_blank_space = '\u3000'
chinese_blank_spaces = '　'

if __name__ == '__main__':
    print(MathSymbols.intersection)
    print(MathSymbols.ls)
