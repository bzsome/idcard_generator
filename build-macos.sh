pyinstaller --windowed --clean --noconfirm --onefile \
-i raw/img/logo.icns \
--add-data "raw:raw" \
main.py