# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\main.py'],
             pathex=['D:\\Studium\\7_Studienarbeit\\Impl\\venv\\Scripts', 'D:\\Studium\\7_Studienarbeit\\Impl\\venv\\Lib\\site-packages\\PySide2', 'D:\\Studium\\7_Studienarbeit\\Impl'],
             binaries=[],
             datas=[
                ('src/view/images/help.svg','src/view/images'),
                ('src/view/images/stornieren.svg','src/view/images'),
                ('src/view/images/change_logic.png','src/view/images'),
                ('src/view/images/change_mode.png','src/view/images'),

                ('src/view/Help_de.html','src/view/'),
                ('src/view/Help_en.html','src/view/'),
             ],
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