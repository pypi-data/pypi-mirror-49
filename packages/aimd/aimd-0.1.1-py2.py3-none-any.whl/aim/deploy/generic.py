

# class DeployFromPath:
#     def __init__(self, model_path):
#         self.model_path = model_path

#     def generate_docker(self, container_name):
#         return True

# import onnxruntime
# import numpy

# deploy_onnx = "/Users/gevorg/repos/sgevorg/aim/.aim/deploy_temp/mnist-test02/mnist-test01.onnx"
# aim_onnx = '/Users/gevorg/repos/sgevorg/aim/.aim/models/test/mnist-test01.onnx'
# test_onnx = '/Users/gevorg/repos/sgevorg/aim/.aim/temp-onnx/mnist-test-6.onnx'

# sess = onnxruntime.InferenceSession(test_onnx)
# input_name = sess.get_inputs()[0].name
# label_name = sess.get_outputs()[0].name

# print(input_name)
# print(label_name)

# X_input = numpy.random.rand(1, 1, 28, 28)

# pred_onx = sess.run([label_name],
#     {input_name: X_input.astype(numpy.float32)})[0]

# print(pred_onx)
