"""
统一配置管理模块
集中管理政权颜色、省份映射、都城坐标等配置
"""

# ============================================
# 政权基础配置
# ============================================

# 五代政权
WUDAI_REGIMES = [
    {"name": "后梁", "start": 907, "end": 923, "capital": "开封", "founder": "朱温", "color": "#e74c3c"},
    {"name": "后唐", "start": 923, "end": 936, "capital": "洛阳", "founder": "李存勖", "color": "#3498db"},
    {"name": "后晋", "start": 936, "end": 947, "capital": "开封", "founder": "石敬瑭", "color": "#9b59b6"},
    {"name": "后汉", "start": 947, "end": 950, "capital": "开封", "founder": "刘知远", "color": "#e67e22"},
    {"name": "后周", "start": 951, "end": 960, "capital": "开封", "founder": "郭威", "color": "#2ecc71"},
]

# 十国政权
SHIGUO_REGIMES = [
    {"name": "吴越", "start": 907, "end": 978, "capital": "杭州", "founder": "钱镠", "color": "#1abc9c"},
    {"name": "南唐", "start": 937, "end": 975, "capital": "南京", "founder": "李昪", "color": "#e74c3c"},
    {"name": "前蜀", "start": 907, "end": 925, "capital": "成都", "founder": "王建", "color": "#f39c12"},
    {"name": "后蜀", "start": 934, "end": 965, "capital": "成都", "founder": "孟知祥", "color": "#d35400"},
    {"name": "闽国", "start": 909, "end": 945, "capital": "福州", "founder": "王审知", "color": "#9b59b6"},
    {"name": "南汉", "start": 917, "end": 971, "capital": "广州", "founder": "刘䶮", "color": "#e74c3c"},
    {"name": "楚", "start": 907, "end": 951, "capital": "长沙", "founder": "马殷", "color": "#3498db"},
    {"name": "荆南", "start": 924, "end": 963, "capital": "荆州", "founder": "高季兴", "color": "#1abc9c"},
    {"name": "北汉", "start": 951, "end": 979, "capital": "太原", "founder": "刘崇", "color": "#95a5a6"},
]

# ============================================
# 颜色配置
# ============================================

# 政权颜色配置（与上面保持一致，方便单独引用）
REGIME_COLORS = {
    # 五代
    "后梁": "#e74c3c",
    "后唐": "#3498db",
    "后晋": "#9b59b6",
    "后汉": "#e67e22",
    "后周": "#2ecc71",
    # 十国
    "吴越": "#1abc9c",
    "南唐": "#e74c3c",
    "前蜀": "#f39c12",
    "后蜀": "#d35400",
    "闽国": "#9b59b6",
    "南汉": "#e74c3c",
    "楚": "#3498db",
    "荆南": "#1abc9c",
    "北汉": "#95a5a6",
}

# 藩镇颜色配置
FANZHEN_COLORS = {
    "宣武": "#e74c3c",
    "河东": "#3498db",
    "凤翔": "#9b59b6",
    "成德": "#e67e22",
    "魏博": "#2ecc71",
    "卢龙": "#1abc9c",
    "淮南": "#f39c12",
    "镇海": "#e74c3c",
    "武安": "#3498db",
    "武宁": "#9b59b6",
}

# ============================================
# 地理配置
# ============================================

# 省份名称映射（古 -> 今）
PROVINCE_MAPPING = {
    "河南": "河南省",
    "河北": "河北省",
    "山东": "山东省",
    "山西": "山西省",
    "陕西": "陕西省",
    "浙江": "浙江省",
    "江苏": "江苏省",
    "上海": "上海市",
    "安徽": "安徽省",
    "江西": "江西省",
    "湖北": "湖北省",
    "湖南": "湖南省",
    "四川": "四川省",
    "重庆": "重庆市",
    "福建": "福建省",
    "广东": "广东省",
    "广西": "广西",
    "海南": "海南省",
    "甘肃": "甘肃省",
    "辽宁": "辽宁省",
    "内蒙古": "内蒙古",
}

