"""Configuration for the Dolang D2 humanoid robot."""

from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

from whole_body_tracking.assets import ASSET_DIR

D2_JOINT_NAMES = [
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "truck_joint",
    "neck_joint",
    "head_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_pitch_joint",
    "left_elbow_yaw_joint",
    "left_wrist_pitch_joint",
    "left_wrist_roll_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_pitch_joint",
    "right_elbow_yaw_joint",
    "right_wrist_pitch_joint",
    "right_wrist_roll_joint",
]

D2_TRACKING_BODY_NAMES = [
    "base_link",
    "left_hip_yaw_link",
    "left_knee_link",
    "left_ankle_roll_link",
    "right_hip_yaw_link",
    "right_knee_link",
    "right_ankle_roll_link",
    "truck_link",
    "head_link",
    "left_shoulder_yaw_link",
    "left_elbow_yaw_link",
    "left_wrist_pitch_link",
    "right_shoulder_yaw_link",
    "right_elbow_yaw_link",
    "right_wrist_pitch_link",
]

D2_LEG_HIP_KNEE_JOINTS = [".*_hip_.*", ".*_knee_joint"]
D2_ANKLE_JOINTS = [".*_ankle_.*"]
D2_TORSO_JOINTS = ["truck_joint"]
D2_HEAD_JOINTS = ["neck_joint", "head_joint"]
D2_SHOULDER_PITCH_ROLL_JOINTS = [".*_shoulder_pitch_joint", ".*_shoulder_roll_joint"]
D2_SHOULDER_YAW_ELBOW_PITCH_JOINTS = [".*_shoulder_yaw_joint", ".*_elbow_pitch_joint"]
D2_ELBOW_YAW_WRIST_JOINTS = [".*_elbow_yaw_joint", ".*_wrist_.*"]


D2_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        fix_base=False,
        merge_fixed_joints=True,
        replace_cylinders_with_capsules=False,
        asset_path=f"{ASSET_DIR}/d2_smplify/D2_QIAOJIE_smplify.urdf",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=0,
        ),
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 1.0),
        joint_pos={
            ".*_hip_pitch_joint": -0.12,
            ".*_hip_roll_joint": 0.0,
            ".*_hip_yaw_joint": 0.0,
            ".*_knee_joint": 0.35,
            ".*_ankle_pitch_joint": -0.18,
            ".*_ankle_roll_joint": 0.0,
            "truck_joint": 0.0,
            "neck_joint": 0.0,
            "head_joint": 0.0,
            ".*_shoulder_pitch_joint": 0.15,
            ".*_shoulder_roll_joint": 0.0,
            ".*_shoulder_yaw_joint": 0.0,
            ".*_elbow_pitch_joint": 0.35,
            ".*_elbow_yaw_joint": 0.0,
            ".*_wrist_pitch_joint": 0.0,
            ".*_wrist_roll_joint": 0.0,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "leg_hip_knee": ImplicitActuatorCfg(
            joint_names_expr=D2_LEG_HIP_KNEE_JOINTS,
            effort_limit_sim=330.0,
            velocity_limit_sim=12.04,
            stiffness=80.0,
            damping=3.0,
            friction=0.0,
        ),
        "ankles": ImplicitActuatorCfg(
            joint_names_expr=D2_ANKLE_JOINTS,
            effort_limit_sim=75.0,
            velocity_limit_sim=11.4,
            stiffness=45.0,
            damping=2.0,
            friction=0.0,
        ),
        "torso": ImplicitActuatorCfg(
            joint_names_expr=D2_TORSO_JOINTS,
            effort_limit_sim=150.0,
            velocity_limit_sim=13.2,
            stiffness=50.0,
            damping=2.5,
            friction=0.0,
        ),
        "head": ImplicitActuatorCfg(
            joint_names_expr=D2_HEAD_JOINTS,
            effort_limit_sim=12.0,
            velocity_limit_sim=21.6,
            stiffness=8.0,
            damping=0.8,
            friction=0.0,
        ),
        "shoulder_pitch_roll": ImplicitActuatorCfg(
            joint_names_expr=D2_SHOULDER_PITCH_ROLL_JOINTS,
            effort_limit_sim=130.0,
            velocity_limit_sim=4.7,
            stiffness=35.0,
            damping=1.5,
            friction=0.0,
        ),
        "shoulder_yaw_elbow_pitch": ImplicitActuatorCfg(
            joint_names_expr=D2_SHOULDER_YAW_ELBOW_PITCH_JOINTS,
            effort_limit_sim=90.0,
            velocity_limit_sim=3.4,
            stiffness=30.0,
            damping=1.3,
            friction=0.0,
        ),
        "elbow_yaw_wrist": ImplicitActuatorCfg(
            joint_names_expr=D2_ELBOW_YAW_WRIST_JOINTS,
            effort_limit_sim=60.0,
            velocity_limit_sim=4.9,
            stiffness=20.0,
            damping=1.0,
            friction=0.0,
        ),
    },
)


def _action_scale_from_actuators(cfg: ArticulationCfg) -> dict[str, float]:
    action_scale = {}
    for actuator in cfg.actuators.values():
        effort = actuator.effort_limit_sim
        stiffness = actuator.stiffness
        names = actuator.joint_names_expr
        if not isinstance(effort, dict):
            effort = {name: effort for name in names}
        if not isinstance(stiffness, dict):
            stiffness = {name: stiffness for name in names}
        for name in names:
            if name in effort and name in stiffness and stiffness[name]:
                action_scale[name] = 0.25 * effort[name] / stiffness[name]
    return action_scale


D2_ACTION_SCALE = _action_scale_from_actuators(D2_CFG)
