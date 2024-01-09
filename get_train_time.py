from datetime import datetime
def find_station_name(start_,end_):
    name = {'台北車站':'A1' , '三重站':"A2" , '新北產業園區站':"A3" , '新莊副都心站':"A4" , "泰山站":"A5" , "泰山貴和站":"A6" ,"體育大學站":"A7" , 
            "長庚醫院站":"A8" , "林口站":"A9" , "山鼻站":"A10" , "坑口站":'A11' , "機場第一航廈站":'A12' , "機場第二航廈站":"A13" , "機場旅館站":"A15" ,
            "大園站":"A16" , "橫山站":"A17" , "領航站":"A18" , "桃園體育園區站":"A20" , "興南站":'A21' , "環北站":'A22' , "老街溪站":'A23'}


    for i in name:
        if start_ in i:
            start_station_number = name[i]
            start_station_name = i
        if start_ == name[i]:
            start_station_number = name[i]
            start_station_name = i
    for i in name:
        if end_ in i:
            end_station_number = name[i]
            end_station_name = i
        if end_ == name[i]:
            end_station_number = name[i]
            end_station_name = i
    return start_station_number , start_station_name , end_station_number , end_station_name


def search(start_station_number , end_station_number , time):
    f = open('C:\\Users\\jayce\\Desktop\\tymetro\\data\\'+start_station_number+'-'+end_station_number+'.txt')
    tmp  = str(f.read()).replace('\'','').replace(' ','').replace('[','').replace(']','').split(',')
    
    for i in tmp:
        i = i.split(';')
        print(i[2])


def test():
    time_1 = datetime.strptime("05:00:00", "%H:%M:%S")
    time_2 = datetime.strptime("06:00:00", "%H:%M:%S")

    time_interval = time_1 - time_2
    print(time_interval.seconds)
def main():
    start_station_number , start_station_name , end_station_number , end_station_name =  find_station_name('A1',"A2")
    search(start_station_number=start_station_number , end_station_number=end_station_number , time = 'test')
    test()


if __name__ == "__main__":
    main()

