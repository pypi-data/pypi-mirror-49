#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import glob
import os
import time
from collections import Iterable
from itertools import count
from typing import Type

import gym
import torch

import draugr
from agent import utilities as U
from agent.exceptions.exceptions import NoTrainingProcedure
from agent.interfaces.agent import Agent
from agent.interfaces.specifications import TrainingSession
from agent.training.procedures import train_episodically
from agent.utilities import save_model
from draugr.stopping_key import add_early_stopping_key_combination
from neodroid import NeodroidEnvironment
from neodroid.environments.wrappers import NeodroidGymWrapper
from neodroid.environments.wrappers.vector_environment import VectorEnvironment
from trolls.multiple_environments_wrapper import SubProcessEnvironments, make_gym_env
from trolls.wrappers.vector_environments import VectorWrap
from warg.arguments import config_to_mapping, add_bool_arg

__author__ = 'cnheider'
__doc__ = ''


class linear_training(TrainingSession):

  def __call__(self,
               agent_type : Type[Agent],
               *,
               environment=None,
               save=False,
               has_x_server=False,
               **kwargs):

    kwargs = draugr.NOD(**kwargs)

    if not kwargs.connect_to_running:
      if not environment:
        if '-v' in kwargs.environment_name:
          environment = VectorWrap(NeodroidGymWrapper(gym.make(kwargs.environment_name)))
        else:
          environment = VectorEnvironment(name= kwargs.environment_name,
                                          connect_to_running= kwargs.connect_to_running)
    else:
      environment = VectorEnvironment(name= kwargs.environment_name,
                                      connect_to_running=kwargs.connect_to_running)

    U.set_seeds(kwargs['SEED'])
    environment.seed(kwargs['SEED'])

    agent = agent_type(**kwargs)
    agent.build(environment)

    listener = add_early_stopping_key_combination(agent.stop_training, has_x_server=save)

    if listener:
      listener.start()
    try:
      training_resume = self._training_procedure(agent,
                                                 environment,
                                                 render=kwargs.render_environment,
                                                 **kwargs)
    finally:
      if listener:
        listener.stop()

    if save:
      identifier = count()
      if isinstance(training_resume.models, Iterable):
        for model in training_resume.models:
          U.save_model(model, name=f'{agent.__class__.__name__}-{identifier.__next__()}',**kwargs)
      else:
        U.save_model(training_resume.models,
                     name=f'{agent.__class__.__name__}-{identifier.__next__()}',**kwargs)

      if training_resume.stats:
        training_resume.stats.save(project_name=kwargs.project,
                                   config_name=kwargs.config_name,
                                   directory=kwargs.log_directory)

    environment.close()


class parallelised_training(TrainingSession):
  def __init__(self,
               *,

               environments=None,
               default_num_train_envs=6,
               auto_reset_on_terminal_state=False,
               **kwargs):
    super().__init__(**kwargs)
    self.environments = environments
    self.default_num_train_envs = default_num_train_envs
    self.auto_reset_on_terminal = auto_reset_on_terminal_state

  def __call__(self,
               agent_type : Type[Agent],
               *,
               save=True,
               has_x_server=False,
               **kwargs):

    kwargs = draugr.NOD(**kwargs)

    if not self.environments:
      if '-v' in kwargs.environment_name:

        if self.default_num_train_envs > 0:
          self.environments = [make_gym_env(kwargs.environment_name) for _ in
                               range(self.default_num_train_envs)]
          self.environments = NeodroidGymWrapper(SubProcessEnvironments(self.environments,
                                                                        auto_reset_on_terminal=self.auto_reset_on_terminal))

      else:
        self.environments = VectorEnvironment(name=kwargs.environment_name,
                                              connect_to_running=kwargs.connect_to_running)

    U.set_seeds(kwargs.seed)
    self.environments.seed(kwargs.seed)

    agent = agent_type(**kwargs)
    agent.build(self.environments)

    listener = add_early_stopping_key_combination(agent.stop_training, has_x_server=has_x_server)

    training_start_timestamp = time.time()

    training_resume = None
    if listener:
      listener.start()
    try:
      training_resume = self._training_procedure(agent,
                                                 self.environments,
                                                 **kwargs)
    except KeyboardInterrupt:
      for identifier, model in enumerate(agent.models):
        save_model(model, name=f'{agent}-{identifier}-interrupted',**kwargs)
      exit()
    finally:
      if listener:
        listener.stop()

    time_elapsed = time.time() - training_start_timestamp
    end_message = f'Training done, time elapsed: {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s'
    print(f'\n{"-" * 9} {end_message} {"-" * 9}\n')

    if save and training_resume:
      if isinstance(training_resume.models, Iterable):
        for identifier, model in enumerate(training_resume.models):
          save_model(model,  name=f'{agent}-{identifier}',**kwargs)
      else:
        save_model(training_resume.models,

                   name=f'{agent}-0',**kwargs)

        if 'stats' in training_resume:
          training_resume.stats.save(project_name=kwargs.project,
                                     config_name=kwargs.config_name,
                                     directory=kwargs.log_directory)

    self.environments.close()


