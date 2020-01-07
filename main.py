from fraktal.Drawing import Drawing as dr, draw_scenes
from appJar import gui

def create_default_scenes(width: int, height: int) -> list:

	collection_of_scenes = []

	scenes = []
	for i in range(47):
		p = {"width": width,
		     "height": height,
		     "fractal": "mandelbrot",
		     "center": -0.8 - 0.1550000000291j,
		     "zoomlevel": i,
		     "iterate_max": 2560,
		     "style": "default"}
		scenes.append(p)
	collection_of_scenes.append(scenes)

	scenes = []
	for i in range(47):
		p = {"width": width,
		     "height": height,
		     "fractal": "mandelbrot",
		     "center": -0.8 - 0.1550000000291j,
		     "zoomlevel": i,
		     "iterate_max": 2560,
		     "style": "rainbow"}
		scenes.append(p)
	collection_of_scenes.append(scenes)

	scenes = []
	for i in range(47):
		p = {"width": width,
		     "height": height,
		     "fractal": "julia",
			 "c": -0.79 + 0.135j,
		     "center": +0.4938793215408734 - 0.15j,
		     "zoomlevel": i,
		     "iterate_max": 2560,
		     "style": "default"}
		scenes.append(p)
	collection_of_scenes.append(scenes)

	scenes = []
	for i in range(8):
		p = {"width": width,
		     "height": height,
		     "fractal": "mandelbrot4",
		     "center": +0.4938793215408734 - 0.15j,
		     "zoomlevel": i,
		     "iterate_max": 2560,
		     "style": "default"}
		scenes.append(p)
	collection_of_scenes.append(scenes)

	scenes = []
	for i in range(8):
		p = {"width": width,
		     "height": height,
		     "fractal": "julia4",
			 "c": -0.78 + 0.115j,
		     "center": +0.4938793215408734 - 0.15j,
		     "zoomlevel": i,
		     "iterate_max": 2560,
		     "style": "default"}
		scenes.append(p)
	collection_of_scenes.append(scenes)

	return collection_of_scenes


# handle button events
def press(button):
	if button == "Cancel":
		app.stop()
	else:
		d = dr(width = int(app.appWindow.winfo_screenwidth()/2),
			   height = app.appWindow.winfo_screenheight())
		scenes = create_default_scenes(width = int(app.appWindow.winfo_screenwidth()/2),
		                               height = app.appWindow.winfo_screenheight())
		draw_scenes(scenes[1])

	app.stop()

if __name__ == "__main__":
	app = gui("Fractal Designer", "500x600")
	app.addLabel("title", "Fractal Designer")
	app.setLabelBg("title", "grey")
	app.addButtons(["Go", "Cancel"], press)
	# start the GUI
	#app.go()
	press("Go")