# 政权与现代省份对照
REGIME_TO_PROVINCE = {
    "后梁": ["河南", "山东", "陕西"],
    "后唐": ["河南", "河北", "山西", "山东"],
    "后晋": ["河南", "河北", "山西", "山东"],
    "后汉": ["河南", "河北", "山西", "山东"],
    "后周": ["河南", "河北", "山东", "安徽"],
    "吴越": ["浙江", "上海", "江苏"],
    "南唐": ["江苏", "安徽", "江西", "湖北"],
    "前蜀": ["四川", "重庆", "陕西"],
    "后蜀": ["四川", "重庆", "陕西"],
    "闽国": ["福建"],
    "南汉": ["广东", "广西", "海南"],
    "楚": ["湖南"],
    "荆南": ["湖北"],
    "北汉": ["山西"],
}

# 都城坐标配置
CAPITAL_COORDS = {
    "开封": (114.34, 34.79, "后梁/后晋/后汉/后周"),
    "洛阳": (112.43, 34.62, "后唐"),
    "杭州": (120.16, 30.27, "吴越"),
    "南京": (118.78, 32.07, "南唐"),
    "成都": (104.07, 30.67, "前蜀/后蜀"),
    "福州": (119.30, 26.08, "闽国"),
    "广州": (113.27, 23.13, "南汉"),
    "长沙": (112.94, 28.23, "楚"),
    "荆州": (112.19, 30.33, "荆南"),
    "太原": (112.55, 37.87, "北汉"),
}

# 都城与省份映射
CAPITAL_TO_PROVINCE = {
    "开封": "河南省",
    "洛阳": "河南省",
    "杭州": "浙江省",
    "南京": "江苏省",
    "成都": "四川省",
    "福州": "福建省",
    "广州": "广东省",
    "长沙": "湖南省",
    "荆州": "湖北省",
    "太原": "山西省",
}

# ============================================
# 藩镇基础配置
# ============================================

# 唐末主要藩镇基础数据
FANZHEN_BASE_DATA = {
    "宣武": {"color": "#e74c3c", "area": "河南", "power": 95, "province": "河南省"},
    "河东": {"color": "#3498db", "area": "山西", "power": 90, "province": "山西省"},
    "凤翔": {"color": "#9b59b6", "area": "陕西", "power": 75, "province": "陕西省"},
    "成德": {"color": "#e67e22", "area": "河北", "power": 70, "province": "河北省"},
    "魏博": {"color": "#2ecc71", "area": "河北", "power": 85, "province": "河北省"},
    "卢龙": {"color": "#1abc9c", "area": "河北", "power": 80, "province": "河北省"},
    "淮南": {"color": "#f39c12", "area": "江苏", "power": 70, "province": "江苏省"},
    "镇海": {"color": "#e74c3c", "area": "浙江", "power": 60, "province": "浙江省"},
    "武安": {"color": "#3498db", "area": "湖南", "power": 55, "province": "湖南省"},
    "武宁": {"color": "#9b59b6", "area": "江苏", "power": 50, "province": "江苏省"},
}

# ============================================
# 藩镇编年史配置
# ============================================

