
def getHomePageAuctions(db_cursor,count):
    db_cursor.execute("{CALL SP_getTopAuctions(?)}",(count))
    return db_cursor.fetchall() #data from database