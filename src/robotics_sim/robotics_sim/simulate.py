import time

import mujoco
import mujoco.viewer


MODEL_PATH = "config/simple_scene.xml"


model = mujoco.MjModel.from_xml_path(MODEL_PATH)
data = mujoco.MjData(model)


with mujoco.viewer.launch_passive(model, data) as viewer:
    viewer.cam.distance = 3
    viewer.cam.azimuth = 115
    viewer.cam.elevation = -20

    while viewer.is_running():
        mujoco.mj_step(model, data)
        viewer.sync()
        time.sleep(0.002)