# D2 Local Inventory

This directory stores the D2-specific names and local data layout used to adapt BeyondMimic to the D2 robot.

## Copied Assets

D2 robot files were copied from:

```text
/home/dl/wy/barrier_main/D2_smplify
```

to the BeyondMimic extension assets directory:

```text
/home/dl/wy/D2_mimic/whole_body_tracking/source/whole_body_tracking/whole_body_tracking/assets/d2_smplify
```

The copied asset directory currently contains 37 files:

- `D2_QIAOJIE_smplify.urdf`
- `D2_QIAOJIE_smplify.xml`
- 35 STL mesh files

The copied XML/URDF `meshdir` was rewritten to:

```text
/home/dl/wy/D2_mimic/whole_body_tracking/source/whole_body_tracking/whole_body_tracking/assets/d2_smplify/
```

## Copied Motion

The retargeted GMR trajectory was copied from:

```text
/home/dl/wy/GMR/outputs/csv/walk1_subject1.csv
```

to:

```text
/home/dl/wy/D2_mimic/data/gmr_csv/walk1_subject1.csv
```

Shape:

```text
rows: 7839
columns: 36
```

Column layout:

```text
root_pos(3) + root_quat_xyzw(4) + dof_pos(29)
```

The matching GMR pickle was also copied to:

```text
/home/dl/wy/D2_mimic/data/gmr_csv/walk1_subject1.pkl
```

## Copied GMR References

Relevant GMR D2 files were copied under:

```text
/home/dl/wy/D2_mimic/references/gmr
```

Files:

```text
references/gmr/d2_configs/bvh_lafan1_to_d2_smplify.json
references/gmr/d2_configs/bvh_xsens_to_d2_smplify.json
references/gmr/params.py
references/gmr/scripts/batch_gmr_pkl_to_csv.py
references/gmr/scripts/bvh_to_robot.py
references/gmr/scripts/xsens_bvh_to_robot.py
```

## Important Lists

- `d2_joint_order.txt`: expected GMR D2 DoF order, 29 joints.
- `d2_tracking_body_names.txt`: initial body list to use for BeyondMimic motion tracking.

The joint order must be compared against IsaacLab's loaded D2 articulation:

```python
env.scene["robot"].data.joint_names
```

If the order differs, reorder the motion `dof_pos` before `csv_to_npz.py` creates `motion.npz`.

## Still Missing

The copied URDF includes joint effort and velocity limits, but not a complete actuator model for training.

Still needed for a proper D2 BeyondMimic config:

- PD stiffness for each joint or joint group.
- PD damping for each joint or joint group.
- Armature for each joint or joint group.
- Recommended initial standing pose for D2 in IsaacLab.
- Confirmation that IsaacLab imports the URDF with the same joint order as GMR.
- Confirmation that `base_link` is the best anchor body for tracking.
- A D2-specific `robots/d2.py`.
- A D2-specific task config and registration, for example `Tracking-Flat-D2-v0`.
- A `csv_to_npz.py` option to use D2 instead of G1 for forward kinematics.

