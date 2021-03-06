# Jeremy Aguilon
from drawing_objects import Frosty, Light, Camera, Sleigh
from goals import *

time = 0   # use time to move objects from one frame to the next

    
angle = 0;

snow = None
igloo = None
sleigh = None
scene = None
cam = Camera()
frosty = Frosty()

# ****INSTANCING AN OBJECT MULTIPLE TIMES****
christmasLights = [Light(90, 45, -30), Light(90, 45, -60), Light(575,160,-25),Light(575,160,-65)]

def setup():
    size (800, 800, P3D)
    perspective (60 * PI / 180, 1, 0.1, 1000)  # 60 degree field of view
    global cam, frosty, snow
    global igloo, scene, sleigh
    scene = loadShape("tinker.obj")
    igloo = loadShape("igloo2.obj")
    snow = loadImage("snow.jpg")
    sleigh =  Sleigh(100,60,-45, loadShape("SantasSleigh.obj"))
    frosty.addGoal(MovementGoal(85, 55, 20))
    frosty.addGoal(MovementGoal(100, 55, -45))
    frosty.addGoal(RotationGoal(0, PI/2, 0))
    frosty.addGoal(EquationGoal(lambda x: 0.0101351351351*x**2 -2.15878378378*x+169.527027027, 140))
    equationGoal = EquationGoal(
        lambda x: 657.4103 - 9.587755*x + 0.03606822*(x**2) + 0.00007670587*(x**3) - 5.681288e-7*(x**4) + 7.060634e-10*(x**5),
        363)
    frosty.addGoal(equationGoal)
    frosty.addGoal(EquationGoal(lambda x: 0.0104012619541*x**2 -9.16020901114*x+2145.59198462, 490))
    frosty.addGoal(EquationGoal(lambda x: -0.00489104824426*x**2+5.44256674412*x-1340.16146959, 575))
    frosty.addGoal(WiggleGoal(.3))
    frosty.addGoal(MovementGoal(577,173,100, base=173))
    cam = Camera()
    cam.setEye(0, 0, 100)
    cam.setUp(0,1,0)
def draw():
    global time, igloo, frosty
    time += 0.01
    if time >= 10000:
        time = 7.20
    walkingUp(time)
def walkingUp(time):
    global cam, frosty
    global scene
    global igloo, sleigh

    background (150, 150, 150)
    
    ambientLight(50, 50, 50);
    
    # *** LIGHT SOURCE ***
    pointLight(255, 255, 255, 20, -300, -400);
    fill(255, 255, 204)
    pushMatrix()
    translate(20,-300,-400)
    sphere(30)
    popMatrix()
    
    for christmasLight in christmasLights:
        christmasLight.disp(time) 
      
    noStroke()
    specular (180, 180, 180)
    pushMatrix()
    translate(270,220,-200)
    scale(2, 2,3.5)
    rotateX(PI/2)
    shape(scene) 
    popMatrix()
    
   
    noStroke()
    specular (180, 180, 180)
    pushMatrix()
    translate(20,0,-300)
    scale(1, 1, 1)
    rotateY(-PI/1.5)
    rotateX(PI)
    shape(igloo) 
    popMatrix()

    cam.manipulate(time)
    cam.disp()
    frosty.disp(time, sleigh)
    sleigh.disp(time)