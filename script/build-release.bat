cd ../
nuitka --standalone --onefile ^
--windows-console-mode=attach ^
--include-data-dir="assets=assets" ^
--windows-icon-from-ico="assets/img/logo.ico" ^
--noinclude-dlls=cv2/opencv_videoio_*.dll ^
--no-pyi-file  --no-pyi-stubs ^
--output-dir=build/release ^
--output-filename=main-release.exe ^
--run ^
main.py