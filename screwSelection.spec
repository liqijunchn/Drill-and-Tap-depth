# -*- mode: python -*-

block_cipher = None


a = Analysis(['screwSelection.py'],
             pathex=['d:\\boltSelection'],
             binaries=[],
             datas=[('screwSelection.db','.'),('screw.png','.'),('jci.ico','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='screwSelection',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='.\\jci.ico')
