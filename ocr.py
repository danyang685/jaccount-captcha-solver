# a slightly modified ocr.py from pysjtu (onnx version)
from io import BytesIO

import numpy as np
import onnxruntime as rt
from PIL import Image

class IncorrentImageSizeException(Exception):
    pass
class InvalidImageException(Exception):
    pass


class Recognizer:
    """ Base class for Recognizers """
    pass


class NNRecognizer(Recognizer):
    """
    A ResNet-20 based captcha recognizer.

    It feeds the image directly into a pre-trained ResNet-20 model to predict the answer.

    It consumes more memory and computing power than :class:`SVMRecognizer`. The accuracy is around 98%.

    This recognizer requires pytorch and torchvision to work.

    .. note::

        You may set the flag `use_cuda` to speed up predicting, but be aware that it takes time to load the model
        into your GPU and there won't be significant speed-up unless you have a weak CPU.
    """

    def __init__(self, model_file: str = "nn_model.onnx"):
        self._table = [0] * 156 + [1] * 100
        self._sess = rt.InferenceSession(model_file)

    @staticmethod
    def _tensor_to_captcha(tensors):
        captcha = ""
        for tensor in tensors:
            asc = int(np.argmax(tensor, 1))
            if asc < 26:
                captcha += chr(ord("a") + asc)
        return captcha

    def recognize(self, img: bytes):
        """
        Predict the captcha.

        :param img: An PIL Image containing the captcha.
        :return: captcha in plain text.
        """
        try:
            img_rec = Image.open(BytesIO(img))
        except:
            raise InvalidImageException()
        if img_rec.size!=(100,40):
            raise IncorrentImageSizeException()

        img_rec = img_rec.convert("L")
        img_rec = img_rec.point(self._table, "1")
        img_np = np.array(img_rec, dtype=np.float32)
        img_np = np.expand_dims(img_np, 0)
        img_np = np.expand_dims(img_np, 0)

        out_tensor = self._sess.run(None, {self._sess.get_inputs()[0].name: img_np})
        output = NNRecognizer._tensor_to_captcha(out_tensor)
        return output
