class Cuboid():
    def __init__(self, x, y, z):
        self.x0 = x[0]
        self.x1 = x[1]
        self.y0 = y[0]
        self.y1 = y[1]
        self.z0 = z[0]
        self.z1 = z[1]
    
    @property
    def x(self):
        return self.x0, self.x1

    @property
    def y(self):
        return self.y0, self.y1
    
    @property
    def z(self):
        return self.z0, self.z1
    
    @property
    def size(self):
        return (self.x1-self.x0+1) * (self.y1-self.y0+1) * (self.z1-self.z0+1)
    
    def __and__(self, other):
        if self.x0 > other.x1 or self.x1 < other.x0 or \
            self.y0 > other.y1 or self.y1 < other.y0 or \
            self.z0 > other.z1 or self.z1 < other.z0:
            return None
        return Cuboid(
            (max(self.x0, other.x0), min(self.x1, other.x1)),
            (max(self.y0, other.y0), min(self.y1, other.y1)),
            (max(self.z0, other.z0), min(self.z1, other.z1)))
    
    def __sub__(self, other):
        if intxn := self & other:
            cuboids = []
            left   = (self.x0, intxn.x0-1) if self.x0 < intxn.x0 else False
            right  = (intxn.x1+1, self.x1) if self.x1 > intxn.x1 else False
            bottom = (self.y0, intxn.y0-1) if self.y0 < intxn.y0 else False
            top    = (intxn.y1+1, self.y1) if self.y1 > intxn.y1 else False 
            back   = (self.z0, intxn.z0-1) if self.z0 < intxn.z0 else False
            front  = (intxn.z1+1, self.z1) if self.z1 > intxn.z1 else False

            if left:   cuboids.append(Cuboid(left, intxn.y, intxn.z))
            if right:  cuboids.append(Cuboid(right, intxn.y, intxn.z))
            if bottom: cuboids.append(Cuboid(intxn.x, bottom, intxn.z))
            if top:    cuboids.append(Cuboid(intxn.x, top, intxn.z))
            if back:   cuboids.append(Cuboid(intxn.x, intxn.y, back))
            if front:  cuboids.append(Cuboid(intxn.x, intxn.y, front))

            if left  and bottom: cuboids.append(Cuboid(left, bottom, intxn.z))
            if left  and top:    cuboids.append(Cuboid(left, top, intxn.z))
            if left  and back:   cuboids.append(Cuboid(left, intxn.y, back))
            if left  and front:  cuboids.append(Cuboid(left, intxn.y, front))
            if right and bottom: cuboids.append(Cuboid(right, bottom, intxn.z))
            if right and top:    cuboids.append(Cuboid(right, top, intxn.z))
            if right and back:   cuboids.append(Cuboid(right, intxn.y, back))
            if right and front:  cuboids.append(Cuboid(right, intxn.y, front))
            if back  and bottom: cuboids.append(Cuboid(intxn.x, bottom, back))
            if back  and top:    cuboids.append(Cuboid(intxn.x, top, back))
            if front and bottom: cuboids.append(Cuboid(intxn.x, bottom, front))
            if front and top:    cuboids.append(Cuboid(intxn.x, top, front))

            if left  and bottom and back:  cuboids.append(Cuboid(left, bottom, back))
            if left  and bottom and front: cuboids.append(Cuboid(left, bottom, front))
            if left  and top    and back:  cuboids.append(Cuboid(left, top, back))
            if left  and top    and front: cuboids.append(Cuboid(left, top, front))
            if right and bottom and back:  cuboids.append(Cuboid(right, bottom, back))
            if right and bottom and front: cuboids.append(Cuboid(right, bottom, front))
            if right and top    and back:  cuboids.append(Cuboid(right, top, back))
            if right and top    and front: cuboids.append(Cuboid(right, top, front))
            
            return cuboids
        else:
            return [self]
    
    def __repr__(self):
        return f"x={self.x0}..{self.x1},y={self.y0}..{self.y1},z={self.z0}..{self.z1}"

if __name__ == '__main__':
    c0 = Cuboid((-1, 1), (-1, 1), (-1, 1))

    c1 = Cuboid((0, 0), (0, 0), (0, 0))
    print("center", (c0 & c1).size == 1 and sum(c.size for c in c0-c1) == 26)

    c1 = Cuboid((-3, 3), (1, 1), (-3, 3))
    print("y top", (c0 & c1).size == 9 and len(c0-c1) == 1 and sum(c.size for c in c0-c1) == 18)

    c1 = Cuboid((-3, 3), (0, 0), (-3, 3))
    print("y middle", (c0 & c1).size == 9 and len(c0-c1) == 2 and sum(c.size for c in c0-c1) == 18)
