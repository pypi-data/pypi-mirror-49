# Welcome to TFlex Program about Edge Computing Running on EPU.

## TFlex Program Installation and Usage.
1. Installation: Download from https://pypi.org/project/tflex/ and install

```python
pip install tflex
```
2. Conversion: Convert source model(.pb,.h5,tf.SavedModel) to target model(.tflex graph) running on EPU.

```python
$ tflexconverter -h
Using TensorFlow backend.
usage: tflexconverter [-h] [--keras_model KERAS_MODEL]
                      [--frozen_model FROZEN_MODEL]
                      [--saved_model SAVED_MODEL] [--export_dir EXPORT_DIR]
                      [--input_arrays INPUT_ARRAYS]
                      [--output_arrays OUTPUT_ARRAYS]

Convert source model(.pb,.h5,SavedModel) to target model(.tflex graph)
supported on EPU.

optional arguments:
  -h, --help            show this help message and exit
  --keras_model KERAS_MODEL, -km KERAS_MODEL
                        Source model with .h5 file to be converted.
  --frozen_model FROZEN_MODEL, -fm FROZEN_MODEL
                        Source model with .pb file to be converted.
  --saved_model SAVED_MODEL, -sm SAVED_MODEL
                        Source SavedModel with .pb file and variables to be
                        converted.
  --export_dir EXPORT_DIR, -ed EXPORT_DIR
                        Directory to save the optimized graph(i.e.,model.tflex
                        file will be saved here).
  --input_arrays INPUT_ARRAYS, -i INPUT_ARRAYS
                        String of input node names. If your model has more
                        inputs, please use tflexconverter -i input_1,input_2.
  --output_arrays OUTPUT_ARRAYS, -o OUTPUT_ARRAYS
                        String of output node names. If your model has more
                        outputs, please use tflexconverter -o
                        output_1,output_2.
```

```python
$ tflexconverter -fm tflex/models/mobilenet/mobilenet_v1_1.0_224_frozen.pb \
                 -i input \
                 -o MobilenetV1/Predictions/Reshape_1 \
                 -ed tflex/models/mobilenet/mobilenet.tflex \
                 2>&1 | tee tflex/models/mobilenet/logs/mobilenet.log
```
3. Viewer: Visualization of the network architecture supporting .pb and .tflex file.

```python
$ tflexviewer -h
Using TensorFlow backend.
usage: tflexviewer [-h] --graph GRAPH [--logdir LOGDIR]

Visualization of deep learning models(.pb and .tflex file are supported).

optional arguments:
  -h, --help            show this help message and exit
  --graph GRAPH, -g GRAPH
                        Import protobuf graphDef file (.pb or .tflex) to
                        tensorboard.
  --logdir LOGDIR, -l LOGDIR
                        Log directory specified by user to save tensorboard
                        logs.
```

```python
tflexviewer -g tflex/models/mobilenet/mobilenet.tflex
```

## Partial Pre-trained Models are Available From the Following Website for Testing.
1. TensorFlow Hub: https://www.tensorflow.org/hub
2. TF-Slim: https://github.com/tensorflow/models/tree/master/research/slim
3. TensorFlow Lite Host Models: https://www.tensorflow.org/lite/guide/hosted_models
4. Weights of VGG and ResNet trained with tf.Keras: https://github.com/fchollet/deep-learning-models/releases

## Testing Cases

1. Test Class Converter Method.

```python
import tflex
# test from_session(sess,) method.
converter = tflex.Converter.from_session(sess, input_tensors, output_tensors)
converter._print()  //print graph node information.

# test from_frozen_graph() method.
converter = tflex.Converter.from_frozen_graph("frozen_vgg_19.pb",  ["input"],["vgg_19/fc8/squeezed"])
converter._print()

# test from_keras_model() method.
converter = tflex.Converter.from_keras_model("vgg19.h5")
converter._print()

# test from_saved_model() method.
converter = tflex.Converter.from_saved_model("vgg/")
converter._print()

#  test convert() method.
tflex_graph = converter.convert(export_dir)  // save model.tflex file to specified directory `export_dir` simultaneously.
```

2. Test Module utils method.
```python
import tflex
# test import_graph() method.
graph, input_arrays, output_arrays = tflex.utils.import_graph("model.tflex")

# test get_tensors() method.
input_tensors = tflex.utils.get_tensors(graph, input_arrays)
output_tensors = tflex.utils.get_tensors(graph, output_arrays)
```

3. Test Inference.
```pyhton
python tests/test_inference.py --batch_size=4 --top_n=5
```