class agent_test_gym(TrainingSession):
  def __call__(self, *args, **kwargs):
    '''

  '''

    import agent.configs.agent_test_configs.pg_test_config as C
    from agent.agents.model_free.policy_optimisation.pg_agent import PGAgent

    _environment = gym.make(C.ENVIRONMENT_NAME)
    _environment.seed(C.SEED)

    _list_of_files = glob.glob(str(C.MODEL_DIRECTORY) + '/*.model')
    _latest_model = max(_list_of_files, key=os.path.getctime)

    _agent = PGAgent(C)
    _agent.build(_environment)
    _agent.load(_latest_model, evaluation=True)

    _agent.infer(_environment)


def parse_arguments(desc, C):
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--ENVIRONMENT_NAME",
        "-E",
        type=str,
        default=C.ENVIRONMENT_NAME,
        metavar="ENVIRONMENT_NAME",
        help="Name of the environment to run",
    )
    parser.add_argument(
        "--PRETRAINED_PATH", "-T", metavar="PATH", type=str, default="", help="Path of pre-trained model"
    )
    add_bool_arg(
        parser,
        "render",
        dest="RENDER_ENVIRONMENT",
        default=C.RENDER_ENVIRONMENT,
        help="Rendering of the environment",
    )
    parser.add_argument(
        "--NUM_WORKERS",
        "-N",
        type=int,
        default=6,
        metavar="NUM_WORKERS",
        help="Number of threads for agent (default: 4)",
    )
    add_bool_arg(
        parser,
        "connect_to_running",
        dest="CONNECT_TO_RUNNING",
        default=C.CONNECT_TO_RUNNING,
        help="Connect to already running simulation or start an instance",
    )
    parser.add_argument(
        "--SEED", "-S", type=int, default=C.SEED, metavar="SEED", help=f"Random seed (default: {C.SEED})"
    )
    parser.add_argument(
        "--VERBOSE", "-V", action="store_true", default=C.VERBOSE, help="Enable verbose debug prints"
    )
    add_bool_arg(
        parser,
        "skip",
        dest="SKIP_CONFIRMATION",
        default=True,
        help="Skip confirmation of config to be used",
    )
    parser.add_argument(
        "--ROLLOUTS", "-rollouts", type=int, default=C.ROLLOUTS, metavar="ROLLOUTS", help="Number of rollouts"
    )
    parser.add_argument(
        "--CONFIG",
        "-config",
        type=str,
        default=None,
        metavar="CONFIG",
        help="Path to a config (nullifies all other arguments, if specified)",
    )
    add_bool_arg(parser, "cuda", dest="USE_CUDA", default=C.USE_CUDA, help="Cuda flag")

    args = parser.parse_args()

    return args

def train_agent(agent: Type[Agent],
                config: object,
                *,
                training_session: TrainingSession = linear_training,
                parse_args: bool = True,
                save: bool = True,
                has_x_server: bool = True,
                skip_confirmation: bool = True
                ):
  '''

'''

  if training_session is None:
    raise NoTrainingProcedure
  elif isinstance(training_session, type):
    training_session = training_session(training_procedure=train_episodically)

  if parse_args:
    args = parse_arguments(f'{type(agent)}', config)
    args_dict = args.__dict__

    skip_confirmation = args.SKIP_CONFIRMATION

    #TODo: load earlier model and inference flags

    if 'CONFIG' in args_dict.keys() and args_dict['CONFIG']:
      import importlib.util
      spec = importlib.util.spec_from_file_location('overloaded.config', args_dict['CONFIG'])
      config = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(config)
    else:
      for key, arg in args_dict.items():
        if key != 'CONFIG':
          setattr(config, key, arg)

  if has_x_server:
    display_env = os.getenv('DISPLAY', None)
    if display_env is None:
      config.RENDER_ENVIRONMENT = False
      has_x_server = False

  config_mapping = config_to_mapping(config)

  if not skip_confirmation:
    draugr.sprint(f'\nUsing config: {config}\n', highlight=True, color='yellow')
    for key, arg in config_mapping:
      print(f'{key} = {arg}')

    draugr.sprint(f'\n.. Also save:{save}, has_x_server:{has_x_server}')
    input('\nPress Enter to begin... ')

  try:
    training_session(agent,
                     save=save,
                     has_x_server=has_x_server,
                     **config_mapping)
  except KeyboardInterrupt:
    print('Stopping')

  torch.cuda.empty_cache()


if __name__ == '__main__':
  import agent.configs.agent_test_configs.pg_test_config as C
  from agent.agents.model_free.policy_optimisation.pg_agent import PGAgent

  env = VectorEnvironment(name=C.ENVIRONMENT_NAME,
                                      connect_to_running=C.CONNECT_TO_RUNNING)
  env.seed(C.SEED)

  linear_training(training_procedure=train_episodically)(agent_type=PGAgent, config=C, environment=env)