# 藩镇编年史数据（藩镇名：[{年份，事件，节度使}，...]）
FANZHEN_CHRONICLES = {
    "宣武": [
        {"year": 763, "event": "安史之乱平定后，设宣武节度使", "jiedushi": "田承嗣"},
        {"year": 882, "event": "朱温降唐，被任命为宣武节度使", "jiedushi": "朱温"},
        {"year": 901, "event": "朱温受封梁王", "jiedushi": "朱温"},
        {"year": 907, "event": "朱温篡唐建立后梁，宣武归中央", "jiedushi": "(中央直辖)"},
    ],
    "河东": [
        {"year": 763, "event": "安史之乱平定后，设河东节度使", "jiedushi": "李光弼"},
        {"year": 878, "event": "李克用任河东节度使", "jiedushi": "李克用"},
        {"year": 891, "event": "李克用被封为晋王", "jiedushi": "李克用"},
        {"year": 923, "event": "李存勖建立后唐，河东归中央", "jiedushi": "(中央直辖)"},
    ],
    "魏博": [
        {"year": 763, "event": "安史之乱平定后，设魏博节度使", "jiedushi": "田承嗣"},
        {"year": 812, "event": "田弘正归顺朝廷", "jiedushi": "田弘正"},
        {"year": 829, "event": "史宪诚杀田弘正", "jiedushi": "史宪诚"},
        {"year": 907, "event": "归附后梁", "jiedushi": "(梁属)"},
        {"year": 915, "event": "后梁分割魏博，引发兵变", "jiedushi": "(兵变)"},
        {"year": 923, "event": "归附后唐", "jiedushi": "(唐属)"},
    ],
    "成德": [
        {"year": 763, "event": "安史之乱平定后，设成德节度使", "jiedushi": "李宝臣"},
        {"year": 820, "event": "王承宗归顺朝廷", "jiedushi": "王承宗"},
        {"year": 821, "event": "王廷凑杀田弘正，复叛", "jiedushi": "王廷凑"},
        {"year": 907, "event": "归附后梁", "jiedushi": "(梁属)"},
        {"year": 922, "event": "被后唐所灭", "jiedushi": "(唐直辖)"},
    ],
    "卢龙": [
        {"year": 763, "event": "安史之乱平定后，设卢龙节度使", "jiedushi": "李怀仙"},
        {"year": 826, "event": "李载义杀朱延嗣", "jiedushi": "李载义"},
        {"year": 907, "event": "刘守光称帝，国号大燕", "jiedushi": "刘守光"},
        {"year": 913, "event": "被后梁所灭", "jiedushi": "(梁直辖)"},
    ],
    "凤翔": [
        {"year": 763, "event": "安史之乱平定后，设凤翔节度使", "jiedushi": "李抱玉"},
        {"year": 887, "event": "李茂贞任凤翔节度使", "jiedushi": "李茂贞"},
        {"year": 901, "event": "李茂贞与朱温交战", "jiedushi": "李茂贞"},
        {"year": 907, "event": "向后梁称臣", "jiedushi": "李茂贞"},
        {"year": 923, "event": "被后唐所灭", "jiedushi": "(唐直辖)"},
    ],
    "淮南": [
        {"year": 763, "event": "安史之乱平定后，设淮南节度使", "jiedushi": "陈少游"},
        {"year": 882, "event": "高骈任淮南节度使", "jiedushi": "高骈"},
        {"year": 887, "event": "杨行密据有淮南", "jiedushi": "杨行密"},
        {"year": 907, "event": "建立吴国（十国之一）", "jiedushi": "杨渥"},
        {"year": 937, "event": "徐知诰篡吴建南唐", "jiedushi": "李昪"},
    ],
    "镇海": [
        {"year": 787, "event": "设镇海节度使", "jiedushi": "韩滉"},
        {"year": 882, "event": "周宝任镇海节度使", "jiedushi": "周宝"},
        {"year": 887, "event": "钱镠据有镇海", "jiedushi": "钱镠"},
        {"year": 907, "event": "钱镠建立吴越", "jiedushi": "钱镠"},
    ],
}

# ============================================
# 重大历史事件配置
# ============================================

# 五代十国重大事件
MAJOR_EVENTS = [
    {"year": 907, "event": "朱温篡唐，建立后梁，五代十国开始", "regime": "后梁"},
    {"year": 923, "event": "李存勖灭后梁，建立后唐", "regime": "后唐"},
    {"year": 936, "event": "石敬瑭割让燕云十六州，借契丹兵建立后晋", "regime": "后晋"},
    {"year": 947, "event": "契丹灭后晋，刘知远建立后汉", "regime": "后汉"},
    {"year": 951, "event": "郭威建立后周，刘崇建立北汉", "regime": "后周/北汉"},
    {"year": 954, "event": "柴荣即位周世宗，开始统一战争", "regime": "后周"},
    {"year": 960, "event": "赵匡胤陈桥兵变，建立北宋，后周灭亡", "regime": "北宋"},
    {"year": 963, "event": "宋灭荆南", "regime": "北宋"},
    {"year": 965, "event": "宋灭后蜀", "regime": "北宋"},
    {"year": 971, "event": "宋灭南汉", "regime": "北宋"},
    {"year": 975, "event": "宋灭南唐，李煜被俘", "regime": "北宋"},
    {"year": 978, "event": "吴越钱俶纳土归宋，和平统一", "regime": "北宋"},
    {"year": 979, "event": "宋灭北汉，五代十国结束", "regime": "北宋"},
]

