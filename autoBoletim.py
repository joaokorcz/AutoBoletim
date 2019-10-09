import os
import time
from pynput.keyboard import Key, Controller
import pyscreenshot as ImageGrab
import pytesseract
from PIL import Image
from PIL import ImageChops
import PIL.ImageOps


def inputDados():
    loginBaiano = input('Informe seu RA (aNNNNNNN): ')
    senhaBaiano = input('Informe sua senha: ')
    print(' -\n'*44)
    return loginBaiano, senhaBaiano


def abreBoletim():
    os.system('start https://utfws.utfpr.edu.br/aluno03/sistema/mpboletim.inicioAluno?p_pesscodnr=181783\"&\"p_curscodnr=14\"&\"p_alcuordemnr=1')
    time.sleep(5)


def insereCredenciais(loginBaiano, senhaBaiano):
    keyboard = Controller()
    keyboard.type(loginBaiano)
    keyboard.press(Key.tab)
    keyboard.type(senhaBaiano)
    keyboard.press(Key.enter)
    time.sleep(1)


def tiraPrint():
    #imM = ImageGrab.grab(bbox=(273, 287, 594, 806))
    # imM.save('materias.png')
    #imS = ImageChops.multiply(imM, imN)
    # imS.save('teste.png')
    imC = Image.open('compara.png')
    yS = 253
    yL = 271
    aM = 260
    bM = 278
    for ix in range(1, 15):
        aM += 37
        bM += 37
        yS += 37
        yL += 37
        imM = ImageGrab.grab(bbox=(273, aM, 594, bM))
        imM.save(f'materia{ix}.png')
        im = ImageGrab.grab(bbox=(1311, yS, 1349, yL))
        imV = ImageChops.add(im, imC)
        #imV = imV.convert("L")
        #imV = PIL.ImageOps.invert(imV)
        imV.save(f'notas{ix}.png')
        time.sleep(0.05)


def encontraTexto():
    m = []
    n = []
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract"
    for ix in range(1, 15):
        im = Image.open(f'materia{ix}.png')
        text = pytesseract.image_to_string(im)
        m.append(text)
    for ix in range(1, 15):
        im = Image.open(f'notas{ix}.png').convert("L")
        text = pytesseract.image_to_string(im)
        text = text.replace(',', '.')
        n.append(text)
    return m, n


def fechaAba():
    keyboard = Controller()
    keyboard.press(Key.ctrl_l)
    keyboard.press('w')
    keyboard.release('w')
    keyboard.release(Key.ctrl_l)


def apresentaResultado(materias, notas):
    print('-----------------')
    for i in range(len(materias)):
        n = int(float(notas[i]) * 10)
        ft = 240 - (n*4)
        print('-',materias[i])
        print('- Faltam:',ft,'pontos\n-----------------')


def main():
    l, s = inputDados()
    abreBoletim()
    insereCredenciais(l, s)
    tiraPrint()
    fechaAba()
    materias, notas = encontraTexto()
    apresentaResultado(materias, notas)
    input('PRESSIONE [ENTER] PARA FECHAR!')
    

main()
