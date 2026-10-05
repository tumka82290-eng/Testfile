from collections.abc import Iterable
from typing import Callable
from functools import wraps
import time

def time_deco(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        #start = time.perf_counter()
        res = func(*args, **kwargs)
        # end = time.perf_counter()
        #print(f"{func.__name__}: {end - start:.6f} secs")
        return res
    return wrapper  

class Counter:
    def __init__(self, iterable: Iterable):
        self._counts = {}
        for item in iterable:
            self._counts[item] = self._counts.get(item, 0) + 1

    def __getitem__(self, key):
        return self._counts.get(key, 0)

    def keys(self):
        return self._counts.keys()
        
    def __iter__(self):
        return iter(self._counts)

class Repunit:
    def __init__(self, num: int):
        self.num = num
        self.repunits = self.calculate_repunits(num)
        self.counts = self.optimal_calculate_repunits(num)

    @staticmethod
    @time_deco
    def calculate_repunits(num: int) -> list[int]:
        reps = []
        while num > 0:
            length = len(str(num))
            rep = int(length * '1')
            if rep > num:
                rep = int((length - 1) * '1') if length > 1 else 1
            reps.append(rep)
            num -= rep
        return reps

    @staticmethod
    @time_deco
    def optimal_calculate_repunits(num: int) -> int:
        if num <= 0:
            return 0
            
        total_repunits_count = 0
        length = len(str(num))
        
        while num > 0 and length > 0:
            rep = int(length * '1')
            
            if num >= rep:
                # Добавляем количество вошедших репюнитов в общий счетчик
                total_repunits_count += num // rep
                num %= rep  # Оставляем остаток
                
            length -= 1
            
        return total_repunits_count
    
    @property
    def compact(self) -> str:
        counts = Counter(self.repunits)
        sorted_reps = sorted(counts.keys(), reverse=True)
        
        parts = []
        for rep in sorted_reps:
            count = counts[rep]
            if rep == 1:
                parts.append(f"{count}")
            elif count == 1:
                parts.append(f"{rep}")
            else:
                parts.append(f"{rep} * {count}")
                
        string = " + ".join(parts)
        return f"R({self.num})={string}({len(self.repunits)})"

    @property
    def full(self) -> str:
        a = " + ".join([str(x) for x in self.repunits])
        return f"R({self.num})={a}({len(self.repunits)})"

    def __str__(self):
        return f"R({self.num})={self.counts}"

a = 1000
reps = [Repunit(x).compact + "\n" if x != a else Repunit(x).compact for x in range(1, a + 1)]
open("reps.txt", "w").writelines(reps)
