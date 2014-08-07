::下面要设置包名 -p 后面的
set p_name=com.richinfo.thinkmail
adb shell am force-stop  %p_name%
adb shell am start -n com.wakelock.cn/com.wakelock.cn.MainActivity
::获取日期 将格式设置为：20110820
set datevar=%date:~0,4%%date:~5,2%%date:~8,2%
::获取时间中的小时 将格式设置为：24小时制
set timevar=%time:~0,2%
if /i %timevar% LSS 10 (
set timevar=0%time:~1,1%
)
::获取时间中的分、秒 将格式设置为：3220 ，表示 32分20秒
set timevar=%timevar%%time:~3,2%%time:~6,2%

adb shell monkey -p %p_name% -s %timevar%  -v --throttle 200 10000 >%datevar%%timevar%.txt
::>%datevar%%timevar%.txt
del /a/f/q monkey_temp.txt
copy /y %datevar%%timevar%.txt monkey_temp.txt
md %datevar%
move /y %datevar%%timevar%.txt %datevar%\%datevar%%timevar%.txt
::
adb shell screencap -p /sdcard/monkey_run_end.png
adb pull /sdcard/monkey_run_end.png ./image
::
python jiexi_monkey_temp.py
pause
::adb shell monkey -p mail139.mpost --monitor-native-crashes --pct-touch 30 -s 1 -v -v -v --throttle 200 8000 >%datevar%%timevar%.txt