import requests
import json
import csv
import jsonpath


def creat_csv():
    '''
    创建保存数据的 csv
    '''
    with open('data.csv','w',encoding='utf8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['英雄','Pick场数','总击杀','场均KDA','场均击杀',
                         '场均死亡','场均助攻','GPM','XPM','被Ban场数',
                         '胜率','出场率','Ban率','热度'])


def get_json_data(url):
    '''
    请求数据，并解析 json 为字典类型
    '''
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'cookie' : 'RK=W15gCZnjRo; ptcz=9fb3de5fcdb825b460c004015a48ae94ab83d077d998bf5e8b6b614c50af90d6; pgv_pvi=1868072960; tvfe_boss_uuid=a4dafd271519e3df; pgv_pvid=1462566206; LW_uid=91s5a9J1H5f3s9c75051e6d4w3; eas_sid=x1w5n9i1Z5l3p9v7t0b1F645d5; LW_sid=q1Z5g9L1Y5J4E119f2h4Z057x3; ied_qq=o1347904922; ptui_loginuin=760542165; pt_sms_phone=152******81; psrf_access_token_expiresAt=1599321386; psrf_musickey_createtime=1591545386; qqmusic_key=Q_H_L_2eY3Tx50eC4fNCykhOG-7hiIbt4qug9-V246AutS_VTYpmchSeq0mKhL089w7fD; pgv_info=ssid=s2774480965; pgv_si=s465319936; _qpsvr_localtk=0.25823656607926226; uin=o1347904922; skey=@PfGTx5H91; IED_LOG_INFO2=userUin%3D1347904922%26nickName%3D%2525E5%2525A4%2525AA%2525E4%2525B9%2525BE%2525E5%2525AD%252590%26nickname%3D%25E5%25A4%25AA%25E4%25B9%25BE%25E5%25AD%2590%26userLoginTime%3D1591617130%26logtype%3Dqq%26loginType%3Dqq%26uin%3D1347904922; dmwxsession=null'
    }
    response = requests.get(url,headers=headers)
    json_data = json.loads(response.text)
    return json_data


def get_data(json_data):
    '''
    提取数据
    '''
    # 英雄名
    hero = jsonpath.jsonpath(json_data, '$..hero_name')
    # pick 场数
    pick_cnt = jsonpath.jsonpath(json_data,'$..pick_cnt')
    # 总击杀
    total_kill = jsonpath.jsonpath(json_data,'$..total_kill')
    # 场均 KDA
    kda = jsonpath.jsonpath(json_data, '$..kda')
    # 场均击杀
    tavg_kill = jsonpath.jsonpath(json_data, '$..avg_kill')
    # 场均死亡
    avg_bekill = jsonpath.jsonpath(json_data, '$..avg_bekill')
    # 场均助攻
    avg_assist = jsonpath.jsonpath(json_data, '$..avg_assist')
    # GPM
    gpm = jsonpath.jsonpath(json_data, '$..gpm')
    # XPM
    xpm = jsonpath.jsonpath(json_data, '$..xpm')
    # 被 Ban 场数
    ban_cnt = jsonpath.jsonpath(json_data, '$..ban_cnt')
    # 胜率
    win_rate = jsonpath.jsonpath(json_data, '$..win_rate')
    # 出场率
    in_rate = jsonpath.jsonpath(json_data, '$..in_rate')
    # Ban 率
    ban_rate = jsonpath.jsonpath(json_data, '$..ban_rate')
    # 热度
    hot_rate = jsonpath.jsonpath(json_data, '$..hot_rate')

    data = list(zip(hero,pick_cnt,total_kill,kda,tavg_kill,avg_bekill,
                    avg_assist,gpm,xpm,ban_cnt,win_rate,in_rate,ban_rate,
                    hot_rate))

    return data


def write_to_csv(data):
    '''
    保存数据
    '''
    with open('data.csv','a+',encoding='utf8',newline='') as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)


if __name__ == '__main__':
    creat_csv()
    urls = ['https://smobac.odp.qq.com/datamore/smobac/hero/index?page={}&page_size=20&start_date=2019-12-11&end_date=2020-06-08&sort_field=pick_cnt&sort_dir=desc&season_id=all&hero_id=all&team_id=all&export=0&acctype=qq&location=cn'
           .format(str(i)) for i in range(1,6)]
    for url in urls:
        json_data = get_json_data(url)
        data = get_data(json_data)
        write_to_csv(data)
