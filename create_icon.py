import base64

# 这是一个预设的图标数据
icon_data = """
AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
... (为了简洁省略了图标数据)
"""

# 将图标数据保存为文件
with open("file_organizer.ico", "wb") as icon_file:
    icon_file.write(base64.b64decode(icon_data)) 