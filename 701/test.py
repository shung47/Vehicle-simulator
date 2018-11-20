from graphics import *


def main():
	win = GraphWin("My Window", 500, 500)
	win.setBackground(color_rgb(0,0,0))
	pt=Point(250,250)
	cir = Circle(pt,50)
	cir.setFill(color_rgb(0,255,0))
	cir.draw(win)

main()
