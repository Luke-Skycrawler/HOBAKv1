import polyscope as ps
import polyscope.imgui as gui


class PSViewer():
    def __init__(self, V, F, Q, eigenvalues):
        self.V = V
        self.F = F
        self.Q = Q
        self.eigenvalues = eigenvalues

        self.is_true1 = False
        self.is_true2 = True
        self.ui_int = 7
        self.ui_float1 = -3.2
        self.ui_float2 = 0.8
        self.ui_color3 = (1., 0.5, 0.5)
        self.ui_color4 = (0.3, 0.5, 0.5, 0.8)
        self.ui_angle_rad = 0.2
        self.ui_text = "some input text"
        self.ui_options = ["option A", "option B", "option C"]
        self.ui_options_selected = self.ui_options[1]



        self.deformed_mode = 0
        self.magnitude = 1.0

        self.mesh = ps.register_surface_mesh("mesh", self.V, self.F)
        


    def my_function(self):
        # ... do something important here ...
        print("executing function")

# Define our callback function, which Polyscope will repeatedly execute while running the UI.
# We can write any code we want here, but in particular it is an opportunity to create ImGui 
# interface elements and define a custom UI.
    def callback(self):

        # If we want to use local variables & assign to them in the UI code below, 
        # we need to mark them as nonlocal. This is because of how Python scoping 
        # rules work, not anything particular about Polyscope or ImGui.
        # Of course, you can also use any other kind of python variable as a controllable 
        # value in the UI, such as a value from a dictionary, or a class member. Just be 
        # sure to assign the result of the ImGui call to the value, as in the examples below.
        # 
        # If these variables are defined at the top level of a Python script file (i.e., not
        # inside any method), you will need to use the `global` keyword instead of `nonlocal`.
        # global is_true1, is_true2, ui_int, ui_float1, ui_float2, ui_color3, ui_color4, ui_text, ui_options_selected, ui_angle_rad
        is_true1, is_true2, ui_int, ui_float1, ui_float2, ui_color3, ui_color4, ui_text, ui_options_selected, ui_angle_rad = self.is_true1, self.is_true2, self.ui_int, self.ui_float1, self.ui_float2, self.ui_color3, self.ui_color4, self.ui_text, self.ui_options_selected, self.ui_angle_rad
        


        # == Settings

        # Use settings like this to change the UI appearance.
        # Note that it is a push/pop pair, with the matching pop() below.
        gui.PushItemWidth(150)


        # == Show text in the UI

        gui.TextUnformatted("Some sample text")
        gui.TextUnformatted("An important value: {}".format(42))
        gui.Separator()


        # == Buttons

        if(gui.Button("A button")):
            # This code is executed when the button is pressed
            print("Hello")

        # By default, each element goes on a new line. Use this 
        # to put the next element on the _same_ line.
        gui.SameLine() 

        if(gui.Button("Another button")):
            # This code is executed when the button is pressed
            self.my_function()


        # == Set parameters

        # These commands allow the user to adjust the value of variables.
        # It is important that we assign the return result to the variable to
        # update it. 
        # For most elements, the return is actually a tuple `(changed, newval)`, 
        # where `changed` indicates whether the setting was modified on this 
        # frame, and `newval` gives the new value of the variable (or the same 
        # old value if unchanged).
        #
        # For numeric inputs, ctrl-click on the box to type in a value.

        # Checkbox
        changed, is_true1 = gui.Checkbox("flag1", is_true1) 
        if(changed): # optionally, use this conditional to take action on the new value
            pass 
        gui.SameLine() 
        changed, is_true2 = gui.Checkbox("flag2", is_true2) 

        # Input ints
        changed, ui_int = gui.InputInt("ui_int", ui_int, step=1, step_fast=10) 

        changed, self.deformed_mode = gui.InputInt("#mode", self.deformed_mode, step = 1, step_fast = 10)
        
        changed, self.magnitude = gui.SliderFloat("magnitude", self.magnitude, v_min = 0.0, v_max = 5.0)

        # Input floats using two different styles of widget
        changed, ui_float1 = gui.InputFloat("ui_float1", ui_float1) 
        gui.SameLine() 
        changed, ui_float2 = gui.SliderFloat("ui_float2", ui_float2, v_min=-5, v_max=5)

        # Input colors
        changed, ui_color3 = gui.ColorEdit3("ui_color3", ui_color3)
        gui.SameLine() 
        changed, ui_color4 = gui.ColorEdit4("ui_color4", ui_color4)

        # Input text
        changed, ui_text = gui.InputText("enter text", ui_text)

        # Combo box to choose from options
        # There, the options are a list of strings in `ui_options`,
        # and the currently selected element is stored in `ui_options_selected`.
        gui.PushItemWidth(200)
        changed = gui.BeginCombo("Pick one", ui_options_selected)
        if changed:
            for val in ui_options:
                _, selected = gui.Selectable(val, ui_options_selected==val)
                if selected:
                    ui_options_selected = val
            gui.EndCombo()
        gui.PopItemWidth()


        # Use tree headers to logically group options

        # This a stateful option to set the tree node below to be open initially.
        # The second argument is a flag, which works like a bitmask.
        # Many ImGui elements accept flags to modify their behavior.
        gui.SetNextItemOpen(True, gui.ImGuiCond_FirstUseEver)

        # The body is executed only when the sub-menu is open. Note the push/pop pair!
        if(gui.TreeNode("Collapsible sub-menu")):

            gui.TextUnformatted("Detailed information")

            if(gui.Button("sub-button")):
                print("hello")

            # There are many different UI elements offered by ImGui, many of which
            # are bound in python by Polyscope. See ImGui's documentation in `imgui.h`,
            # or the polyscope bindings in `polyscope/src/cpp/imgui.cpp`.
            changed, ui_angle_rad = gui.SliderAngle("ui_float2", ui_angle_rad, 
                    v_degrees_min=-90, v_degrees_max=90)

            gui.TreePop()

        gui.PopItemWidth()
        
        # disp = self.magnitude * self.Q[:, 49 - self.deformed_mode]
        disp = self.magnitude * self.Q[:, self.deformed_mode]
        disp = disp.reshape(-1, 3)
        self.mesh.update_vertex_positions(self.V + disp)

        

if __name__ == "__main__":
    ps.init() 
    viewer = PSViewer()
    ps.set_user_callback(viewer.callback)
    ps.show()
