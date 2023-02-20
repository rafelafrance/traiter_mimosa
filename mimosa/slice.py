#!/usr/bin/env python3
import json
from dataclasses import dataclass
from dataclasses import field
from itertools import cycle
from pathlib import Path
from typing import Any

import customtkinter as ctk
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from pylib.spin_box import IntSpinbox
from tkinter import filedialog


COLORS = """ red blue green black purple orange cyan olive gray """.split()


@dataclass
class Page:
    path: Path = None
    _image: Image = None
    resized: Image = None
    photo: ImageTk = None
    boxes: list = field(default_factory=list)

    def as_dict(self):
        return {
            "path": self.path,
            "resized_x": self.resized.size[0],
            "resized_y": self.resized.size[1],
            "boxes": [b.as_dict() for b in self.boxes],
        }

    @property
    def image(self):
        if not self._image:
            self._image = Image.open(self.path)
        return self._image

    def resize(self, canvas_height):
        if not self.resized:
            image_width, image_height = self.image.size
            ratio = canvas_height / image_height
            new_width = int(image_width * ratio)
            new_height = int(image_height * ratio)
            self.resized = self.image.resize((new_width, new_height))
            self.photo = ImageTk.PhotoImage(self.resized)

    def filter_small_boxes(self, canvas):
        new = []
        for box in self.boxes:
            if abs(box.x1 - box.x0) < 20 or abs(box.y1 - box.y0) < 20:
                canvas.delete(box.id)
            else:
                new.append(box)
        self.boxes = new

    def filter_point_boxes(self, canvas, x, y):
        new = []
        for box in self.boxes:
            x0, x1 = (box.x0, box.x1) if box.x1 > box.x0 else (box.x1, box.x0)
            y0, y1 = (box.y0, box.y1) if box.y1 > box.y0 else (box.y1, box.y0)
            if x0 <= x <= x1 and y0 <= y <= y1:
                print(f"{box.id=}")
                canvas.delete(box.id)
            else:
                new.append(box)
        print(new)
        self.boxes = new


@dataclass
class Box:
    x0: float = None
    y0: float = None
    x1: float = None
    y1: float = None
    color: str = ""
    id: Any = None

    def as_dict(self):
        return {"x0": self.x0, "y0": self.y0, "x1": self.x1, "y1": self.y1}


class App(ctk.CTk):
    row_span = 7

    def __init__(self):
        super().__init__()

        self.curr_dir = "."
        self.image_dir = None
        self.canvas = None
        self.pages = []
        self.colors = None

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Slice images for OCR")

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)  # noqa
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.image_frame = ctk.CTkFrame(master=self)
        self.image_frame.grid(row=0, column=0, rowspan=self.row_span, sticky="nsew")

        self.image_button = ctk.CTkButton(
            master=self, text="Choose image directory", command=self.get_image_dir
        )
        self.image_button.grid(row=0, column=1, padx=16, pady=16)

        self.save_button = ctk.CTkButton(master=self, text="Save", command=self.save)
        self.save_button.grid(row=1, column=1, padx=16, pady=16)

        self.spinner = IntSpinbox(master=self, command=self.change_image, width=140)
        self.spinner.grid(row=2, column=1, padx=16, pady=16)

        self.action = tk.StringVar()
        self.action.set("add")
        self.radio_add = ctk.CTkRadioButton(
            master=self, variable=self.action, text="add", value="add"
        )
        self.radio_del = ctk.CTkRadioButton(
            master=self, variable=self.action, text="delete", value="delete"
        )
        self.radio_add.grid(row=4, column=1, padx=16, pady=16)
        self.radio_del.grid(row=5, column=1, padx=16, pady=16)

    @property
    def index(self):
        return self.spinner.get() - 1

    @property
    def page(self):
        return self.pages[self.index]

    def change_image(self):
        if not self.pages:
            return
        self.display_page()

    def setup_canvas(self):
        self.update()

        self.canvas = ctk.CTkCanvas(
            master=self.image_frame,
            width=self.image_frame.winfo_width(),
            height=self.image_frame.winfo_height(),
            background="black",
            cursor="cross",
        )
        self.canvas.grid(row=0, column=0, rowspan=self.row_span, sticky="nsew")

        self.canvas.bind("<ButtonPress-1>", self.on_canvas_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

    def display_page(self):
        canvas_height = self.image_frame.winfo_height()
        self.page.resize(canvas_height)
        self.canvas.create_image((0, 0), image=self.page.photo, anchor="nw")
        self.display_page_boxes()

    def display_page_boxes(self):
        self.colors = cycle(COLORS)
        for box in self.page.boxes:
            color = next(self.colors)
            self.canvas.create_rectangle(
                box.x0, box.y0, box.x1, box.y1, outline=color, width=4
            )

    def on_canvas_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.action.get() == "add":
            color = next(self.colors)
            id_ = self.canvas.create_rectangle(0, 0, 1, 1, outline=color, width=4)
            self.page.boxes.append(Box(x0=x, y0=y, x1=x, y1=y, color=color, id=id_))
        else:
            self.page.filter_point_boxes(self.canvas, x, y)
            self.display_page_boxes()

    def on_canvas_move(self, event):
        if self.action.get() == "add":
            box = self.page.boxes[-1]
            box.x1 = self.canvas.canvasx(event.x)
            box.y1 = self.canvas.canvasy(event.y)
            self.canvas.coords(box.id, box.x0, box.y0, box.x1, box.y1)

    def on_canvas_release(self, _):
        if self.action.get() == "add":
            pass
            # self.page.filter_small_boxes(self.canvas)
            # self.display_page_boxes()

    def save(self):
        if not self.pages:
            return

        path = tk.filedialog.asksaveasfilename(
            initialdir=self.curr_dir,
            title="Save image boxes",
            filetypes=(("json", "*.json"), ("all files", "*.*")),
        )

        if not path:
            return

        path = Path(path)
        self.curr_dir = path.parent

        output = []
        for page in self.pages:
            output.append(page.as_dict())

        with open(path, "w") as out_json:
            json.dump(output, out_json, indent=4)

    def get_image_dir(self):
        image_dir = filedialog.askdirectory(
            initialdir=self.curr_dir, title="Choose image directory"
        )
        if not image_dir:
            return

        if self.canvas is None:
            self.setup_canvas()

        self.curr_dir = image_dir
        self.image_dir = Path(image_dir)
        paths = []
        for image_dir in self.image_dir.glob("*"):
            if image_dir.suffix.lower() in (".png", ".jpg", "jpeg", ".tiff"):
                paths.append(image_dir)
        if not paths:
            return

        paths = sorted(p.name for p in paths)

        self.spinner.low = 1
        self.spinner.high = len(paths)
        self.spinner.set(1)

        self.pages = [Page(path=self.image_dir / p) for p in paths]
        self.display_page()


if __name__ == "__main__":
    APP = App()
    APP.mainloop()
