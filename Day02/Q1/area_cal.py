
import math_utils

rec_lenght = int(input("Enter the lenght of rectangle"))
rec_breadth = int(input("Enter the breadth of rectangle"))

area_rec =math_utils.area_rec(rec_lenght, rec_breadth)
print(area_rec)

squ_side = int(input("Enter the side of square"))
area_squ = math_utils.area_squ(squ_side)
print(area_squ)

tri_base = int(input("Enter the base of triangle"))
tri_height = int(input("Enter the height of triangle"))

area_tri = math_utils.area_tri(tri_base,tri_height)
print(area_tri)

cir_rad = int(input("Enter the radius of circle"))
area_cir = math_utils.area_circle(cir_rad)
print(area_cir)