from monodepth2.test_changed import monodepth2
from objsize import objsize

class mono_vision:
    def __init__(self, image,pos):
        print(pos)
        # print(method)
        self.img = image
        self.position = pos
        # self.method = method

        # if self.method == 'dens_depth':
        #     dis=self.method1()

    def method1(self):      #monodepth
        depth = monodepth2(self.img,self.position)
        # print(depth)
        return depth

    def method2(self,box,F):
        # box = yolo(self.img)
        depth = objsize(box,F)
        # print(depth)
        return depth