# ============================================
# 人物世系配置
# ============================================

# 五代帝王世系（详细版）
WUDAI_SUCCESSION = {
    "后梁": [
        {"name": "朱温", "relation": "开国皇帝", "years": "907-912", "temple_name": "太祖", "posthumous_name": "神武元圣孝皇帝", "bio": "宋州砀山人，唐末参加黄巢起义，后降唐赐名全忠。907 年篡唐建立后梁，开启五代十国时期。"},
        {"name": "朱友珪", "relation": "子", "years": "912-913", "temple_name": "", "posthumous_name": "", "bio": "朱温次子，弑父篡位，在位仅 8 个月被杀。"},
        {"name": "朱友贞", "relation": "子", "years": "913-923", "temple_name": "末帝", "posthumous_name": "", "bio": "朱温三子，即位后与晋军作战不利，后唐军攻入开封时自杀。"},
    ],
    "后唐": [
        {"name": "李存勖", "relation": "开国皇帝", "years": "923-926", "temple_name": "庄宗", "posthumous_name": "光圣神闵孝皇帝", "bio": "沙陀人，李克用之子。骁勇善战，灭后梁统一中原，晚年宠信伶人死于兵变。"},
        {"name": "李嗣源", "relation": "养子", "years": "926-933", "temple_name": "明宗", "posthumous_name": "圣德和武钦孝皇帝", "bio": "沙陀人，李克用养子。在位期间励精图治，是五代时期较有作为的君主。"},
        {"name": "李从厚", "relation": "子", "years": "933-934", "temple_name": "闵帝", "posthumous_name": "", "bio": "李嗣源第三子，在位仅 5 个月被李从珂所杀。"},
        {"name": "李从珂", "relation": "养子", "years": "934-936", "temple_name": "末帝", "posthumous_name": "", "bio": "李嗣源养子，与石敬瑭交战不利，自焚而死。"},
    ],
    "后晋": [
        {"name": "石敬瑭", "relation": "开国皇帝", "years": "936-942", "temple_name": "高祖", "posthumous_name": "圣文章武明德孝皇帝", "bio": "沙陀人，李嗣源女婿。为借契丹兵灭后唐，割让燕云十六州，称儿皇帝。"},
        {"name": "石重贵", "relation": "侄", "years": "942-947", "temple_name": "出帝", "posthumous_name": "", "bio": "石敬瑭之侄，对契丹称孙不称臣，招致契丹入侵，被俘北迁。"},
    ],
    "后汉": [
        {"name": "刘知远", "relation": "开国皇帝", "years": "947-950", "temple_name": "高祖", "posthumous_name": "睿文圣武昭肃孝皇帝", "bio": "沙陀人，石敬瑭部将。契丹北撤后称帝，在位 10 个月病逝。"},
        {"name": "刘承祐", "relation": "子", "years": "950-951", "temple_name": "隐帝", "posthumous_name": "", "bio": "刘知远次子，猜忌大臣，杀郭威家属，被郭威所灭。"},
    ],
    "后周": [
        {"name": "郭威", "relation": "开国皇帝", "years": "951-954", "temple_name": "太祖", "posthumous_name": "圣神恭肃文武孝皇帝", "bio": "邢州尧山人，刘知远部将。建立后周后励精图治，为北宋统一奠定基础。"},
        {"name": "柴荣", "relation": "养子", "years": "954-959", "temple_name": "世宗", "posthumous_name": "睿武孝文皇帝", "bio": "邢州尧山人，郭威养子。五代时期最有作为的君主，南征北战统一在即却英年早逝。"},
        {"name": "柴宗训", "relation": "子", "years": "959-960", "temple_name": "恭帝", "posthumous_name": "", "bio": "柴荣第四子，7 岁即位，次年赵匡胤发动陈桥兵变，北宋建立。"},
    ],
}

