import cv2
import numpy as np
from ctypes import windll
import win32gui
import win32ui

class WindowCapture:
    def __init__(self, window_name):
        self.window_name = window_name

    def capture(self):
        windll.user32.SetProcessDPIAware()
        hwnd = win32gui.FindWindow(None, self.window_name)

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :-1]

        if not result:
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            raise RuntimeError(f"Não foi possível obter a captura da tela! Resultado: {result}")

        return img

# Localiza uma imagem compativel com um "template" salvo
class TemplateMatcher:
    def __init__(self, template_path):
        self.template_path = template_path

    def find_template(self, screenshot):
        template = cv2.imread(self.template_path, cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8
        if max_val >= threshold:
            template_height, template_width = template.shape[:2]
            match_location = (max_loc[0] + template_width // 2, max_loc[1] + template_height // 2)
            return match_location
        else:
            return None
        
class TemplateSupMatcher:
    def __init__(self, template_path):
        self.template_path = template_path

    def find_template(self, screenshot):
        template = cv2.imread(self.template_path, cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8
        if max_val >= threshold:
            match_location = max_loc
            return match_location
        else:
            return None
        
# Localiza as coordenadas do canto superior da imagem 
def LocateImage(image, window_name, Region=None, Precision=0.8):
    window_capture = WindowCapture(window_name)
    template_matcher = TemplateSupMatcher(image)

    screenshot = window_capture.capture()
    if Region is not None:
        x, y, width, height = Region
        screenshot = screenshot[y:y+height, x:x+width]

    template_location = template_matcher.find_template(screenshot)

    if template_location is not None:
        # Retornar as coordenadas do canto superior esquerdo da imagem
        x, y, *_ = template_location
        if Region is not None:
            x += Region[0]
            y += Region[1]
        return x, y

    return 0,0

def LocateImage2(image, window_name, Region=None, Precision=0.8):
    window_capture = WindowCapture(window_name)
    template_matcher = TemplateMatcher(image)

    screenshot = window_capture.capture()
    if Region is not None:
        x, y, width, height = Region
        screenshot = screenshot[y:y+height, x:x+width]

    template_location = template_matcher.find_template(screenshot)

    if template_location is not None:
        # Retornar as coordenadas do canto superior esquerdo da imagem
        x, y, *_ = template_location
        if Region is not None:
            x += Region[0]
            y += Region[1]
        return x, y

    return 0,0

# Localiza as coordenadas centro da imagem 
def LocateImageCenter(image, window_name, Region=None, Precision=0.8):
    template_location = LocateImage2(image, window_name, Region, Precision)

    if template_location != (0, 0):
        x, y = template_location
        if Region is not None:
            # Retornar as coordenadas do centro da imagem
            x += Region[0]
            y += Region[1]
        return x, y

    # Caso nenhum template seja encontrado, retornar (0, 0)
    return 0, 0

# Localiza todas as coordenadas do canto superior esquerdo das imagens compatíveis com o template
def LocateAllImages(image, window_name, Region=None, Precision=0.8):
    window_capture = WindowCapture(window_name)
    template_matcher = TemplateMatcher(image)

    screenshot = window_capture.capture()
    if Region is not None:
        x, y, width, height = Region
        screenshot = screenshot[y:y+height, x:x+width]

    template_count = 0  # Variável para contar o número de ocorrências do template

    while True:
        template_location = template_matcher.find_template(screenshot)
        
        if template_location is not None:
            # Adicionar as coordenadas do canto superior esquerdo da imagem à lista
            x, y, *_ = template_location

            template_count += 1  # Incrementar o contador de ocorrências

            # Atualizar a região de busca para encontrar outras ocorrências
            if Region is not None:
                x += Region[0]
                y += Region[1]
                screenshot = screenshot[:y, :x]
            else:
                screenshot = screenshot[:y, :x]
        else:
            break

    return template_count