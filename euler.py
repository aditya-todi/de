from math import sin, cos, log, pow, pi, exp
from matplotlib import pyplot as plt


class Euler(object):
    def __init__(self, derivative, x0, y0, curve=None):
        self.derivative = derivative
        self.curve = curve
        self.x0 = x0
        self.y0 = y0

    def eval_equation(self, x, y):
        return eval(self.derivative)

    def run(self, x_final, step_size, optimise=False):
        curr_x = self.x0
        curr_y = self.y0
        x_data = [curr_x]
        y_data = [curr_y]
        flag = False
        avg_derivative = self.eval_equation(curr_x, curr_y)
        curr_range = [1, 2]
        while curr_x < x_final:
            derivative = self.eval_equation(curr_x, curr_y)
            if curr_x + step_size > x_final:
                curr_y += derivative * (x_final - curr_x)
                curr_x = x_final
            else:
                curr_y += derivative * step_size
                curr_x += step_size
            x_data.extend([curr_x])
            y_data.extend([curr_y])
            if optimise:
                if (
                    (max(derivative, -derivative) > avg_derivative)
                    and (not flag)
                    and curr_x > (0.75 * x_final)
                ):
                    step_size = self.optimise_step_size(step_size)
                    print(derivative, avg_derivative, step_size, len(x_data), curr_x)
                    flag = not flag
                if (max(derivative, -derivative) < avg_derivative) and (flag):
                    step_size = self.increase_step_size(step_size)
                    print(derivative, avg_derivative, step_size, len(x_data), curr_x)
                    flag = not flag
            avg_derivative = (
                len(y_data) * avg_derivative + max(derivative, -derivative)
            ) / (len(y_data) + 1)
        return x_data, y_data

    def calculate_error(self, x_data, y_data):
        actual_y = []
        error = []
        for x in x_data:
            actual_y.append(eval(self.curve))
        for y, a_y in zip(y_data, actual_y):
            error.append(max(y - a_y, a_y - y))
        print("max error {}".format(max(error)))
        print("avg error {}".format(sum(error) / len(error)))
        return error, actual_y

    def generate_data(self, x_final, step_size, optimise=False):
        euler_x, euler_y = self.run(x_final, step_size, optimise)
        print("steps : {}".format(len(euler_x)))
        if self.curve != None:
            error, actual_y = self.calculate_error(euler_x, euler_y)
        else:
            error, actual_y = [], []
        de_y = []
        for x in euler_x:
            de_y.append(eval(self.derivative))
        return [euler_x, euler_y, de_y, actual_y, error]

    def compare_errors(self, x_final, step_size):
        print("runing with true")
        true_data = self.generate_data(x_final, step_size, True)
        print("with optimise: {}".format(true_data[1][-1]))
        print("runing with false")
        false_data = self.generate_data(x_final, step_size, False)
        print("without optimise: {}".format(false_data[1][-1]))
        plt.figure(1)
        plt.plot(true_data[0], true_data[1])
        # plt.legend(loc="best")
        plt.figure(2)
        plt.plot(false_data[0], false_data[1], label="False")
        # plt.legend(loc="best")
        plt.figure(3)
        plt.plot(true_data[0], true_data[2])
        plt.plot(true_data[0], true_data[3])
        # plt.legend(loc="best")
        plt.figure(4)
        # plt.plot(true_data[0], true_data[4], label="Optimized")
        plt.plot(false_data[0], false_data[4], label="Error")
        plt.legend(loc="best")
        plt.show()

    @staticmethod
    def optimise_step_size(step_size):
        return max(0.001, 0.5 * step_size)

    @staticmethod
    def increase_step_size(step_size):
        return 2 * step_size
