def pre_all(train, test):
    print(f"전처리 전 train 크기 : {train.shape}")
    print(f"전처리 전 test 크기 : {test.shape}")
    print("=================전처리 중=================")

    # 합쳐서 전처리하기
    train["timestamp"] = pd.to_datetime(train["timestamp"])
    test["timestamp"] = pd.to_datetime(test["timestamp"])
    df = pd.concat([train,test]).reset_index(drop = True)

    df.rename(columns={'supply(kg)':'supply', 'price(원/kg)':'price'},inplace=True)

    #년/월/일 추가
    df['year']=df['timestamp'].dt.year
    df['month']=df['timestamp'].dt.month
    df['day']=df['timestamp'].dt.day

    #요일 추가
    df['week_day']=df['timestamp'].dt.weekday

    # 년-월 변수 추가 : year-month의 형태, 개월단위 누적값
    le = LabelEncoder()
    df["year_month"] = df["timestamp"].map(lambda x :str(x.year) + "-"+str(x.month))

    # 라벨 인코딩
    df["year_month"] = le.fit_transform(df["year_month"])


    # 주차 변수 추가
    df["week"] = df["timestamp"].map(lambda x: datetime.datetime(x.year, x.month, x.day).isocalendar()[1])

    # 주차 누적값
    week_list=[]
    for i in range(len(df['year'])) :
        if df['year'][i] == 2019 :
            week_list.append(int(df['week'][i]))
        elif df['year'][i] == 2020 :
            week_list.append(int(df['week'][i])+52)
        elif df['year'][i] == 2021 :
            week_list.append(int(df['week'][i])+52+53)
        elif df['year'][i] == 2022 :
            week_list.append(int(df['week'][i])+52+53+53)
        elif df['year'][i] == 2023 :
            week_list.append(int(df['week'][i])+52+53+53+52)
    df['week_num']= week_list

    # datetime 패키지에서 19년 12월 마지막주가 첫째주로 들어가는거 발견하여 수정
    df.loc[df['timestamp']=='2019-12-30','week_num']=52
    df.loc[df['timestamp']=='2019-12-31','week_num']=52


    # 공휴일 변수 추가
    def make_holi(x):
        kr_holi = holidays.KR()

        if x in kr_holi:
            return 1
        else:
            return 0
        
    df["holiday"] = df["timestamp"].map(lambda x : make_holi(x))
    

    # train, test 분리하기
    train = df[~df["price"].isnull()].sort_values("timestamp").reset_index(drop = True)
    test = df[df["price"].isnull()].sort_values("timestamp").reset_index(drop=True)


    print(f"전처리 후 train 크기 : {train.shape}")
    print(f"전처리 후 test 크기 : {test.shape}")

    return train, test




def seed_everything(seed: int = 2024):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)