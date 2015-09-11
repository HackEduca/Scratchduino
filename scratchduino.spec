# -*- mode: python -*-
a = Analysis(['scratchduino.py'],
             pathex=['/home/awangenh/scratchduino'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='scratchduino',
          debug=False,
          strip=None,
          upx=True,
          console=True )
