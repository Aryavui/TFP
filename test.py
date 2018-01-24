from compfunc import FP
from anoyfunc import underscore as _
from anoyfunc import uunderscore as __
from functools import partial, reduce
import math


f = _**3

print(f(2))

print((_**2 + _**2)(3, 4))

pl = FP >> _**2 >> _ - 1 >>_*4

print(3 | pl)

words = "Arya Sansa Brandon Snow Hodor Lady Ghost Cersei Imp Jaime Renly Joffery"
print(sorted(filter(lambda s: s.startswith(('a', 's')), map(str.lower, filter(lambda x: len(x) > 3, words.split(" "))))))
print(
    sorted(
        filter(
            lambda s: s.startswith(('a', 's')),
            map(
                str.lower,
                filter(
                    lambda x: len(x) > 3, words.split(" ")
                )
            )
        )
    )
)

'''Create a pipe to perform this task divided into six steps according to the description.
step 1~6:
(1) get a list of words in a string
(2) filter out words whose length is longer than 3
(3) turn all these words into lowercase
(4) filter out the words that start with 'a' or 's'
(5) sort them alphabetically
(6) prints them on the screen
'''
pipeline = FP >> (lambda li: li.split(" ")) \
     >> partial(filter, FP >> len >> (_ > 3))\
     >> partial(map, str.lower)\
     >> partial(filter, lambda s: s.startswith(('a', 's')))\
     >> sorted\
     >> print

# Then throw the list into the created pipe
pipeline <= words

# You can use the same pipe to handle another string
another_words = "Balon Samwell Theon Yara Arynn Jon Lysa Robin Mord Frey Walder Pyp "
another_words | pipeline

sqrt = FP(math.sqrt)
safe_sqrt = sqrt << abs
print(safe_sqrt(4))

vec = [3, 4]
norm_2 = FP >> (lambda li: map(_**2, li))\
         >> sum\
         >> math.sqrt\
         >>print
norm_2(vec)
norm_2 | vec

print(-16 | FP(abs) | FP(math.sqrt) | FP(math.sqrt))
print(-16 | FP(abs) >> FP(math.sqrt) | FP(math.sqrt))
print(-16 | FP(abs) >> FP(math.sqrt) >> FP(math.sqrt))
print(-16 | abs >> FP(math.sqrt) >> FP(math.sqrt))
print(-16 | abs >> FP(math.sqrt) >> math.sqrt)

# print(-16 | abs >> math.sqrt >> FP(math.sqrt))
# print(FP(abs) | FP(math.sqrt) | FP(math.sqrt) | -16)
# print(FP(abs) >> FP(math.sqrt) | FP(math.sqrt) | -16)

f = __ **2 + _ - 2*__ + _/3
print(f)

pipeline = FP >> partial(map, _*2) \
           >> partial(filter, _ > 10) \
           >> partial(reduce, _ + _)\
           >> print
range(0, 10) | pipeline

