import adsk.core

def point3d_from_string(pt: str):
    pts = pt.split()
    return adsk.core.Point3D.create(
        x = float(pts[0]),
        y = float(pts[2]),
        z = float(pts[1])
    )