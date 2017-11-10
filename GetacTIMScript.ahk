; This is the run keyboard command ==> ctrl + alt + r
; Windows + x will terminate the script, code for which at the bottom of script
^!r::
 
WinWait, TIM Connect (Rel. 2.16.2227.0), 
IfWinNotActive, TIM Connect (Rel. 2.16.2227.0), , WinActivate, TIM Connect (Rel. 2.16.2227.0), 
WinWaitActive, TIM Connect (Rel. 2.16.2227.0), 
; Click on the outer border of Tim Connect
MouseClick, left,  260,  21
Sleep, 1000
; Click on the outer border of Tim Connect
MouseClick, left,  260,  21
Sleep, 1000

; Code for selecting the file to be opened
; FileSelectFile, SelectedFile, 3, , Open a file, Text Documents (*.ravi)
; if SelectedFile =
;	MsgBox, The user didn't select anything.
; else
;	MsgBox, The user selected the following:`n%SelectedFile%
; Code for selecting the folder snapshots are to be saved to
FileSelectFolder, OutputVar, , 3
if OutputVar =
	MsgBox, You didn't select a folder.
else
	MsgBox, You selected folder "%OutputVar%".
	
; Click on the file button
; MouseClick, left,  40,  41
; Sleep, 300
; Click on the open button
; MouseClick, left,  40,  62
; Sleep, 1000
; Waits for the Open File menu to pop up, then when it does makes it the active window
; WinWait, Open file, 
; IfWinNotActive, Open file, , WinActivate, Open file, 
; WinWaitActive, Open file, 
; Clicks into the open file dialogue box
; MouseClick, left,  232,  417
; Sleep, 1000
; Typed input of open file location
; Send, %SelectedFile%{ENTER}
; Waits for the TIM Connect window to pop up, then when it does makes it the active window
; WinWait, TIM Connect (Rel. 2.16.2227.0), 
; IfWinNotActive, TIM Connect (Rel. 2.16.2227.0), , WinActivate, TIM Connect (Rel. 2.16.2227.0), 
; WinWaitActive, TIM Connect (Rel. 2.16.2227.0), 

iterationCount = 0

; Click pause
; MouseClick, left,  190,  558
; Sleep, 400

; User input of the length of the video in seconds so the script knows how long to run for
InputBox, runtimeInSecs, Run Time Input, Please enter the number of seconds the video runs for:, , 180, 180

; User input of the length of the video in seconds so the script knows how long to run for
InputBox, runtimeInterval, Run Time Interval Input, Please enter the interval in seconds between each image:, , 180, 180
runtimeIntervalMS:= runtimeInterval*1000

; Subtract 5 here just in case the wait timer is not exactly a second
runtimeInSecs:= runtimeInSecs - 5

SetFormat, integer, d
runThroughs:= runtimeInSecs/runtimeInterval

Loop %runThroughs%
{

; Click file
MouseClick, left,  34,  42
Sleep, 400
; Click snapshot
MouseClick, left,  90,  244
Sleep, 400
; Click Save
MouseClick, left,  276,  251
Sleep, 400
; Waits for the Save As File menu to pop up, then when it does makes it the active window
WinWait, Save As, 
IfWinNotActive, Save As, , WinActivate, Save As, 
WinWaitActive, Save As, 
; Clicks on the save format drop down menu
MouseClick, left,  568,  408
Sleep, 100
; Selects tiff file format
MouseClick, left,  563,  423
Sleep, 100
; Clicks into the save file dialogue box
MouseClick, left,  254,  378
Sleep, 100
; Typed input of save file location
saveName = %OutputVar% \ %iterationCount%
Send, %saveName%{ENTER}
; Wait for it to press enter
Sleep, 300
; Press save, if the save image box is gone should just click on the video window harmlessly
MouseClick, left, 500, 440
; Need to wait 1000 so as not to full screen the video window
Sleep, 1000
MouseClick, left, 500, 440
Sleep, 100
WinWait, TIM Connect (Rel. 2.16.2227.0), 
IfWinNotActive, TIM Connect (Rel. 2.16.2227.0), , WinActivate, TIM Connect (Rel. 2.16.2227.0), 
WinWaitActive, TIM Connect (Rel. 2.16.2227.0), 

; Click file
MouseClick, left,  34,  42
Sleep, 400
; Click snapshot
MouseClick, left,  90,  244
Sleep, 400
; Click Save
MouseClick, left,  276,  251
Sleep, 400
; Waits for the Save As File menu to pop up, then when it does makes it the active window
WinWait, Save As, 
IfWinNotActive, Save As, , WinActivate, Save As, 
WinWaitActive, Save As,
; Clicks on the save format drop down menu 
MouseClick, left,  561,  400
Sleep, 100
; Selects (imagedata)csv file format
MouseClick, left,  561,  435
Sleep, 100
; Clicks into the save file dialogue box
MouseClick, left,  254,  378
Sleep, 100
; Typed input of save file location
saveName = %OutputVar% \ %iterationCount%
Send, %saveName%{ENTER}
; Wait for it to press enter
Sleep, 300
; Press save, if the save image box is gone should just click on the video window harmlessly
MouseClick, left, 500, 440
; Need to wait 1000 so as not to full screen the video window
Sleep, 1000
MouseClick, left, 500, 440
Sleep, 100
WinWait, TIM Connect (Rel. 2.16.2227.0), 
IfWinNotActive, TIM Connect (Rel. 2.16.2227.0), , WinActivate, TIM Connect (Rel. 2.16.2227.0), 
WinWaitActive, TIM Connect (Rel. 2.16.2227.0),

; Click play, and wait for the user inputted amount of time in milli seconds
MouseClick, left,  190,  558
Sleep, %runtimeIntervalMS%
iterationCount := iterationCount + 1
; Click pause
MouseClick, left,  190,  558
Sleep, 100

}

; Assign a hotkey to terminate this script
#x::ExitApp

; Return control to the user
return
