import pygame, csv, os, sys, random, math
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

##########
# Appearances and global parameters
##########
white = '#FFFFFF'
black = '#000000'
offwhite = '#FAF9F6'

instructions = [
    "Rod-and-Disk Task",
    "Goal: Align the central rod to your perceived vertical.",
    "Controls: Mouse wheel to rotate.",
    "When satisfied, press SPACE to advance.",
    "Press ENTER to start.",
    "Double-press ESC to quit."
]

debriefs = [
    "Task end.",
    "Double-press ESC to quit."
]

font = None
font_size = 50

results_dir = 'results/'

##########
# tkinter functions
##########

def ask_params(defaults={"participant_id": "001", "trials": 20, "speed_deg_s": 30.0, "duration": 60, "direction":"clockwise", "seed":1, "disk_count": 440, "rod_len_px": 200, "central_radius_px": 110, "disk_diam_px": 50, "between_disk_gap": 20, "rod_init_angle": 40, "rod_velocity": 0.5}):
    root = tk.Tk()
    root.withdraw()  # hide the empty root window

    dlg = tk.Toplevel(root)
    dlg.title("Rod and Disk Task - Experiment setup")
    dlg.resizable(False, False)

    # Get a tk dialogue window
    frm = ttk.Frame(dlg, padding=12)
    frm.grid(row=0, column=0)

    # Define variables for user to input
    pid_var = tk.StringVar(value=defaults["participant_id"])
    trials_var = tk.StringVar(value=str(defaults["trials"]))
    speed_var = tk.StringVar(value=str(defaults["speed_deg_s"]))
    seed_var = tk.StringVar(value=str(defaults["seed"]))
    rod_init_angle_var = tk.StringVar(value=str(defaults["rod_init_angle"]))
    rod_vel_var = tk.StringVar(value=str(defaults["rod_velocity"]))
    conditions = ["motion", "static"]
    condition_var = tk.StringVar(value=conditions[0])
    directions = ["clockwise", "counterclockwise"]
    direction_var = tk.StringVar(value=directions[0])

    # Define appearances variables for user to input (can change into fixed)
    diskc_var = tk.StringVar(value=defaults["disk_count"])
    rodl_var = tk.StringVar(value=defaults["rod_len_px"])
    centralr_var = tk.StringVar(value=defaults["central_radius_px"])
    diskd_var = tk.StringVar(value=defaults["disk_diam_px"])
    gap_var = tk.StringVar(value=defaults["between_disk_gap"])

    # Define labels and entry/choice fields to show on screen
    ## First set: experiment parameters
    ttk.Label(frm, text="Participant ID:").grid(row=0, column=0, sticky="e", padx=(0,8), pady=6)
    pid_entry = ttk.Entry(frm, textvariable=pid_var, width=24)
    pid_entry.grid(row=0, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Condition:").grid(row=1, column=0, sticky="e", padx=(0,8), pady=6)
    cond_cb = ttk.Combobox(frm, values=conditions, textvariable=condition_var, state="readonly", width=18)
    cond_cb.grid(row=1, column=1, padx=8, pady=8, sticky="w")

    ttk.Label(frm, text="Number of trials:").grid(row=2, column=0, sticky="e", padx=(0,8), pady=6)
    trials_entry = ttk.Entry(frm, textvariable=trials_var, width=10)
    trials_entry.grid(row=2, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Rod beginning angle (+/-):").grid(row=3, column=0, sticky="e", padx=(0,8), pady=6)
    rod_init_angle_entry = ttk.Entry(frm, textvariable=rod_init_angle_var, width=10)
    rod_init_angle_entry.grid(row=3, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Rod velocity (deg/input):").grid(row=4, column=0, sticky="e", padx=(0,8), pady=6)
    rod_vel_entry = ttk.Entry(frm, textvariable=rod_vel_var, width=10)
    rod_vel_entry.grid(row=4, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Disk rotation direction:").grid(row=5, column=0, sticky="e", padx=(0,8), pady=6)
    dir_cb = ttk.Combobox(frm, values=directions, textvariable=direction_var, state="readonly", width=18)
    dir_cb.grid(row=5, column=1, padx=8, pady=8, sticky="w")

    ttk.Label(frm, text="Disk rotation speed (deg/s):").grid(row=6, column=0, sticky="e", padx=(0,8), pady=6)
    speed_entry = ttk.Entry(frm, textvariable=speed_var, width=10)
    speed_entry.grid(row=6, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Radomisation seed:").grid(row=7, column=0, sticky="e", padx=(0,8), pady=6)
    seed_entry = ttk.Entry(frm, textvariable=seed_var, width=10)
    seed_entry.grid(row=7, column=1, sticky="w", pady=6)

    ## Second set: appearances
    ttk.Label(frm, text="Disk count:").grid(row=0, column=3, sticky="e", padx=(0,8), pady=6)
    diskc_entry = ttk.Entry(frm, textvariable=diskc_var, width=24)
    diskc_entry.grid(row=0, column=4, sticky="w", pady=6)

    ttk.Label(frm, text="Rod length (px):").grid(row=1, column=3, sticky="e", padx=(0,8), pady=6)
    rodl_entry = ttk.Entry(frm, textvariable=rodl_var, width=24)
    rodl_entry.grid(row=1, column=4, sticky="w", pady=6)

    ttk.Label(frm, text="Central radius (px):").grid(row=2, column=3, sticky="e", padx=(0,8), pady=6)
    centralr_entry = ttk.Entry(frm, textvariable=centralr_var, width=10)
    centralr_entry.grid(row=2, column=4, sticky="w", pady=6)

    ttk.Label(frm, text="Disk diameter (px):").grid(row=3, column=3, sticky="e", padx=(0,8), pady=6)
    diskd_entry = ttk.Entry(frm, textvariable=diskd_var, width=10)
    diskd_entry.grid(row=3, column=4, sticky="w", pady=6)

    ttk.Label(frm, text="Minimum gap between disks (px):").grid(row=4, column=3, sticky="e", padx=(0,8), pady=6)
    gap_entry = ttk.Entry(frm, textvariable=gap_var, width=24)
    gap_entry.grid(row=4, column=4, sticky="w", pady=6)

    result = None

    # To do when user presses ok button
    def on_ok(event=None):
        nonlocal result
        try:
            pid = pid_var.get().strip()
            if not pid:
                raise ValueError("Participant ID required.")
            trials = int(trials_var.get())
            if trials <= 0:
                raise ValueError("Trials must be > 0.")
            speed = float(speed_var.get())
            if speed < 0:
                raise ValueError("Speed must be >= 0.")
            seed = int(seed_var.get())
            if len(str(abs(seed))) > 20:
                raise ValueError("Seed must be an integer of 20 digits max.")
            rod_init_angle = int(rod_init_angle_var.get())
            if rod_init_angle < 0:
                raise ValueError("Rod initial angle must be >= 0.")
            rod_vel = float(rod_vel_var.get())
            if rod_vel <= 0 or rod_vel > 360:
                raise ValueError("Rod velocity must be between 0 and 360.")
            condition = str(condition_var.get())
            direction = str(direction_var.get())

            disk_count = int(diskc_var.get())
            rod_len_px = int(rodl_var.get())
            central_radius_px = int(centralr_var.get())
            disk_diam_px = int(diskd_var.get())
            between_disk_gap = int(gap_var.get())

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e), parent=dlg)
            return
        result = {"participant_id": pid, "trials": trials, "speed_deg_s": speed, "condition": condition, "rod_init_angle": rod_init_angle, "rod_velocity":rod_vel, "direction":direction, "seed": seed, "disk_count": disk_count, "rod_len_px": rod_len_px, "central_radius_px": central_radius_px, "disk_diam_px": disk_diam_px, "between_disk_gap": between_disk_gap}
        dlg.destroy()

    # To do when user presses cancel button
    def on_cancel(event=None):
        dlg.destroy()
    
    # Make close button behave like cancel
    dlg.protocol("WM_DELETE_WINDOW", on_cancel)

    # Define buttons locations
    btns = ttk.Frame(frm)
    btns.grid(row=10, column=2, columnspan=2, pady=(10,0))
    ttk.Button(btns, text="OK", command=on_ok).grid(row=0, column=0, padx=4)
    ttk.Button(btns, text="Cancel", command=on_cancel).grid(row=0, column=1, padx=4)

    # Define equivalent keyboard responses
    dlg.bind("<Return>", on_ok)
    dlg.bind("<Escape>", on_cancel)

    # Layout finalized; compute size, position, and ensure it comes to front
    dlg.withdraw()
    dlg.update_idletasks()

    # center on screen
    x = (dlg.winfo_screenwidth() - dlg.winfo_reqwidth()) // 2
    y = (dlg.winfo_screenheight() - dlg.winfo_reqheight()) // 2
    dlg.geometry(f"+{x}+{y}")

    dlg.deiconify()
    dlg.lift()
    dlg.attributes("-topmost", True)
    dlg.focus_force()
    pid_entry.focus_set()
    dlg.update_idletasks()
    try:
        dlg.wait_visibility()      # wait until mapped/visible (helps on Wayland/macOS)
    except Exception:
        pass
    # drop topmost after it’s visible, so it doesn’t pin above everything
    dlg.after(100, lambda: dlg.attributes("-topmost", False))

    # modal behavior
    dlg.grab_set()

    # block here until dialog is destroyed
    root.wait_window(dlg)
    root.destroy()
    return result

##########
# pygame functions
##########

# wipe screen
def wipe(screen, screen_width, screen_height):
    pygame.draw.rect(screen, black, pygame.Rect(0, 0, screen_width, screen_height))
    # pygame.display.flip()

# build disks image
def draw_disks(screen_width, screen_height, rand_seed, disk_count, central_radius_px, disk_diam_px, between_disk_gap):
    # define a surface that will cover the entire screen no matter rotation angle. width & height = screen diagnal
    coverable_surface_width = int(math.sqrt(screen_width**2+screen_height**2))

    disk_surface = pygame.Surface((coverable_surface_width, coverable_surface_width), pygame.SRCALPHA)
    disk_surface.fill(black)
    disk_surface_center = (coverable_surface_width//2, coverable_surface_width//2)

    placed = 0
    positions = []
    max_iters = disk_count * 200
    iters = 0
    
    min_center_distance_between_disks = (disk_diam_px + between_disk_gap)**2
    while placed < disk_count and iters < max_iters:
        iters += 1
        x = rand_seed.randint(0, coverable_surface_width - (disk_diam_px/2))
        y = rand_seed.randint(0, coverable_surface_width - (disk_diam_px/2))
        dx = x - disk_surface_center[0]
        dy = y - disk_surface_center[1]
        if math.hypot(dx, dy) >= central_radius_px + disk_diam_px*0.5:
            ok = True
            for px, py in positions:
                ddx = x - px
                ddy = y - py
                if ddx*ddx + ddy*ddy < min_center_distance_between_disks:
                    ok = False
                    break
            if not ok:
                continue
            pygame.draw.circle(disk_surface, offwhite, (x, y), disk_diam_px // 2)
            placed += 1
            positions.append((x,y))
    
    return disk_surface.convert_alpha()

# get a set of rotated images
##### use 0.5 degree steps to make sure smooth animation, but increases build time
def get_rotations(surface, condition="motion"):
    rotations = None
    if condition == "motion":
        rotations = {angle: pygame.transform.rotozoom(surface, -angle*0.5, 1.0) for angle in range(720)}
        # rotations = {angle: pygame.transform.rotozoom(surface, -angle, 1.0) for angle in range(360)}
    else:
        rotations = {angle: surface for angle in range(720)} # no need to compute rotated versions if static condition
        # rotations = {angle: surface for angle in range(360)} # no need to compute rotated versions if static condition
    return rotations

# build rod image
def draw_rod(screen_width, screen_height, center, central_radius_px, rod_len_px):
    # draw a central circle 
    rod_surface = pygame.Surface((screen_width, screen_height),pygame.SRCALPHA)
    pygame.draw.circle(rod_surface, black, center, central_radius_px)
    # draw vertical rod on surface
    p1 = (center[0], center[1] - (rod_len_px/2))
    p2 = (center[0], center[1] + (rod_len_px/2))
    pygame.draw.line(rod_surface, white, p1, p2, 5)

    return rod_surface.convert_alpha()

##########
# Main function
##########
def main():
    ##########
    # Set working directory
    ##########
    # Set working directory to the location of this .py file
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # create results folder if nonexistent
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    ##########
    # Use tkinter to ask for variables
    ##########
    params = ask_params()
    print("Parameters:", params)
    subject, trial_total, disk_rotation_speed, condition, rod_init_angle, rod_velocity, direction_str, seed, disk_count, rod_len_px, central_radius_px, disk_diam_px, between_disk_gap = params.values()
    log_file = subject + f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    disk_rotation_speed_dat = disk_rotation_speed
    if condition == "static":
        direction = 0
        direction_str = "N/A"
        disk_rotation_speed_dat = "N/A"
    else:
        if direction_str == "clockwise":
            direction = 1
        else:
            direction = -1
    # set randomisation seed for both rod init position and disk generation
    rand_seed = random.Random(seed)
    rod_start_angles = [rand_seed.choice([1, -1]) for _ in range(trial_total)]
    wheel_step_degree = rod_velocity
    

    ##########
    # Initialise pygame
    ##########
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=1)
    screen_width, screen_height = screen.get_size()
    center = (screen_width // 2, screen_height // 2)
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Rod and Disk')
    pygame.mouse.set_visible(False)
    screen.fill(black)

    ##########
    # Experiment assets
    ##########
    # text fonts
    text_font = pygame.font.SysFont(font, font_size)
    # manage double esc quit
    esc_pressed = False
    last_esc_time = 0
    double_esc_time = 500  # milliseconds
    # task variables
    data = [['Date', 'Time', 'Trial Start Time (ms)', 'Trial End Time (ms)', 'Randomisation seed', 'Participant', 'Condition', 'Trial', 'Trial Duration (ms)', 'Rod Start Position (deg)', 'Rod Set Position (deg)', 'Roll Direction', 'Roll Velocity (deg/s)']]
    trial = 0
    duration_ms = 0
    disk_angle = 0.0
    rod_angle = 0
    disk_surface = None
    rotated = None
    rod_surface = None
    started = False
    in_trial = False
    ended = False
    running = True

    ##########
    # Build and pre-load stimulus
    ##########
    # roll text
    intro = text_font.render("Initializing...", True, white)
    screen.blit(intro, intro.get_rect(center = (screen_width*0.5, screen_height*0.75)))
    pygame.display.flip()
    # stimulus
    disk_angle = 0.0
    disk_surface = draw_disks(screen_width, screen_height, rand_seed, disk_count, central_radius_px, disk_diam_px, between_disk_gap)
    rotated = get_rotations(disk_surface, condition)
    rod_surface = draw_rod(screen_width, screen_height, center, central_radius_px, rod_len_px)
    rod_start_angle = rod_start_angles[trial] * 40
    rod_angle = rod_start_angles[trial] * 40
    # wipe text
    wipe(screen, screen_width, screen_height)

    ##########
    # Main experiment loop
    ##########
    # main loop
    while running:
        # response (input) behaviour
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # quit if esc key is pressed twice within double_esc_time (500ms)
            elif event.type == pygame.KEYDOWN:
                # handle first half of quit if esc key pressed twice
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = True
                    current_time = pygame.time.get_ticks()
                    if esc_pressed and (current_time - last_esc_time) < double_esc_time:
                        # write data file anyways even in case of force quit
                        with open(results_dir+log_file, 'w', encoding='utf-8') as output:
                            wr = csv.writer(output, lineterminator='\n')
                            for row in data:
                                wr.writerow(row)
                        pygame.quit()
                        sys.exit()
                    esc_pressed = True
                    last_esc_time = current_time
                elif not started:
                        # enter to start experiment
                        if event.key == pygame.K_RETURN:
                            started_time = pygame.time.get_ticks()
                            trial_start_time = pygame.time.get_ticks()
                            started = True
                            in_trial = True
                else:
                    # space to advance to next trial only if not ended
                    if event.key == pygame.K_SPACE:
                        if in_trial and not ended:
                            now = datetime.now()
                            current_time = pygame.time.get_ticks()
                            duration_ms = current_time - trial_start_time
                            trial += 1
                            data.append([now.strftime("%Y-%m-%d"),now.strftime("%H-%M-%S"),trial_start_time,current_time,seed,subject,condition,trial,duration_ms,rod_start_angle,rod_angle,direction_str,disk_rotation_speed_dat])
                            if trial >= trial_total:
                                ended = True
                            else:
                                # start a new trial
                                rod_start_angle = rod_start_angles[trial] * rod_init_angle
                                rod_angle = rod_start_angles[trial] * rod_init_angle
                                trial_start_time = pygame.time.get_ticks()
            # second half of handling quit, when esc is up (unpressed), esc_pressed is set to false
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = False
            # add rod angles if in trial
            if event.type == pygame.MOUSEWHEEL:
                if in_trial:
                    rod_angle -= event.y * wheel_step_degree

        # display behaviour
        if not started:
            for i in range(len(instructions)):
                message = text_font.render(instructions[i], True, white)
                screen.blit(message, message.get_rect(center = (screen_width*0.5, (i+1)*(screen_height*(1/(len(instructions)+3))))))
        elif ended:
            wipe(screen, screen_width, screen_height)
            for i in range(len(debriefs)):
                message = text_font.render(debriefs[i], True, white)
                screen.blit(message, message.get_rect(center = (screen_width*0.5, (i+1)*(screen_height*(1/(len(debriefs)+5))))))
        else:
            now = pygame.time.get_ticks()
            elapsed = (now - started_time) * 0.001
            disk_angle = int(((direction * disk_rotation_speed * elapsed) % 360)*2) # x2 to map onto 720 pre-built frames
            # disk_angle = int((direction * disk_rotation_speed * elapsed) % 360)
            rod_rotated = pygame.transform.rotozoom(rod_surface, -rod_angle, 1.0)
            screen.blit(rotated[disk_angle], rotated[disk_angle].get_rect(center=center))
            screen.blit(rod_rotated, rod_rotated.get_rect(center=center))
        pygame.display.flip()
        clock.tick(120) # cap at 120 fps to allow smoother animation on better PCs

    # quit game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()