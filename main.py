from utils.config_loader import load_config
from simulation.heat_conductor import HeatConductor
from simulation.propagator import Propagator
from visualization.animator import Animator

CONFIG_PATH = "config.yaml"

config = load_config(CONFIG_PATH)

cube_size = int(config['propagator']['cube_size'])
origin = tuple(config['propagator']['origin'])
start_temp = float(config['propagator']['start_temp'])
end_temp = float(config['propagator']['end_temp'])
increment = float(config['propagator']['increment'])
delay = int(config['propagator']['delay'])
max_iterations = int(float(config['propagator']['max_iterations']))
delta_tolerance = float(config['propagator']['delta_tolerance'])
k = float(config['heat_conductor']['k'])
c_p = float(config['heat_conductor']['c_p'])
rho = float(config['heat_conductor']['rho'])
min_delta = float(config['heat_conductor']['min_delta'])
conduction_time = float(config['heat_conductor']['conduction_time'])
delta_x = float(config['heat_conductor']['delta_x'])
a = float(config['heat_conductor']['a'])

if __name__ == "__main__":
    h = HeatConductor(k=k, c_p=c_p, rho=rho, min_delta=min_delta, conduction_time=conduction_time, delta_x=delta_x, a=a)
    p = Propagator(cube_size=cube_size, origin=origin, start_temp=start_temp, end_temp=end_temp, increment=increment,
                   delay=delay, max_iterations=max_iterations, delta_tolerance=delta_tolerance, heat_conductor=h)
    cube_data = p.propagate()

    a = Animator(cube_data, start_value=start_temp, end_value=end_temp)
    a.plot()
