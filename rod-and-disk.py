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

def ask_params(defaults={"participant_id": "001", "trials": 20, "speed_deg_s": 12.0, "duration": 60, "direction":"clockwise", "seed":1, "disk_count": 440, "rod_len_px": 200, "central_radius_px": 110, "disk_diam_px": 50, "between_disk_gap": 20}):
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
    duration_var = tk.StringVar(value=str(defaults["duration"]))
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

    ttk.Label(frm, text="Trial duration:").grid(row=3, column=0, sticky="e", padx=(0,8), pady=6)
    duration_entry = ttk.Entry(frm, textvariable=duration_var, width=10)
    duration_entry.grid(row=3, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Direction:").grid(row=4, column=0, sticky="e", padx=(0,8), pady=6)
    dir_cb = ttk.Combobox(frm, values=directions, textvariable=direction_var, state="readonly", width=18)
    dir_cb.grid(row=4, column=1, padx=8, pady=8, sticky="w")

    ttk.Label(frm, text="Disk rotation speed (degree/s):").grid(row=5, column=0, sticky="e", padx=(0,8), pady=6)
    speed_entry = ttk.Entry(frm, textvariable=speed_var, width=10)
    speed_entry.grid(row=5, column=1, sticky="w", pady=6)

    ttk.Label(frm, text="Radomisation seed:").grid(row=6, column=0, sticky="e", padx=(0,8), pady=6)
    seed_entry = ttk.Entry(frm, textvariable=seed_var, width=10)
    seed_entry.grid(row=6, column=1, sticky="w", pady=6)

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
            if seed < 1 or seed > 10000:
                raise ValueError("Seed must be an integer between 1 and 10000.")
            duration = int(duration_var.get())
            if duration <= 0:
                raise ValueError("Duration must be >= 0.")
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
        result = {"participant_id": pid, "trials": trials, "speed_deg_s": speed, "condition": condition, "duration": duration, "direction":direction, "seed": seed, "disk_count": disk_count, "rod_len_px": rod_len_px, "central_radius_px": central_radius_px, "disk_diam_px": disk_diam_px, "between_disk_gap": between_disk_gap}
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
def draw_disks(screen_width, screen_height, seed, disk_count, central_radius_px, disk_diam_px, between_disk_gap):
    # define a surface that will cover the entire screen no matter rotation angle. width & height = screen diagnal
    coverable_surface_width = int(math.sqrt(screen_width**2+screen_height**2))

    disk_surface = pygame.Surface((coverable_surface_width, coverable_surface_width), pygame.SRCALPHA)
    disk_surface.fill(black)
    disk_surface_center = (coverable_surface_width//2, coverable_surface_width//2)

    seed = random.Random(seed)
    placed = 0
    positions = []
    max_iters = disk_count * 200
    iters = 0
    
    min_center_distance_between_disks = (disk_diam_px + between_disk_gap)**2
    while placed < disk_count and iters < max_iters:
        iters += 1
        x = seed.randint(0, coverable_surface_width - 1)
        y = seed.randint(0, coverable_surface_width - 1)
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
    
    return disk_surface

def draw_rod(screen_width, screen_height, center, central_radius_px, rod_len_px):
    # draw a central circle 
    rod_surface = pygame.Surface((screen_width, screen_height),pygame.SRCALPHA)
    pygame.draw.circle(rod_surface, black, center, central_radius_px)
    # draw vertical rod on surface
    p1 = (center[0], center[1] - (rod_len_px/2))
    p2 = (center[0], center[1] + (rod_len_px/2))
    pygame.draw.line(rod_surface, white, p1, p2, 5)

    return rod_surface

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
    subject, trial_total, disk_rotation_speed, condition, duration, direction_str, seed, disk_count, rod_len_px, central_radius_px, disk_diam_px, between_disk_gap = params.values()
    log_file = subject + f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    if condition == "static":
        direction = 0
        direction_str = "N/A"
    else:
        if direction_str == "clockwise":
            direction = 1
        else:
            direction = -1
    rod_start_angles = [random.choice([1, -1]) for _ in range(trial_total)]
    wheel_step_degree = 0.5 #### Not sure what speed John needs, for now randomly using 0.5 degree per input

    ##########
    # Initialise pygame
    ##########
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0)
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
    data = [['date', 'time', 'start_time', 'end_time', 'participant', 'condition', 'trial', 'duration_ms', 'rod_start_angle', 'rod_end_angle', 'disk_rotation_direction', 'disk_speed']]
    trial = 0
    disk_angle = 0.0
    rod_angle = 0
    disk_surface = None
    rod_surface = None
    started_time = 0
    duration_ms = duration * 1000
    started = False
    in_trial = False
    ended = False
    running = True

    # main loop
    while running:
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
                        if event.key == pygame.K_RETURN:
                            disk_angle = 0.0
                            disk_surface = draw_disks(screen_width, screen_height, seed, disk_count, central_radius_px, disk_diam_px, between_disk_gap)
                            rod_surface = draw_rod(screen_width, screen_height, center, central_radius_px, rod_len_px)
                            rod_start_angle = rod_start_angles[trial] * 40
                            rod_angle = rod_start_angles[trial] * 40
                            started_time = pygame.time.get_ticks()
                            started = True
                            in_trial = True
                else:
                    if event.key == pygame.K_SPACE:
                        if not in_trial and not ended:
                            disk_angle = 0.0
                            disk_surface = draw_disks(screen_width, screen_height, seed, disk_count, central_radius_px, disk_diam_px, between_disk_gap)
                            rod_surface = draw_rod(screen_width, screen_height, center, central_radius_px, rod_len_px)
                            rod_start_angle = rod_start_angles[trial] * 40
                            rod_angle = rod_start_angles[trial] * 40
                            started_time = pygame.time.get_ticks()
                            in_trial = True
            # second half of handling quit, when esc is up (unpressed), esc_pressed is set to false
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    esc_pressed = False
            # add rod angles if in trial
            if event.type == pygame.MOUSEWHEEL:
                if in_trial:
                    rod_angle -= event.y * wheel_step_degree
        
        if not started:
            for i in range(len(instructions)):
                message = text_font.render(instructions[i], True, white)
                screen.blit(message, message.get_rect(center = (screen_width*0.5, (i+1)*(screen_height*(1/(len(instructions)+1))))))
        elif ended:
            wipe(screen, screen_width, screen_height)
            for i in range(len(debriefs)):
                message = text_font.render(debriefs[i], True, white)
                screen.blit(message, message.get_rect(center = (screen_width*0.5, (i+1)*(screen_height*(1/(len(instructions)+1))))))
        elif in_trial:
            now = pygame.time.get_ticks()
            elapsed = (now - started_time) * 0.001
            disk_angle = (direction * disk_rotation_speed * elapsed) % 360
            disk_rotated = pygame.transform.rotozoom(disk_surface, -disk_angle, 1.0)
            rod_rotated = pygame.transform.rotozoom(rod_surface, -rod_angle, 1.0)
            wipe(screen, screen_width, screen_height)
            screen.blit(disk_rotated, disk_rotated.get_rect(center=center))
            screen.blit(rod_rotated, rod_rotated.get_rect(center=center))
            current_time = pygame.time.get_ticks()
            if current_time - started_time >= duration_ms:
                trial += 1
                now = datetime.now()
                data.append([now.strftime("%Y-%m-%d"),now.strftime("%H-%M-%S"),started_time,current_time,subject,condition,trial,duration_ms,rod_start_angle,rod_angle,direction_str,disk_rotation_speed])
                in_trial = False
                if trial >= trial_total:
                    ended = True
        else:
            wipe(screen, screen_width, screen_height)
            message = text_font.render("press space for the next trial.", True, white)
            screen.blit(message, message.get_rect(center = (screen_width*0.5, (i+1)*(screen_height*(1/(len(instructions)+1))))))
        pygame.display.flip()
        clock.tick(30) # cap at 30 fps to try to deal with slow computer

    # quit game
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()