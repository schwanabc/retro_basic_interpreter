# Retro Basic Interpreter
This is a intrepreter of retro basic language for PROG LANG PRIN class using python.
# Required library
sys
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
<h4>หาก Grammar ใน input file ไม่ถูกต้อง จะมี Exception ถูก raise ขึ้นมาบอกผู้ใช้เพื่อบอกว่า grammar ของ file นำเข้าไม่ถูกต้อง เช่น</h4>

``` shell
$ python interpreter.py wrong.txt
A = 1
Traceback (most recent call last):
  File "interpreter.py", line 169, in <module>
    bcode_string = convert_to_bcode(scanned_line)
  File "interpreter.py", line 152, in convert_to_bcode
    parsed_list.append((parse(token), token))
  File "interpreter.py", line 139, in parse
    raise Exception("Wrong Grammar: symbol '"+ token + "' is unexpected (mismatch terminal symbol to parsing table)") 
Exception: Wrong Grammar: symbol 'A' is unexpected (mismatch terminal symbol to parsing table)


```
