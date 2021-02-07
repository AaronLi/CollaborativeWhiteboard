import cv2
import torch

from ai_hand.hand_shape_pose.config import cfg
from ai_hand.hand_shape_pose.model.pose_mlp_network import MLPPoseNetwork

config_file = "configs/eval_webcam.yaml"
K = [
    [744.79691291, 0., 294.55017305],
    [0., 747.29652405, 221.87545914],
    [0., 0., 1.]
]
cfg.merge_from_file(config_file)
cfg.freeze()
device = cfg.MODEL.DEVICE
K = torch.tensor(K).to(device)
K = K.reshape((1, 3, 3))


class HandPoseDetector:
    pose_scale = 0.03  # hand pose scale ~3cm
    cropped_dim = (480, 480)  # cropped dimension from the origial webcam image
    resize_dim = (256, 256)  # input image dim accepted by the learning model
    ratio_dim = (cropped_dim[0] / resize_dim[0], cropped_dim[1] / resize_dim[1])
    avg_per_frame = 1  # number of images averaged to help reduce noise

    def __init__(self) -> None:
        super().__init__()

        self.model = MLPPoseNetwork(cfg)
        self.model.to(device)
        self.model.load_model(cfg, load_mlp=True)
        self.model = self.model.eval()
        self.pose_scale = torch.tensor(HandPoseDetector.pose_scale).to(device).reshape((1, 1))

    def detect(self, frame):
        frame = cv2.resize(frame, (HandPoseDetector.resize_dim[1], HandPoseDetector.resize_dim[0]))
        frame = frame.reshape((-1, HandPoseDetector.resize_dim[1], HandPoseDetector.resize_dim[0], 3))
        frame_device = torch.from_numpy(frame).to(device)
        _, est_pose_uv, est_pose_cam_xyz = self.model(frame_device, K, self.pose_scale)
        est_pose_uv = est_pose_uv.to('cpu')
        est_pose_cam_xyz = est_pose_cam_xyz.to('cpu')
        est_pose_uv[0, :, 0] = est_pose_uv[0, :, 0] * HandPoseDetector.ratio_dim[0]
        est_pose_uv[0, :, 1] = est_pose_uv[0, :, 1] * HandPoseDetector.ratio_dim[1]
        est_pose_uv += 25    # manual tuning to fit hand pose on top of the hand
        est_pose_uv[:,1] += 10
        return est_pose_uv.detach().numpy()[0], est_pose_cam_xyz.detach().numpy()[0]