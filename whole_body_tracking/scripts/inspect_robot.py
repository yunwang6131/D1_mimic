"""Inspect robot joint and body names loaded by Isaac Lab."""

import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Inspect a robot articulation loaded through Isaac Lab.")
parser.add_argument("--robot", type=str, default="d2", choices=("g1", "d2"), help="Robot model to inspect.")

AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.sim import SimulationContext
from isaaclab.utils import configclass

from whole_body_tracking.robots.d2 import D2_CFG, D2_JOINT_NAMES, D2_TRACKING_BODY_NAMES
from whole_body_tracking.robots.g1 import G1_CYLINDER_CFG

ROBOT_CFGS = {
    "g1": G1_CYLINDER_CFG,
    "d2": D2_CFG,
}

EXPECTED_JOINT_NAMES = {
    "d2": D2_JOINT_NAMES,
}

EXPECTED_BODY_NAMES = {
    "d2": D2_TRACKING_BODY_NAMES,
}


@configclass
class InspectSceneCfg(InteractiveSceneCfg):
    robot: ArticulationCfg = ROBOT_CFGS[args_cli.robot].replace(prim_path="{ENV_REGEX_NS}/Robot")


def _print_list(title: str, values: list[str]) -> None:
    print(f"\n{title} ({len(values)}):")
    for i, value in enumerate(values):
        print(f"{i:02d}: {value}")


def main():
    sim = SimulationContext(sim_utils.SimulationCfg(device=args_cli.device))
    scene = InteractiveScene(InspectSceneCfg(num_envs=1, env_spacing=2.0))
    sim.reset()

    robot = scene["robot"]
    joint_names = list(robot.data.joint_names)
    body_names = list(robot.data.body_names)

    _print_list("Loaded joint_names", joint_names)
    _print_list("Loaded body_names", body_names)

    expected_joints = EXPECTED_JOINT_NAMES.get(args_cli.robot)
    if expected_joints is not None:
        print("\nExpected joint order match:", joint_names == expected_joints)
        if joint_names != expected_joints:
            for i, (loaded, expected) in enumerate(zip(joint_names, expected_joints)):
                if loaded != expected:
                    print(f"First joint mismatch at {i}: loaded={loaded}, expected={expected}")
                    break
            if len(joint_names) != len(expected_joints):
                print(f"Joint count mismatch: loaded={len(joint_names)}, expected={len(expected_joints)}")

    expected_bodies = EXPECTED_BODY_NAMES.get(args_cli.robot)
    if expected_bodies is not None:
        missing_bodies = [name for name in expected_bodies if name not in body_names]
        print("\nExpected tracking bodies present:", not missing_bodies)
        if missing_bodies:
            print("Missing tracking bodies:", missing_bodies)


if __name__ == "__main__":
    main()
    simulation_app.close()
