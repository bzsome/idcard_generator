cd ../
nuitka --standalone --onefile ^
--windows-console-mode=attach ^
--include-data-dir="assets=assets" ^
--windows-icon-from-ico="assets/img/logo.ico" ^
 --no-pyi-file  --no-pyi-stubs ^
--plugin-enable=upx ^
--onefile-no-compression ^
--output-dir=build/release-upxn ^
--output-filename=main-release.exe ^
--run ^
main.py