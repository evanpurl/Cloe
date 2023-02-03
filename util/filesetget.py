import os


async def fileget(module, serverid):
    if not os.path.exists(f"values/{serverid}/{module}"):
        return False
    with open(f"values/{serverid}/{module}/{module}.txt", "r+") as f:
        line = f.readline()
    return line


async def fileset(module, value, serverid):
    try:
        if not os.path.exists(f"values/{serverid}/{module}"):
            os.makedirs(f"values/{serverid}/{module}")
        with open(f"values/{serverid}/{module}/{module}.txt", "w") as f:
            f.write(str(value))
        return True
    except Exception as e:
        print(e)
