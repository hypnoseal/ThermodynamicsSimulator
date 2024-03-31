# Thermodynamics Simulator

## Introduction

The Thermodynamics Simulator is a project developed as part of my journey to understand physics and learn how to program
physics simulations. It serves as an educational tool for visualizing heat propagation through materials in 3D space.
This simulator is the result of my exploration into both the conceptual and practical aspects of thermodynamics, aiming
to bridge the gap between theoretical physics and applied simulation. It's designed to provide an interactive learning
experience, making complex concepts more accessible and engaging.

## Installation

Before running the project, make sure you have the following packages installed:

* [PyYAML](https://pypi.org/project/PyYAML/)
* [contourpy](https://pypi.org/project/Contourpy/)
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* numpy
* pillow
* cycler
* fonttools
* kiwisolver
* matplotlib
* pip
* pyparsing
* python-dateutil
* six

To install these packages, use pip:

`pip install -r requirements.txt`

Ensure that you have ffmpeg installed, so you can save the video output.

Once these packages are installed, you should be able to run `main.py` to start the simulator.

## Running the Program

Ensure you have installed all necessary python packages (PyYAML, matplotlib, numpy, etc.)

Run the program using:

`python3 main.py`

## Physics Concepts Utilized

The 3D heat simulation application utilizes a centralized propagation model, designed around the core concepts of heat
transfer and thermodynamics. As per these concepts, the models adapt the principles of the three laws of thermodynamics.

### First Law of Thermodynamics - Conservation of Energy

The first law of Thermodynamics, also known as the law of Conservation of Energy, states that energy cannot be created
or destroyed, only transferred or changed from one form to another. This principle is represented in both
propagation and heat conduction models.

#### Propagation Model

In the Propagator class, heat is initiated at a specific origin point and, for each step, is distributed evenly to its
adjacent points. The temperature increase at each step is defined by a specific increment. This process emulates the
transfer of energy but does not create or destroy it, adhering to the First Law of Thermodynamics.

#### Heat Conduction Model

The HeatConductor class calculates the temperature change of a unit (cell) over a given time period. It considers the
physics aspects such as thermal conductivity, specific heat capacity, and density of the material. The heat transferred
to a cell is equal to the heat lost by its neighbors, which again follows the principle of energy conservation. The
model leverage's Fourier's Law of Heat Conduction.

### Second Law of Thermodynamics - Entropy

The second law of Thermodynamics states that the total entropy of an isolated system can never decrease over time, and
is constant if and only if all processes are reversible. Entropy can be seen as a measure of disorder or randomness. In
our simulation, the gradual distribution of heat from a high-temperature point (origin) to other lower-temperature
points increases the randomness of the system, which is analogous to increasing entropy.

### Third Law of Thermodynamics - Absolute Zero

The third law of Thermodynamics states that the entropy of a perfect crystal at absolute zero is exactly equal to zero.
Since the simulation does not deal with absolute zero or crystalline substances, this law doesn't directly apply to the
models. The models, however, do consider the different characteristics of a material, such as specific heat capacity and
thermal conductivity, which would be integral when modeling substances approaching absolute zero temperatures.

## Configuration

The configuration file `config.yaml` allows you to adjust the parameters of the simulation. It contains configuration
parameters for three main sections of the application: `propagator`, `heat_conductor`, and `animator`.

### Propagator Configuration

The `propagator` section controls the main simulation parameters:

* `cube_size`: Size of the cube.
* `origin`: The origin coordinates of the cube.
* `start_temp`: Initial temperature in Kelvin.
* `end_temp`: Final temperature in Kelvin.
* `increment`: Size of temperature increment added to the system in Kelvin.
* `delay`: Delay between temperature increments.
* `max_iterations`: Maximum number of iterations for the simulation to run.
* `delta_tolerance`: Temperature tolerance for Numpy isclose check.

### Heat Conductor Configuration

The `heat_conductor` section controls the parameters related to heat conduction:

* `k`: Thermal conductivity of the material (W/m·K).
* `c_p`: Specific heat capacity of the material (J/kg·K).
* `rho`: Density of the material (kg/m³).
* `min_delta`: Minimum temperature delta to help reduce complexity.
* `conduction_time`: Simulated time in seconds per "time step".
* `delta_x`: Distance between cell centers (m).
* `a`: Cross-sectional area of heat transfer (m²).

### Animator Configuration

The `animator` section controls how the animation is shown:

* `interval`: Interval for updating the plot.

By adjusting these parameters in `config.yaml`, you can control how the simulation is run and even visualize different
materials under the heat conduction model.

## Architecture

### Propagator Class

The `Propagator` class models the heat diffusion within a 3-dimensional domain, represented as a cube. It initializes
the heat at the origin (or a user-defined point) and then propagates this heat outwards to the adjacent points based on
given conditions.

#### Class Definition

The `Propagator` class is initialized with the following parameters:

- `cube_size`: An integer that denotes the edge length of the cube.
- `origin`: A tuple of coordinates from where heat propagation starts.
- `start_temp` : The starting temperature at the origin.
- `end_temp` : The expected final temperature at the origin.
- `increment` : The temperature increment at each step of propagation.
- `delay` : The number of steps between increments of temperature at the origin. This adds a delay to the propagation.
- `max_iterations` : The maximum allowed number of heat propagation steps. This prevents from getting stuck in an
  infinite loop.
- `delta_tolerance` : This parameter manages temperature fluctuations within the system. It is used for
  the `np.isclose()` check.
- `heat_conductor` : An instance of the HeatConductor class to handle the heat conduction calculations.

The `Propagator` class returns a list of numpy arrays representing the state of the cube after each propagation step.

#### propagate() Method

The `propagate()` method simulates the propagation of heat within the cube. It distributes the heat from the cube's
origin to all other positions in the 3-dimensional space along six fixed directions iteratively.

The propagation is done until all positions in the cube reach a near-uniform temperature (within a set tolerance level)
or until maximum number of allowed iterations are completed.

The state of the cube at every propagation step is recorded. These states are then saved enabling the tracking of the
heat evolution.

`propagate()` returns a list of numpy arrays, known as `cube_states`. Each state in `cube_states` represents the
temperatures at all positions within the cube post a propagation step.

### HeatConductor Class

The `HeatConductor` class models the heat conduction process through a material. It calculates the net change in
temperature that a unit (cell) of the material will undergo over a specific time period.

#### Class Definition

The `HeatConductor` class is initialized with the following parameters:

- `k` : Thermal conductivity of the material (W/m·K), a higher value means the material conducts heat faster.
- `c_p` : Specific heat capacity of the material (J/kg·K). This property defines how much heat is needed to change the
  temperature of 1 kg of the material by 1 K.
- `rho` : Density of the material (kg/m³). Alongside with `a` and `delta_x`, it calculates the mass of a cell.
- `min_delta` : The smallest reasonable value for temperature change. If any calculated temperature change is smaller
  than this, it is approximated to zero for computational efficiency.
- `conduction_time` : The timestep over which the heat conduction process is going to be computed (seconds).
- `delta_x` : The spatial length of each cell (m). A smaller value indicates a finer partition and more fine-grained
  computations.
- `a` : Cross-sectional area of the heat path through the cell (m²).

#### calculate_temperature_change() Method

This method calculates the change in the cell temperature caused by heat transfer to or from a neighbouring cell. The
steps it follows are:

- Compute `q`, the rate of heat transfer (J/s) across the cell boundary using Fourier's law.
- Multiply `q` by the duration of conduction to compute `delta_q`, the total heat transferred (J).
- Compute `mass` of the cell considering its size and material properties.
- Calculate the change in temperature (`delta_temp`).

And if the calculated temperature change is smaller than the prescribed smallest discernible value (`min_delta`), it
approximates it to zero to save computational cost.

The method `calculate_temperature_change()` takes as parameters:

- `initial_temp`: Initial temperature of the cell in Kelvin.
- `neighbour_temp`: Temperature of the neighbouring cell in Kelvin.

It returns the change in the cell's temperature due to heat transferred to or from the neighbour cell in Kelvin.

## Contributing

As this is a learning project, contributions in the form of suggestions, bug reports, or pull requests are welcome.

## License

This project is licensed under the MIT License, details of which can be found in `LICENSE.md`.