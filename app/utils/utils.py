def calculate_average(itemList):
        average = 0
        
        if len(itemList) == 0:
            return 0
        else:
            for i in itemList:
                average += i
            
            return float(average)/len(itemList)