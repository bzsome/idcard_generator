cd ../
nuitka --standalone --onefile ^
--windows-console-mode=attach ^
--include-data-dir="assets=assets" ^
--include-data-dir=".venv/Lib/site-packages/cv2/data=cv2/data" ^
--windows-icon-from-ico="assets/img/logo.ico" ^
--noinclude-dlls=cv2/opencv_videoio_*.dll ^
--noinclude-dlls=cv2/opencv_ffmpeg*.dll ^
--enable-plugin=tk-inter ^
--onefile-no-compression ^
--output-dir=build/test ^
--output-filename=main-test.exe ^
--run ^
main.py