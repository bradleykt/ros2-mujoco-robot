import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String


class StatusNode(Node):
    def __init__(self):
        super().__init__('status_node')

        self.publisher = self.create_publisher(
            String,
            'robot_status',
            10
        )

        self.command_publisher = self.create_publisher(
            Float64,
            'robot_command',
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_status
        )

        self.get_logger().info('Status node started')

    def publish_status(self):
        msg = String()
        msg.data = 'Robot simulation running'

        self.publisher.publish(msg)

        command = Float64()
        command.data = 1000.0

        self.command_publisher.publish(command)

        self.get_logger().info(
            f'Published status: {msg.data}, command: {command.data}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = StatusNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()