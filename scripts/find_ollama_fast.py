import os

roots = [
    r'C:\Users\ankit\AppData\Local\Programs',
    r'C:\Program Files',
    r'C:\Program Files (x86)',
    r'C:\Users\ankit\AppData\Local\Microsoft\WindowsApps',
]
max_depth = 5
found = []
for root in roots:
    if not os.path.isdir(root):
        continue
    for dirpath, dirnames, filenames in os.walk(root):
        depth = dirpath[len(root):].count(os.sep)
        if depth > max_depth:
            dirnames.clear()
            continue
        if 'ollama.exe' in filenames:
            found.append(os.path.join(dirpath, 'ollama.exe'))
            break
if found:
    for path in sorted(found):
        print(path)
else:
    print('NOT FOUND')
