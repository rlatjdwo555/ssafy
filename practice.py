import urllib.request
from bs4 import BeautifulSoup
from string import punctuation

url = "https://us.soccerway.com/national/england/premier-league/20182019/regular-season/r48730/?ICID=SN_01_01"
soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

team_name_en = ['AFC Bournemouth', 'Arsenal', 'Brighton & Hov…', 'Burnley', 'Cardiff City', 'Chelsea',
             'Crystal Palace', 'Everton', 'Fulham', 'Huddersfield Town', 'Leicester City', 'Liverpool',
             'Manchester City', 'Manchester United', 'Newcastle United', 'Southampton', 'Tottenham Hotspur',
             'Watford', 'West Ham United', 'Wolverhampton …']

team_name_kr = {'본머스': 0, '아스날':1, '아스널':1, '브라이튼':2, '번리':3, '카디프시티':4, '첼시':5,
                '크리스탈 팰리스':6, '에버턴':7, '에버튼':7, '풀햄':8, '허드슨타운':9, '레스터':10, '레스터시티':10,
                '리버풀':11, '맨체스터 시티':12, '맨시티':12, '맨시':12, '맨체스터 유나이티드':13, '맨유':13, '뉴캐슬':14, '뉴캐슬 유나이티드':14,
                '사우샘프턴':15, '토트넘':16, '토튼햄':16, '토트넘 핫스퍼':16, '왓포드':17, '웨스트햄':18, '울버햄튼':19, '울버햄턴':19}

command_options ={'전체':0, '정보':1, '순위':2, '일정':3, '결과':4, '전체순위':0}

sample_command_list = ['전체 순위']

# keywords = ['리버풀', '맨시티', '토트넘', '왓포드']
#
# for key in keywords:
#     print(team_name_en[int(team_name_kr[key])])

#========================================================================
#                               Input
#========================================================================
# 명령어 공백단위로 분리
def test_funtion(command, keyword_team, keyword_option):
    for word in command.split():
        #print(word)
        # 특수문자 제거
        for symbol in punctuation:
            word = word.replace(symbol, '')

        # 조사 제거
        for key in team_name_kr.keys():
            if word.startswith(key):
                keyword_team.append(team_name_en[int(team_name_kr.get(key))])

        # 목적 정보 입력
        for op in command_options.keys():
            if word.__contains__(op):
                if (op == '순위' and keyword_option.__contains__('전체')):
                    continue
                else :
                    keyword_option.append(command_options.get(op))

# 전체 순위 출력
def show_tables():
    print("전체 순위 정보")

# 팀 상세정보
def show_info(team_list):
    for team in team_list:
        print(team+"의 상세정보")

# 팀 순위(기본정보)
def show_rank(team_list):
    for team in team_list:
        print(team+"의 순위정보")

# 다음 경기일정
def show_schedules(team_list):
    for team in team_list:
        print(team+"의 다음 경기일정")

# 경기 결과
def show_result(team_list):
    for team in team_list:
        print(team+"의 경기결과")

# '전체':0, '정보':1, '순위':2, '일정':3, '결과':4
def excute_fun(keyword_team, keyword_option):

    # 실행 함수 분기
    if len(keyword_team) == 0 | len(keyword_option) == 0:
        return print("무슨 말인지 모르겠어요ㅠ 질문을 다시 해주세요!")
    elif len(keyword_option) == 0:
        return show_info(keyword_team)

    for op in keyword_option:
        #print('옵션넘버 : '+str(op))
        if op == 0 : show_tables()
        elif op == 1 : show_info(keyword_team)
        elif op == 2 : show_rank(keyword_team)
        elif op == 3 : show_schedules(keyword_team)
        elif op == 4 : show_result(keyword_team)

def test_case(command):
    keyword_team = []
    keyword_option = []

    print(command)
    test_funtion(command, keyword_team, keyword_option)
    excute_fun(keyword_team, keyword_option)
    print('============================')

for command in sample_command_list:
    test_case(command)



#========================================================================
#                               Output
#========================================================================
team_name = []
teams = []
rank = 1

for a in soup.find_all("table", class_="leaguetable sortable table detailed-table"):
    for col in a.find_all("tbody"):
        for tr in col.find_all("tr"):

            for data in tr.find_all("td", "text team large-link"):
                team_name.append(data.get_text())


