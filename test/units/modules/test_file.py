from hypothesis import given, strategies as st
import angr
import claripy

import unittest
from unittest.mock import MagicMock
from ansible.modules.file import check_owner_exists, check_group_exists
    
class TestOwnerAndGroupExists(unittest.TestCase):
    def test_check_owner_exists(self):
        module = MagicMock()
        check_owner_exists(module,'1000')
        module.warn.assert_not_called()

        check_owner_exists(module,'9999')
        module.warn.assert_called_with("failed to look up user with uid 9999. Create user up to this point in real play")    
        
    def test_check_group_exists(self):
        module = MagicMock()
        check_group_exists(module,'1000')
        module.warn.assert_not_called()

        check_group_exists(module,'9999')
        module.warn.assert_called_with("failed to look up group with gid 9999. Create group up to this point in real play")    

    @given(owner=st.text())
    def test_check_owner_exists_hypothesis(self,owner):
        module = MagicMock()
        check_owner_exists(module,owner)

    @given(group=st.text())
    def test_check_group_exists_hypothesis(self,group):
        module = MagicMock()
        check_group_exists(module,group)


    def test_check_owner_exists_angr(self):
        module = MagicMock()
        project = angr.Project("file")

        owner = claripy.BVS('owner', 32) 

        initial_state = project.factory.entry_state(args=[owner])

        simulation = project.factory.simulation_manager(initial_state)
        simulation.explore()

        for path in simulation.found:
            constraints = path.state.solver.constraints
            solver = project.solver.BVSolver()
            for constraint in constraints:
                solver.add(constraint)

            solutions = solver.solve([owner])
            for solution in solutions:
                concrete_owner = solution[owner]
                check_owner_exists(module, concrete_owner)


if __name__ == '__main__':
    unittest.main()