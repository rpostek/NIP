Program pobiera dane o firmie na podstawie NIP. NIP można wpisywac zarówno z myślnikami, jak i bez. Pobranie danych nastepuje po wpisaniu dokładnie 10 cyfr (a pozostałe znai są ignorowane).

Utworzyć plik exe można za pomocą komendy _pyinstaller main.py -w --onefile_
W wersji produkcyjnej należy zamienić ściżkę do API na _https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc_ oraz klucz.

