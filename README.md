# D2 Mimic 训练流程

## 当前数据

项目内已经有一份可用的 D2 GMR CSV：

```text
/home/dl/wy/D2_mimic/data/gmr_csv/walk1_subject1.csv
```

这个 CSV 格式是：

```text
root_pos_x, root_pos_y, root_pos_z,
root_quat_x, root_quat_y, root_quat_z, root_quat_w,
dof_pos...
```

`csv_to_npz.py` 会把 `xyzw` 四元数转换成 IsaacLab 用的 `wxyz`，并生成训练用的 motion npz。

## 安装扩展

用 IsaacLab 的 Python 安装，不要用系统 Python：

```bash
cd /home/dl/wy/D2_mimic/whole_body_tracking

/home/dl/sim/IsaacLab/isaaclab.sh -p -m pip install -e source/whole_body_tracking
```

## CSV 转 NPZ

```bash
cd /home/dl/wy/D2_mimic/whole_body_tracking

/home/dl/sim/IsaacLab/isaaclab.sh -p scripts/csv_to_npz.py \
  --robot d2 \
  --input_file /home/dl/wy/D2_mimic/data/gmr_csv/walk1_subject1.csv \
  --input_fps 30 \
  --output_name d2_walk1_subject1 \
  --output_file /home/dl/wy/D2_mimic/whole_body_tracking/motions/d2_walk1_subject1.npz \
  --headless
```

输出文件：

```text
/home/dl/wy/D2_mimic/whole_body_tracking/motions/d2_walk1_subject1.npz
```

脚本会每 500 帧打印一次进度，保存完成后自动退出。

## 回放检查 NPZ

可视化检查时不要加 `--headless`：

```bash
cd /home/dl/wy/D2_mimic/whole_body_tracking

/home/dl/sim/IsaacLab/isaaclab.sh -p scripts/replay_npz.py \
  --robot d2 \
  --motion_file /home/dl/wy/D2_mimic/whole_body_tracking/motions/d2_walk1_subject1.npz \
  --loop
```

主要检查：

- 脚是否贴近地面。
- base 高度是否正常。
- 左右腿有没有反。
- 关节是否大面积打到 limit。
- 手臂和头部是否抖动。
- body tracking marker 是否在机器人对应 link 附近。

如果 replay 不正常，不要训练，先回到 GMR 或 joint order 修。

## Smoke Train

先跑短训练，确认环境、motion、reward、RSL-RL 配置都能通：

```bash
cd /home/dl/wy/D2_mimic/whole_body_tracking

/home/dl/sim/IsaacLab/isaaclab.sh -p scripts/rsl_rl/train.py \
  --task=Tracking-Flat-D2-v0 \
  --motion_file /home/dl/wy/D2_mimic/whole_body_tracking/motions/d2_walk1_subject1.npz \
  --headless \
  --device cuda:0 \
  --num_envs 64 \
  --max_iterations 100 \
  --logger tensorboard \
  --run_name d2_smoke
```

## 正式训练

Smoke test 通过后再跑正式训练：

```bash
cd /home/dl/wy/D2_mimic/whole_body_tracking

/home/dl/sim/IsaacLab/isaaclab.sh -p scripts/rsl_rl/train.py \
  --task=Tracking-Flat-D2-v0 \
  --motion_file /home/dl/wy/D2_mimic/whole_body_tracking/motions/d2_walk1_subject1.npz \
  --headless \
  --device cuda:0 \
  --logger wandb \
  --log_project_name d2_beyondmimic \
  --run_name d2_motion_test
```

## Play Policy

本地 checkpoint 可以用 `play.py` 加载本地 run。示例：

```bash
cd /home/dl/wy/D2_mimic/whole_body_tracking

/home/dl/sim/IsaacLab/isaaclab.sh -p scripts/rsl_rl/play.py \
  --task=Tracking-Flat-D2-v0 \
  --motion_file /home/dl/wy/D2_mimic/whole_body_tracking/motions/d2_walk1_subject1.npz
  --num_envs 40
```

## 关键风险

最关键的是 joint order。只要 GMR 输出的 `dof_pos` 顺序和 IsaacLab D2 articulation 的 `joint_names` 顺序不一致，训练一定会乱。

D2 的 actuator 参数目前是第一版：

- torque limit
- velocity limit
- PD stiffness
- PD damping
- armature
- joint friction

这些参数会显著影响训练稳定性和策略能否部署。
