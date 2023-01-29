from database.database import getwhohasaccess
async def whohasaccess(userid):
    data = await getwhohasaccess(userid)
    return data