from collections import deque
import numpy as np
import random
from simulation.heat_conductor import HeatConductor


class Propagator:
    """
    The Propagator class models the processing of heat diffusion within a 3D domain (cube).
    It initializes the heat at the origin (or a user-defined point) and then propagates this heat outwards to adjacent points
    based on given conditions.

    The class uses the concept of a grid (numpy array) that represents a 3D environment, where each point in the grid
    symbolizes a point in the 3D domain. Heat is diffused from each point to its neighbours in a random direction.

    :param cube_size: An integer representing the edge length of the cube.
    :param origin: A tuple representing the coordinates from which heat propagation starts.
    :param start_temp: An initial temperature at the origin.
    :param end_temp: A final expected temperature at the origin.
    :param increment: A temperature increment at each propagation step.
    :param delay: The number of steps between increments of temperature at the origin.
    :param max_iterations: The maximum number of heat propagation steps to prevent infinite looping.
    :param delta_tolerance: This manages temperature fluctuations within the system for the np.isclose check.
    :param heat_conductor: An instance of the HeatConductor class to handle heat conduction calculations.

    Returns:
        A list of numpy arrays representing the cube's state after each step of the propagation.
        Each state in the list represents the temperatures at all points within the cube after a propagation step.
    """

    def __init__(self, cube_size=4, origin=(0, 0, 0), start_temp=0, end_temp=1, increment=1, delay=1,
                 max_iterations=1E4, delta_tolerance=1E-1, heat_conductor=HeatConductor):
        self.cube_size = cube_size
        self.origin = origin
        self.start_temp = start_temp
        self.end_temp = end_temp
        self.increment = increment
        self.delay = delay
        self.max_iterations = max_iterations
        self.delta_tolerance = delta_tolerance
        self.heat_conductor = heat_conductor

    def propagate(self):
        """
        Method to simulate heat propagation within a 3D cube.

        This method iteratively distributes heat from the origin of the cube to all other positions in a 3D space
        along six fixed directions. The propagation process continues until a specified maximum number of iterations
        or until all positions in the cube reach a near-uniform temperature, within a set tolerance level.

        The state of temperature at all points within the 3D cube is recorded after each step, and these states are
        saved for tracking the heat evolution.

        :return: Returns a list of numpy arrays (cube_states), where each state represents the temperatures at all
        points within the cube after a propagation step.
        """
        # Create a 3D numpy array (cube) filled with the starting temperature of every cell
        cube = np.full((self.cube_size, self.cube_size, self.cube_size), self.start_temp, dtype=float)
        # Initialize a list that will store the state of the cube at each step of the propagation
        cube_states = []

        # Define the possible directions of propagation as unit vectors in 3D space
        directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

        # Initialize a list of deques each containing current points of temperature propagation. Start from the origin.
        propagation_queues = [deque([self.origin])]

        # Increase the temperature at the origin by the defined increment
        cube[self.origin] = self.start_temp + self.increment

        # Initialize the index that keeps track of the number of completed propagation steps
        propagation_index = 0

        # Define the maximum number of iterations to run the propagation loop
        max_iterations = self.max_iterations
        iterations = 0

        while propagation_queues and iterations < max_iterations:

            iterations += 1
            # Increase temperature at origin periodically if origin cube is less than end temp and start new propagation
            if propagation_index % self.delay == 0:
                if cube[self.origin] < self.end_temp:
                    cube[self.origin] += self.increment
                propagation_queues.append(deque([self.origin]))

            # Always add origin to propagation queue when total iterations is less than self.delay
            elif propagation_index < self.delay:
                propagation_queues.append(deque([self.origin]))

            # Clear queues if we get close to the end_temp
            if np.all(np.isclose(cube, self.end_temp, rtol=0, atol=self.delta_tolerance)):
                for queue in propagation_queues:
                    queue.clear()
                break

            # Loop over propagation_queues in reverse order
            for i in reversed(range(len(propagation_queues))):
                # If the queue corresponding to index i is non-empty
                if propagation_queues[i]:
                    # Dequeue a coordinate tuple from the queue and unpack it to x, y, z
                    x, y, z = propagation_queues[i].popleft()

                    # Shuffle the direction list for random propagation direction, otherwise one direction will
                    # receive more energy that others (in this case z direction gets hotter quicker)
                    random.shuffle(directions)

                    # Iterate over each direction
                    for dx, dy, dz in directions:
                        # Compute new coordinates by applying direction deltas
                        nx, ny, nz = x + dx, y + dy, z + dz

                        # If the new position is within the cube and lower temperature than the current point
                        if (0 <= nx < self.cube_size and 0 <= ny < self.cube_size and 0 <= nz < self.cube_size and
                                cube[x, y, z] > cube[nx, ny, nz]):

                            # Calculate the temperature change after heat conduction from heat_conductor
                            diff = self.heat_conductor.calculate_temperature_change(
                                initial_temp=cube[x, y, z], neighbour_temp=cube[nx, ny, nz]
                            )

                            # If temperature difference is less than 0 and new coordinate is not already in queue
                            if diff < 0 and (nx, ny, nz) not in propagation_queues[i]:
                                # Update temperatures of new and current position
                                cube[nx, ny, nz] -= diff
                                cube[x, y, z] += diff
                                # Append new point to propagation queue
                                propagation_queues[i].append((nx, ny, nz))

                            # If temperature difference is greater than or equal to 0 and current position is not
                            # already in queue
                            elif diff >= 0 and (x, y, z) not in propagation_queues[i]:
                                # Update temperatures of new and current position
                                cube[nx, ny, nz] += diff
                                cube[x, y, z] -= diff
                                # Append current point to propagation queue
                                propagation_queues[i].append((x, y, z))

                # If propagation queue is empty up to this point
                if not propagation_queues[i]:
                    # Remove it from the batch of propagation_queues
                    propagation_queues.pop(i)

            # Add the state of the current cube to the cube_states list
            cube_states.append(cube.copy())
            # Increment the propagation index
            propagation_index += 1
        print("Final cube state: ")
        print(cube_states[-1])
        print("Cube states length: ")
        print(len(cube_states))
        return cube_states
