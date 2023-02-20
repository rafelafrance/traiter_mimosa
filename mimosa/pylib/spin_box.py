from typing import Callable
from typing import Union

import customtkinter as ctk


class IntSpinbox(ctk.CTkFrame):
    def __init__(
        self,
        *args,
        width: int = 100,
        height: int = 32,
        step_size: int = 1,
        command: Callable = None,
        start: int = 0,
        low: int = 0,
        high: int = 0,
        **kwargs,
    ):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.low = low
        self.high = high

        self.grid_columnconfigure((0, 2), weight=0)  # noqa
        self.grid_columnconfigure(1, weight=1)

        self.subtract_button = ctk.CTkButton(
            self,
            text="-",
            width=height - 6,
            height=height - 6,
            command=self.subtract_button_callback,
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(
            self,
            width=width - (2 * height),
            height=height - 6,
            border_width=0,
            justify="center",
        )
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(
            self,
            text="+",
            width=height - 6,
            height=height - 6,
            command=self.add_button_callback,
        )
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        self.entry.insert(0, str(int(start)))

    def add_button_callback(self):
        try:
            value = int(self.entry.get()) + self.step_size
            if value > self.high:
                value = self.high
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None:
            self.command()

    def subtract_button_callback(self):
        try:
            value = int(self.entry.get()) - self.step_size
            if value < self.low:
                value = self.low
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return
        if self.command is not None:
            self.command()

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))
