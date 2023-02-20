#!/usr/bin/env python3
import json
from dataclasses import dataclass
from dataclasses import field
from itertools import cycle
from pathlib import Path
from typing import Optional

import customtkinter as ctk
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from pylib.spin_box import IntSpinbox
from tkinter import filedialog
from tkinter import messagebox

COLORS = """ red blue green black purple orange cyan olive gray pink """.split()


@dataclass
class Box:
    id: int = None
    x0: float = None
    y0: float = None
    x1: float = None
    y1: float = None
    start: bool = False

    def as_dict(self) -> dict:
        return {
            "x0": self.x0,
            "y0": self.y0,
            "x1": self.x1,
            "y1": self.y1,
            "start": self.start,
        }

    def too_small(self) -> bool:
        if abs(self.x1 - self.x0) < 20 or abs(self.y1 - self.y0) < 20:
            return True
        return False

    def point_hit(self, x, y) -> bool:
        x0, x1 = (self.x0, self.x1) if self.x1 > self.x0 else (self.x1, self.x0)
        y0, y1 = (self.y0, self.y1) if self.y1 > self.y0 else (self.y1, self.y0)
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
        return False


@dataclass
class Page:
    path: Path = None
    photo: ImageTk = None
    boxes: list = field(default_factory=list)

    def as_dict(self) -> dict:
        output = {
            "path": str(self.path),
            "photo_x": 0,
            "photo_y": 0,
            "boxes": [b.as_dict() for b in self.boxes],
        }
        if self.photo:
            output["photo_x"] = self.photo.width()
            output["photo_y"] = self.photo.height()
        return output

    def resize(self, canvas_height):
        if not self.photo:
            image = Image.open(self.path)
            image_width, image_height = image.size
            ratio = canvas_height / image_height
            new_width = int(image_width * ratio)
            new_height = int(image_height * ratio)
            resized = image.resize((new_width, new_height))
            self.photo = ImageTk.PhotoImage(resized)

    def filter(self, x=None, y=None):
        new = []
        for box in self.boxes:
            if x is not None and box.point_hit(x, y):
                continue
            elif x is None and box.too_small():
                continue
            new.append(box)
        self.boxes = new

    def find(self, x, y) -> Optional[Box]:
        for box in self.boxes:
            if box.point_hit(x, y):
                return box
        return None

    def all_box_ids(self) -> list[int]:
        return [b.id for b in self.boxes]


