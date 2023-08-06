import numpy as np
import cv2
import os.path as osp
from skimage import transform
import time

try:
    import onnx
    import tensorrt as trt
    from onnx import TensorProto
    import torch
    from torch2trt.torch2trt import TRTModule
except ModuleNotFoundError as e:
    print(f"warning not fount module {e}")


class FaceDetection(object):
    def __init__(self, threshold=0.4, nms_thresh=0.3, targetId=cv2.dnn.DNN_TARGET_CPU):
        onnx_path = osp.join(osp.dirname(__file__), "centerface.onnx")
        self.net = cv2.dnn.readNetFromONNX(onnx_path)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.img_h_new, self.img_w_new, self.scale_h, self.scale_w = 0, 0, 0, 0
        self.threshold = threshold
        self.nms_thresh = nms_thresh

    def __call__(self, bgr_img, showresult=False):
        height, width = bgr_img.shape[:2]
        self.img_h_new, self.img_w_new, self.scale_h, self.scale_w = self.transform(height, width)
        dets, lms = self.inference_opencv(bgr_img)
        if showresult:
            for det in dets:
                boxes, score = det[:4], det[4]
                cv2.rectangle(bgr_img, (int(boxes[0]), int(boxes[1])), (int(boxes[2]), int(boxes[3])), (2, 255, 0), 1)
            for lm in lms:
                for i in range(0, 5):
                    cv2.circle(bgr_img, (int(lm[i * 2]), int(lm[i * 2 + 1])), 2, (0, 0, 255), -1)
            cv2.imshow('detection result', bgr_img)
            cv2.waitKey(0)
        return dets, lms

    def detect_face(self, bgr_img, align=False):
        height, width = bgr_img.shape[:2]
        self.img_h_new, self.img_w_new, self.scale_h, self.scale_w = self.transform(height, width)
        dets, lms = self.inference_opencv(bgr_img)
        if align:
            face_bgr_list = [self._align(bgr_img, b) for b, lm in zip(dets, lms)]
        else:
            face_bgr_list = [bgr_img[int(b[1]):int(b[3]), int(b[0]):int(b[2]), :] for b in dets]

        return face_bgr_list, dets, lms

    def _align(self, img, bbox=None, landmark=None, image_size=(112, 112), **kwargs):
        M = None
        # landmark = landmark.reshape(5, 2)
        if landmark is not None:
            src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041]], dtype=np.float32)
            if image_size[1] == 112:
                src[:, 0] += 8.0
            dst = landmark.astype(np.float32)

            tform = transform.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2, :]

        if M is None:
            if bbox is None:  # use center crop
                det = np.zeros(4, dtype=np.int32)
                det[0] = int(img.shape[1] * 0.0625)
                det[1] = int(img.shape[0] * 0.0625)
                det[2] = img.shape[1] - det[0]
                det[3] = img.shape[0] - det[1]
            else:
                det = bbox
            margin = kwargs.get('margin', 44)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2, 0)
            bb[1] = np.maximum(det[1] - margin / 2, 0)
            bb[2] = np.minimum(det[2] + margin / 2, img.shape[1])
            bb[3] = np.minimum(det[3] + margin / 2, img.shape[0])
            ret = img[bb[1]:bb[3], bb[0]:bb[2], :]
            if len(image_size) > 0:
                ret = cv2.resize(ret, (image_size[1], image_size[0]))
            return ret
        else:  # do align using landmark
            assert len(image_size) == 2

            warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)
            return warped

    def demo(self):
        test_image_path = osp.join(osp.dirname(__file__), "test.jpg")
        bgr_image = cv2.imread(test_image_path)
        self.__call__(bgr_image, showresult=True)

    def inference_opencv(self, img):
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0,
                                     size=(self.img_w_new, self.img_h_new),
                                     mean=(0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        heatmap, scale, offset, lms = self.net.forward(["537", "538", "539", '540'])
        print(scale[0, 0, 0, :20])
        return self.postprocess(heatmap, lms, offset, scale)

    def transform(self, h, w):
        img_h_new, img_w_new = int(np.ceil(h / 32) * 32), int(np.ceil(w / 32) * 32)
        print(img_h_new, img_w_new)
        scale_h, scale_w = img_h_new / h, img_w_new / w
        return img_h_new, img_w_new, scale_h, scale_w

    def postprocess(self, heatmap, lms, offset, scale):
        dets, lms = self.decode(heatmap, scale, offset, lms, (self.img_h_new, self.img_w_new),
                                threshold=self.threshold, nms_thresh=self.nms_thresh)
        if len(dets) > 0:
            dets[:, 0:4:2], dets[:, 1:4:2] = dets[:, 0:4:2] / self.scale_w, dets[:, 1:4:2] / self.scale_h
            lms[:, 0:10:2], lms[:, 1:10:2] = lms[:, 0:10:2] / self.scale_w, lms[:, 1:10:2] / self.scale_h
        else:
            dets = np.empty(shape=[0, 5], dtype=np.float32)
            lms = np.empty(shape=[0, 10], dtype=np.float32)

        return dets, lms

    def decode(self, heatmap, scale, offset, landmark, size, threshold=0.1, nms_thresh=0.3):
        heatmap = np.squeeze(heatmap)
        scale0, scale1 = scale[0, 0, :, :], scale[0, 1, :, :]
        offset0, offset1 = offset[0, 0, :, :], offset[0, 1, :, :]
        c0, c1 = np.where(heatmap > threshold)
        boxes, lms = [], []

        if len(c0) > 0:
            for i in range(len(c0)):
                s0, s1 = np.exp(scale0[c0[i], c1[i]]) * 4, np.exp(scale1[c0[i], c1[i]]) * 4
                o0, o1 = offset0[c0[i], c1[i]], offset1[c0[i], c1[i]]
                s = heatmap[c0[i], c1[i]]
                x1, y1 = max(0, (c1[i] + o1 + 0.5) * 4 - s1 / 2), max(0, (c0[i] + o0 + 0.5) * 4 - s0 / 2)
                x1, y1 = min(x1, size[1]), min(y1, size[0])
                boxes.append([x1, y1, min(x1 + s1, size[1]), min(y1 + s0, size[0]), s])
                lm = []
                for j in range(5):
                    lm.append(landmark[0, j * 2 + 1, c0[i], c1[i]] * s1 + x1)
                    lm.append(landmark[0, j * 2, c0[i], c1[i]] * s0 + y1)
                lms.append(lm)
            boxes = np.asarray(boxes, dtype=np.float32)
            keep = self.nms(boxes[:, :4], boxes[:, 4], nms_thresh)

            boxes = boxes[keep, :]
            lms = np.asarray(lms, dtype=np.float32)
            lms = lms[keep, :]
        return boxes, lms

    def nms(self, boxes, scores, nms_thresh):
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = np.argsort(scores)[::-1]
        num_detections = boxes.shape[0]
        suppressed = np.zeros((num_detections,), dtype=np.bool)

        keep = []
        for _i in range(num_detections):
            i = order[_i]
            if suppressed[i]:
                continue
            keep.append(i)

            ix1 = x1[i]
            iy1 = y1[i]
            ix2 = x2[i]
            iy2 = y2[i]
            iarea = areas[i]

            for _j in range(_i + 1, num_detections):
                j = order[_j]
                if suppressed[j]:
                    continue

                xx1 = max(ix1, x1[j])
                yy1 = max(iy1, y1[j])
                xx2 = min(ix2, x2[j])
                yy2 = min(iy2, y2[j])
                w = max(0, xx2 - xx1 + 1)
                h = max(0, yy2 - yy1 + 1)

                inter = w * h
                ovr = inter / (iarea + areas[j] - inter)
                if ovr >= nms_thresh:
                    suppressed[j] = True

        return keep


class FaceDetectionTRT(object):
    def __init__(self, threshold=0.4, nms_threshold=0.3, inputsize=(800, 480)):
        self.ori_onnx_path = osp.join(osp.dirname(__file__), "centerface.onnx")
        self.onnx_path = self.ori_onnx_path.replace(".onnx", f"{inputsize[0]}_{inputsize[1]}.onnx")
        self.trt_path = self.onnx_path.replace(".onnx", ".trt")
        if self._convert_trt() is False:
            raise Exception("convert_trt error")

        trt_log = trt.Logger(trt.Logger.WARNING)

        with open(self.trt_path, 'rb') as fp:
            fs = fp.read()
        with trt.Runtime(trt_log) as runtime:
            engine = runtime.deserialize_cuda_engine(fs)

        self.model = TRTModule(engine=engine).cuda()
        self.model.input_names = ["input.1"]
        self.model.output_names = ["537", "538", "539", "540"]

        self.input_shapes = []
        self.output_shapes = []
        for binding in engine:
            if engine.binding_is_input(binding):
                self.input_shapes.append(tuple([engine.max_batch_size] + list(engine.get_binding_shape(binding))))
            else:
                self.output_shapes.append(tuple([engine.max_batch_size] + list(engine.get_binding_shape(binding))))

        if len(self.input_shapes) != 1:
            print('Only one input data is supported.')

        self.input_shape = self.input_shapes[0]
        self.input_channel = self.input_shape[1]
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

        self.threshold = threshold    # 检测分数阈值,越大错检越少,漏检越多
        self.nms_threshold = nms_threshold   # nms阈值,越小重复框越少

    def __call__(self, input_image_bgrs, showresult=False):
        """
        input image_rgb list detect face from each image
        :param input_image_bgrs: input image_list or one image
        :param showresult: if show result image
        :return:
            coordinations: boxes, [[[x1,y1,x2,y2], [x1,y1,x2,y2]],   # image1 result face boxes
                                   [[x1,y1,x2,y2],[x1,y1,x2,y2], [x1,y1,x2,y2]],  # image2 result face boxes
                                   ... # imageN result face boxes, if not found any face in this image, it will be []
                                  ]
            scores, [s1, s2, s3, ...]
        """
        if isinstance(input_image_bgrs, (list, tuple)):
            image_rgb_list = [bgr[..., ::-1] for bgr in input_image_bgrs]
        else:
            image_rgb_list = [input_image_bgrs[..., ::-1]]

        input_batch_tensor, resize_scale = self.imagelist2batch(image_rgb_list)

        heatmap, scale, offset, landmarks = self.model(input_batch_tensor.cuda())

        heatmap = heatmap.cpu().numpy()
        scale = scale.cpu().numpy()
        offset = offset.cpu().numpy()
        landmarks = landmarks.cpu().numpy()

        all_boxes, all_scores, all_landmarks = self.postprocess(heatmap, landmarks, offset, scale, resize_scale=resize_scale)

        if showresult is True:
            colors_hp = [(0, 0, 255), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 0)]
            for image_rgb, boxes, scores, landmarks in zip(image_rgb_list, all_boxes, all_scores, all_landmarks):
                img_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                image_h, image_w, _ = image_rgb.shape

                for box, land_mark in zip(boxes, landmarks):
                    cv2.rectangle(img_bgr, (box[0], box[1]), (box[2], box[3]), color=(0, 0, 255), thickness=3)
                    for color_index, point in enumerate(land_mark):
                        cv2.circle(img_bgr, (point[0], point[1]), 3, colors_hp[color_index], -1)

                cv2.imshow("test", img_bgr)
                cv2.waitKey()

        if isinstance(input_image_bgrs, (list, tuple)):
            return all_boxes, all_scores
        else:
            return all_boxes[0], all_scores[0]

    def detect_face(self, input_image_bgrs, align=False):
        if isinstance(input_image_bgrs, (list, tuple)):
            image_rgb_list = [bgr[..., ::-1] for bgr in input_image_bgrs]
        else:
            image_rgb_list = [input_image_bgrs[..., ::-1]]

        input_batch_tensor, resize_scale = self.imagelist2batch(image_rgb_list)

        heatmap, scale, offset, landmarks = self.model(input_batch_tensor.cuda())

        heatmap = heatmap.cpu().numpy()
        scale = scale.cpu().numpy()
        offset = offset.cpu().numpy()
        landmarks = landmarks.cpu().numpy()

        all_boxes, all_scores, all_landmarks = self.postprocess(heatmap, landmarks, offset, scale, resize_scale=resize_scale)
        all_face_bgr_list = []

        if isinstance(input_image_bgrs, (list, tuple)):
            if align:
                for bgr_img, boxes, landmarks in zip(input_image_bgrs, all_boxes, all_landmarks):
                    face_bgr_list = [self._align(bgr_img, b) for b, lm in zip(boxes, landmarks)]
                    all_face_bgr_list.append(face_bgr_list)
            else:
                for bgr_img, boxes in zip(input_image_bgrs, all_boxes):
                    face_bgr_list = [bgr_img[int(b[1]):int(b[3]), int(b[0]):int(b[2]), :] for b in boxes]
                    all_face_bgr_list.append(face_bgr_list)
            return all_face_bgr_list, all_scores, all_landmarks
        else:
            input_image_bgrs = [input_image_bgrs]
            if align:
                for bgr_img, boxes, landmarks in zip(input_image_bgrs, all_boxes, all_landmarks):
                    face_bgr_list = [self._align(bgr_img, b) for b, lm in zip(boxes, landmarks)]
                    all_face_bgr_list.append(face_bgr_list)
            else:
                for bgr_img, boxes in zip(input_image_bgrs, all_boxes):
                    face_bgr_list = [bgr_img[int(b[1]):int(b[3]), int(b[0]):int(b[2]), :] for b in boxes]
                    all_face_bgr_list.append(face_bgr_list)

            return all_face_bgr_list[0], all_scores[0], all_landmarks[0]

    def _align(self, img, bbox=None, landmark=None, image_size=(112, 112), **kwargs):
        M = None
        # landmark = landmark.reshape(5, 2)
        if landmark is not None:
            src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041]], dtype=np.float32)
            if image_size[1] == 112:
                src[:, 0] += 8.0
            dst = landmark.astype(np.float32)

            tform = transform.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2, :]

        if M is None:
            if bbox is None:  # use center crop
                det = np.zeros(4, dtype=np.int32)
                det[0] = int(img.shape[1] * 0.0625)
                det[1] = int(img.shape[0] * 0.0625)
                det[2] = img.shape[1] - det[0]
                det[3] = img.shape[0] - det[1]
            else:
                det = bbox
            margin = kwargs.get('margin', 44)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2, 0)
            bb[1] = np.maximum(det[1] - margin / 2, 0)
            bb[2] = np.minimum(det[2] + margin / 2, img.shape[1])
            bb[3] = np.minimum(det[3] + margin / 2, img.shape[0])
            ret = img[bb[1]:bb[3], bb[0]:bb[2], :]
            if len(image_size) > 0:
                ret = cv2.resize(ret, (image_size[1], image_size[0]))
            return ret
        else:  # do align using landmark
            assert len(image_size) == 2

            warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)
            return warped

    def postprocess(self, heatmap, landmark, offset, scale, resize_scale):
        """

        :param heatmap:   N  *  1 * 120 * 200
        :param landmark:  N  * 10 * 120 * 200
        :param offset:    N  *  2 * 120 * 200
        :param scale:     N  *  2 * 120 * 200
        :param resize_scale:
        :return:
        """
        all_boxes = []
        all_lms = []
        all_scores = []
        for one_heatmap, one_landmark, one_offset, one_scale, one_resize_scale in zip(heatmap, landmark, offset, scale, resize_scale):
            one_heatmap = np.squeeze(one_heatmap)
            scale0, scale1 = one_scale[0, :, :], one_scale[1, :, :]
            offset0, offset1 = one_offset[0, :, :], one_offset[1, :, :]
            x_indexs, y_indexs = np.where(one_heatmap > self.threshold)
            boxes, lms = [], []
            scores = []

            for x_index, y_index in zip(x_indexs, y_indexs):
                s0, s1 = np.exp(scale0[x_index, y_index]) * 4, np.exp(scale1[x_index, y_index]) * 4
                o0, o1 = offset0[x_index, y_index], offset1[x_index, y_index]
                s = one_heatmap[x_index, y_index]
                x1, y1 = max(0, (y_index + o1 + 0.5) * 4 - s1 / 2), max(0, (x_index + o0 + 0.5) * 4 - s0 / 2)
                x1, y1 = min(x1, self.input_width), min(y1, self.input_height)
                boxes.append(
                    [int(x1), int(y1), int(min(x1 + s1, self.input_width)), int(min(y1 + s0, self.input_height))])
                scores.append(float(s))
                lm = []
                for j in range(5):
                    lm.append(one_landmark[j * 2 + 1, x_index, y_index] * s1 + x1)
                    lm.append(one_landmark[j * 2, x_index, y_index] * s0 + y1)
                lms.append(lm)

            if boxes:
                keep = cv2.dnn.NMSBoxes(boxes, scores, score_threshold=self.threshold, nms_threshold=self.nms_threshold)
                keep = keep.flatten().tolist()
                boxes = np.asarray(boxes, dtype=np.float32)[keep, :]
                scores = np.asarray(scores, dtype=np.float32)[keep].reshape((-1))
                lms = np.asarray(lms, dtype=np.float32)
                lms = lms[keep, :]

                boxes = boxes / one_resize_scale
                lms = lms / one_resize_scale
                all_boxes.append(boxes.astype(np.int))
                all_scores.append(scores)
                # all_lms.append(lms.astype(np.int))
                all_lms.append(lms.astype(np.int).reshape((-1, 5, 2)))
            else:
                all_boxes.append([])
                all_scores.append([])
                all_lms.append([])

        return all_boxes, all_scores, all_lms

    def fix_box(self, boxes, max_w, max_h):
        """
        adjust target rectangular'box into square'box
        """
        for one_box in boxes:
            diff = (one_box[3] - one_box[1]) - (one_box[2] - one_box[0])
            if diff > 0:
                one_box[0] -= diff // 2
                one_box[2] += diff - (diff // 2)
                one_box[0] = max(one_box[0], 0)
                one_box[2] = min(one_box[2], max_w)
            elif diff < 0:
                one_box[1] += diff // 2
                one_box[3] -= diff - (diff // 2)
                one_box[1] = max(one_box[1], 0)
                one_box[3] = min(one_box[3], max_h)

        return boxes

    def imagelist2batch(self, img_list):
        n = len(img_list)
        input_batch = np.zeros((n, self.input_height, self.input_width, self.input_channel), dtype=np.uint8)
        resize_scale = []
        for index, image_rgb in enumerate(img_list):
            image_h, image_w, image_c = image_rgb.shape
            if image_h / image_w > self.input_height / self.input_width:
                one_resize_scale = self.input_height / image_h
                input_image = cv2.resize(image_rgb, (0, 0), fx=one_resize_scale, fy=one_resize_scale)
                input_batch[index, :, 0:input_image.shape[1], :] = input_image
            else:
                one_resize_scale = self.input_width / image_w
                input_image = cv2.resize(image_rgb, (0, 0), fx=one_resize_scale, fy=one_resize_scale)
                input_batch[index, 0:input_image.shape[0], :, :] = input_image
            resize_scale.append(one_resize_scale)

        input_batch = input_batch.transpose([0, 3, 1, 2])
        input_batch = np.array(input_batch, dtype=np.float32, order='C')
        input_batch_tensor = torch.Tensor(input_batch)

        return input_batch_tensor, resize_scale

    def _modify_onnx_inputsize(self, output_onnx_path, input_size=(800, 480)):
        w, h = input_size
        onnx_model = onnx.load(self.ori_onnx_path)
        graph = onnx_model.graph

        input0 = graph.input[0]
        new_input0 = onnx.helper.make_tensor_value_info("input.1", TensorProto.FLOAT, (1, 3, h, w))
        graph.input.remove(input0)
        graph.input.insert(0, new_input0)

        output0 = graph.output[0]
        new_output0 = onnx.helper.make_tensor_value_info("537", TensorProto.FLOAT, (1, 1, h//4, w//4))
        graph.output.remove(output0)
        graph.output.insert(0, new_output0)

        output1 = graph.output[1]
        new_output1 = onnx.helper.make_tensor_value_info("538", TensorProto.FLOAT, (1, 2, h//4, w//4))
        graph.output.remove(output1)
        graph.output.insert(1, new_output1)

        output2 = graph.output[2]
        new_output2 = onnx.helper.make_tensor_value_info("539", TensorProto.FLOAT, (1, 2, h//4, w//4))
        graph.output.remove(output2)
        graph.output.insert(2, new_output2)

        output3 = graph.output[3]
        new_output3 = onnx.helper.make_tensor_value_info("540", TensorProto.FLOAT, (1, 10, h//4, w//4))
        graph.output.remove(output3)
        graph.output.insert(3, new_output3)

        onnx.save(onnx_model, output_onnx_path)

    def _convert_trt(self, batchsize=8, force=False, inputsize=(800, 480)):
        self._modify_onnx_inputsize(self.onnx_path, inputsize)
        if osp.exists(self.trt_path) and not force:
            return True

        TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
        builder = trt.Builder(TRT_LOGGER)

        # get network object via builder
        network = builder.create_network()

        # create ONNX parser object
        parser = trt.OnnxParser(network, TRT_LOGGER)

        with open(self.onnx_path, 'rb') as onnx_fin:
            parser.parse(onnx_fin.read())

        # print possible errors
        num_error = parser.num_errors
        if num_error != 0:
            for i in range(num_error):
                temp_error = parser.get_error(i)
                print(temp_error.desc())

        # create engine via builder
        builder.max_batch_size = batchsize
        builder.average_find_iterations = 2
        builder.max_workspace_size = 1 << 30   # 1G
        builder.fp16_mode = False

        engine = builder.build_cuda_engine(network)

        with open(self.trt_path, 'wb') as fout:
            fout.write(engine.serialize())

        if osp.exists(self.trt_path):
            return True
        else:
            return False

    def demo(self):
        test_image_path = osp.join(osp.dirname(__file__), "test.jpg")
        bgr_image = cv2.imread(test_image_path)
        self.__call__(bgr_image, showresult=True)


if __name__ == "__main__":
    import time
    frame = cv2.imread('test.jpg')
    centerface = FaceDetection()
    st = time.time()
    centerface(frame, showresult=True)
    print(time.time() - st)
