@ECHO OFF
cd..
ECHO ====================================
ECHO compiling meowencrypt using nuitka
ECHO ====================================
nuitka boot.py --windows-icon-from-ico=files\level-128_avatar_256x256.ico --standalone --output-dir=meowencrypt_build --lto

ECHO ====================================
ECHO complete
ECHO ====================================
PAUSE