import polyscope as ps
import polyscope.imgui as gui
import igl
from bary_centric import TetBaryCentricCompute

class PSViewer():
    def __init__(self, V, F, Q, eigenvalues):
        self.V = V
        self.F = F
        self.Q = Q
        self.eigenvalues = eigenvalues


        self.n_modes = self.Q.shape[1]
        self.deformed_mode = self.n_modes - 7
        self.magnitude = 1.0
        self.objfile = "output/bar2/bar_deformed.obj"
        self.surface_mesh_file = "data/bar.obj"

        self.surface_V, _, _, self.surface_F, _, _ = igl.read_obj(self.surface_mesh_file)

        self.mesh = ps.register_surface_mesh("mesh", self.V, self.F)
        self.tbtt = TetBaryCentricCompute()
        self.slabmesh = ps.register_point_cloud("slabmesh", self.tbtt.slabmesh.V, radius = 0.1)

        
        # b, tid= tbtt.barycentric_coord(tbtt.medial_V[0])
        # print(b, tid)
        # print(tbtt.bc)
        # print(tbtt.tids)



    def my_function(self):
        # ... do something important here ...
        print("executing function")

# Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
    def callback(self):
        

        # disp = self.magnitude * self.Q[:, 49 - self.deformed_mode]
        Qi = self.Q[:, self.deformed_mode]
        disp = self.magnitude * Qi 

        disp = disp.reshape(-1, 3)
        self.mesh.update_vertex_positions(self.V + disp)

        self.tbtt.deform(disp)
        self.slabmesh.update_point_positions(self.tbtt.slabmesh.V)
        

        # == Settings

        # Use settings like this to change the UI appearance.
        # Note that it is a push/pop pair, with the matching pop() below.
        gui.PushItemWidth(150)

        gui.Separator()

        changed, self.deformed_mode = gui.InputInt("#mode", self.deformed_mode, step = 1, step_fast = 10)
        # Input text
        changed, self.objfile = gui.InputText("File", self.objfile)
        changed, self.magnitude = gui.SliderFloat("Magnitude", self.magnitude, v_min = 0.0, v_max = 5.0)
        # == Buttons
        if(gui.Button("Export deformed obj")):
            # This code is executed when the button is pressed
            surface_V = (self.V + disp)[: self.surface_V.shape[0]]
            
            if self.objfile.endswith(".obj"):
                igl.write_obj(f"{self.objfile}", surface_V, self.F)
            elif self.objfile.endswith(".off"): 
                igl.write_off(f"{self.objfile}", surface_V, self.F)
            # igl.write_obj(f"{self.objfile}", surface_V, self.surface_F)
            print(f"{self.objfile} saved")

        if (gui.Button("Export deformed ma & ply")):
            pass


        

        

if __name__ == "__main__":
    ps.init() 
    viewer = PSViewer()
    ps.set_user_callback(viewer.callback)
    ps.show()
