# Retro Basic Interpreter
This is a intrepreter of retro basic language for PROG LANG PRIN class.
# วิธีใช้
เรียกใช้ retro basic interpreter โดย รับ ชื่อไฟล์ เป็น input argument
```shell
$ python interpreter.py [filename]
```
เช่น 
```shell
$ python interpreter.py basic.txt
```
output ซึ่งอยู่ในรูปแบบ bcode จะอยู่ใน filename.bout (เช่น basic.txt.bout)
<h4>หาก Grammar ใน input file ไม่ถูกต้อง จะมี Exception ถูก raise ขึ้นมาเพื่อบอกว่า grammar ไม่ถูกต้อง
