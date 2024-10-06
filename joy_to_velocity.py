#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyToVelocityNode(Node):
    def __init__(self):
        super().__init__('joy_to_velocity_node')

        # Subscribe to the /joy topic
        self.joy_subscriber = self.create_subscription(Joy, '/joy', self.joy_callback, 10)
        
        # Publisher for /commands/velocity
        self.velocity_publisher = self.create_publisher(Twist, '/commands/velocity', 10)

        # Parameters for scaling joystick input to velocity
        self.declare_parameter('linear_scale', 0.5)
        self.declare_parameter('angular_scale', 1.0)
        
        self.linear_scale = self.get_parameter('linear_scale').value
        self.angular_scale = self.get_parameter('angular_scale').value

        self.get_logger().info('Joy to Velocity Node Initialized')

    def joy_callback(self, joy_msg):
        # Create a new Twist message
        velocity_msg = Twist()

        # Map the joystick axes to linear and angular velocity
        # Assuming left stick Y-axis (index 1) controls linear velocity (forward/backward)
        # Assuming right stick X-axis (index 3) controls angular velocity (left/right)
        velocity_msg.linear.x = self.linear_scale * joy_msg.axes[1]  # Forward/backward
        velocity_msg.angular.z = self.angular_scale * joy_msg.axes[3]  # Left/right rotation

        # Publish the Twist message
        self.velocity_publisher.publish(velocity_msg)

def main(args=None):
    rclpy.init(args=args)
    node = JoyToVelocityNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
