import polyscope as ps
import polyscope.imgui as gui
import igl
from bary_centric import TetBaryCentricCompute
from pyqmat import nqmat
import numpy as np
from off import write_off
from sklearn.mixture import GaussianMixture

from sqem import Sqem
class PSViewer():
    def __init__(self, Q, eigenvalues, model = "bar2"):
        self.Q = Q
        self.eigenvalues = eigenvalues


        self.n_modes = self.Q.shape[1]
        self.deformed_mode = self.n_modes - 7
        self.magnitude = 1.0
        self.threshold = 0.9
        self.objfile = f"output/{model}/{model}_deformed.obj"
        self.ma_file = f"output/{model}/{model}_deformed.ma"
        # self.surface_mesh_file = f"data/{model}.obj"
        self.surface_mesh_file = f"data/{model}.off"
        
        self.fitting_save_folder = f"output/{model}/fitting"
        

        # self.surface_V, _, _, self.surface_F, _, _ = igl.read_obj(self.surface_mesh_file)
        self.surface_V, self.surface_F, _ = igl.read_off(self.surface_mesh_file)


        self.V_deform = np.copy(self.surface_V)
        
        self.mesh = ps.register_surface_mesh("mesh", self.surface_V, self.surface_F)

        self.tbtt = TetBaryCentricCompute(model = model)
        self.slabmesh = ps.register_point_cloud("slabmesh", self.tbtt.slabmesh.V, radius = 0.1)

        self.vf, self.ni = igl.vertex_triangle_adjacency(self.surface_F, self.surface_V.shape[0])
        # print(self.vf.shape, self.ni.shape, self.vf.dtype, self.ni.dtype)
        self.N = igl.per_face_normals(self.surface_V, self.surface_F, np.array([0.0, 0.0, 1.0]))


        self.faces_set = np.zeros((0), dtype = np.int32)
        self.points_set= None

        self.hausdorff = None
        self.h:np.ndarray = None
        # self.qmat = qmat("data/{model}.off", f"data/{model}.ma")
        # h = self.qmat.export_hausdorff_distance()
        # self.slabmesh.add_scalar_quantity("hausdorff", h)
        
        # b, tid= tbtt.barycentric_coord(tbtt.medial_V[0])
        # print(b, tid)
        # print(tbtt.bc)
        # print(tbtt.tids)
        self.num_spheres = 1



# Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
    def callback(self):
        

        # disp = self.magnitude * self.Q[:, 49 - self.deformed_mode]
        Qi = self.Q[:, self.deformed_mode]
        disp = self.magnitude * Qi 

        disp = disp.reshape(-1, 3)

        self.V_deform = self.surface_V + disp[: self.surface_V.shape[0]]
        self.mesh.update_vertex_positions(self.V_deform)

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
            
            if self.objfile.endswith(".obj"):
                igl.write_obj(f"{self.objfile}", self.V_deform, self.surface_F)
            elif self.objfile.endswith(".off"): 
                write_off(f"{off_file}", self.V_deform, self.surface_F)
            # igl.write_obj(f"{self.objfile}", surface_V, self.surface_F)
            print(f"{self.objfile} saved")

        changed, self.ma_file = gui.InputText("MA File", self.ma_file)
        if (gui.Button("Export deformed ma & ply")):
            self.tbtt.slabmesh.export_ma(self.ma_file)
            self.tbtt.slabmesh.export_ply(self.ma_file.replace(".ma", ".ply"))

        if (gui.Button("compute hausdorff")):
            self.tbtt.slabmesh.export_ma(self.ma_file)
            off_file = self.ma_file.replace(".ma", ".off")
            write_off(f"{off_file}", self.V_deform, self.surface_F)
            self.qmat = nqmat(off_file, self.ma_file)

            h = self.qmat.hausdorff()
            self.h = np.array(h)
            # print(self.h.shape, self.surface_V.shape)
            self.hausdorff = self.mesh.add_scalar_quantity("hausdorff", self.h, enabled = True)
            print("hausdorff computed")
            
        # if (gui.Button("save extreme set")):
        #     # saving for greedy optimization
        #     write_off(f"{self.fitting_save_folder}/mesh.off", self.V_deform, self.surface_F)
        #     np.save(f"{self.fitting_save_folder}/points_set.npy", self.points_set)
        #     np.save(f"{self.fitting_save_folder}/faces_set.npy", self.faces_set)
        #     self.tbtt.slabmesh.export_ma(f'{self.fitting_save_folder}/slabmesh.ma')

        changed, self.threshold = gui.SliderFloat("threshold", self.threshold, v_min = 0.0, v_max = 1.0)
        if (gui.Button("extract maximum points")):
            self.extract_max_points()
            

        changed, self.num_spheres = gui.InputInt("#spheres", self.num_spheres, step = 1, step_fast = 10)
        if (gui.Button("em cluster")):
            self.em_cluster()
        if (gui.Button("add sphere")):
            self.add_sphere()

    def em_cluster(self):
        gmm = GaussianMixture(n_components= self.num_spheres, covariance_type='full')

        points = self.V_deform[self.points_set]
        gmm.fit(points)
        
        self.labels = np.zeros_like((self.V_deform.shape[0]), dtype = np.int32)

        labels = gmm.predict(self.V_deform)
        self.labels = np.where(self.points_set, labels, -1) 
        print(self.labels.dtype)
        self.label_quantity = self.mesh.add_scalar_quantity("label", self.labels, enabled = True)




    def add_sphere(self): 
        self.N = igl.per_face_normals(self.V_deform, self.surface_F, np.array([0.0, 0.0, 1.0]))

        self.centers = np.zeros((self.num_spheres, 3))
        self.rs = np.zeros((self.num_spheres))
        
        for component in range(self.num_spheres):
            print(component)
            select = self.labels == component
            faces_set = self.face_set_from_points(select)

            
            sum = Sqem()
            sum.set_zero()
            for f in faces_set:
                p = self.V_deform[self.surface_F[f, 0]]
                n = self.N[f]
                sf = Sqem(p, n)
                sum = sum + sf

            pa = np.ones((3)) * -10.0
            pb = np.ones((3)) * 10.0
            center,  r = sum.minimize(pa, pb)

            self.centers[component] = center
            self.rs[component] = r

        print(self.centers)
        self.added_sphere = ps.register_point_cloud("added", self.centers.reshape((-1, 3)), radius = 0.1)
        self.added_sphere.add_scalar_quantity("radius", self.rs)
        self.added_sphere.set_point_radius_quantity("radius")
        


    def face_set_from_points(self, bool_selection):
        faces_set = np.zeros((0), dtype = np.int32)
        for _v in np.argwhere(bool_selection):
            v = int(_v)
            fv = self.vf[self.ni[v]: self.ni[v + 1]]
            faces_set = np.concatenate((faces_set, fv))

        return faces_set

        
    def extract_max_points(self):
        if self.h is None:
            print("hausdorff not computed")
            return
        
        hmax = np.max(self.h)
        thres= hmax * self.threshold

        self.points_set = self.h > thres

        self.faces_set = self.face_set_from_points(self.points_set)

        

        



        self.colors = np.zeros((self.surface_V.shape[0], 3))
        self.colors[self.points_set] = np.array([1, 0, 0])
        self.mesh.add_color_quantity("extreme points", self.colors, enabled = True)

        

        

if __name__ == "__main__":
    ps.init() 
    ps.set_ground_plane_mode("none")
    model = "cap"
    Q = np.load(f"output/{model}/Q.npy")
    eigenvalues = np.load(f"output/{model}/eigenvalues.npy")
    viewer = PSViewer(Q, eigenvalues, model = model)
    ps.set_user_callback(viewer.callback)
    ps.show()
