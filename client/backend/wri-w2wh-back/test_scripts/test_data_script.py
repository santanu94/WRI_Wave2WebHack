import sys
def main():
    region=sys.argv[1]
    dataType=sys.argv[2]
    dataList=[]
    dataString=''
    if region=='KRS':
        if dataType=='inflowcc':
            dataList=[85, 72, 78, 75, 77, 75, 55, 55.3, 22.3, 59, 61, 84]
        elif dataType=='outflow':
            dataList=[85, 61, 78, 25, 44, 75, 35, 55.3, 22.3, 117, 17, 84]
        elif dataType=='inflowtrends':
            dataList=[85, 72, 78, 3, 77, 11, 74, 53, 94, 37, 43, 14]
    elif region=='KAB':
        if dataType=='inflowcc':
            dataList=[14, 72, 18, 45, 77, 75, 55, 51.1, 22.3, 41, 61, 84]
        elif dataType=='outflow':
            dataList=[82, 61, 78, 25, 34, 75, 35, 55.3, 22.3, 117, 37, 60]
        elif dataType=='inflowtrends':
            dataList=[62, 72, 78, 13, 7, 11, 42, 53, 21, 37, 17, 94]
    elif region=='HEM':
        if dataType=='inflowcc':
            dataList=[35, 62, 14, 125, 97, 75, 55, 55.3, 22.3, 59, 61, 84]
        elif dataType=='outflow':
            dataList=[77, 31, 18, 53, 34, 75, 35, 55.3, 22.3, 117, 17, 84]
        elif dataType=='inflowtrends':
            dataList=[15, 52, 98, 3, 77, 11, 74, 53, 94, 37, 43, 14]
    elif region=='HAR':
        if dataType=='inflowcc':
            dataList=[11, 71, 38, 75, 97, 38, 55, 55.3, 108, 59, 61, 84]
        elif dataType=='outflow':
            dataList=[65, 61, 78, 25, 44, 75, 145, 55.3, 22.3, 117, 17, 84]
        elif dataType=='inflowtrends':
            dataList=[5, 72, 7, 33, 77, 101, 74, 53, 94, 44, 43, 4]
    
    print(dataList)

if __name__ == '__main__':
    main()