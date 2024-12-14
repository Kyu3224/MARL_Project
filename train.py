import yaml
import torch

from pettingzoo.butterfly import pistonball_v6
from supersuit import color_reduction_v0, frame_stack_v1, resize_v1

# Use skrl framework
from skrl.memories.torch import RandomMemory
from skrl.envs.wrappers.torch import wrap_env

# Algorithms
from Algorithms.ppo.ppo_agent import Agent
from Algorithms.ppo.ppo import PPO
from Algorithms.mappo.mappo_agent import Runner

Alg = 'mappo'
# Alg = 'ppo'

with open(f'./Algorithms/{Alg}/{Alg}_config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Hyperparameters for env.
stack_size = config['env']['stack_size']
max_cycles = config['env']['max_cycles']
frame_size = config['env']['frame_size']
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from datetime import datetime

current_time = datetime.now().strftime("%m%d_%H%M")

# Initialize environment
env = pistonball_v6.parallel_env(
    render_mode="rgb_array",
    continuous=False,
    max_cycles=max_cycles
)

env = color_reduction_v0(env)
env = resize_v1(env, frame_size[0], frame_size[1])
env = frame_stack_v1(env, stack_size=stack_size)

if Alg == 'mappo':
    # wrap the env
    # Frame stack 안해서 학습 잘 안될수도
    env = wrap_env(env)
    runner = Runner(env, config)
# Default env is set as PPO
else:
    runner = PPO(env)


runner.run()
