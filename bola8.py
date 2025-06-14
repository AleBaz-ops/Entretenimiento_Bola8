import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import random

RESPUESTAS = [
    "It is certain", "Without a doubt", "Yes definitely",
    "You may rely on it", "As I see it, yes", "Most likely",
    "Outlook good", "Yes", "Signs point to yes",
    "Reply hazy try again", "Ask again later", "Better not tell you now",
    "Cannot predict now", "Concentrate and ask again",
    "Don't count on it", "My reply is no", "My sources say no",
    "Outlook not so good", "Very doubtful", "No"
]

class Bola8:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Magic 8 Ball")
        self.window.geometry("600x800")
        self.window.configure(bg='#1a1a1a')
        
        # Question Entry
        self.question_frame = tk.Frame(self.window, bg='#1a1a1a')
        self.question_frame.pack(pady=20)
        
        self.question_label = tk.Label(self.question_frame, 
                                        text="Ask your question:",
                                        font=("Arial", 14),
                                        bg='#1a1a1a',
                                        fg='white')
        self.question_label.pack()
        
        self.question_entry = tk.Entry(self.question_frame,
                                        width=40,
                                        font=("Arial", 12))
        self.question_entry.pack(pady=10)
        
        # Shake Button
        self.shake_button = tk.Button(self.window,
                                       text="Shake",
                                       command=self.shake,
                                       bg='#4CAF50',
                                       fg='white',
                                       font=("Arial", 12),
                                       width=15)
        self.shake_button.pack(pady=10)
        
        # Answer Label
        self.answer_label = tk.Label(self.window,
                                      text="",
                                      font=("Arial", 14, "bold"),
                                      bg='#1a1a1a',
                                      fg='white',
                                      wraplength=400)
        self.answer_label.pack(pady=20)
        
        # 3D Ball Display
        self.fig = plt.figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack()
        
        self.draw_ball()
        
    def draw_ball(self, answer_visible=False):
        self.ax.clear()
        
        # Create sphere
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot the surface
        self.ax.plot_surface(x, y, z, color='black', alpha=1)
        
        # Add white circle around number 8
        circle_radius = 0.25
        circle_theta = np.linspace(0, 2*np.pi, 100)
        circle_x = circle_radius * np.cos(circle_theta)
        circle_y = -0.5 + circle_radius * np.sin(circle_theta)
        circle_z = np.full_like(circle_theta, 0.9)
        self.ax.plot(circle_x, circle_y, circle_z, color='white', linewidth=2)
        
        # Add number 8
        self.ax.text(0, -0.5, 0.87, "8", color='white', fontsize=30, 
                     fontweight='bold', ha='center', va='center')
        
        if answer_visible:
            # Add a triangle centered below the number 8
            triangle_size = 0.3
            vertices = np.array([
                [0, -0.5 - triangle_size, 0.85],  # Bottom point
                [-triangle_size, -0.5 + triangle_size, 0.85],  # Left point
                [triangle_size, -0.5 + triangle_size, 0.85]   # Right point
            ])
            
            # Plot triangle using 3D line segments
            self.ax.plot([vertices[0][0], vertices[1][0]], 
                         [vertices[0][1], vertices[1][1]], 
                         [vertices[0][2], vertices[1][2]], color='red', linewidth=2)
            self.ax.plot([vertices[1][0], vertices[2][0]], 
                         [vertices[1][1], vertices[2][1]], 
                         [vertices[1][2], vertices[2][2]], color='red', linewidth=2)
            self.ax.plot([vertices[2][0], vertices[0][0]], 
                         [vertices[2][1], vertices[0][1]], 
                         [vertices[2][2], vertices[0][2]], color='red', linewidth=2)
        
        # Adjust viewing angle for better visibility
        self.ax.set_box_aspect([1, 1, 1])
        self.ax.view_init(elev=20, azim=45 if not answer_visible else 0)  # Fixed angle to show triangle
        self.ax.axis('off')
        
        # Update canvas
        self.canvas.draw()
    
    def shake(self):
        if not self.question_entry.get().strip():
            self.answer_label.config(text="Please ask a question first!")
            return
        
        self.shake_button.config(state='disabled')
        self.answer_label.config(text="Shaking...")
        
        # Animation effect
        for _ in range(10):
            self.ax.view_init(elev=random.randint(0, 360), 
                              azim=random.randint(0, 360))
            self.canvas.draw()
            self.window.update()
            self.window.after(100)
        
        # Show answer
        answer = random.choice(RESPUESTAS)
        self.answer_label.config(text=answer)
        self.draw_ball(answer_visible=True)
        self.shake_button.config(state='normal')
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Bola8()
    app.run()