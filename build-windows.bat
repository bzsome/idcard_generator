pyinstaller --windowed --clean --noconfirm --onefile  ^
-i raw/img/logo.ico ^
--add-data "raw;raw" ^
main.py