# 十国帝王世系（详细版）
SHIGUO_SUCCESSION = {
    "吴越": [
        {"name": "钱镠", "relation": "开国君主", "years": "907-932", "temple_name": "太祖", "posthumous_name": "武肃王", "bio": "杭州临安人，唐末参加董昌起义，后据有两浙之地。在位期间兴修水利，发展经济。"},
        {"name": "钱元瓘", "relation": "子", "years": "932-941", "temple_name": "世宗", "posthumous_name": "文穆王", "bio": "钱镠第六子，继承父业，继续发展吴越。"},
        {"name": "钱弘佐", "relation": "子", "years": "941-947", "temple_name": "成宗", "posthumous_name": "忠献王", "bio": "钱元瓘第六子，在位期间减免赋税，赈济灾民。"},
        {"name": "钱弘倧", "relation": "弟", "years": "947", "temple_name": "", "posthumous_name": "", "bio": "钱元瓘第七子，在位仅半年被权臣废黜。"},
        {"name": "钱弘俶", "relation": "弟", "years": "947-978", "temple_name": "忠懿王", "posthumous_name": "", "bio": "钱元瓘第九子，在位期间纳土归宋，实现和平统一。"},
    ],
    "南唐": [
        {"name": "李昪", "relation": "开国君主", "years": "937-943", "temple_name": "烈祖", "posthumous_name": "光文肃武孝高皇帝", "bio": "徐州人，杨行密部将徐温养子。建立南唐后休养生息，国力强盛。"},
        {"name": "李璟", "relation": "子", "years": "943-961", "temple_name": "元宗", "posthumous_name": "明道崇德文宣孝皇帝", "bio": "李昪长子，在位期间南唐疆域最大，但后期国势衰落。擅长诗词。"},
        {"name": "李煜", "relation": "子", "years": "961-975", "temple_name": "后主", "posthumous_name": "", "bio": "李璟第六子，著名词人，亡国后被俘至开封，作《虞美人》后被毒死。"},
    ],
    "前蜀": [
        {"name": "王建", "relation": "开国君主", "years": "907-918", "temple_name": "高祖", "posthumous_name": "神武圣文孝德明惠皇帝", "bio": "许州舞阳人，唐末参加忠武军，后据有蜀地。在位期间励精图治。"},
        {"name": "王衍", "relation": "子", "years": "918-925", "temple_name": "后主", "posthumous_name": "", "bio": "王建第十一子，荒淫无度，后唐军入侵时投降被杀。"},
    ],
    "后蜀": [
        {"name": "孟知祥", "relation": "开国君主", "years": "934-935", "temple_name": "高祖", "posthumous_name": "文武圣德英烈明孝皇帝", "bio": "邢州龙冈人，孟昶之父。建立后蜀后不久病逝。"},
        {"name": "孟昶", "relation": "子", "years": "935-965", "temple_name": "后主", "posthumous_name": "", "bio": "孟知祥第三子，在位初期励精图治，后期奢靡亡国，被俘至开封。"},
    ],
    "闽国": [
        {"name": "王审知", "relation": "开国君主", "years": "909-925", "temple_name": "太祖", "posthumous_name": "昭武孝皇帝", "bio": "光州固始人，与兄王潮起兵，据有福建。在位期间发展海外贸易。"},
        {"name": "王延翰", "relation": "子", "years": "925-927", "temple_name": "", "posthumous_name": "", "bio": "王审知长子，即位后被弟王延钧所杀。"},
        {"name": "王延钧", "relation": "弟", "years": "927-935", "temple_name": "惠帝", "posthumous_name": "", "bio": "王审知次子，被部将所杀。"},
        {"name": "王继鹏", "relation": "子", "years": "935-939", "temple_name": "康宗", "posthumous_name": "", "bio": "王延钧长子，被叔父王延羲所杀。"},
        {"name": "王延羲", "relation": "叔", "years": "939-944", "temple_name": "景宗", "posthumous_name": "", "bio": "王审知第二十八子，被部将所杀。"},
        {"name": "王延政", "relation": "弟", "years": "944-945", "temple_name": "天德帝", "posthumous_name": "", "bio": "王审知第二十一子，南唐入侵时被俘，闽国灭亡。"},
    ],
    "南汉": [
        {"name": "刘䶮", "relation": "开国君主", "years": "917-942", "temple_name": "高祖", "posthumous_name": "天皇大帝", "bio": "封州人，刘隐之弟。建立大越国，后改国号为汉。在位期间刑罚残酷。"},
        {"name": "刘玢", "relation": "子", "years": "942-943", "temple_name": "殇帝", "posthumous_name": "", "bio": "刘䶮第三子，荒淫无道，被弟刘晟所杀。"},
        {"name": "刘晟", "relation": "弟", "years": "943-958", "temple_name": "中宗", "posthumous_name": "", "bio": "刘䶮第四子，杀兄篡位，猜忌宗室。"},
        {"name": "刘鋹", "relation": "子", "years": "958-971", "temple_name": "后主", "posthumous_name": "", "bio": "刘晟长子，荒淫无能，南唐军入侵时投降。"},
    ],
    "楚": [
        {"name": "马殷", "relation": "开国君主", "years": "907-930", "temple_name": "武穆王", "posthumous_name": "", "bio": "许州鄢陵人，孙儒部将。据有湖南之地，向后梁称臣。"},
        {"name": "马希声", "relation": "子", "years": "930-932", "temple_name": "", "posthumous_name": "", "bio": "马殷次子，在位 2 年病逝。"},
        {"name": "马希范", "relation": "弟", "years": "932-947", "temple_name": "文昭王", "posthumous_name": "", "bio": "马殷第四子，在位期间奢侈无度。"},
        {"name": "马希广", "relation": "弟", "years": "947-950", "temple_name": "", "posthumous_name": "", "bio": "马殷第三十五子，被兄马希萼所杀。"},
        {"name": "马希萼", "relation": "兄", "years": "950-951", "temple_name": "", "posthumous_name": "", "bio": "马殷第十五子，被弟马希崇所废。"},
    ],
    "荆南": [
        {"name": "高季兴", "relation": "开国君主", "years": "924-928", "temple_name": "武信王", "posthumous_name": "", "bio": "陕州陕县人，朱温部将。据有荆南之地，向多国称臣以求生存。"},
        {"name": "高从诲", "relation": "子", "years": "928-948", "temple_name": "文献王", "posthumous_name": "", "bio": "高季兴长子，继承父业，向各国称臣。"},
        {"name": "高保融", "relation": "子", "years": "948-960", "temple_name": "贞懿王", "posthumous_name": "", "bio": "高从诲第三子，在位期间向北宋称臣。"},
        {"name": "高保勖", "relation": "子", "years": "960-962", "temple_name": "", "posthumous_name": "", "bio": "高从诲第十子，在位 2 年病逝。"},
        {"name": "高继冲", "relation": "侄", "years": "962-963", "temple_name": "", "posthumous_name": "", "bio": "高保融长子，北宋入侵时投降，荆南灭亡。"},
    ],
    "北汉": [
        {"name": "刘崇", "relation": "开国君主", "years": "951-954", "temple_name": "世祖", "posthumous_name": "神武皇帝", "bio": "并州太原人，刘知远之弟。后汉灭亡后在太原称帝，依附契丹。"},
        {"name": "刘承钧", "relation": "子", "years": "954-968", "temple_name": "睿宗", "posthumous_name": "英武皇帝", "bio": "刘崇次子，在位期间依附契丹，与北宋对抗。"},
        {"name": "刘继恩", "relation": "子", "years": "968", "temple_name": "", "posthumous_name": "", "bio": "刘承钧养子，在位仅 2 个月被杀。"},
        {"name": "刘继元", "relation": "养子", "years": "968-979", "temple_name": "英武帝", "posthumous_name": "", "bio": "刘承钧养子，北宋灭北汉时投降，五代十国结束。"},
    ],
}

