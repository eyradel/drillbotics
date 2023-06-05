"""
Drill String Module

Calculates Torque and drag and also, buckling
"""
import numpy as np
import math


class DrillString:
    """
    Drill String Model: Represents a drill string instance

    Parameters
    ----------
        - friction_co: Friction coefficient
        - string_force: Force in the drill string in pounds
        - youngs_modulus: Young's modulus of the drill string in psi
        - internal_fluid_pressure: Internal fluid pressure in pipe in psi
        - external_fluid_pressure: External fluid pressure of pipe in psi
        - hole_diameter: Diameter of hole
        - inner_mud_weight: Initial mud weight
        - outer_mud_weight: Final mud weight
        - buoyancy_factor: Buoyancy factor
        - pip_weight: Weight of the drill pipe in pounds
        - pipe_outer_diameter: Outer diameter of pipe
        - pipe_inner_diameter: Inner diameter of pipe
        - more_info: A dictionary containg other info of the drill string such as grade
    """

    def __init__(
        self,
        friction_co,
        string_force: float,
        youngs_modulus,
        internal_fluid_pressure,
        external_fluid_pressure,
        hole_diameter,
        inner_mud_weight,
        outer_mud_weight,
        buoyancy_factor,
        pipe_weight,
        pipe_outer_diameter,
        pipe_inner_diameter,
        more_info={},
    ):
        self.friction_co = friction_co
        self.string_force = (string_force,)
        self.youngs_modulus = youngs_modulus
        self.internal_fluid_pressure = internal_fluid_pressure
        self.external_fluid_pressure = external_fluid_pressure
        self.hole_diameter = hole_diameter
        self.inner_mud_weight = inner_mud_weight
        self.outer_mud_weight = outer_mud_weight
        self.buoyancy_factor = (buoyancy_factor,)
        self.pipe_weight = pipe_weight
        self.pipe_outer_diameter = pipe_outer_diameter
        self.pipe_inner_diameter = pipe_inner_diameter
        self.info = more_info

    def more_info(self):
        """
        Returns a dict with more infomation about drill string
        Connection, Grade, Range, Wall (in), Adjusted Weight (lb/ft), TJ OD (in),
        TJ ID (in), TJ YIELD (ft-lbs), MUT Min (ft-lbs), MUT Max (ft-lbs),
        Prem Tube Tensile (lbs), pipe_weight, pipe_inner_diameter, pipe_outer_diameter

        """
        info = self.info
        info["pipe_weight"] = self.pipe_weight
        info["pipe_inner_diameter"] = self.pipe_inner_diameter
        info["pipe_outer_diameter"] = self.pipe_outer_diameter

        return info

    @property
    def pipe_radius(self):
        return self.pipe_outer_diameter / 2

    @property
    def inertia(self):
        return (math.pi / 64) * (
            self.pipe_outer_diameter**4 - self.pipe_inner_diameter**4
        )

    @property
    def tubing_clearance(self):
        return 0.5 * (self.hole_diameter - self.pipe_outer_diameter)

    @property
    def internal_flow_area(self):
        return math.pi * self.pipe_inner_diameter**2 / 4

    @property
    def external_flow_area(self):
        return math.pi * self.pipe_outer_diameter**2 / 4

    @property
    def buoyed_pipe_weight(self):
        return np.abs(
            self.pipe_weight
            + 0.0408
            * (
                (self.inner_mud_weight * self.pipe_inner_diameter**2)
                - (self.outer_mud_weight * self.pipe_outer_diameter**2)
            )
        )

    def get_drag(
        self, pre_azimuth, curr_azimuth, pre_inclination, curr_inclination, delta_length
    ) -> float:
        """
        Calculates the drag on the drill string

        Parameters
        ----------
            pre_azimuth: Previous in azimuth
            curr_azimuth: Current azimuth
            pre_inclination: Change in inclination
            curr_inclination: Current inclination
            delta_length: Change in length of drill pipe

        Returns
        -------
            value of drag on the drill string
        """

        delta_azi = abs(pre_azimuth - curr_azimuth)
        delta_incli = abs(pre_inclination - curr_inclination)

        # NOTE: Those tuples
        if delta_incli > 0:
            drag_val = self.string_force[
                0
            ] * np.exp(-self.friction_co * abs(curr_azimuth)) + self.buoyancy_factor[
                0
            ] * self.pipe_weight * delta_length * (
                (math.sin(pre_inclination) - math.sin(curr_inclination)) / delta_incli
            )
        else:
            drag_val = 0

        return drag_val

    def get_torque(self, pre_azimuth, curr_azimuth) -> float:
        """
        Calculates torque on drill string

        Parameters
        ----------
            pre_azimuth: Previous azimuth
            curr_azimuth: Current azimuth

        Returns
        -------
            value of torque on drill string
        """

        delta_azimuth = pre_azimuth - curr_azimuth

        torque_val = (
            self.friction_co
            * self.pipe_radius
            * self.string_force[0]
            * abs(curr_azimuth)
        )

        return torque_val

    def _paslay_buckling(self, curr_azimuth) -> float:
        """
        Calculates the paslay buckling on the drill string

        Parameters
        ----------
            curr_azimuth: Current azimuth

        Returns
        -------
            value of buckling on the string
        """
        numerator = (
            self.youngs_modulus
            * self.inertia
            * self.buoyed_pipe_weight
            * np.sin(curr_azimuth)
        )
        denominator = self.pipe_radius
        buckling_val = 2 * np.sqrt(numerator / denominator)

        return buckling_val

    def _buckling_force(self, axial_force):
        """
        Calculates buckling force

        Parameters
        ----------
            axial_force: Axial force

        Returns
        -------
            value of buckling force
        """

        buckling_force_val = (
            -axial_force
            + (self.internal_fluid_pressure * self.internal_flow_area)
            - (self.external_fluid_pressure * self.external_flow_area)
        )

        return buckling_force_val

    def buckling(self, axial_force, curr_azimuth):
        """
        Determines if there's buckling

        Parameters
        ----------
            axial_force: Axial force
            curr_azimuth: current azimuth

        Returns
        -------
            `True` if there's buckling else `False`
        """

        return self._buckling_force(axial_force) < self._paslay_buckling(curr_azimuth)
