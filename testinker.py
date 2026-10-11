import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from copy import deepcopy
import math
import CTkGradient as ctkg
from PIL import Image, ImageDraw, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from more_tinkering import plane, test_plane


default_trajectory = [
    (50, 200), (70, 195), (90, 192), (110, 190), (130, 191),
    (150, 195), (170, 202), (190, 210), (210, 220), (230, 235),
    (250, 255), (270, 280), (290, 310), (310, 345), (330, 390)
]


def compute_trajectory(wingspan=5, starting_angle=270, starting_velocity=0, center_of_mass_x=0.0, center_of_mass_y=0.0):
    """Backend contract: take UI inputs and return a list of (x, y) points."""
    if starting_velocity <= 0:
        starting_velocity = 0.5

    speed = float(starting_velocity)
    launch_angle = math.radians(starting_angle - 270)
    wing_bias = float(wingspan) * 2.0
    x_offset = float(center_of_mass_x) * 2.0
    y_offset = float(center_of_mass_y) * 2.0

    trajectory = [(0.0, 0.0)]
    x = 0.0
    y = 0.0

    for step in range(1, 120):
        dx = speed * math.cos(launch_angle) * 2.0
        dy = -speed * math.sin(launch_angle) * 2.0

        x += dx + x_offset * (step / 80.0)
        y += dy + y_offset * (step / 80.0)
        y -= 0.35 * step
        y += wing_bias * math.sin(step / 12.0)

        if x > 0 and y > -1000:
            trajectory.append((round(x, 2), round(y, 2)))

    if len(trajectory) == 1:
        return [(0.0, 0.0)]
    return trajectory


root = ctk.CTk()
global trajectory
trajectory = default_trajectory
trajectory_in_meters = False
AIRPLANE_OFFSET_X = 20
AIRPLANE_OFFSET_Y = 20

airplane_image_path = Path(__file__).with_name("paper_airplane.png")
if airplane_image_path.exists():
    original_airplane_image = Image.open(airplane_image_path).convert("RGBA")
