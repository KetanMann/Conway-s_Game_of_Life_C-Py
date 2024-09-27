import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.colors as colors

class ConwayGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Conway's Game of Life")
        
        # Increase the window size
        self.master.geometry("800x900")  # Adjust these values as needed
        
        self.size_label = tk.Label(master, text="Grid Size:")
        self.size_label.pack()
        
        self.size_entry = tk.Entry(master)
        self.size_entry.pack()
        
        self.create_button = tk.Button(master, text="Create Grid", command=self.create_grid)
        self.create_button.pack()
        
        self.start_button = tk.Button(master, text="Start Simulation", command=self.start_simulation, state=tk.DISABLED)
        self.start_button.pack()
        
        self.reset_button = tk.Button(master, text="Reset", command=self.reset, state=tk.DISABLED)
        self.reset_button.pack()
        
        # Increase the figure size
        self.fig, self.ax = plt.subplots(figsize=(10, 10))  # Increased from (6, 6) to (10, 10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)  # Allow the canvas to expand
        
        self.grid = None
        self.N = None
        self.img = None
        self.cmap = colors.ListedColormap(['white', 'red'])
        self.ani = None
        self.click_cid = None
        self.generation = 0
        self.generation_text = None
    
    def create_grid(self):
        try:
            self.N = int(self.size_entry.get())
            if self.N <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer for grid size.")
            return
        
        self.grid = np.zeros((self.N, self.N))
        self.ax.clear()
        self.img = self.ax.imshow(self.grid, cmap=self.cmap, vmin=0, vmax=1, interpolation='nearest')
        
        # Set the correct extent for the imshow
        self.ax.set_xlim(-0.5, self.N - 0.5)
        self.ax.set_ylim(self.N - 0.5, -0.5)
        
        # Create grid lines
        self.draw_grid_lines()
        
        self.ax.set_xticks(np.arange(0, self.N, 1))
        self.ax.set_yticks(np.arange(0, self.N, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        
        # Add generation counter
        self.generation = 0
        self.generation_text = self.ax.text(0.02, 0.98, f"Generation: {self.generation}", 
                                            transform=self.ax.transAxes, ha='left', va='top')
        
        self.canvas.draw()
        
        if self.click_cid is not None:
            self.canvas.mpl_disconnect(self.click_cid)
        self.click_cid = self.canvas.mpl_connect('button_press_event', self.on_click)
        self.start_button['state'] = tk.NORMAL
        self.reset_button['state'] = tk.NORMAL
    
    def draw_grid_lines(self):
        for x in range(self.N + 1):
            self.ax.axvline(x - 0.5, color='black', linewidth=1)
            self.ax.axhline(x - 0.5, color='black', linewidth=1)
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        col = int(event.xdata + 0.5)
        row = int(event.ydata + 0.5)
        if 0 <= row < self.N and 0 <= col < self.N:
            self.grid[row, col] = 1 - self.grid[row, col]  # Toggle cell state
            self.img.set_data(self.grid)
            self.canvas.draw_idle()
    
    def start_simulation(self):
        if self.click_cid is not None:
            self.canvas.mpl_disconnect(self.click_cid)
        self.start_button['state'] = tk.DISABLED
        self.generation = 0
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=200,
                                           interval=200, blit=False)
        self.canvas.draw()
    
    def update(self, frame):
        new_grid = self.grid.copy()
        for i in range(self.N):
            for j in range(self.N):
                total = int((self.grid[i, (j-1)%self.N] + self.grid[i, (j+1)%self.N] +
                             self.grid[(i-1)%self.N, j] + self.grid[(i+1)%self.N, j] +
                             self.grid[(i-1)%self.N, (j-1)%self.N] + self.grid[(i-1)%self.N, (j+1)%self.N] +
                             self.grid[(i+1)%self.N, (j-1)%self.N] + self.grid[(i+1)%self.N, (j+1)%self.N]))
                if self.grid[i, j] == 1:
                    if (total < 2) or (total > 3):
                        new_grid[i, j] = 0
                else:
                    if total == 3:
                        new_grid[i, j] = 1
        self.grid = new_grid
        self.img.set_data(self.grid)
        
        # Redraw grid lines
        self.draw_grid_lines()
        
        # Update generation counter
        self.generation += 1
        self.generation_text.set_text(f"Generation: {self.generation}")
        
        return [self.img, self.generation_text]
    
    def reset(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        self.grid = np.zeros((self.N, self.N))
        self.img.set_data(self.grid)
        self.generation = 0
        self.generation_text.set_text(f"Generation: {self.generation}")
        self.draw_grid_lines()
        self.canvas.draw()
        if self.click_cid is not None:
            self.canvas.mpl_disconnect(self.click_cid)
        self.click_cid = self.canvas.mpl_connect('button_press_event', self.on_click)
        self.start_button['state'] = tk.NORMAL

root = tk.Tk()
gui = ConwayGUI(root)
root.mainloop()