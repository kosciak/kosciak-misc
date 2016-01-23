# O skrypcie #

Skrypt służy do tworzenia kopii zapasowych zawartości bloga znajdującego się na platformie Blox.pl


# Pobieranie #

Pobierz archiwum z działu [Downloads](http://code.google.com/p/kosciak-misc/downloads/list) lub pobierz skrypt z repozytorium Subversion
```
svn checkout http://kosciak-misc.googlecode.com/svn/python/blox-exporter/trunk/ blox-exporter
```


# Wymagania #

Do poprawnego działania skryptu wymagane jest zainstalowanie środowiska Python. Skrypt był testowany na Linuksie z użyciem Python 2.5 i Windowsie z użyciem Python 2.6


# Sposób użycia #

Po prostu uruchom skrypt, jeśli nie podasz loginu, hasła, nazwy bloga jako argument wywołania, skrypt poprosi o wpisanie odpowiednich danych. Przy pytaniu o pobranie bloga wpisanie odpowiedzi innej niż `t` lub `tak` (wielkość liter nie ma znaczenia) anuluje pobieranie danego bloga.

```
Użycie: blox-exporter.py [opcje]
Przykład: blox-exporter.py -L login -P hasło -B blog1

Opcje:
  -H, --help             Pokaż pomoc i zakończ działanie
  -V, --version          Pokaż wersję skryptu
  -L, --login <login>    Login dla blox.pl
  -P, --password <hasło> Hasło dla blox.pl
  -A, --all              Pobierz wszystkie blogi
  -B, --blog <blog>      Nazwa bloga do pobrania
```

Skrypt utworzy w bieżącym katalogu folder z nazwą bloga o strukturze:
```
/nazwa_bloga
  /2010
    /01
      /tytul_notki.html
  /index.html
  /resources.html
```
Plik `index.html` zawiera spis wszystkich wpisów w kolejności chronologicznej. Plik `resources.txt` zawiera spis wszystkich użytych obrazów oraz plików znajdujących się w zasobach Blox. By je ściągnąć polecam użycie programu `wget`:
```
wget -i resources.txt -P resource
```
Pliki zostaną ściągnięte na dysk i umieszczone w folderze `/resource`

# Znane błędy #

  * W systemie Windows wyświetlają się krzaczki zamiast polskich liter
  * Brak obsługi tagów, komentarzy, trackbacków
  * Generowane strony to praktycznie czysty HTML, nie wyglądają zbyt pięknie

# Changelog #

0.1
  * pierwsze wydanie