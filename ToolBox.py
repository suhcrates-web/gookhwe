

## a에 b를 넣음. 리스트 숫자는 10개 유지
def still_10(a,b):
    a=a[len(b):] + b
    return a
