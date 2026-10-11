import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# VIRTUAL MEMORY STRESS LAB
# ============================================================

window = tk.Tk()

window.title("Virtual Memory Stress Lab")
window.geometry("1100x850")
window.resizable(False, False)


# ============================================================
# VARIABLES
# ============================================================

stress_memory = []
stress_running = False

# Data for graphs
time_data = []
ram_data = []
swap_data = []
cpu_data = []

start_time = time.time()


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    window,
    text="VIRTUAL MEMORY STRESS LAB",
    font=("Arial", 26, "bold")
)

title.pack(pady=15)


# ============================================================
# CURRENT RAM INFORMATION
# ============================================================

ram_label = tk.Label(
    window,
    text="RAM Usage: Loading...",
    font=("Arial", 16)
)

ram_label.pack(pady=3)


ram_bar = ttk.Progressbar(
    window,
    length=700,
    maximum=100
)

ram_bar.pack(pady=3)


# ============================================================
# CURRENT VIRTUAL MEMORY INFORMATION
# ============================================================

swap_label = tk.Label(
    window,
    text="Virtual Memory: Loading...",
    font=("Arial", 16)
)

swap_label.pack(pady=3)


swap_bar = ttk.Progressbar(
    window,
    length=700,
    maximum=100
)

swap_bar.pack(pady=3)


# ============================================================
# CPU INFORMATION
# ============================================================

cpu_label = tk.Label(
    window,
    text="CPU Usage: Loading...",
    font=("Arial", 16)
)

cpu_label.pack(pady=3)


# ============================================================
# GRAPH
# ============================================================

figure = Figure(
    figsize=(9, 3.2),
    dpi=100
)

graph = figure.add_subplot(111)

graph.set_title("System Resource Usage")
graph.set_xlabel("Time (seconds)")
graph.set_ylabel("Usage (%)")

graph.set_ylim(0, 100)
graph.grid(True)


canvas = FigureCanvasTkAgg(
    figure,
    master=window
)

canvas.draw()

canvas.get_tk_widget().pack(pady=10)


# ============================================================
# STRESS TEST SECTION
# ============================================================

stress_title = tk.Label(
    window,
    text="MEMORY STRESS TEST",
    font=("Arial", 19, "bold")
)

stress_title.pack(pady=5)


selection_frame = tk.Frame(window)

selection_frame.pack(pady=3)


tk.Label(
    selection_frame,
    text="Memory to allocate:",
    font=("Arial", 13)
).pack(side=tk.LEFT, padx=8)


memory_choice = ttk.Combobox(
    selection_frame,
    values=["1 GB", "2 GB", "3 GB", "4 GB"],
    state="readonly",
    width=8,
    font=("Arial", 12)
)

memory_choice.set("1 GB")

memory_choice.pack(side=tk.LEFT)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    window,
    text="Status: Ready",
    font=("Arial", 13)
)

status_label.pack(pady=5)


# ============================================================
# MEMORY SELECTION
# ============================================================

def get_selected_memory():

    selected = memory_choice.get()

    return int(selected.split()[0])


# ============================================================
# MEMORY STRESS FUNCTION
# ============================================================

def stress_memory_function():

    global stress_running
    global stress_memory

    amount_gb = get_selected_memory()

    chunk_size = 64 * 1024 * 1024

    total_bytes = amount_gb * 1024 * 1024 * 1024

    allocated = 0

    stress_memory = []

    try:

        while allocated < total_bytes and stress_running:

            remaining = total_bytes - allocated

            current_chunk = min(
                chunk_size,
                remaining
            )

            block = bytearray(current_chunk)

            # Touch each memory page so the OS commits it
            for i in range(0, len(block), 4096):
                block[i] = 1

            stress_memory.append(block)

            allocated += current_chunk

            time.sleep(0.1)

        if stress_running:

            window.after(
                0,
                lambda: status_label.config(
                    text=f"Status: {amount_gb} GB stress active"
                )
            )

    except MemoryError:

        window.after(
            0,
            lambda: status_label.config(
                text="Status: Memory allocation stopped"
            )
        )

        stop_stress()


# ============================================================
# START STRESS
# ============================================================

def start_stress():

    global stress_running

    if stress_running:
        return

    stress_running = True

    status_label.config(
        text="Status: Starting stress test..."
    )

    thread = threading.Thread(
        target=stress_memory_function,
        daemon=True
    )

    thread.start()


# ============================================================
# STOP STRESS
# ============================================================

def stop_stress():

    global stress_running
    global stress_memory

    stress_running = False

    stress_memory.clear()

    status_label.config(
        text="Status: Stress stopped - memory released"
    )


# ============================================================
# BUTTONS
# ============================================================

button_frame = tk.Frame(window)

button_frame.pack(pady=5)


start_button = tk.Button(
    button_frame,
    text="START STRESS",
    command=start_stress,
    font=("Arial", 13, "bold"),
    width=15,
    height=2
)

start_button.pack(side=tk.LEFT, padx=8)


stop_button = tk.Button(
    button_frame,
    text="STOP STRESS",
    command=stop_stress,
    font=("Arial", 13, "bold"),
    width=15,
    height=2
)

stop_button.pack(side=tk.LEFT, padx=8)


# ============================================================
# LIVE MONITORING
# ============================================================

def update_memory():

    global time_data
    global ram_data
    global swap_data
    global cpu_data

    # Get system information
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu = psutil.cpu_percent(interval=None)

    # Convert RAM values to GB
    total_ram = ram.total / (1024 ** 3)
    used_ram = ram.used / (1024 ** 3)

    # Convert swap values to GB
    total_swap = swap.total / (1024 ** 3)
    used_swap = swap.used / (1024 ** 3)

    # Update text
    ram_label.config(
        text=f"RAM Usage: {ram.percent:.1f}% "
             f"({used_ram:.2f} / {total_ram:.2f} GB)"
    )

    swap_label.config(
        text=f"Virtual Memory: {swap.percent:.1f}% "
             f"({used_swap:.2f} / {total_swap:.2f} GB)"
    )

    cpu_label.config(
        text=f"CPU Usage: {cpu:.1f}%"
    )

    # Update progress bars
    ram_bar["value"] = ram.percent
    swap_bar["value"] = swap.percent

    # Calculate elapsed time
    elapsed = time.time() - start_time

    # Store data
    time_data.append(elapsed)
    ram_data.append(ram.percent)
    swap_data.append(swap.percent)
    cpu_data.append(cpu)

    # Keep only the latest 60 readings
    if len(time_data) > 60:

        time_data.pop(0)
        ram_data.pop(0)
        swap_data.pop(0)
        cpu_data.pop(0)

    # Clear graph
    graph.clear()

    # Plot RAM
    graph.plot(
        time_data,
        ram_data,
        label="RAM",
        linewidth=2
    )

    # Plot virtual memory
    graph.plot(
        time_data,
        swap_data,
        label="Virtual Memory",
        linewidth=2
    )

    # Plot CPU
    graph.plot(
        time_data,
        cpu_data,
        label="CPU",
        linewidth=2
    )

    # Graph settings
    graph.set_title("Live System Resource Usage")

    graph.set_xlabel("Time (seconds)")

    graph.set_ylabel("Usage (%)")

    graph.set_ylim(0, 100)

    graph.grid(True)

    graph.legend()

    canvas.draw_idle()

    # Update every second
    window.after(
        1000,
        update_memory
    )


# ============================================================
# START MONITORING
# ============================================================

update_memory()


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()