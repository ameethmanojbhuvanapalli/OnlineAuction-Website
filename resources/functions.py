from flask import request, g,session

def getHomePageAuctions(db_cursor,count):
    db_cursor.execute("{CALL SP_getTopAuctions(?)}",(count))
    return db_cursor.fetchall() 

def getRoleFunctions(db_cursor,role_id):
    db_cursor.execute("{CALL SP_getRoleFunctions(?)}",(role_id))
    return db_cursor.fetchall()

def referral():
    url = request.referrer
    if url :
        session["url"] = url
    print(url)
