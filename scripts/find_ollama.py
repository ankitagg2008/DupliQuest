import glob
import os

roots = [
    r'C:\Users\ankit\AppData\Local\Programs',
    r'C:\Program Files',
    r'C:\Program Files (x86)',
    r'C:\Users\ankit\AppData\Local\Microsoft\WindowsApps',
]
found = []
for root in roots:
    if not os.path.exists(root):
        continue
    found.extend(glob.glob(os.path.join(root, '**', 'ollama.exe'), recursive=True))
if found:
    for path in sorted(found)[:50]:
        print(path)
else:
    print('NOT FOUND')
