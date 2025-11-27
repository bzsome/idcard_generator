cd ../
nuitka  --standalone ^
--include-data-dir="assets=assets" ^
--include-data-dir=".venv/Lib/site-packages/cv2/data=cv2/data" ^
--windows-icon-from-ico="assets/img/logo.ico" ^
--noinclude-dlls=cv2/opencv_videoio_*.dll ^
--noinclude-dlls=cv2/opencv_ffmpeg*.dll ^
--include-module=cv2 ^
--include-module=cv2.cv2 ^
--show-progress ^
--enable-plugin=tk-inter ^
--onefile-no-compression ^
--output-dir=build/dev ^
--output-filename=main-dev.exe ^
--run ^
main.py