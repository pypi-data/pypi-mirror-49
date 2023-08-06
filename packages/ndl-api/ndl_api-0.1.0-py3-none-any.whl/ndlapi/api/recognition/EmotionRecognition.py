"""
NeurodataLab LLC 12.04.2019
Created by Andrey Belyaev
"""
import ndlapi.api.recognition.recognition as RC
import ndlapi._pyproto.SingleFrameEmotionService_pb2_grpc as sf_pb2_grpc


class EmotionRecognition(RC.IRecognition):

    def __init__(self, auth):
        super().__init__(auth)
        self.stub = sf_pb2_grpc.SingleFrameEmotionStub(self.channel)

    @staticmethod
    def postprocess_result(result):
        fd_result = result['FaceDetector']['cutted_result']
        er_result = result['SingleFrameEmotionsDetector']

        er_result_balanced = {}
        blob_size = len(er_result[sorted(er_result.keys())[0]])
        for blob_num, blob_info in er_result.items():
            for im_num, faces_info in enumerate(blob_info):
                er_result_balanced[str(int(blob_num) * blob_size + im_num)] = faces_info

        for key in fd_result.keys():
            for n in range(len(fd_result[key])):
                fd_result[key][n]['emotions'] = er_result_balanced[key][n]

        return fd_result
