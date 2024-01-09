from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from lxml import html
option = webdriver.EdgeOptions()
option.add_argument("headless")
driver = webdriver.Edge(options=option)
driver.get('https://www.tymetro.com.tw/tymetro-new/tw/_pages/travel-guide/timetable-search.php')
for i in range(1,24):
    if i == 14:
        continue
    else:
        for j in range(1,24):
            if j == 14 or i==j :
                continue
            else:
                
                start_ = Select(driver.find_element(by = By.NAME, value='start_station'))
                start_.select_by_value(str(i))
                end_ = Select(driver.find_element(by = By.NAME, value='end_station'))
                end_.select_by_value(str(j))
                submmit = driver.find_element(by = By.XPATH , value="/html/body/div[2]/div[3]/div[2]/section/fieldset/form/div/div[4]/div/button")
                submmit.click()               
                data = html.fromstring(driver.page_source)
                #day = data.xpath("//tr[@class='counter_6 commuter-car']/td[@class='all_time']/text()")
                #day = data.xpath("//tr[@class='counter_6 commuter-car']/td/text()")
                number = data.xpath("//table[@class='table table-hover table-bordered']/tbody/tr/td/text()")
                number_len = len(number)

                tmp  = []
                for a in range (0 , number_len , 4):
                    if '元' in str(number[a]) :
                        break
                    else:
                        txt = (number[a] +';'+ number[a+1] +';'+ number[a+2] +';'+ number[a+3])
                        tmp.append(txt)
                        

               
                f = open('C:\\Users\\jayce\\Desktop\\data\\A'+str(i)+'-A'+str(j)+'.txt' , 'w')
                f.write(str(tmp))
                f.close()                    