class App(ctk.CTk):
    row_span = 8

    def __init__(self):
        super().__init__()

        self.curr_dir = "."
        self.image_dir = None
        self.canvas = None
        self.pages = []
        self.colors = None
        self.dirty = False

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Slice images for OCR")

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0)  # noqa
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.image_frame = ctk.CTkFrame(master=self)
        self.image_frame.grid(row=0, column=0, rowspan=self.row_span, sticky="nsew")

        self.image_button = ctk.CTkButton(
            master=self, text="Choose image directory", command=self.get_image_dir
        )
        self.image_button.grid(row=0, column=1, padx=16, pady=16)

        self.load_button = ctk.CTkButton(master=self, text="Load", command=self.load)
        self.load_button.grid(row=1, column=1, padx=16, pady=16)

        self.save_button = ctk.CTkButton(
            master=self, text="Save", command=self.save, state="disabled"
        )
        self.save_button.grid(row=2, column=1, padx=16, pady=16)

        self.spinner = IntSpinbox(master=self, command=self.change_page, width=140)
        self.spinner.grid(row=3, column=1, padx=16, pady=16)

        self.action = tk.StringVar()
        self.action.set("add")
        self.radio_add = ctk.CTkRadioButton(
            master=self, variable=self.action, text="add", value="add"
        )
        self.radio_del = ctk.CTkRadioButton(
            master=self, variable=self.action, text="delete", value="delete"
        )
        self.radio_treatment = ctk.CTkRadioButton(
            master=self, variable=self.action, text="treatment start", value="start"
        )
        self.radio_add.grid(row=4, column=1, padx=16, pady=16)
        self.radio_del.grid(row=5, column=1, padx=16, pady=16)
        self.radio_treatment.grid(row=6, column=1, padx=16, pady=16)

        self.protocol("WM_DELETE_WINDOW", self.safe_quit)

    @property
    def index(self):
        return self.spinner.get() - 1

    @property
    def page(self):
        return self.pages[self.index]

    def change_page(self):
        if self.pages:
            self.display_page()

    def display_page(self):
        canvas_height = self.image_frame.winfo_height()
        self.page.resize(canvas_height)
        self.canvas.delete("all")
        self.canvas.create_image((0, 0), image=self.page.photo, anchor="nw")
        self.display_page_boxes()

    def display_page_boxes(self):
        self.clear_page_boxes()
        self.colors = cycle(COLORS)
        for box in self.page.boxes:
            color = next(self.colors)
            dash = (30, 20) if box.start else ()
            self.canvas.create_rectangle(
                box.x0, box.y0, box.x1, box.y1, outline=color, width=4, dash=dash
            )

    def clear_page_boxes(self):
        for i, id_ in enumerate(self.canvas.find_all()):
            if i:  # First object should be the page itself
                self.canvas.delete(id_)

    def on_canvas_press(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        if self.pages and self.action.get() == "add":
            self.dirty = True
            color = next(self.colors)
            id_ = self.canvas.create_rectangle(0, 0, 1, 1, outline=color, width=4)
            self.page.boxes.append(Box(id=id_, x0=x, y0=y, x1=x, y1=y))
        elif self.pages and self.action.get() == "delete":
            self.page.filter(x, y)
            self.display_page_boxes()
        elif self.pages and self.action.get() == "start":
            box = self.page.find(x, y)
            if box:
                box.start = not box.start
                self.display_page_boxes()

    def on_canvas_move(self, event):
        if self.pages and self.action.get() == "add":
            box = self.page.boxes[-1]
            box.x1 = self.canvas.canvasx(event.x)
            box.y1 = self.canvas.canvasy(event.y)
            self.canvas.coords(box.id, box.x0, box.y0, box.x1, box.y1)

    def on_canvas_release(self, _):
        if self.pages and self.action.get() == "add":
            self.page.filter()
            self.display_page_boxes()

    def save(self):
        if not self.pages:
            return

        path = tk.filedialog.asksaveasfilename(
            initialdir=self.curr_dir,
            title="Save image boxes",
            filetypes=(("json", "*.json"), ("all files", "*")),
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

        self.dirty = False

    def load(self):
        path = filedialog.askopenfilename(
            initialdir=self.curr_dir,
            title="Load image boxes",
            filetypes=(("json", "*.json"), ("all files", "*")),
        )
        if not path:
            return

        path = Path(path)
        self.curr_dir = path.parent

        if self.canvas is None:
            self.setup_canvas()

        with open(path) as in_json:
            pages = json.load(in_json)

        self.dirty = False
        self.pages = []
        data = []
        try:
            for page in pages:
                boxes = []
                for box in page["boxes"]:
                    boxes.append(
                        Box(
                            x0=box["x0"],
                            y0=box["y0"],
                            x1=box["x1"],
                            y1=box["y1"],
                            start=box["start"],
                        )
                    )
                data.append(Page(path=page["path"], boxes=boxes))

            self.pages = data
            self.spinner_update(len(data))
            self.save_button.configure(state="normal")
            self.display_page()

        except KeyError:
            messagebox.showerror(
                title="Load error", message="Could not load the JSON file"
            )
            self.pages = []
            self.save_button.configure(state="disabled")
            self.spinner_clear()
            self.canvas.delete("all")

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
        self.colors = cycle(COLORS)
        self.dirty = False

        paths = []
        for path in self.image_dir.glob("*"):
            if path.suffix.lower() in (".png", ".jpg", "jpeg", ".tiff"):
                paths.append(path)

        if paths:
            paths = sorted(p.name for p in paths)
            self.spinner_update(len(paths))
            self.pages = [Page(path=self.image_dir / p) for p in paths]
            self.save_button.configure(state="normal")
            self.display_page()
        else:
            self.pages = []
            self.save_button.configure(state="disabled")
            self.spinner_clear()
            self.canvas.delete("all")

    def spinner_update(self, high):
        self.spinner.low = 1
        self.spinner.high = high
        self.spinner.set(1)

    def spinner_clear(self):
        self.spinner.low = 0
        self.spinner.high = 0
        self.spinner.set(0)

    def safe_quit(self):
        if self.dirty:
            yes = messagebox.askyesno(
                self.title(), "Are you sure you want to exit without saving?"
            )
            if not yes:
                return
        self.destroy()


if __name__ == "__main__":
    APP = App()
    APP.mainloop()
