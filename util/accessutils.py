from database.database import getwhohasaccess
async def whohasaccess():
    datalist = getwhohasaccess()
    return datalist