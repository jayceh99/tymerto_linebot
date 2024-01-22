from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lxml import html
from datetime import datetime


class c_find_train:
    def __init__(self,start_,end_, start_or_arriv_time) -> None:
        self.start_ = start_
        self.end_ = end_
        self.start_or_arriv_time = start_or_arriv_time

            
                #f = open('C:\\Users\\jayce\\Desktop\\data\\A'+str(i)+'-A'+str(j)+'.txt' , 'w')
                #f.write(str(tmp))
                #f.close()                    
    def f_name_to_number(self):
        name = {'台北車站':'A1' , '三重站':"A2" , '新北產業園區站':"A3" , '新莊副都心站':"A4" , "泰山站":"A5" , "泰山貴和站":"A6" ,"體育大學站":"A7" , 
            "長庚醫院站":"A8" , "林口站":"A9" , "山鼻站":"A10" , "坑口站":'A11' , "機場第一航廈站":'A12' , "機場第二航廈站":"A13" , "機場旅館站":"A15" ,
            "大園站":"A16" , "橫山站":"A17" , "領航站":"A18" , "桃園體育園區站":"A20" , "興南站":'A21' , "環北站":'A22' , "老街溪站":'A23'}
        for i in name:
            if self.start_ in i:
                self.start_station_number = name[i]
                self.start_station_name = i
            if self.start_ == name[i]:
                self.start_station_number = name[i]
                self.start_station_name = i
        for i in name:
            if self.end_ in i:
                self.end_station_number = name[i]
                self.end_station_name = i
            if self.end_ == name[i]:
                self.end_station_number = name[i]
                self.end_station_name = i
    def f_find_train(self):

        option = webdriver.EdgeOptions()
        option.add_argument("headless")
        driver = webdriver.Edge(options=option)
        driver.get('https://www.tymetro.com.tw/tymetro-new/tw/_pages/travel-guide/timetable-search.php')
        start_ = Select(driver.find_element(by = By.NAME, value='start_station'))
        start_.select_by_value(str(self.start_station_number.replace('A','')))
        end_ = Select(driver.find_element(by = By.NAME, value='end_station'))
        end_.select_by_value(str(self.end_station_number.replace('A','')))
        submmit = driver.find_element(by = By.XPATH , value="//button[@class='btn btn-lg']")
        submmit.click()
        data = html.fromstring(driver.page_source)
        number = data.xpath("//table[@class='table table-hover table-bordered']/tbody/tr/td/text()")
        number_len = len(number)
        self.tmp  = []
        for a in range (0 , number_len , 4):
            if '元' in str(number[a]) :
                break
            else:
                txt = (number[a] +';'+ number[a+1] +';'+ number[a+2] +';'+ number[a+3])
                self.tmp.append(txt)


    def f_search(self):
        next_train = 86400
        start_or_arrive = None
        
        if "!" in self.start_or_arriv_time:
            self.start_or_arriv_time = self.start_or_arriv_time.replace('!' , '')
            start_or_arrive = 1
        elif "@" in self.start_or_arriv_time:
            self.start_or_arriv_time = self.start_or_arriv_time.replace('@' , '')
            start_or_arrive = 2
        else :
            print('exception')
            quit()
        self.start_or_arriv_time = self.start_or_arriv_time[0]+self.start_or_arriv_time[1]+":"+self.start_or_arriv_time[2]+self.start_or_arriv_time[3]+":00"
    
        self.start_or_arriv_time = datetime.strptime(self.start_or_arriv_time , "%H:%M:%S")

        for i in range (0 , len(self.tmp) ):
            k = self.tmp[i].split(';')
            #print(i[2])
            time2 = datetime.strptime(str(k[start_or_arrive])+":00", "%H:%M:%S")
            time_3 = time2 - self.start_or_arriv_time
            if int(time_3.seconds) < next_train:
                next_train = int(time_3.seconds)

                tmp_next = i

        previous_ = self.tmp[tmp_next-1].split(';')
        now_ = self.tmp[tmp_next].split(';')
        next_ = self.tmp[tmp_next+1].split(';')
        next_train_time_1 = self.start_station_number+' '+self.start_station_name+'- '+self.end_station_number+' '+\
            self.end_station_name+' 車種 : '+previous_[0]+' 出發時間 : '+previous_[1]+' 抵達時間 : '+previous_[2]+' 行駛時間 : '+previous_[3]
        next_train_time_2 = self.start_station_number+' '+self.start_station_name+'- '+self.end_station_number+' '+\
            self.end_station_name+' 車種 : '+now_[0]+' 出發時間 : '+now_[1]+' 抵達時間 : '+now_[2]+' 行駛時間 : '+now_[3]
        next_train_time_3 = self.start_station_number+' '+self.start_station_name+'- '+self.end_station_number+' '+\
            self.end_station_name+' 車種 : '+next_[0]+' 出發時間 : '+next_[1]+' 抵達時間 : '+next_[2]+' 行駛時間 : '+next_[3]
        print(next_train_time_1)
        print(next_train_time_2)
        print(next_train_time_3)
def main():
    c_find_train_q = c_find_train(start_='北車' , end_= "A8" , start_or_arriv_time= '!1400')
    c_find_train_q.f_name_to_number()
    c_find_train_q.f_find_train()
    c_find_train_q.f_search()
if __name__ == "__main__":
    main()