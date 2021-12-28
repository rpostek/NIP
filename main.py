from litex.regon import REGONAPI, REGONAPIError
import pyperclip
import PySimpleGUI as sg

copy_image = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAEIUExURQUFBePj47+/vwMDA9jY2PPz84+Pj6CgnxMTExAQEB0dHaampgAAAPf398LCwgEBAc3NzAsLCxEREcPDw+Tk5PHx8QkJCbi4t6mpqe/v7w4ODszMzNfX1wQEBPj4+MfHxwoKCvv7+6GhoJCQkOrq6qOjo15eXvLy8pmZmfn5+fz8/AYGBpOTk6urqhAQDxYWFj4+Punp6QYGBebm5qysq6enpqKiosvLy7m5udDQz7S0s7GxsaSkpK2trLOzsrCwsOXl5c7OzXp6eba2tvX19aKioZKSkh4eHiQkJIuLi56enhQUFPf39hUVFaWlpQ0NDSEhIU9PTxsbG+7u7kdHRxoaGv39/f///xhyacIAAABYdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wB4m8IIAAABA0lEQVR42mIIJwAYwvDLhxFWQNAKqrnBRVeJHQpcbXmxKGDkF+SAAjFZQyyOZGSwkINqdFZQweJIRga+8HBpYT4+PmFPsWAsjmRkYApn1efRZmBgkOVRU8TiBpACIR1jEREHVQaeQF7sCjglQExxKXmPEFFMR4IUcIOYVjxeTjwGohiOhCvgC/AODeKXweZIiAItXl45eWYZrG7ghrnNkpkFvwIBhIJw/AqQHCkczivkh0UBzAojO0kRPWxWwGOTQVCQ3wSmQBpDgY+4tb2pggRMgSOGI8FAyCY8DAzCzTEcCQLq/lLuXBDgy8OCJU1qmrmxQYGyhiTR+WIwZBxCJgAEGABXKCGxnYE3RwAAAABJRU5ErkJggg=='

def get_data(nip):
    api = REGONAPI("https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc")
    api.login("abcde12345abcde12345")

    entities = api.search(nip=nip)
    addr = entities[0]['Ulica'].__str__() + ' ' + entities[0]['NrNieruchomosci'].__str__()
    if len(entities[0]['NrLokalu'].__str__()):
        addr = addr + ' lok.' + entities[0]['NrLokalu'].__str__()
    addr = addr + '\n' + entities[0]['KodPocztowy'].__str__() + ' ' + entities[0]['Miejscowosc'].__str__()
    end_date = entities[0]['DataZakonczeniaDzialalnosci'].__str__()
    return (entities[0]['Nazwa'].__str__(), addr, end_date)

def extract_digits(s):
    return ''.join(c for c in s if c.isdigit())

def clear_result():
    window.Element('-NAME-').update('')
    window.Element('-ADDR-').update('')

if __name__ == '__main__':
    last_NIP = ''
    sg.theme('LightBrown1')
    layout = [[sg.Text('NIP:', size=(5, 1)), sg.InputText(change_submits=True, size=(50,1), key='-NIP-'), sg.Button('', button_color=sg.theme_background_color(), image_data=copy_image, key='-COPY_NIP-')],
              [sg.Text('Name:', size=(5, 1)), sg.InputText(readonly=False, size=(50,1), key='-NAME-'), sg.Button('', button_color=sg.theme_background_color(), image_data=copy_image, key='-COPY_NAME-')],
              [sg.Text('Addr:', size=(5, 1)), sg.Multiline( no_scrollbar=True, size=(50, 2), key='-ADDR-'), sg.Button('', button_color=sg.theme_background_color(), image_data=copy_image, key='-COPY_ADDR-')],
              [sg.Button('Clear', key='-CLEAR-')]]
    window = sg.Window("NIP", layout)
    while True:
        event, values = window.read()
        try:
            nip_digits = extract_digits(values['-NIP-'])
        except TypeError:
            nip_digits = ''
        if event == '-CLEAR-':
            window.Element('-NIP-').update('')
            clear_result()
            last_NIP = ''
            continue
        if event == '-COPY_NIP-':
            pyperclip.copy(values['-NIP-'])
            continue
        if event == '-COPY_NAME-':
            pyperclip.copy(values['-NAME-'])
            continue
        if event == '-COPY_ADDR-':
            pyperclip.copy(values['-ADDR-'])
            continue
        if event == sg.WIN_CLOSED:
            break
        if len(nip_digits) == 10 and nip_digits != last_NIP:
            last_NIP = nip_digits
            clear_result()
            try:
                name, addr, end_date = get_data(nip_digits)
                window.Element('-NAME-').update(name)
                window.Element('-ADDR-').update(addr)
                if end_date != '':
                    sg.PopupError('Data zakończenia działalności', end_date)
            except REGONAPIError:
                sg.PopupError("Błędny NIP")
    window.close()