# ============================================
# 统计数据配置
# ============================================

# 年度重大事件数量统计（模拟数据）
YEARLY_EVENTS = {
    907: 5, 908: 2, 909: 1, 910: 2, 911: 1,
    912: 3, 913: 2, 914: 1, 915: 2, 916: 1,
    917: 2, 918: 1, 919: 1, 920: 1, 921: 1,
    922: 2, 923: 4, 924: 2, 925: 3, 926: 3,
    927: 1, 928: 1, 929: 1, 930: 2, 931: 1,
    932: 2, 933: 2, 934: 3, 935: 1, 936: 4,
    937: 2, 938: 1, 939: 1, 940: 1, 941: 1,
    942: 2, 943: 2, 944: 1, 945: 3, 946: 1,
    947: 4, 948: 1, 949: 1, 950: 3, 951: 4,
    952: 1, 953: 1, 954: 3, 955: 2, 956: 2,
    957: 2, 958: 2, 959: 2, 960: 4, 961: 2,
    962: 1, 963: 3, 964: 1, 965: 3, 966: 1,
    967: 1, 968: 1, 969: 1, 970: 1, 971: 2,
    972: 1, 973: 1, 974: 1, 975: 3, 976: 1,
    977: 1, 978: 2, 979: 3,
}

# 政权综合实力对比数据
REGIME_POWER_DATA = [
    {"name": "后周", "duration": 9, "area": 50, "power": 95, "culture": 80, "military": 95},
    {"name": "南唐", "duration": 38, "area": 35, "power": 85, "culture": 95, "military": 75},
    {"name": "吴越", "duration": 71, "area": 12, "power": 60, "culture": 85, "military": 70},
    {"name": "前蜀", "duration": 18, "area": 25, "power": 70, "culture": 75, "military": 65},
    {"name": "后蜀", "duration": 31, "area": 25, "power": 65, "culture": 80, "military": 60},
    {"name": "南汉", "duration": 54, "area": 20, "power": 50, "culture": 60, "military": 55},
]

