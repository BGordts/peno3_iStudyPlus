from datetime import datetime

def calculate_average(itemList):
        average = 0
        
        if len(itemList) == 0:
            return 0
        else:
            for i in itemList:
                average += i
            
            return float(average)/len(itemList)
        
def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0