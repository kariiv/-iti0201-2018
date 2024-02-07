class RobotMazer:

    # robot = PiBot()
    # speed = -17
    # slower_speed = -14
    # sensor_reach = 0.159
    # turn_degree = 86

    def __init__(self):
        # self.sensor_from_wall = 0.095
        # self.block_size = 0.3
        # self.robot.set_grabber_height(100)
        # self.robot.close_grabber(100)
        # if self.robot.get_rear_right_side_ir() > self.sensor_reach:
        #     self.map.dirs["E"] = (0, -1)
        #     self.map.dirs["W"] = (0, 1)
        pass

    def wheel_speed(self, left, right):
        """Change both wheel speed."""
        # self.robot.set_left_wheel_speed(left)
        # self.robot.set_right_wheel_speed(right)
        pass

    def last_read(self, degrees):
        """calculate the direction."""
        # return self.robot.get_right_wheel_encoder() * (1 if degrees > 0 else -1)
        pass

    def turn_degrees(self, degrees, speed):
        """Turn robot by given amount of degrees."""
        # wheel_degrees = degrees * self.robot.AXIS_LENGTH / self.robot.WHEEL_DIAMETER
        # right_encoder = self.last_read(degrees) - (wheel_degrees if degrees > 0 else -wheel_degrees)
        # rospy.sleep(0.1)
        # self.wheel_speed(-speed if degrees > 0 else speed, speed if degrees > 0 else -speed)
        # while self.last_read(degrees) > right_encoder:
        #     rospy.sleep(0.02)
        # self.wheel_speed(0, 0)
        pass

    def turn_with_wall(self, right=True):
        """Better turning without encoder."""
        # self.wheel_speed(-self.speed if right else self.speed, self.speed if right else -self.speed)
        # while self.walls()[1]:
        #     rospy.sleep(0.05)
        # self.wheel_speed(-self.slower_speed if right else self.slower_speed,
        #                  self.slower_speed if right else -self.slower_speed)
        # previous = self.robot.get_rear_right_side_ir() if right else self.robot.get_rear_left_side_ir()
        # last = previous
        # rospy.sleep(0.07)
        # while previous >= last:
        #     previous = last
        #     rospy.sleep(0.05)
        #     last = self.robot.get_rear_right_side_ir() if right else self.robot.get_rear_left_side_ir()
        # self.wheel_speed(0, 0)
        pass

    def parallel_to_right_wall(self):
        """Fix robot with right wall."""
        # previous = self.robot.get_rear_left_side_ir()
        # last = previous
        # self.wheel_speed(-self.slower_speed, self.slower_speed)
        # rospy.sleep(0.05)
        # while previous >= last:
        #     previous = last
        #     rospy.sleep(0.05)
        #     last = self.robot.get_rear_left_side_ir()
        # self.wheel_speed(0, 0)
        # rospy.sleep(0.08)
        # previous = self.robot.get_rear_left_side_ir()
        # last = previous
        # self.wheel_speed(self.slower_speed, -self.slower_speed)
        # rospy.sleep(0.05)
        # while previous >= last:
        #     previous = last
        #     rospy.sleep(0.05)
        #     last = self.robot.get_rear_left_side_ir()
        # self.wheel_speed(0, 0)
        pass

    def parallel_to_left_wall(self):
        """Fix robot with left wall."""
        # previous = self.robot.get_rear_right_side_ir()
        # last = previous
        # self.wheel_speed(self.slower_speed, -self.slower_speed)
        # rospy.sleep(0.05)
        # while previous >= last:
        #     previous = last
        #     rospy.sleep(0.05)
        #     last = self.robot.get_rear_right_side_ir()
        # self.wheel_speed(0, 0)
        # rospy.sleep(0.1)
        # previous = self.robot.get_rear_right_side_ir()
        # last = previous
        # self.wheel_speed(-self.slower_speed, self.slower_speed)
        # rospy.sleep(0.05)
        # while previous >= last:
        #     previous = last
        #     rospy.sleep(0.05)
        #     last = self.robot.get_rear_right_side_ir()
        # self.wheel_speed(0, 0)
        # rospy.sleep(0.1)
        pass

    def fix_speed(self):
        """While driving, use diagonal sensors for maneuvering."""
        # fix_speed = 1
        # (l_d, r_d) = self.diagonals()
        # l_d_is = l_d < self.sensor_reach
        # r_d_is = r_d < self.sensor_reach
        # if l_d_is and r_d_is:
        #     if r_d > l_d:
        #         self.wheel_speed(self.speed, self.speed + fix_speed)  # Vasakule
        #     else:
        #         self.wheel_speed(self.speed + fix_speed, self.speed)  # Paremale
        # elif l_d_is:
        #     if l_d < 0.14:
        #         self.wheel_speed(self.speed + fix_speed, self.speed)  # Paremale
        #     else:
        #         self.wheel_speed(self.speed, self.speed + fix_speed)  # Vasakule
        # elif r_d_is:
        #     if r_d < 0.14:
        #         self.wheel_speed(self.speed, self.speed + fix_speed)  # Vasakule
        #     else:
        #         self.wheel_speed(self.speed + fix_speed, self.speed)  # Paremale
        # else:
        #     self.wheel_speed(self.speed, self.speed)
        pass

    def move_forward(self, multi=1):
        """Move robot one block forward."""
        # wheel_degrees = (self.block_size * multi * 2 / self.robot.WHEEL_DIAMETER) * 180 / 3.14
        # last_read = self.robot.get_right_wheel_encoder()
        # right_encoder = last_read - wheel_degrees
        # rospy.sleep(0.08)
        # self.wheel_speed(self.speed, self.speed)
        # while (last_read > right_encoder or self.sensor_reach > self.robot.get_rear_right_straight_ir()) \
        #         and self.robot.get_rear_right_straight_ir() > self.sensor_from_wall:
        #     self.fix_speed()
        #     rospy.sleep(0.03)
        #     last_read = self.robot.get_right_wheel_encoder()
        # self.wheel_speed(0, 0)
        # if self.robot.get_right_wheel_encoder() < right_encoder + wheel_degrees / 3:
        #     self.map.my_pos = self.map.dir_add(self.map.dirs[self.map.facing], 2 * multi)
        #     self.map.set_max_cords()
        # else:
        #     self.check_walls()
        #     print("Wall was too early! Skip position!")
        # walls = self.walls()
        # if walls[0]:
        #     self.parell_to_left_wall()
        # elif walls[2]:
        #     self.parell_to_right_wall()
        pass

    def walls(self) -> tuple:
        """Return triple Left, Center, Right - BOOL values where is wall."""
        return False, False, False

    def diagonals(self) -> tuple:
        """Return triple Left, Center, Right - BOOL values where is wall."""
        # return self.robot.get_rear_right_diagonal_ir(), self.robot.get_rear_left_diagonal_ir()
        return False, False, False

