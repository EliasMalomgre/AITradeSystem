# from datetime import datetime, timezone
# from flask_restful import inputs
# from flask_restful import Resource, reqparse
#
# from application.stock_puller import StockPuller
# from domain.frequency import Frequency
# from rest.rest_controller import RestController
#
# from tensorflow.keras import backend as K
# from tensorflow.python.keras.layers import Activation
# from tensorflow.python.keras.utils.generic_utils import get_custom_objects
# from ai.agent.agent import Agent
# from ai.agent.gradient_agent import GradientAgent
# from ai.enviroment.trading_environment import TradingSystem
# from ai.learning.policy_gradient.reinforce import Reinforce
#
# api = RestController().getAPI()
#
#
# def softplusk(x):
#     """Some implementations use a modified softplus
#         to ensure that the stddev is never zero
#     Argument:
#         x (tensor): activation input
#     """
#     return K.softplus(x) + 1e-10
#
#
# class StartTraining(Resource):
#     def get(self):
#         get_custom_objects().update({'softplusk': Activation(softplusk)})
#         environment = TradingSystem()
#         agent: Agent = GradientAgent(environment, Reinforce(environment))
#         agent.train()
#         return "Agent is training"
#
# class Test(Resource):
#     def get(self):
#         return "TEST SUCCEEDED"
#
# api.add_resource(StartTraining, '/startTraining')
# api.add_resource(Test, '/test')