# 政权面积估算（万平方公里）
REGIME_AREA_DATA = {
    "后周": 50,
    "南唐": 35,
    "前蜀": 25,
    "后蜀": 25,
    "南汉": 20,
    "楚": 21,
    "吴越": 12,
    "闽国": 12,
    "北汉": 8,
    "荆南": 3,
}

# ============================================
# 快捷搜索词配置
# ============================================

# 文献检索快捷搜索词
QUICK_SEARCH_TERMS = [
    "朱温", "李存勖", "石敬瑭", "郭威", "柴荣",
    "钱镠", "李煜", "王建", "孟知祥",
    "后梁", "后唐", "后晋", "后汉", "后周",
    "吴越", "南唐", "前蜀", "后蜀",
    "开封", "洛阳", "杭州", "南京", "成都",
    "节度使", "藩镇", "称帝", "即位",
]

# 历史专有名词分类
HISTORICAL_TERMS = {
    "政权": ['五代', '十国', '后梁', '后唐', '后晋', '后汉', '后周',
            '吴越', '南唐', '前蜀', '后蜀', '闽国', '南汉', '荆南',
            '北汉', '契丹', '北宋', '南宋', '唐朝', '隋朝', '汉朝'],
    "人物": ['朱温', '李存勖', '石敬瑭', '刘知远', '郭威', '柴荣',
            '钱镠', '李昪', '李煜', '王建', '孟知祥', '王审知',
            '马殷', '高季兴', '刘䶮', '刘崇'],
    "官职": ['节度使', '刺史', '知州', '知县', '尚书', '侍郎',
            '宰相', '丞相', '御史', '太尉', '大将军'],
    "地名": ['开封', '洛阳', '杭州', '南京', '成都', '福州', '广州',
            '长沙', '荆州', '太原', '长安'],
    "事件": ['藩镇', '藩王', '割据', '称帝', '即位', '禅让',
            '陈桥兵变', '安史之乱', '黄巢起义', '赤壁之战'],
}

# ============================================
# 辅助函数
# ============================================

def get_all_regimes():
    """获取所有政权列表"""
    return WUDAI_REGIMES + SHIGUO_REGIMES


def get_regime_by_name(name: str):
    """根据名称获取政权信息"""
    for regime in get_all_regimes():
        if regime['name'] == name:
            return regime
    return None


def get_fanzhen_by_name(name: str):
    """根据名称获取藩镇信息"""
    return FANZHEN_BASE_DATA.get(name, None)


def get_major_events():
    """获取重大事件列表"""
    return MAJOR_EVENTS


def get_succession_data(regime_name: str):
    """获取政权世系数据"""
    all_succession = {**WUDAI_SUCCESSION, **SHIGUO_SUCCESSION}
    return all_succession.get(regime_name, [])


def get_regime_type(regime_name: str) -> str:
    """获取政权类型（五代/十国）"""
    for r in WUDAI_REGIMES:
        if r['name'] == regime_name:
            return "五代"
    for r in SHIGUO_REGIMES:
        if r['name'] == regime_name:
            return "十国"
    return ""
