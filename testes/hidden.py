import cv2
import numpy as np
from ctypes import windll
import win32gui
import win32ui
import pyautogui


def capture_win_alt(window_name: str):
    # Adaptado de https://stackoverflow.com/questions/19695214/screenshot-of-inactive-window-printwindow-win32gui

    windll.user32.SetProcessDPIAware()  # Torna o processo DPI-aware
    hwnd = win32gui.FindWindow(None, window_name)  # Encontra o identificador da janela pelo nome

    left, top, right, bottom = win32gui.GetClientRect(hwnd)  # Obtém as coordenadas do retângulo da janela
    w = right - left  # Calcula a largura da janela
    h = bottom - top  # Calcula a altura da janela

    hwnd_dc = win32gui.GetWindowDC(hwnd)  # Obtém o contexto do dispositivo da janela
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)  # Cria um contexto de dispositivo a partir do contexto da janela
    save_dc = mfc_dc.CreateCompatibleDC()  # Cria um contexto de dispositivo compatível para salvar
    bitmap = win32ui.CreateBitmap()  # Cria um objeto de bitmap
    bitmap.CreateCompatibleBitmap(mfc_dc, w, h)  # Cria um bitmap compatível com o contexto de dispositivo
    save_dc.SelectObject(bitmap)  # Seleciona o bitmap no contexto de dispositivo de salvamento

    # Se o Special K estiver sendo executado, esse número é 3. Caso contrário, é 1
    result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)  # Captura a janela no bitmap

    bmpinfo = bitmap.GetInfo()  # Obtém informações do bitmap
    bmpstr = bitmap.GetBitmapBits(True)  # Obtém os bits do bitmap como uma sequência de bytes

    img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
    img = np.ascontiguousarray(img)[..., :-1]  # Converte o formato da imagem e remove o canal alfa

    if not result:  # O resultado deve ser 1 se a captura foi bem-sucedida
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)
        raise RuntimeError(f"Não foi possível obter a captura da tela! Resultado: {result}")

    return img

def find_template(template_path, screenshot):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        template_height, template_width = template.shape[:2]
        match_location = (max_loc[0] + template_width // 2, max_loc[1] + template_height // 2)
        return match_location
    else:
        return None

def main():
    WINDOW_NAME = "Projetor em tela cheia (prévia)"
    template_path = "club.png"
    
    while cv2.waitKey(1) != ord('q'):  # Espera pela tecla 'q' para encerrar o programa
        screenshot = capture_win_alt(WINDOW_NAME)
        # cv2.imshow('Computer Vision', screenshot) # Mostra em fullscreen a tela gravada

        template_location = find_template(template_path, screenshot)
        if template_location:
            # print("Template encontrado nas coordenadas:", template_location)
            pyautogui.moveTo(template_location)
            pyautogui.leftClick()
            break

if __name__ == '__main__':
    main()
