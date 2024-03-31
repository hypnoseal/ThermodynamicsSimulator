class HeatConductor:
    """
    This class models the heat conduction process through a material. It calculates the change in temperature that a
    unit of the material (cell) will undergo over a given time period. We model the material as a 1D lattice of cells
    each having a specific temperature.

    :param min_delta: The smallest discernible temperature change. If the calculated delta_temp is smaller
                      than this, it is approximated to zero to cut computational costs.
    :param k: Thermal conductivity of the material (W/m·K). Higher values mean the material conducts heat faster.
    :param a: Cross-sectional area of the heat path through the cell (m²).
    :param delta_x: Spatial length of each cell (m). Smaller values make computations more precise.
    :param c_p: Specific heat capacity of the material (J/kg·K). It defines how much heat is needed to change
                the temperature of 1 kg of the material by 1 K.
    :param rho: Density of the material (kg/m³). Together with `a` and `delta_x`, it helps compute the mass of a cell.
    :param conduction_time: The timestep over which the heat conduction process will be computed (seconds).
    """
    def __init__(self, k=237, c_p=900, rho=2700, min_delta=1E-5, conduction_time=1, delta_x=1, a=1):
        self.min_delta = min_delta
        self.k = k
        self.a = a
        self.conduction_time = conduction_time
        self.delta_x = delta_x
        self.c_p = c_p
        self.rho = rho

    def calculate_temperature_change(self, initial_temp, neighbour_temp):
        """
        Predicts the change in the cell temperature caused by heat transfer to or from a neighboring cell.

        Steps:

        - Calculate the rate of heat transfer (q) across the cell boundary by Fourier's law.
        - Multiply q by the time duration to get the total heat transferred (delta_q).
        - Compute the mass of the cell based on its size and material properties.
        - Use the formula for heat energy to compute the change in temperature.

        :param initial_temp: Initial temperature of the cell (K).
        :param neighbour_temp: Temperature of the neighboring cell (K).
        :return: The change in the cell's temperature due to heat transferred to or from the neighbor cell (K).
        """
        # Calculate heat transferred rate (J/s)
        q = -self.k * self.a * (initial_temp - neighbour_temp) / self.delta_x

        # Calculate the total heat transferred over the time duration (J)
        delta_q = q * self.conduction_time

        # Calculate the mass of the cell (kg)
        mass = self.rho * self.a * self.delta_x

        # Calculate the temperature change (K)
        delta_temp = delta_q / (mass * self.c_p)

        # If the change is too small, it's approximated to 0 to simplify computations
        if abs(delta_temp) < self.min_delta:
            return 0
        else:
            return delta_temp
