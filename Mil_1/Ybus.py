from settings import s
import numpy as np

class Ybus:
    def __init__(self,ybus):
        self.ybus = np.array([y11, y12,y13,y14,y15,y16,y17],
                    [y21,y22,y23,y24,y25,y26,y27],
                    [y31,y32,y33,y34,y35,y36,y37],
                    [y41,y42,y43,y44,y45,y46,y47],
                    [y51,y52,y53,y54,y55,y56,y57],
                    [y61,y62,y63,y64,y65,y66,y67],
                    [y71,y72,y73,y74,y75,y76,y77])

        print(self.ybus)