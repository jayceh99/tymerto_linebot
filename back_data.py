
def f_back_data(start_ , end_ , car_type):

    #預先查詢功能 須搭 find_train_backup.py使用 並在get_all_train_train.py的f_find_train 裡面呼叫此功能
    if car_type == '2':
        #path = "C:\\Users\\jayce\\Desktop\\tymetro_linebot\\A"+start_+"-A"+end_+'ex.txt'
        path = "/home/jayce/tymrtro/tymetro_linebot/data/A"+start_+"-A"+end_+'ex.txt'
    else:
        #path = "C:\\Users\\jayce\\Desktop\\tymetro_linebot\\A"+start_+"-A"+end_+'.txt'
        path = "/home/jayce/tymrtro/tymetro_linebot/data/A"+start_+"-A"+end_+'.txt'
    data  = open(path)
    data_ = data.read().replace('[','').replace('\'' , '').replace(' ','').replace(']','').split(',')
    '''
    data_new = []
    if car_type == '2':
        for i in range (0,len(data_)):
            if i%4 == 3:
                continue
            elif data_[i] == '直達車' :

                for k in range(0,3):
                    data_new.append(data_[i+k])
                i = i+3
        return(data_new)

    else :
        for i in range (0,len(data_)):
            if i%4 == 3:
                continue
            else:
                data_new.append(data_[i])
    '''
    return(data_)
    
#if __name__ == '__main__':
#    print(f_back_data('1','2','')[0])
