nuitka --standalone --onefile --disable-console ^
--full-compat ^
--windows-icon-from-ico=./raw/logo.ico ^
--include-data-file=./raw/**=./raw/ ^
--plugin-enable=upx ^
--output-dir=out ^
main.py