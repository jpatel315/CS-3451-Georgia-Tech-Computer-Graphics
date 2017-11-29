# Sample code for starting the mesh processing project

class Mesh(object):
    def __init__(self, num_vertices, num_faces, vertices, geometry):
        self.num_vertices = num_vertices
        self.num_faces = num_faces
        self.vertices = vertices
        self.geometry = geometry
        self.face_normals = self._getFaceNormals()
        self.vertex_normals = self._getVertexNormals()
        self.vertex_shading = True
        self.white = True
        self.colors = [(random(255), random(255), random(255)) for _ in range(self.num_faces)]
    
    def set_random_colors(self):
        self.colors = [(random(255), random(255), random(255)) for _ in range(self.num_faces)]
                  
    def _getFaceNormals(self):
        output = []
        for i in range(len(self.geometry) / 3):
            v1 = self.vertices[self.geometry[i * 3]]
            v2 = self.vertices[self.geometry[i * 3 + 1]]
            v3 = self.vertices[self.geometry[i * 3 + 2]]
            
            u = PVector.sub(v2, v1)
            v = PVector.sub(v3, v1)
            n = u.cross(v).normalize()
            n.mult(-1)
            output.append(n)
        return output
    def _getVertexNormals(self):
        output = []
        
        for i in range(len(self.vertices)):
            adj_face_normals = []
            for j in range(len(self.geometry)):
                if self.geometry[j] == i:
                    adj_face_normals.append(self.face_normals[j / 3])
            v = PVector(0,0,0)
            for norm in adj_face_normals:
                v.add(norm)
            v.normalize()
            output.append(v)
        return output
    
    def get_vertex_normal(self, v):
        for i in range(len(self.vertices)):
            if self.vertices[i] == v:
                return self.vertex_normals[i]
        raise Exception()
    
    def _next(self, cornerId):
        return cornerId + ((currCorner+1) % 3)
    def _prev(self, cornerId):
        return _next(_next(cornerId))


rotate_flag = True    # automatic rotation of model?
time = 0   # keep track of passing time, for automatic rotation
current_mesh = None

# initalize stuff
def setup():
    size (600, 600, OPENGL)
    noStroke()

# draw the current mesh
def draw():
    global time
    
    background(0)    # clear screen to black

    perspective (PI*0.333, 1.0, 0.01, 1000.0)
    camera (0, 0, 5, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    scale (1, -1, 1)    # change to right-handed coordinate system
    
    # create an ambient light source
    ambientLight (102, 102, 102)
  
    # create two directional light sources
    lightSpecular (204, 204, 204)
    directionalLight (102, 102, 102, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();
    fill (50, 50, 200)            # set polygon color
    ambient (200, 200, 200)
    specular (0, 0, 0)            # no specular highlights
    shininess (1.0)
    rotate (time, 1.0, 0.0, 0.0)

    # THIS IS WHERE YOU SHOULD DRAW THE MESH
    if current_mesh == None:
        beginShape()
        normal (0.0, 0.0, 1.0)
        vertex (-1.0, -1.0, 0.0)
        vertex ( 1.0, -1.0, 0.0)
        vertex ( 1.0,  1.0, 0.0)
        vertex (-1.0,  1.0, 0.0)
        endShape(CLOSE)
    else:
        for face_id in range(len(current_mesh.geometry) / 3):
            if current_mesh.white:
                fill(200,200,200)
            else:
                fill(*current_mesh.colors[face_id])
            print(face_id)
            v1 = current_mesh.vertices[current_mesh.geometry[face_id * 3]]
            v2 = current_mesh.vertices[current_mesh.geometry[face_id * 3 + 1]]
            v3 = current_mesh.vertices[current_mesh.geometry[face_id * 3 + 2]]
            
            if current_mesh.vertex_shading:
                n1 = current_mesh.get_vertex_normal(v1)
                n2 = current_mesh.get_vertex_normal(v2)
                n3 = current_mesh.get_vertex_normal(v3)
                beginShape()
                normal(n1.x, n1.y, n1.z)
                vertex(v1.x, v1.y, v1.z)
                normal(n2.x, n2.y, n2.z)
                vertex(v2.x, v2.y, v2.z)
                normal(n3.x, n3.y, n3.z)
                vertex(v3.x, v3.y, v3.z)
                endShape(CLOSE)
            else:
                n = current_mesh.face_normals[face_id]
                beginShape()
                normal(n.x, n.y, n.z)
                vertex(v1.x, v1.y, v1.z)
                vertex(v2.x, v2.y, v2.z)
                vertex(v3.x, v3.y, v3.z)
                endShape(CLOSE)
    popMatrix()
    
    # maybe step forward in time (for object rotation)
    if rotate_flag:
        time += 0.02

# process key presses
def keyPressed():
    global rotate_flag, current_mesh
    if key == ' ':
        rotate_flag = not rotate_flag
    elif key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == '5':
        read_mesh ('torus.ply')
    elif key == 'n':
        if current_mesh != None:
            current_mesh.vertex_shading = not current_mesh.vertex_shading
        pass  # toggle per-vertex shading
    elif key == 'r':
        if current_mesh != None:
            current_mesh.white = False
            current_mesh.set_random_colors()
        pass  # randomly color faces
    elif key == 'w':
        if current_mesh != None:
            current_mesh.white = True
        pass  # color faces white
    elif key == 'd':
        pass  # calculate the dual mesh
    elif key == 'q':
        exit()

# read in a mesh file (THIS NEEDS TO BE MODIFIED !!!)
def read_mesh(filename):
    global current_mesh
    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()
        
    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])
    print "number of vertices =", num_vertices

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    print "number of faces =", num_faces

    # read in the vertices
    vertices = []
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        print "vertex = ", x, y, z
        vertices.append(PVector(x,y,z))
    # read in the faces
    geometry = []
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if nverts != 3:
            print "error: this face is not a triangle"
            exit()
        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        print "face =", index1, index2, index3
        geometry += [index1, index2, index3] # i * 3 + j
    current_mesh = Mesh(num_vertices, num_faces, vertices, geometry)
