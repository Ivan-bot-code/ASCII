import cv2
import numpy as np


class ASCIIConverter:
    def __init__(self, width=160, height=60):  # Увеличил разрешение
        self.width = width
        self.height = height
        self.ascii_chars = "@%#*+=-:. "  # Более детальная градация
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.2  # Уменьшил размер шрифта для большего разрешения
        self.font_color = (0, 255, 0)
        self.line_type = 1
        self.char_width = 4  # Ширина символа в пикселях
        self.char_height = 8  # Высота символа в пикселях

    def convert_frame(self, frame):
        # Изменяем размер с сохранением пропорций
        small_frame = cv2.resize(frame, (self.width, self.height))
        gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

        # Создаем изображение для ASCII арта с увеличенным разрешением
        ascii_image = np.zeros((self.height * self.char_height,
                                self.width * self.char_width, 3), dtype=np.uint8)

        for y in range(self.height):
            for x in range(self.width):
                pixel = gray_frame[y, x]
                char_index = int(pixel / 255 * (len(self.ascii_chars) - 1))
                char = self.ascii_chars[char_index]

                # Рисуем символ с улучшенным позиционированием
                cv2.putText(ascii_image, char,
                            (x * self.char_width, y * self.char_height + 6),
                            self.font,
                            self.font_scale,
                            self.font_color,
                            self.line_type)

        return ascii_image


def main():
    # Создаем конвертер с высоким разрешением
    converter = ASCIIConverter(width=200, height=80)  # Еще большее разрешение

    # Открываем камеру с лучшими настройками
    cap = cv2.VideoCapture(0)

    # Пытаемся установить максимальное разрешение камеры
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    print("Разрешение ASCII:", converter.width, "x", converter.height)
    print("Нажмите 'q' для выхода")
    print("Нажмите '+' для увеличения детализации")
    print("Нажмите '-' для уменьшения детализации")

    current_width = converter.width
    current_height = converter.height

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_art = converter.convert_frame(frame)
        cv2.imshow('ASCII Camera - High Resolution', ascii_art)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('+'):
            # Увеличиваем детализацию
            current_width = min(current_width + 20, 300)
            current_height = min(current_height + 10, 120)
            converter = ASCIIConverter(width=current_width, height=current_height)
            print(f"Увеличено до: {current_width}x{current_height}")
        elif key == ord('-'):
            # Уменьшаем детализацию
            current_width = max(current_width - 20, 60)
            current_height = max(current_height - 10, 30)
            converter = ASCIIConverter(width=current_width, height=current_height)
            print(f"Уменьшено до: {current_width}x{current_height}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()