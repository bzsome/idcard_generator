cd ../
nuitka --standalone --onefile ^
--windows-console-mode=attach ^
--nofollow-imports ^
--include-data-dir="assets=assets" ^
--windows-icon-from-ico="assets/img/logo.ico" ^
 --no-pyi-file  --no-pyi-stubs ^
--output-dir=build/test ^
--output-filename=main-test.exe ^
--run ^
main.py