import random #random select에서 사용
import time #각 알고리즘 시간 측정


f = open('input.txt', 'r')
input = f.readlines()
input= list(map(lambda s: s.strip(), input))

n = int(input[0])
r_numbers = list(map(int, input[1].split()))
d_numbers = list(map(int, input[1].split()))
c_numbers = list(map(int, input[1].split()))
i = int(input[2])

#input.txt = 첫줄 n, 둘째줄 n개의 정수, 셋째줄 idx i



def rselect(numbers, p, r, i):
    
    if p==r:
        return numbers[p] #p==r, numbers원소가 하나일 때 그 원소 return
    q = rpartition(numbers, p, r)
    k = q - p + 1
    if i==k:
        return numbers[q]
    elif i<k:
        return rselect(numbers, p, q-1, i)
    else:
        return rselect(numbers, q+1, r, i-k)
    
    

def rpartition(numbers, p, r):
    idx = random.randint(p, r) #partition의 pivot을 p와 r사이 랜덤 정수로 설정
    numbers[idx], numbers[r] = numbers[r], numbers[idx] #맨 끝 원소와 pivot 원소 swap
    #pivot 원소(numbers[r])를 기준으로 partiton 진행
    x = numbers[r]
    i = p-1
    for j in range(p, r):
        if numbers[j] <= x:
            i=i+1
            numbers[i], numbers[j] = numbers[j], numbers[i]
    numbers[i+1], numbers[r] = numbers[r], numbers[i+1]

    return i+1



def insertionsort(numbers, p, r):
    #dselect에 사용될 insertion sort 구현, 책 참고
    for j in range(p+1, r+1):
        key = numbers[j]
        loc = j-1
        while (loc>=p and numbers[loc]> key):
            numbers[loc+1] = numbers[loc]
            loc -= 1
        numbers[loc+1] = key
    




def swap(numbers, a, b):
    numbers[a], numbers[b]= numbers[b], numbers[a]



def dpartition(numbers, p, r, pivot):
    #raprtition과 동일하나, pivot이 랜덤이 아니라 dselect에서 구한 median of medians(mediannum)으로 설정
    swap(numbers, r, pivot)    
    x = numbers[r]
    i = p-1
    for j in range(p, r):
        if numbers[j] <= x:
            i+=1
            swap(numbers, i, j)
    swap(numbers, i+1, r)
    return i+1





        
def dselect(numbers, p, r, i):
    
    #n <=5 일때 삽입정렬로 구한 후 return
    if (r-p+1) <= 5:
        insertionsort(numbers, p, r)
        return numbers[p+i-1]
    


    medians = []
    index = 0
    #(r-p+1)개의 원소를 5개로 구분한 후, 각 그룹을 정렬하여 중앙값을 medians에 저장
    while (index < (r-p+1)//5):
        insertionsort(numbers, p+index*5, p+index*5+4)
        medians.append(numbers[p+index*5+2])
        index+=1
        
        
    #전체 원소 개수가 5의 배수가 아닐 때, 마지막 그룹을 정렬한 후 추가
    if ((r-p+1)%5!=0):
        insertionsort(numbers, p+index*5, r)
        medians.append(numbers[index*5+((r-p+1)%5-1)//2])
        index+=1
    
    #각 median에서 다시 중앙값 mediannum을 찾기위해 dselect함수를 재귀로 불러옴 
    mediannum = dselect(medians, 0, index-1, (index-2)//2)


    #numbers에서 median값의 index를 찾아 pivot으로 지정
    pivot=p
    for m in range(p, r+1):
        if numbers[m] == mediannum:
            pivot=m
            break;

    #median값의 index인 pivot을 기준으로 partition 진행
    q = dpartition(numbers, p, r, pivot)

    k = q - p + 1
    
    if i==k:
        return numbers[q]
    elif (i < k):
        return dselect(numbers, p, q-1, i)
    else: 
        return dselect(numbers, q+1, r, i-k)
    
    
    
def checker(numbers, i, output):
    count = 0 #numbers의 원소 중 output보다 작은 원소의 개수
    equal = 0 #numbers의 원소 중 output과 같은 원소의 개수로 중복처리
    for j in range(len(numbers)): #모든 원소를 훑어 output보다 작은 값과 같은 값 확인
        if numbers[j] < output:
            count+=1
        if numbers[j] == output:
            equal+=1
    if (count<i<=count+equal):
        return "correct!"
    else:
        return "wrong!"



r_output=open("random.txt", 'w')
d_output=open("deter.txt", 'w')
checker_output=open("result.txt", 'w')

#main
randomstart=time.time()
r_result = rselect(r_numbers, 0, n-1, i)
randomend=time.time()
random_time=round((randomend-randomstart)*1000)
r_output.writelines([str(r_result), "\n", str(random_time), "ms"])

deterstart=time.time()
d_result = dselect(d_numbers, 0, n-1, i)
deterend=time.time()
deter_time=round((deterend-deterstart)*1000)
d_output.writelines([str(d_result), "\n", str(deter_time), "ms"])

r_check=checker(c_numbers, i, r_result)
d_check=checker(c_numbers, i, d_result)
checker_output.writelines(["***random result***\n", r_check, "\n", "***deter result***\n", d_check])
