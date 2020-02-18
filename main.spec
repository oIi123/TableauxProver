# -*- mode: python ; coding: utf-8 -*-

import os


block_cipher = None
cwd = os.getcwd()

datas = []
for dir in ['src/view/images/', 'src/view/Help/', 'src/view/Help/images/', 'src/view/Help/images/derivation_rules/']:
   datas.extend([(dir + f, dir) for f in os.listdir(cwd + '/' + dir) if os.path.isfile(dir + '/' + f)])

a = Analysis(['src\\main.py'],
             pathex=[
                  cwd + '\\venv\\Scripts',
                  cwd + '\\venv\\Lib\\site-packages\\PySide2',
                  cwd
               ],
             binaries=[],
             datas= datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Tableau Prover',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
         a.binaries,
         a.zipfiles,
         a.datas,
         strip=False,
         upx=True,
         upx_exclude=[],
         name='main')