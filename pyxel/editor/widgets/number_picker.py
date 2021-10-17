import pyxel

from .settings import INPUT_FIELD_COLOR, INPUT_TEXT_COLOR
from .text_button import TextButton
from .widget import Widget
from .widget_variable import WidgetVariable


class NumberPicker(Widget):
    """
    Variables:
        is_visible_var
        is_enabled_var
        value_var

    Events:
        change (value)
        show
        hide
        enabled
        disabled
        mouse_down (key, x, y)
        mouse_up (key, x, y)
        mouse_drag (key, x, y, dx, dy)
        mouse_repeat (key, x, y)
        mouse_click (key, x, y)
        mouse_hover (x, y)
        update
        draw
    """

    def __init__(self, parent, x, y, min_value, max_value, value, **kwargs):
        self._number_len = max(len(str(min_value)), len(str(max_value)))
        width = self._number_len * 4 + 21
        height = 7
        super().__init__(parent, x, y, width, height, **kwargs)

        self._min_value = min_value
        self._max_value = max_value

        self.dec_button = TextButton(self, x, y, "-")
        self.dec_button.add_event_listener("press", self.__on_dec_button_press)
        self.dec_button.add_event_listener("repeat", self.__on_dec_button_press)

        self.inc_button = TextButton(self, x + width - 7, y, "+")
        self.inc_button.add_event_listener("press", self.__on_inc_button_press)
        self.inc_button.add_event_listener("repeat", self.__on_inc_button_press)

        self.value_var = WidgetVariable(value)
        self.value_var.add_event_listener("set", self.__on_value_set)
        self.value_var.add_event_listener("change", self.__on_value_change)

        self.add_event_listener("draw", self.__on_draw)

    def __on_dec_button_press(self):
        offset = 10 if pyxel.btn(pyxel.KEY_SHIFT) else 1
        self.value_var.v = self.value_var.v - offset

    def __on_inc_button_press(self):
        offset = 10 if pyxel.btn(pyxel.KEY_SHIFT) else 1
        self.value_var.v = self.value_var.v + offset

    def __on_value_set(self, value):
        return min(max(value, self._min_value), self._max_value)

    def __on_value_change(self, value):
        self.dec_button.is_enabled_var.v = self.value_var.v > self._min_value
        self.inc_button.is_enabled_var.v = self.value_var.v < self._max_value

        self.trigger_event("change", value)

    def __on_draw(self):
        pyxel.rect(self.x + 9, self.y, self.width - 18, self.height, INPUT_FIELD_COLOR)
        pyxel.text(
            self.x + 11,
            self.y + 1,
            ("{:>" + str(self._number_len) + "}").format(self.value_var.v),
            INPUT_TEXT_COLOR,
        )