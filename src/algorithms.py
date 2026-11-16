"""Sorts mutate and return the supplied list; other functions preserve input."""
def bubble_sort(values):
    for end in range(len(values)-1,0,-1):
        swapped=False
        for j in range(end):
            if values[j]>values[j+1]:
                values[j],values[j+1]=values[j+1],values[j]
                swapped=True
        if not swapped: break
    return values

def insertion_sort(values):
    for i in range(1,len(values)):
        key=values[i]; j=i-1
        while j>=0 and values[j]>key:
            values[j+1]=values[j]; j-=1
        values[j+1]=key
    return values

def merge_sort(values):
    if len(values)>1:
        mid=len(values)//2
        left=merge_sort(values[:mid]); right=merge_sort(values[mid:])
        i=j=k=0
        while i<len(left) and j<len(right):
            if left[i]<=right[j]: values[k]=left[i]; i+=1
            else: values[k]=right[j]; j+=1
            k+=1
        while i<len(left): values[k]=left[i]; i+=1; k+=1
        while j<len(right): values[k]=right[j]; j+=1; k+=1
    return values

def binary_search(sorted_values,target):
    low=0; high=len(sorted_values)-1
    while low<=high:
        mid=low+(high-low)//2
        if sorted_values[mid]==target: return mid
        if sorted_values[mid]<target: low=mid+1
        else: high=mid-1
    return -1

def activity_selection(activities):
    ordered=sorted(activities,key=lambda a:(a[1],a[0],a[2]))
    selected=[]; last_finish=float('-inf')
    for a in ordered:
        if a[0]>=last_finish: selected.append(a); last_finish=a[1]
    return selected
