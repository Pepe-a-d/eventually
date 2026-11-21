from comun import *
from shapely.geometry import Polygon
from shapely.ops import unary_union, nearest_points
def seccion_xz(m, y):
    # corta por el plano Y = y: gira para que Y pase a ser Z. (x,y,z)->(x,-z,y)
    r = m.rotate([-90, 0, 0])      # y -> -z ? se comprueba con bounding box
    b0 = m.bounding_box(); b1 = r.bounding_box()
    cs = None
    # rotate([-90,0,0]): (x,y,z) -> (x, z, -y)
    cs = r.slice(-y)
    return unary_union([Polygon(q) for q in cs.to_polygons()])   # coords (x, z)
if __name__ == '__main__':
    for y in (-9.0, 9.0):
        for ang in (0, 5.25):
            A = seccion_xz(puerta(1, ang), y); B = seccion_xz(puerta(-1, ang), y)
            from shapely.geometry import box
            v = box(-6, -8, 8, 6)
            a = A.intersection(v); b = B.intersection(v)
            pa, pb = nearest_points(a, b)
            print('y=%g ang=%g dist %.4f  punto derecha (%.3f, %.3f)  punto izquierda (%.3f, %.3f)' % (y, ang, a.distance(b), pa.x, pa.y, pb.x, pb.y))
            print('   derecha:', [(round(x,2), round(z,2)) for x, z in a.exterior.coords])
            print('   izquierda:', [(round(x,2), round(z,2)) for x, z in b.exterior.coords])
