from isaaclab.utils import configclass

from whole_body_tracking.robots.d2 import D2_ACTION_SCALE, D2_CFG, D2_TRACKING_BODY_NAMES
from whole_body_tracking.tasks.tracking.config.d2.agents.rsl_rl_ppo_cfg import LOW_FREQ_SCALE
from whole_body_tracking.tasks.tracking.tracking_env_cfg import TrackingEnvCfg


@configclass
class D2FlatEnvCfg(TrackingEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        self.scene.robot = D2_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        self.actions.joint_pos.scale = D2_ACTION_SCALE
        self.commands.motion.anchor_body_name = "base_link"
        self.commands.motion.body_names = D2_TRACKING_BODY_NAMES
        self.events.base_com.params["asset_cfg"].body_names = "truck_link"
        self.rewards.undesired_contacts.params["sensor_cfg"].body_names = [
            r"^(?!left_ankle_roll_link$)(?!right_ankle_roll_link$)(?!left_wrist_pitch_link$)(?!right_wrist_pitch_link$).+$"
        ]
        self.terminations.ee_body_pos.params["body_names"] = [
            "left_ankle_roll_link",
            "right_ankle_roll_link",
            "left_wrist_pitch_link",
            "right_wrist_pitch_link",
        ]


@configclass
class D2FlatWoStateEstimationEnvCfg(D2FlatEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.observations.policy.motion_anchor_pos_b = None
        self.observations.policy.base_lin_vel = None


@configclass
class D2FlatLowFreqEnvCfg(D2FlatEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.decimation = round(self.decimation / LOW_FREQ_SCALE)
        self.rewards.action_rate_l2.weight *= LOW_FREQ_SCALE
