import random
import pytest
from src.algorithms import *
from src.cases import *

@pytest.mark.parametrize('fn',[bubble_sort,insertion_sort,merge_sort])
def test_sort(fn):
    samples=[[],[1],[-2,0,-2,3],list(range(100)),list(range(100,-1,-1))]
    samples += [list(numbers(n,run)) for n in [2,9,50,300] for run in range(10)]
    for values in samples:
        expected=sorted(values); result=fn(values)
        assert result is values and result==expected

@pytest.mark.parametrize('fn',[bubble_sort,insertion_sort,merge_sort])
def test_stability(fn):
    class Item:
        def __init__(self,key,i):self.key,self.i=key,i
        def __gt__(self,other):return self.key>other.key
        def __le__(self,other):return self.key<=other.key
    values=[Item(i%3,i) for i in range(30)]
    assert [x.i for x in fn(values)]==[i for key in range(3) for i in range(30) if i%3==key]

def test_binary():
    for n in range(50):
        a=sorted(numbers(n,1)); before=a[:]
        for t in a+[-10000,10000]:
            result=binary_search(a,t)
            assert (result==-1 and t not in a) or (0<=result<len(a) and a[result]==t)
        assert a==before

def test_activity():
    samples=[[],[(0,1,0)],[(i,i+1,i) for i in range(8)],[(0,10,i) for i in range(8)],[(0,2,0),(1,2,1),(2,3,2)]]
    samples += [activities(n,r) for n in range(11) for r in range(8)]
    for a in samples:
        before=a[:]; result=activity_selection(a)
        assert a==before and feasible(result)
        assert all(x in a for x in result)
        assert len(result)==optimum(a)

def test_generators():
    assert numbers(50,1)==numbers(50,1)!=numbers(50,2)
    assert activities(50,1)==activities(50,1)!=activities(50,2)
