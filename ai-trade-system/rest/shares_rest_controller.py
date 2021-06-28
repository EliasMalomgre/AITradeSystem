from datetime import datetime, timezone
from threading import Thread

from flask import send_file
from flask_restful import Resource, reqparse
from flask_restful import inputs
from tensorflow.keras import backend as K
from tensorflow.python.keras.layers import Activation
from tensorflow.python.keras.utils.generic_utils import get_custom_objects

from ai.agent.agent import Agent
from ai.agent.gradient_agent import GradientAgent
from ai.enviroment.trading_environment import TradingSystem
from ai.learning.policy_gradient.reinforce import Reinforce
from application.stock_puller import StockPuller
from domain.frequency import Frequency
from domain.position import Position
from repositories.transaction_repository import TransactionRepository
from rest.rest_controller import RestController

api = RestController().getAPI()


def softplusk(x):
    """Some implementations use a modified softplus
        to ensure that the stddev is never zero
    Argument:
        x (tensor): activation input
    """
    return K.softplus(x) + 1e-10


# Share related APIs
class UpdateShares(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stock_name', type=str, location='args')
        parser.add_argument('frequency', type=str, location='args')
        args = parser.parse_args()
        sp: StockPuller = StockPuller()
        sp.update_history(args['stock_name'], Frequency(args['frequency']))
        return "Share updated!"


class PullShares(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stock_name', type=str, location='args')
        parser.add_argument('frequency', type=str, location='args')
        parser.add_argument('begin_date', type=inputs.datetime_from_iso8601, location='args')
        parser.add_argument('end_date', type=inputs.datetime_from_iso8601, location='args')
        args = parser.parse_args()

        daysBetween = args['end_date'] - args['begin_date']
        daysBetween = daysBetween.days
        within_last_month = datetime.now(timezone.utc) - args['begin_date']
        within_last_month = within_last_month.days
        if (daysBetween > 7 or daysBetween < 0) and args['frequency'] == "1m":
            return "Error: can only pull 7 days at a time for frequency one minute"
        if (within_last_month > 30) and args['frequency'] == "1m":
            return "Error: can only pull data from within last month for frequency one minute"
        sp: StockPuller = StockPuller()
        sp.pull_data(args['stock_name'], args['begin_date'], args['end_date'], Frequency(args['frequency']))
        return "Pulled data!"


class GetShareInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stock_name', type=str, location='args')
        args = parser.parse_args()
        sp: StockPuller = StockPuller()
        return sp.get_info(args['stock_name'])


# AI related APIs
class StartTraining(Resource):
    def get(self):
        get_custom_objects().update({'softplusk': Activation(softplusk)})
        environment = TradingSystem()
        agent: Agent = GradientAgent(environment, Reinforce(environment))

        thread = Thread(target=agent.train())
        thread.start()
        return "Agent is training"


class StartTrainingAdv(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('stock_name', type=str, location='args')
        parser.add_argument('start_date', type=inputs.datetime_from_iso8601, location='args')
        parser.add_argument('end_date', type=inputs.datetime_from_iso8601, location='args')
        parser.add_argument('frequency', type=str, location='args')
        parser.add_argument('episodes', type=int, location='args')
        parser.add_argument('model_name', type=str, location='args')
        args = parser.parse_args()

        get_custom_objects().update({'softplusk': Activation(softplusk)})
        environment = TradingSystem(args['stock_name'], frequency=Frequency(args['frequency']),
                                    start_date=args['start_date'], end_date=args['end_date'])
        agent: Agent = GradientAgent(environment, Reinforce(environment))

        thread = Thread(target=agent.train())
        thread.start()
        return "Agent is training"


class SendGraph(Resource):
    def get(self):
        return send_file('../plot_images/graph.png', mimetype='image/png')


class CleanPositions(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('skip_amount', type=int, location='args')
        args = parser.parse_args()

        transRepo = TransactionRepository()

        positions = Position.objects()
        counter = 0
        for pos in positions:
            if counter <= args['skip_amount']:
                counter += 1
            else:
                pos.delete()


# Share related APIs
api.add_resource(UpdateShares, '/updateShares')
api.add_resource(PullShares, '/pullShares')
api.add_resource(GetShareInfo, '/getShareInfo')

# AI related APIs
api.add_resource(StartTraining, '/startTraining')
api.add_resource(StartTrainingAdv, '/startTrainingAdv')
api.add_resource(SendGraph, '/sendGraph')

api.add_resource(CleanPositions, '/cleanPositions')
