# -*- coding: utf-8 -*-

import numpy as np
from numpy import real, max as np_max

from ....Classes.MeshMat import MeshMat


def plot_glyph(
    self,
    *args,
    label=None,
    index=None,
    indices=None,
    clim=None,
    factor=None,
    field_name=None,
    save_path=None,
    is_point_arrow=False,
    group_names=None,
    is_show_fig=True,
):
    """Plot the vector field as a glyph (or quiver) over the mesh.

    Parameters
    ----------
    self : MeshSolution
        a MeshSolution object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    label : str
        a label
    index : int
        an index
    indices : list
        list of the points to extract (optional)
    clim : list
        a list of 2 elements for the limits of the colorbar
    factor : float
        factor to multiply vector field
    field_name : str
        title of the field to display on plot
    save_path : str
        path to save the plot into an image
    is_point_arrow : bool
        to plot a nodal field (point-wise solution required)
    group_names : [str]
        plot is restricted to the group(s) corresponding to this list of group names.


    Returns
    -------
    """
    if group_names is not None:
        meshsol_grp = self.get_group(group_names)
        meshsol_grp.plot_glyph(
            *args,
            label=label,
            index=index,
            indices=indices,
            clim=clim,
            factor=factor,
            field_name=field_name,
            save_path=save_path,
            is_point_arrow=is_point_arrow,
            group_names=None,
        )
    else:

        if save_path is None:
            try:
                import pyvistaqt as pv

                is_pyvistaqt = True
            except:
                import pyvista as pv

                is_pyvistaqt = False
        else:
            import pyvista as pv

            is_pyvistaqt = False

        # Get the mesh
        mesh_pv, field, field_name = self.get_mesh_field_pv(
            *args,
            label=label,
            index=index,
            indices=indices,
            field_name=field_name,
        )

        vect_field = real(field)

        # Compute factor
        if factor is None:
            # factor = 1 / (100 * np_max(vect_field))
            factor = 1 / np_max(vect_field) * 10

        # Add third dimension if needed
        solution = self.get_solution(
            label=label,
            index=index,
        )
        if solution.dimension == 2:
            vect_field = np.hstack((vect_field, np.zeros((vect_field.shape[0], 1))))

        # Add field to mesh
        if is_point_arrow:
            mesh_pv.vectors = vect_field * factor
            arrows_plt = mesh_pv.arrows
        else:
            mesh_pv["field"] = vect_field
            mesh_cell = mesh_pv.point_data_to_cell_data()
            surf = mesh_cell.extract_geometry()
            centers2 = surf.cell_centers()
            centers2.vectors = surf["field"] * factor
            arrows_plt = centers2.arrows

        # Configure plot
        if is_pyvistaqt:
            p = pv.BackgroundPlotter()
            p.set_background("white")
        else:
            pv.set_plot_theme("document")
            p = pv.Plotter(notebook=False)
        p.add_mesh(
            mesh_pv, color="grey", opacity=0.7, show_edges=True, edge_color="white"
        )
        p.set_position((0.2, 0.2, 0.5))
        p.reset_camera()
        p.add_mesh(arrows_plt, color="red")
        p.add_axes()
        # if self.dimension:
        #     p.view_xy()
        if save_path is None and is_show_fig:
            p.show()
        else:
            p.show(interactive=False, screenshot=save_path)
