"""
NeurodataLab LLC 12.04.2019
Created by Andrey Belyaev
"""
import ndlapi.api.recognition.recognition as RC
import ndlapi.pyproto.SingleFrameEmotionService_pb2_grpc as sf_pb2_grpc


class EmotionRecognition(RC.IRecognition):

    def __init__(self, auth):
        super().__init__(auth)
        self.stub = sf_pb2_grpc.SingleFrameEmotionStub(self.channel)
