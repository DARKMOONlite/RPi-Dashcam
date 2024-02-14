from numpy import array

class intrinsic_matrix:
    def __init__(self,fx,fy,cx,cy) -> None:
        self.focal_length = [fx,fy]
        self.principal_point = [cx,cy]
        self.matrix = array([[fx,0,cx],[0,fy,cy],[0,0,1]])
        pass