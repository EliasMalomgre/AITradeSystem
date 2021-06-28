from tensorflow.keras import backend as K
from tensorflow.python.keras.layers import Activation
from tensorflow.python.keras.utils.generic_utils import get_custom_objects

from ai.agent.agent import Agent
from ai.agent.gradient_agent import GradientAgent
from ai.enviroment.trading_environment import TradingSystem
from ai.learning.policy_gradient.a2c import A2C


def softplusk(x):
    """Some implementations use a modified softplus
        to ensure that the stddev is never zero
    Argument:
        x (tensor): activation input
    """
    return K.softplus(x) + 1e-10


if __name__ == '__main__':
    get_custom_objects().update({'softplusk': Activation(softplusk)})

    environment = TradingSystem()

    agent: Agent = GradientAgent(environment, A2C(environment))

    agent.train()
