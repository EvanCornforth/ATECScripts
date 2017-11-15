REM %f being a variable, will loop through all the .arw images in this directory
for %%f in (C:\Users\Evan\Documents\PhD\DCIM\testDCRAW\*.arw) do (

			REM Prints out the full path for f, the .arw image
			echo %%f
			REM expands %f to a file name only and adds .arw to the end of the variable
            echo %%~nf.arw	
			REM  -v Development showing the progress information on screen
			REM -w We use the white balance that was configured in the camera
			REM -H 1 We use a linear mode with no clipping in the highlights
			REM -o 0 We convert the resulting image to the sRGB colour space
			REM -q 3 We set the maximum possible quality of interpolation
			REM -4 -T We force 16-bit TIFF linear output
			dcraw-9.27-ms-64-bit.exe -v -w -H 1 -o 1 -q 3 -4 -T %%f
    )
