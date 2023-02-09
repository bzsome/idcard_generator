nuitka --standalone --onefile ^
--windows-icon-from-ico=./raw/img/logo.ico ^
--include-data-file=./raw/fonts/*=./raw/fonts/ ^
--include-data-file=./raw/img/*=./raw/img/ ^
--enable-plugin=tk-inter ^
--output-dir=out ^
--run ^
main.py