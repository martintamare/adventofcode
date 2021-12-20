#!/usr/bin/env python

test_data = {
        'x_min': 20,
        'x_max': 30,
        'y_min':-10,
        'y_max':-5
}

prod_data = {
        'x_min': 85,
        'x_max': 145,
        'y_min':-163,
        'y_max':-108
}

part2_test = [
(23,-10), (25,-9), (27,-5), (29,-6), (22,-6), (21,-7), (9,0), (27,-7), (24,-5),
(25,-7), (26,-6), (25,-5), (6,8), (11,-2), (20,-5), (29,-10), (6,3), (28,-7),
(8,0), (30,-6), (29,-8), (20,-10), (6,7), (6,4), (6,1), (14,-4), (21,-6),
(26,-10), (7,-1), (7,7), (8,-1), (21,-9), (6,2), (20,-7), (30,-10), (14,-3),
(20,-8), (13,-2), (7,3), (28,-8), (29,-9), (15,-3), (22,-5), (26,-8), (25,-8),
(25,-6), (15,-4), (9,-2), (15,-2), (12,-2), (28,-9), (12,-3), (24,-6), (23,-7),
(25,-10), (7,8), (11,-3), (26,-7), (7,1), (23,-9), (6,0), (22,-10), (27,-6),
(8,1), (22,-8), (13,-4), (7,6), (28,-6), (11,-4), (12,-4), (26,-9), (7,4),
(24,-10), (23,-8), (30,-8), (7,0), (9,-1), (10,-1), (26,-5), (22,-9), (6,5),
(7,5), (23,-6), (28,-10), (10,-2), (11,-1), (20,-9), (14,-2), (29,-7), (13,-3),
(23,-5), (24,-8), (27,-9), (30,-7), (28,-5), (21,-10), (7,9), (6,6), (21,-5),
(27,-10), (7,2), (30,-9), (21,-8), (22,-7), (24,-9), (20,-6), (6,9), (29,-5),
(8,-2), (27,-8), (30,-5), (24,-7)]


class Probe:
    def __init__(self, launcher):
        self.launcher = launcher
        self.x = 0
        self.y = 0
        self.x_velocity = None
        self.y_velocity = None

    def reset(self):
        self.x = 0
        self.y = 0
        self.x_velocity = None
        self.y_velocity = None

    def launch(self, x_velocity, y_velocity):
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.start_x_velocity = x_velocity
        self.start_y_velocity = y_velocity

    def iterate(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

        if self.x_velocity > 0:
            self.x_velocity = self.x_velocity - 1
        elif self.x_velocity < 0:
            self.x_velocity = self.x_velocity + 1

        self.y_velocity = self.y_velocity - 1

    @property
    def within_target(self):
        return self.within_x and self.within_y

    @property
    def before_x(self):
        if self.x < self.launcher.x_min:
            return True
        else:
            return False

    @property
    def after_x(self):
        if self.x > self.launcher.x_max:
            return True
        else:
            return False

    @property
    def within_x(self):
        if self.x >= self.launcher.x_min and \
            self.x <= self.launcher.x_max:
            return True
        else:
            return False

    @property
    def before_y(self):
        if self.y < self.launcher.y_min:
            return True
        else:
            return False

    @property
    def after_y(self):
        if self.y > self.launcher.y_max:
            return True
        else:
            return False

    @property
    def within_y(self):
        if self.y >= self.launcher.y_min and \
            self.y <= self.launcher.y_max:
            return True
        else:
            return False


class ProbeLauncher:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.probe = Probe(self)
        self.missed = False
        self.missed_reasons = None

    def launch(self, x_velocity, y_velocity):
        self.probe.launch(x_velocity, y_velocity)

    def prepare_probe(self):
        self.probe.reset()
        self.missed = False

    def compute(self):
        # compute direction
        init_x = range(0,self.x_max+1)
        if self.x_min < 0:
            init_x = range(self.x_min - 1,0)

        y_min = min(self.y_min, self.y_max)
        init_y = range(y_min, -y_min)
        if y_min > 0:
            init_y = range(-y_min, y_min)

        results = []
        for x in init_x:
            for y in init_y:
                self.prepare_probe()
                print(f'testing with {x},{y}')
                self.launch(x, y)

                while not self.missed:
                    self.iterate()
                    if self.probe.within_target:
                        break

                if self.probe.within_target:
                    print(f'hit at {x},{y}')
                    results.append((x,y))

        print(f'{results}')
        return len(results)

    def fire_with_style(self):
        y_max = None

        # compute direction
        init_x = range(1,int(self.x_max/2))
        if self.x_min < 0:
            init_x = range(-int(self.x_max),0)
        init_y = range(0, 200)

        successive_missed = 0
        for x in init_x:
            for y in init_y:
                self.prepare_probe()
                print(f'testing with {x},{y}')
                self.launch(x, y)

                current_y_max = None
                while not self.missed:
                    self.iterate()
                    if current_y_max is None:
                        current_y_max = self.probe.y
                    elif self.probe.y > current_y_max:
                        current_y_max = self.probe.y
                    if self.probe.within_target:
                        break

                if self.probe.within_target:
                    print('hit')
                    if y_max is None:
                        y_max = current_y_max
                    elif current_y_max > y_max:
                        y_max = current_y_max
                        continue
                elif self.missed_reasons == 'x':
                    break
                elif current_y_max is None:
                    break


        print(f'y_max {y_max}')
        return y_max

    def iterate(self):

        self.missed = False
        self.missed_reasons = None

        was_before_x = self.probe.before_x
        was_before_y = self.probe.before_y
        was_after_x = self.probe.after_x
        was_after_y = self.probe.after_y
        was_within_x = self.probe.within_x
        was_within_y = self.probe.within_y

        self.probe.iterate()

        now_before_x = self.probe.before_x
        now_before_y = self.probe.before_y
        now_after_x = self.probe.after_x
        now_after_y = self.probe.after_y
        now_within_x = self.probe.within_x
        now_within_y = self.probe.within_y

        # Probe as pass the target if
        # was_before and now_after
        # was_within and now_after
        # was_within and now_before
        reasons = []

        if was_before_x and now_after_x:
            self.missed = True
        if was_after_x and now_before_x:
            self.missed = True
        if was_within_x and now_after_x:
            self.missed = True
        if was_within_x and now_before_x:
            self.missed = True

        if was_before_y and now_after_y:
            self.missed = True
        if was_within_y and now_after_y:
            self.missed = True
        if was_within_y and now_before_y:
            self.missed = True
        if was_after_y and now_before_y:
            self.missed = True

        if self.missed:
            if was_before_y and now_before_y:
                self.missed_reasons = 'x'
            if was_before_x and now_before_x:
                self.missed_reasons = 'x'
            if was_after_x and now_after_x:
                self.missed_reasons = 'x'



def solve(data):
    launcher = ProbeLauncher(**data)
    y_max = launcher.fire_with_style()
    return y_max

def solve_part2(data):
    launcher = ProbeLauncher(**data)
    result = launcher.compute()
    return result


def test_part1():
    data = test_data
    result = solve(data)
    print(f'test1 is {result}')
    assert result == 45


def test_part2():
    data = test_data
    result = solve_part2(data)
    print(f'test2 is {result}')
    assert result == 112


def part1():
    data = prod_data
    result = solve(data)
    print(f'part1 is {result}')


def part2():
    data = prod_data
    result = solve_part2(data)
    print(f'part2 is {result}')


#test_part1()
#part1()
test_part2()
part2()
