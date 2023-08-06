import aom_framework.protocols_pb2 as aom_pbs
import aom_framework.services_pb2_grpc as aom_services

import grpc


class Trial:
    def __init__(self, conn, trial, state):
        self.connection = conn
        self.state = state
        self.trial = trial

    def Action(self, user_data):
        update = self.connection.stub.Action(aom_pbs.TrialActionRequest(
            trial_id=self.trial.trial_id, content=user_data.SerializeToString()))
        delta = self.connection.delta_type()
        delta.ParseFromString(update.delta.content)
        return delta

    def End(self):
        self.connection.stub.End(aom_pbs.TrialEndRequest(trial_id=self.trial.trial_id))


class Connection:
    def __init__(self, endpoint, state_type, delta_type):
        channel = grpc.insecure_channel(endpoint)
        self.stub = aom_services.TrialStub(channel)
        self.state_type = state_type
        self.delta_type = delta_type

    def Start(self, init_cfg=None):
        req = aom_pbs.TrialStartRequest()

        if init_cfg:
            req.content = init_cfg.SerializeToString()

        trial = self.stub.Start(req)

        game_state = self.state_type()
        game_state.ParseFromString(trial.env_state.content)
        return Trial(self, trial, game_state)
