import nanome
import sys
import time
from .rmsd_calculation import *
# from rmsd_menu import RMSDMenu
from .rmsd_menu import RMSDMenu
from . import rmsd_helpers as help
from nanome.util import Logs

class RMSD(nanome.PluginInstance):
    def start(self):
        Logs.debug("Start RMSD Plugin")
        self.args = RMSD.Args()
        self._menu = RMSDMenu(self)
        self._menu.build_menu()

    def on_run(self):
        menu = self.menu
        menu.enabled = True
        self._menu._request_refresh()

    def on_complex_added(self):
        nanome.util.Logs.debug("Complex added: refreshing")
        self.request_refresh()

    def on_complex_removed(self):
        nanome.util.Logs.debug("Complex removed: refreshing")
        self.request_refresh()
        #self.request_refresh2()

    def request_refresh(self):
        self.request_complex_list(self.on_complex_list_received)
        nanome.util.Logs.debug("Complex list requested")

    # 
    # def request_refresh2(self):
    #     self.request_complex_list(self.on_complex_list_received2)
    #     nanome.util.Logs.debug("Complex list requested")


    def update_button(self, button):
        self.update_content(button)

    def make_plugin_usable(self):
        self._menu.make_plugin_usable()

    def on_complex_list_received(self, complexes):
        Logs.debug("complex received: ", complexes)
        self._menu.change_complex_list(complexes)

    def run_rmsd(self, mobile, target):
        self._mobile = mobile
        self._target = target
        self.request_workspace(self.on_workspace_received)

    def on_workspace_received(self, workspace):
        complexes = workspace.complexes
        for complex in complexes:
            if complex.index == self._mobile.index:
                mobile_complex = complex
            if complex.index == self._target.index:
                target_complex = complex

        result = self.align(target_complex, mobile_complex)
        if result :
            self.update_workspace(workspace)
        Logs.debug("RMSD done")
        self.make_plugin_usable()
        self.request_refresh()
    
    def update_args(self, arg, option):
        setattr(self.args, arg, option)

    class Args(object):
        def __init__(self):
            self.rotation = "kabsch" #alt: "quaternion", "none"
            self.reorder = False
            self.reorder_method = "hungarian" #alt "brute", "distance"
            self.use_reflections = False # scan through reflections in planes (eg Y transformed to -Y -> X, -Y, Z) and axis changes, (eg X and Z coords exchanged -> Z, Y, X). This will affect stereo-chemistry.
            self.use_reflections_keep_stereo = False # scan through reflections in planes (eg Y transformed to -Y -> X, -Y, Z) and axis changes, (eg X and Z coords exchanged -> Z, Y, X). Stereo-chemistry will be kept.
            #exclusion options
            self.no_hydrogen = False
            self.selected_only = False
            self.backbone_only = False
            self.align = True

        @property
        def update(self):
            if self.align and (self.no_hydrogen or self.selected_only):
                Logs.debug('Invalid options: cannot use align with "no hydrogen" or "selected only" options')
                return False
            return self.align

    def align(self, p_complex, q_complex):
        #p is fixed q is mobile
        args = self.args
        p_atoms = list(p_complex.atoms)
        q_atoms = list(q_complex.atoms)

        p_size = len(p_atoms)
        q_size = len(q_atoms)

        if not p_size == q_size:
            Logs.debug("error: Structures not same size")
            return False

        if args.selected_only:
            p_atoms = help.strip_nonselected(p_atoms)
            q_atoms = help.strip_nonselected(q_atoms)

        if args.no_hydrogen:
            p_atoms = help.strip_hydrogens(p_atoms)
            q_atoms = help.strip_hydrogens(q_atoms)

        if args.backbone_only:
            p_atoms = help.strip_non_backbone(p_atoms)
            q_atoms = help.strip_non_backbone(q_atoms)

        p_atom_names = get_atom_types(p_atoms)
        q_atom_names = get_atom_types(q_atoms)
        p_pos_orig = help.get_positions(p_atoms)
        q_pos_orig = help.get_positions(q_atoms)
        q_atoms = np.asarray(q_atoms)
        if np.count_nonzero(p_atom_names != q_atom_names) and not args.reorder:
            #message should be sent to nanome as notification?
            msg = "\nerror: Atoms are not in the same order. \n reorder to align the atoms (can be expensive for large structures)."
            Logs.debug(msg)
            return False

        p_coords = help.positions_to_array(p_pos_orig)
        q_coords = help.positions_to_array(q_pos_orig)

        # Create the centroid of P and Q which is the geometric center of a
        # N-dimensional region and translate P and Q onto that center. 
        # http://en.wikipedia.org/wiki/Centroid
        p_cent = centroid(p_coords)
        q_cent = centroid(q_coords)
        p_coords -= p_cent
        q_coords -= q_cent

        # set rotation method
        if args.rotation.lower() == "kabsch":
            rotation_method = kabsch_rmsd
        elif args.rotation.lower() == "quaternion":
            rotation_method = quaternion_rmsd
        elif args.rotation.lower() == "none":
            rotation_method = None
        else:
            Logs.debug("error: Unknown rotation method:", args.rotation)
            return False

        # set reorder method
        # when reorder==False, set reorder_method to "None"
        if not args.reorder:
            reorder_method = None
        elif args.reorder_method.lower() == "hungarian":
            reorder_method = reorder_hungarian
        elif args.reorder_method.lower() == "brute":
            reorder_method = reorder_brute
        elif args.reorder_method.lower() == "distance":
            reorder_method = reorder_distance
        else:
            Logs.debug("error: Unknown reorder method:", args.reorder_method)
            Logs.debug("The value of reorder is: ",args.reorder)
            return False


        # Save the resulting RMSD
        result_rmsd = None

        if args.use_reflections or args.use_reflections_keep_stereo:
            result_rmsd, q_swap, q_reflection, q_review = check_reflections(
                p_atom_names,
                q_atom_names,
                p_coords,
                q_coords,
                reorder_method=reorder_method,
                rotation_method=rotation_method,
                keep_stereo=args.use_reflections_keep_stereo)
        elif args.reorder:
            q_review = reorder_method(p_atom_names, q_atom_names, p_coords, q_coords)
            q_coords = q_coords[q_review]
            q_atom_names = q_atom_names[q_review]
            q_atoms = q_atoms[q_review]
            if not all(p_atom_names == q_atom_names):
                Logs.debug("error: Structure not aligned")
                return False

        #calculate RMSD
        if result_rmsd:
            pass
        elif rotation_method is None:
            result_rmsd = rmsd(p_coords, q_coords)
        else:
            result_rmsd = rotation_method(p_coords, q_coords)
        Logs.debug("result: {0}".format(result_rmsd))
        self._menu.update_score(result_rmsd)

        # Logs.debug result
        if args.update:
            #resetting coords
            p_coords = help.positions_to_array(p_pos_orig)
            q_coords = help.positions_to_array(q_pos_orig)

            p_coords -= p_cent
            q_coords -= q_cent

            test_qs = copy.deepcopy(q_coords)
            test_inverse_U = [0,0,0]
            # 45 off
            # test_inverse_U[0]=np.asarray([1.0,     0.0,          0.0])
            # test_inverse_U[1]=np.asarray([0.0,     -.4480736,    -0.8939967])
            # test_inverse_U[2]=np.asarray([0.0,     0.8939967,    -0.4480736])
            # 90 off
            test_inverse_U[0]=np.asarray([1.0,     0.0,          0.0])
            test_inverse_U[1]=np.asarray([0.0,     -.5984601,    -0.8011526])
            test_inverse_U[2]=np.asarray([0.0,     0.8011526,    -0.5984601])

            test_inverse_U = np.asarray(test_inverse_U)
            test_qs = np.dot(test_qs, test_inverse_U)

            #reordering coords  ???
            if args.reorder:
                if q_review.shape[0] != len(q_coords):
                    Logs.debug("error: Reorder length error. Full atom list needed for --Logs.debug")
                    return False
                q_coords = q_coords[q_review]
                q_atoms = q_atoms[q_review]

            # Get rotation matrix
            U = kabsch(p_coords, q_coords)
            U = kabsch(p_coords, test_qs)

            # Fake_U = [0,0,0,0]
            # Fake_U[0]=np.asarray([1.0,0.0,0.0,0.0,])
            # Fake_U[1]=np.asarray([0.0,1.0,0.0,0.0,])
            # Fake_U[2]=np.asarray([0.0,0.0,1.0,0.0,])
            # Fake_U[3]=np.asarray([0.0,0.0,0.0,1.0,])
            # Fake_U = np.asarray(Fake_U)
            # U = Fake_U
            #update rotation
            U_matrix = nanome.util.Matrix(4,4)
            for i in range(3):
                for k in range(3):
                    U_matrix[i][k] = U[i][k]
            U_matrix[3][3] = 1
            print("********")

            print(U * test_inverse_U)

            print("==============")
            print(U_matrix)
            print("==============")
            rot_quat = p_complex.rotation
            rot_matrix = nanome.util.Matrix.from_quaternion(rot_quat)
            result_matrix = rot_matrix * U_matrix
            result_quat = nanome.util.Quaternion.from_matrix(result_matrix)
            print(rot_quat)
            print("==============")
            print(result_matrix)
            print("==============")            
            print(q_complex.rotation)
            q_complex.rotation = result_quat
            q_complex.name = q_complex.name[::-1]
            print(p_complex.rotation)
            print(q_complex.rotation)
            Logs.debug("Finished update")

            #align centroids
            q_complex.position = p_complex.position + help.array_to_position(p_cent - q_cent)
        return result_rmsd


def main():
    plugin = nanome.Plugin("RMSD", "A simple plugin that aligns complexes through RMSD calculation", "Test", False)
    plugin.set_plugin_class(RMSD)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
