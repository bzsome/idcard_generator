cd ../
nuitka --standalone --onefile ^
--windows-console-mode=attach ^
--include-data-dir="assets=assets" ^
--windows-icon-from-ico="assets/img/logo.ico" ^
--noinclude-dlls=cv2/opencv_videoio_*.dll ^
--noinclude-dlls=cv2/opencv_ffmpeg*.dll ^
--enable-plugin=tk-inter ^
--enable-plugin=upx ^
--output-dir=build/release-upx ^
--output-filename=main-release.exe ^
--run ^
main.py