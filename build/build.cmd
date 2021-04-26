@ECHO OFF
cd ..

ECHO ====================================
ECHO copying files to the build
ECHO ====================================

mkdir "meowencrypt_build\boot.dist\files"
mkdir "meowencrypt_build\boot.dist\globalization\languages"

copy LICENSE "meowencrypt_build\boot.dist\meowencrypt's license.txt" /y
copy README.md "meowencrypt_build\boot.dist\meowencrypt's introduction.md" /y
copy files\* "meowencrypt_build\boot.dist\files" /y
copy globalization\languages\* "meowencrypt_build\boot.dist\globalization\languages" /y
ECHO ====================================
PAUSE
START meowencrypt_build\boot.dist