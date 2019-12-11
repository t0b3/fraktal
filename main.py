from fraktal.Drawing import Drawing as dr
from appJar import gui




# handle button events
def press(button):
	if button == "Cancel":
		app.stop()
	else:
		d = dr()
		d.mandelbrot2(count=1)

if __name__ == "__main__":
	app = gui("Fractal Designer", "500x600")
	app.addLabel("title", "Fractal Designer")
	app.setLabelBg("title", "grey")
	app.addButtons(["Go", "Cancel"], press)
	# start the GUI
	app.go()