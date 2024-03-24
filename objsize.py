import MyData

def objsize(box,F):
# def objsize(id, pixel, height):
    pixel=float(box[3])                       #box=[x, y, w, h]
    # depth = MyData.Data.focal_length*MyData.Data.objHeight*720/(pixel*4.415)
    depth= (F*MyData.Data.objHeight)/(pixel)
    return depth

