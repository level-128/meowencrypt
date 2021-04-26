nuitka boot.py --windows-icon-from-ico=files\level-128_avatar_256x256.ico --standalone --output-dir=meowencrypt_build --lto
mkdir "meowencrypt_build\boot.dist\meowencrypt's license.txt"
mkdir "meowencrypt_build\boot.dist\meowencrypt's introduction.md"
mkdir "meowencrypt_build\boot.dist\files"
mkdir "meowencrypt_build\boot.dist\globalization\languages"

copy LICENSE "meowencrypt_build\boot.dist\meowencrypt's license" /y
copy README.md "meowencrypt_build\boot.dist\meowencrypt's introduction.md" /y
copy files\* "meowencrypt_build\boot.dist\files" /y
copy globalization\languages\* "meowencrypt_build\boot.dist\globalization\languages" /y
