from manimlib.imports import *


class VisualizeStates(Scene):
    CONFIG = {
        "coordinate_plane_config": {
            "y_line_frequency": PI / 2,
            # "x_line_frequency": PI / 2,
            "x_line_frequency": 1,
            "y_axis_config": {
                # "unit_size": 1.75,
                "unit_size": 1,
            },
            "y_max": 4,
            "faded_line_ratio": 4,
            "background_line_style": {
                "stroke_width": 1,
            },
        },
        "little_pendulum_config": {
            "length": 1,
            "gravity": 4.9,
            "weight_diameter": 0.3,
            "include_theta_label": False,
            "include_velocity_vector": True,
            "angle_arc_config": {
                "radius": 0.2,
            },
            "velocity_vector_config": {
                "max_tip_length_to_length_ratio": 0.35,
                "max_stroke_width_to_length_ratio": 6,
            },
            "velocity_vector_multiple": 0.25,
            "max_velocity_vector_length_to_length_ratio": 0.8,
        },

        "n_thetas": 11,
        "n_omegas": 7,
        # "n_thetas": 5,
        # "n_omegas": 3,
        "initial_grid_wait_time": 15,
    }


class IntroduceVectorField(VisualizeStates):
    CONFIG = {
        "vector_field_config": {
            "max_magnitude": 3,
            # "delta_x": 2,
            # "delta_y": 2,
        },
        "big_pendulum_config": {
            "length": 1.6,
            "gravity": 4.9,
            "damping": 0.2,
            "weight_diameter": 0.3,
            "include_velocity_vector": True,
            "angle_arc_config": {
                "radius": 0.5,
            },
            "initial_theta": -80 * DEGREES,
            "omega": 1,
            "set_theta_label_height_cap": True,
        }
    }

    def initialize_plane(self):
        plane = self.plane = NumberPlane(
            **self.coordinate_plane_config
        )
        plane.axis_labels = VGroup(
            plane.get_x_axis_label(
                "\\theta", RIGHT, UL, buff=SMALL_BUFF
            ),
            plane.get_y_axis_label(
                "\\dot \\theta", UP, DR, buff=SMALL_BUFF
            ).set_color(YELLOW),
        )
        for label in plane.axis_labels:
            label.add_background_rectangle()
        plane.add(plane.axis_labels)

        plane.y_axis.add_numbers(direction=DL)

        x_axis = plane.x_axis
        label_texs = ["\\pi \\over 2", "\\pi", "3\\pi \\over 2", "\\tau"]
        values = [PI / 2, PI, 3 * PI / 2, TAU]
        x_axis.coordinate_labels = VGroup()
        x_axis.add(x_axis.coordinate_labels)
        for value, label_tex in zip(values, label_texs):
            for u in [-1, 1]:
                tex = label_tex
                if u < 0:
                    tex = "-" + tex
                label = TexMobject(tex)
                label.scale(0.5)
                if label.get_height() > 0.4:
                    label.set_height(0.4)
                point = x_axis.number_to_point(u * value)
                label.next_to(point, DR, SMALL_BUFF)
                x_axis.coordinate_labels.add(label)

        self.add(self.plane)

    def initialize_vector_field(self):
        self.vector_field = VectorField(
            self.vector_field_func,
            **self.vector_field_config,
        )
        self.vector_field.sort(get_norm)

    def vector_field_func(self, point):
        x, y = self.plane.point_to_coords(point)

        mu, g, L = [
            self.big_pendulum_config.get(key)
            for key in ["damping", "gravity", "length"]
        ]
        return pendulum_vector_field_func(
            x * RIGHT + y * UP,
            mu=mu, g=g, L=L
        )


class Thumbnail(IntroduceVectorField):
    CONFIG = {
        "vector_field_config": {
            # "delta_x": 0.5,
            # "delta_y": 0.5,
            # "max_magnitude": 5,
            # "length_func": lambda norm: 0.5 * sigmoid(norm),
            "delta_x": 1,
            "delta_y": 1,
            "max_magnitude": 5,
            "length_func": lambda norm: 0.9 * sigmoid(norm),
        },
        "big_pendulum_config": {
            "damping": 0.4,
        },
    }

    def construct(self):
        self.initialize_plane()
        self.plane.axes.set_stroke(width=0.5)
        self.initialize_vector_field()

        self.add(self.vector_field)

        self.wait(1)


def pendulum_vector_field_func(point, mu=0.1, g=9.8, L=3):
    theta, omega = point[:2]
    return np.array([
        omega,
        -np.sqrt(g / L) * np.sin(theta) - mu * omega,
        0,
    ])
