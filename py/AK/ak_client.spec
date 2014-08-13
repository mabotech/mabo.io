# -*- mode: python -*-
a = Analysis(['ak_client.py'],
             pathex=['E:\\mabodev\\mabo.io\\py\\AK'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ak_client.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='app.ico')
