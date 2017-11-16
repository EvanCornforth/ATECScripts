cd "%~dp0"

@echo off
echo Directory of .ARW files to be converted to .TIFF files is: %1
echo Number of files to be converted is: %2

REM Activate the delay expected for referencing feature
setlocal ENABLEDELAYEDEXPANSION

REM c is the counter for how many images have been converted
set /a c=1

REM %f being a variable, will loop through all the .arw images in this directory
for %%f in (%1*.arw) do (
			REM  -v Development showing the progress information on screen
			REM -w We use the white balance that was configured in the camera
			REM -H 1 We use a linear mode with no clipping in the highlights
			REM -o 1 We convert the resulting image to the sRGB colour space
			REM -q 3 We set the maximum possible quality of interpolation
			REM -q 0 is the bilinear interpolation, whereby the red value of a non-red pixel 
			REM is computed as the average of the two or four adjacent red pixels, and similarly for blue and green.
			REM -4 -T We force 16-bit TIFF linear output
			
			REM ~n expands %f to a file name only
			C:\Users\Evan\Desktop\dcraw-9.27-ms-64-bit\dcraw-9.27-ms-64-bit.exe -v -w -H 1 -o 1 -q 3 -4 -T %1%%~nf.arw
			
			REM Variables that should be delay expanded are referenced with !VARIABLE! instead of %VARIABLE%
			echo Converted file !c! of %2
			set /a c=c+1
	
	)
	
REM Deactivate the delay expected for referencing feature
endlocal 