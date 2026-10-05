import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import mujoco
import mujoco.viewer


class SimCommandNode(Node):
    def __init__(self):
        super().__init__('sim_command')

        self.model = mujoco.MjModel.from_xml_path(
            'config/simple_scene.xml'
        )
        self.data = mujoco.MjData(self.model)

        self.command_force = 0.0
        self.step_count = 0

        self.viewer = mujoco.viewer.launch_passive(
            self.model,
            self.data
        )

        self.viewer.cam.distance = 3
        self.viewer.cam.azimuth = 90
        self.viewer.cam.elevation = -20

        self.box_body_id = mujoco.mj_name2id(
            self.model,
            mujoco.mjtObj.mjOBJ_BODY,
            'box'
        )

        self.sim_timer = self.create_timer(
            0.01,
            self.simulation_step
        )

        self.position_publisher = self.create_publisher(
            Float64,
            'robot_position',
            10
        )

        self.subscription = self.create_subscription(
            Float64,
            'robot_command',
            self.command_callback,
            10
        )

        self.get_logger().info('MuJoCo model loaded')
        self.get_logger().info('Simulation command node started')

    def command_callback(self, msg):
        self.command_force = msg.data

        self.get_logger().info(
            f'Received X force command: {msg.data}'
        )

    def simulation_step(self):
        with self.viewer.lock():
            self.data.xfrc_applied[self.box_body_id, 0] = self.command_force

            mujoco.mj_step(self.model, self.data)

            x_position = self.data.xpos[self.box_body_id, 0]
            x_velocity = self.data.qvel[0]

        self.step_count += 1

        if self.step_count % 100 == 0:
            self.get_logger().info(
                f'command={self.command_force:.1f}, '
                f'x={x_position:.4f}, '
                f'vx={x_velocity:.4f}'
            )

        msg = Float64()
        msg.data = x_position

        self.position_publisher.publish(msg)

        self.viewer.sync()


def main(args=None):
    rclpy.init(args=args)

    node = SimCommandNode()

    rclpy.spin(node)

    node.viewer.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()