else:
    original_airplane_image = Image.new("RGBA", (120, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(original_airplane_image)
    draw.polygon([(15, 30), (95, 20), (95, 40), (15, 30)], fill=(255, 255, 255, 255))
    draw.polygon([(35, 15), (75, 30), (35, 45), (35, 15)], fill=(255, 255, 255, 255))
    draw.line((15, 30, 95, 30), fill=(255, 255, 255, 255), width=2)
    draw.line((35, 15, 35, 45), fill=(255, 255, 255, 255), width=2)

paper_airplane = original_airplane_image.resize((60, 60), Image.LANCZOS)
rotated_airplane = ImageTk.PhotoImage(paper_airplane)


root.geometry("1400x700")

root.title("Airplane Simulator")

ctk.set_default_color_theme("dark-blue")

# Side bar
SideFrame = ctk.CTkFrame(
    root, 
    width = 100,
    corner_radius = 10,
    fg_color = "#0359A5"
)
SideFrame.pack(side = ctk.LEFT, fill = ctk.Y)

# Title
titlelabel = ctk.CTkLabel(
    SideFrame, 
    width = 20,
    text = " Paper Airplane SIM ", 
    text_color= "white",
    font = ("Monaco", 24),
    fg_color="black",
    border_width=40,
    border_color="black",
    corner_radius=3
)

titlelabel.pack(anchor = tk.N, pady = 20, padx = 30)

# Where everything goes
MainFrame = ctkg.GradientFrame(
    master = root,
    colors = ("#041FE6", "#07a8ed"),
    direction = "vertical",
    corner_radius = 10,
    height = 300,
    width = 300
)
MainFrame.pack(fill="both", expand=True)

# Sliders box
Internal_Box = ctk.CTkFrame(
    master=SideFrame, 
    width=160, 
    height=100, 
    fg_color="gray20"
)

Internal_Box.pack(pady=20, padx=20)



# Functions for handling slider events (mostly)

def example_back_end(wingspan, starting_angle, starting_velocity, center_of_mass_x, center_of_mass_y):
    global trajectory
    trajectory = compute_trajectory(
        wingspan=wingspan,
        starting_angle=starting_angle,
        starting_velocity=starting_velocity,
        center_of_mass_x=center_of_mass_x,
        center_of_mass_y=center_of_mass_y,
    )
    if trajectory:
        plot_points(trajectory)


def rotate_image(value):
    global rotated_airplane
    rotation_angle = float(value) + 90
    rotated_airplane = ImageTk.PhotoImage(paper_airplane.rotate(rotation_angle, expand=True))
    if 'airplane_id' in globals():
        MainFrame.gradient.itemconfigure(airplane_id, image=rotated_airplane)

def slider_event_wing(value):
    global x, paper_airplane
    x = int(value)
    image_width = max(2, int(10 * float(value)))
    image_height = max(1, round(image_width * original_airplane_image.height / original_airplane_image.width))
    paper_airplane = original_airplane_image.resize((image_width, image_height), Image.LANCZOS)
    WingSpanStatLabel.configure(text=f"Wing Span (cm): {x}")
    rotate_image(StartingAngleSlider.get())

def slider_event_starting_angle(value):
    global x
    x = int(value)
    StartingAngleStatLabel.configure(text=f"Starting Angle (degrees): {x-270}°")
    rotate_image(value)

def slider_event_starting_velocity(value):
    global x
    x = int(value)
    StartingVelocityStatLabel.configure(text=f"Starting Velocity (m/s): {x}")

def slider_event_center_of_mass_x(value):
    global x
    x = float(value)
    CenterOfMassStatLabelX.configure(text=f"Center of Mass Vertical (cm): {x:.3f}")

def slider_event_center_of_mass_y(value):
    global x
    x = float(value)
    CenterOfMassStatLabelY.configure(text=f"Center of Mass Horizontal (cm): {x:.3f}")

def checkbox_event_advanced_options():
    global trajectory, trajectory_in_meters
    trajectory = test_plane(deepcopy(plane), 0, 0)
    trajectory_in_meters = True
    plot_points(trajectory)
    start_animation()

# SLIDERS YOU KNOW! ######################################

# Weight Slider and Title

WingSpanSliderLabel = ctk.CTkLabel(
    Internal_Box,
    width = 20,
    text = "Wing Span (cm): ",
    font = ("Monaco", 14)
)

WingSpanSliderLabel.grid(row = 1, column = 0, padx = 10, pady = 20)

WingSpanSlider = ctk.CTkSlider(
    Internal_Box, 
    width = 100, 
    height = 20,
    from_ = 0, 
    to = 20, 
    number_of_steps = 10,
    command = slider_event_wing,
    fg_color = "red",
    progress_color = "#09C61C",
    button_hover_color = "#096DEF",
)

WingSpanSlider.grid(row = 1, column = 1, padx = 10, pady = 20)

WingSpanSlider.set(5)

#@@@@

StartingAngleLabel = ctk.CTkLabel(
    Internal_Box,
    width = 20,
    text = "Starting Angle (degrees): ",
    font = ("Monaco", 14)
)

StartingAngleLabel.grid(row = 2, column = 0, padx = 10, pady = 20)

StartingAngleSlider = ctk.CTkSlider(
    Internal_Box, 
    width = 100, 
    height = 20,
    from_ = 180, 
    to = 360, 
    number_of_steps = 180,
    command = slider_event_starting_angle,
    fg_color = "red",
    progress_color = "#09C61C",
    button_hover_color = "#096DEF",
)

StartingAngleSlider.grid(row = 2, column = 1, padx = 10, pady = 20)

StartingAngleSlider.set(270)

#@@@@

StartingVelocityLabel = ctk.CTkLabel(
    Internal_Box,
    width = 20,
    text = "Starting Velocity (m/s): ",
    font = ("Monaco", 14)
)

StartingVelocityLabel.grid(row = 3, column = 0, padx = 10, pady = 20)

StartingVelocitySlider = ctk.CTkSlider(
    Internal_Box, 
    width = 100, 
    height = 20,
    from_ = 0, 
    to = 10, 
    number_of_steps = 10,
    command = slider_event_starting_velocity,
    fg_color = "red",
    progress_color = "#09C61C",
    button_hover_color = "#096DEF",
)

StartingVelocitySlider.grid(row = 3, column = 1, padx = 10, pady = 20)

StartingVelocitySlider.set(0)

#@@@@

CenterOfMassLabelX = ctk.CTkLabel(
    Internal_Box,
    width = 20,
    text = "Center of Mass Vertical (cm): ",
    font = ("Monaco", 14)
)

CenterOfMassLabelX.grid(row = 4, column = 0, padx = 10, pady = 20)

CenterOfMassSliderX = ctk.CTkSlider(
    Internal_Box, 
    width = 100, 
    height = 20,
    from_ = -0.005, 
    to = 0.005, 
    number_of_steps = 10,
    command = slider_event_center_of_mass_x,
    fg_color = "red",
    progress_color = "#09C61C",
    button_hover_color = "#096DEF",
)

CenterOfMassSliderX.grid(row = 4, column = 1, padx = 10, pady = 20)

CenterOfMassSliderX.set(0)

#@@@@

CenterOfMassLabelY = ctk.CTkLabel(
    Internal_Box,
    width = 20,
    text = "Center of Mass Horizontal (cm): ",
    font = ("Monaco", 14)
)

CenterOfMassLabelY.grid(row = 5, column = 0, padx = 10, pady = 20)


CenterOfMassSliderY = ctk.CTkSlider(
    Internal_Box, 
    width = 100, 
    height = 20,
    from_ = -0.005, 
    to = 0.005, 
    number_of_steps = 10,
    command = slider_event_center_of_mass_y,
    fg_color = "red",
    progress_color = "#09C61C",
    button_hover_color = "#096DEF",
)

CenterOfMassSliderY.grid(row = 5, column = 1, padx = 10, pady = 20)

CenterOfMassSliderY.set(0)

#@@@@

AdvancedOption = ctk.CTkButton(
    Internal_Box,
    text = "Advanced Options",
    font = ("Monaco", 14),
    fg_color = "gray",
    text_color = "#1AFF00",
    hover_color = "#1B950E",
    bg_color =  "#000000",
    command = checkbox_event_advanced_options
)

AdvancedOption.grid(row=6, column=0, padx=(100, 0), pady=20, sticky = "nsew")

########################################

plt.rcParams.update({
    "axes.facecolor": "lightgray",    # Inner background color
    "figure.facecolor": "lightblue"   # Outer background color
})

# 1. Refactored GraphApp to be a reusable Frame component
GraphApp = ctk.CTkFrame(MainFrame)
GraphApp.place(relx=0.64, rely=0.62, relwidth=0.34, relheight=0.35)

GraphApp.fig, GraphApp.ax = plt.subplots(figsize=(5, 3.5), dpi=50)
GraphApp.fig.subplots_adjust(left=0.22, bottom=0.25, right=1, top=0.89)
GraphApp.ax.set_title("Paper Airplane Trajectory")
GraphApp.ax.set_xlabel("Horizontal position")
GraphApp.ax.set_ylabel("Vertical position")
GraphApp.line, = GraphApp.ax.plot([], [], marker="o", color="blue")
GraphApp.canvas_bridge = FigureCanvasTkAgg(GraphApp.fig, master=GraphApp)
GraphApp.canvas_widget = GraphApp.canvas_bridge.get_tk_widget()
GraphApp.canvas_widget.pack(fill=ctk.BOTH, expand=True, padx=6, pady=6)

def plot_points(points):
    if points:
        x_data, y_data = zip(*points)
    else:
        x_data, y_data = (), ()

    GraphApp.line.set_data(x_data, y_data)
    GraphApp.ax.relim()
    GraphApp.ax.autoscale_view()
    if points and not GraphApp.ax.yaxis_inverted():
        GraphApp.ax.invert_yaxis()
    GraphApp.canvas_bridge.draw_idle()


########################################
def launch_event():
    global trajectory, trajectory_in_meters
    trajectory_in_meters = False
    current_wingspan = WingSpanSlider.get()
    current_starting_angle = StartingAngleSlider.get()
    current_starting_velocity = StartingVelocitySlider.get()
    current_center_of_mass_x = CenterOfMassSliderX.get()
    current_center_of_mass_y = CenterOfMassSliderY.get()

    example_back_end(
        current_wingspan,
        current_starting_angle,
        current_starting_velocity,
        current_center_of_mass_x,
        current_center_of_mass_y,
    )

    if trajectory:
        plot_points(trajectory)

    print(f"Wingspan: {current_wingspan}, Starting Angle: {current_starting_angle}, \nStarting Velocity: {current_starting_velocity}, Center of Mass X: {current_center_of_mass_x}, Center of Mass Y: {current_center_of_mass_y}")
    start_animation()


def start_animation():
    global frame_index
    if trajectory:
        start_x, start_y = canvas_point(trajectory[0])
        MainFrame.gradient.coords(airplane_id, start_x, start_y)
    frame_index = 0
    animation_loop_image()

LaunchButtonFrame = ctk.CTkFrame(
    SideFrame,
    width = 200,
    height = 200,
    fg_color="#3D08E9"
)

LaunchButtonFrame.pack(pady = 20)

LaunchButton = ctk.CTkButton(
    LaunchButtonFrame,
    text = "Launch",
    fg_color="#02CCC6",
    text_color="black",
    width = 190,
    height = 70,
    font = ("Monaco", 26),
    command = launch_event,
)

LaunchButton.pack(pady = 40, padx = 40)

if trajectory:
    airplane_id = MainFrame.gradient.create_image(
        trajectory[0][0] + AIRPLANE_OFFSET_X,
        -trajectory[0][1] + AIRPLANE_OFFSET_Y,
        image=rotated_airplane,
        anchor=tk.CENTER,
        tags="airplane_tag"
    )
    plot_points(trajectory)
    rotate_num = StartingAngleSlider.get()
    rotate_image(rotate_num)


def animation_loop_image():
    global frame_index

    if trajectory and frame_index < len(trajectory):
        screen_x, screen_y = canvas_point(trajectory[frame_index])
        MainFrame.gradient.coords(airplane_id, screen_x, screen_y)

        if frame_index + 1 < len(trajectory):
            next_screen_x, next_screen_y = canvas_point(trajectory[frame_index + 1])

            dx = next_screen_x - screen_x
            dy = next_screen_y - screen_y
            target_angle = math.degrees(math.atan2(dy, dx))

            if 'last_airplane_angle' not in globals():
                last_airplane_angle = target_angle
            else:
                last_airplane_angle = globals()['last_airplane_angle']

            smoothed_angle = last_airplane_angle + (target_angle - last_airplane_angle) * 0.35
            globals()['last_airplane_angle'] = smoothed_angle

            rotated = ImageTk.PhotoImage(paper_airplane.rotate(-smoothed_angle, expand=True))
            MainFrame.gradient.itemconfigure(airplane_id, image=rotated)
            MainFrame.gradient.image = rotated

        frame_index += 1
        root.after(20, animation_loop_image)
    else:
        if trajectory:
            start_x, start_y = canvas_point(trajectory[0])
            MainFrame.gradient.coords(airplane_id, start_x, start_y)
            globals()['last_airplane_angle'] = 0.0
            frame_index = 0


def canvas_point(point):
    x, y = point
    if not trajectory_in_meters:
        return x + AIRPLANE_OFFSET_X, -y + AIRPLANE_OFFSET_Y

    canvas_width = max(1, MainFrame.gradient.winfo_width())
    canvas_height = max(1, MainFrame.gradient.winfo_height())
    padding = 60
    x_values, y_values = zip(*trajectory)
    x_span = max(x_values) - min(x_values) or 1
    y_span = max(y_values) - min(y_values) or 1
    screen_x = padding + (x - min(x_values)) / x_span * max(1, canvas_width - 2 * padding)
    screen_y = padding + (max(y_values) - y) / y_span * max(1, canvas_height - 2 * padding)
    return screen_x + AIRPLANE_OFFSET_X, screen_y + AIRPLANE_OFFSET_Y

########################################

StatLabel = ctk.CTkFrame(
    MainFrame,
    width = 150,
    height = 300,
    bg_color="black",
    corner_radius= 10
)
#StatLabel.pack(side="top", anchor ="se", padx = 10, pady = 10)
StatLabel.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

StatLabelLabel = ctk.CTkLabel(
    StatLabel,
    text = "Statistics:",
    width = 20,
    font = ("Monaco", 14)
)

StatLabelLabel.pack(padx = 10, pady = 10)

#2222

WingSpanStatLabel = ctk.CTkLabel(
    StatLabel,
    width = 20,
    text = "Wing Span (cm): 0",
    font = ("Monaco", 12)
)

WingSpanStatLabel.pack(padx = 10, pady = 10)

#2222

StartingAngleStatLabel = ctk.CTkLabel(
    StatLabel,
    width = 20,
    text = "Starting Angle (degrees): 0°",
    font = ("Monaco", 12)
)

StartingAngleStatLabel.pack(padx = 10, pady = 10)

#2222

StartingVelocityStatLabel = ctk.CTkLabel(
    StatLabel,
    width = 20,
    text = "Starting Velocity (m/s): 0",
    font = ("Monaco", 12)
)

StartingVelocityStatLabel.pack(padx = 10, pady = 10)

#2222

CenterOfMassStatLabelX = ctk.CTkLabel(
    StatLabel,
    width = 20,
    text = "Center of Mass Vertical (cm): 0",
    font = ("Monaco", 12)
)

CenterOfMassStatLabelX.pack(padx = 10, pady = 10)

#2222

CenterOfMassStatLabelY = ctk.CTkLabel(
    StatLabel,
    width = 20,
    text = "Center of Mass Horizontal (cm): 0",
    font = ("Monaco", 12)
)

CenterOfMassStatLabelY.pack(padx = 10, pady = 10)
########################################

slider_event_wing(WingSpanSlider.get())

root.mainloop()
