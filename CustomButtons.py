import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.text import Text

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

class CustomRadioButtons:
    def __init__(self, ax, labels, active=0, callback=None, zorder=1):
        self.ax = ax
        self.labels = labels
        self.active = active
        self.callback = callback
        self.zorder = zorder

        self.circles = []
        self.inner_circles = [None] * len(labels)
        self.texts = []
        self.create_radio_buttons()

        self.ax.figure.canvas.mpl_connect("button_press_event", self.on_click)

    def create_radio_buttons(self):
        self.ax.set_xlim(-0.5, 1)
        self.ax.set_ylim(-len(self.labels), 1)
        self.ax.axis("off")

        for i, label in enumerate(self.labels):
            circle = Circle((0, -i), 0.2, edgecolor="black", facecolor="white", zorder=self.zorder)
            self.ax.add_patch(circle)
            self.circles.append(circle)

            if i == self.active:
                inner_circle = Circle((0, -i), 0.2, color="black", zorder=self.zorder + 1)
                self.ax.add_patch(inner_circle)
                self.inner_circles[i] = inner_circle

            text = self.ax.text(0.5, -i, label, va="center", ha="left", zorder=self.zorder + 1)
            self.texts.append(text)

    def on_click(self, event):
        for i, circle in enumerate(self.circles):
            if circle.contains_point((event.x, event.y)):
                self.set_active(i)
                if self.callback:
                    self.callback(self.labels[i])
                break

    def set_active(self, index):
        if self.inner_circles[self.active]:
            self.inner_circles[self.active].remove()
            self.inner_circles[self.active] = None

        self.active = index
        inner_circle = Circle((0, -index), 0.2, color="black", zorder=self.zorder + 1)
        self.ax.add_patch(inner_circle)
        self.inner_circles[index] = inner_circle

        self.ax.figure.canvas.draw()

class CustomCheckButtons:
    def __init__(self, ax, labels, active=[], callback=None, zorder=1):
        self.ax = ax
        self.labels = labels
        self.active = active
        self.callback = callback
        self.zorder = zorder

        self.boxes = []
        self.inner_boxes = []
        self.texts = []
        self.create_check_buttons()

        self.ax.figure.canvas.mpl_connect("button_press_event", self.on_click)

    def create_check_buttons(self):
        self.ax.set_xlim(-0.5, 1)
        self.ax.set_ylim(-len(self.labels), 1)
        self.ax.axis("off")

        for i, label in enumerate(self.labels):
            box = Rectangle((-0.2, -i - 0.2), 0.4, 0.4, edgecolor="black", facecolor="white", zorder=self.zorder)
            self.ax.add_patch(box)
            self.boxes.append(box)

            if i in self.active:
                inner_box = Rectangle((-0.2, -i - 0.2), 0.4, 0.4, edgecolor="black", facecolor="black", zorder=self.zorder + 1)
                self.ax.add_patch(inner_box)
                self.inner_boxes.append(inner_box)
            else:
                self.inner_boxes.append(None)

            text = self.ax.text(0.5, -i, label, va="center", ha="left", zorder=self.zorder + 1)
            self.texts.append(text)

    def on_click(self, event):
        for i, box in enumerate(self.boxes):
            if box.contains_point((event.x, event.y)):
                self.toggle_active(i)
                if self.callback:
                    self.callback(self.labels[i])
                break

    def toggle_active(self, index):
        if index in self.active:
            self.active.remove(index)
            if self.inner_boxes[index]:
                self.inner_boxes[index].remove()
                self.inner_boxes[index] = None
        else:
            self.active.append(index)
            inner_box = Rectangle((-0.2, -index - 0.2), 0.4, 0.4, edgecolor="black", facecolor="black", zorder=self.zorder + 1)
            self.ax.add_patch(inner_box)
            self.inner_boxes[index] = inner_box

        self.ax.figure.canvas.draw()
