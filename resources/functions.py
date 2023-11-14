from flask import request,session, url_for

def getHomePageAuctions(db_cursor,count):
    db_cursor.execute("{CALL SP_getTopAuctions(?)}",(count))
    return db_cursor.fetchall() 

def getRoleFunctions(db_cursor,role_id):
    db_cursor.execute("{CALL SP_getRoleFunctions(?)}",(role_id))
    return db_cursor.fetchall()

def referral():
    session['url']=request.referrer
    if session['url'] == None:
        session['url'] = url_for('home')

def categoryDetails(db_cursor,catid):
    db_cursor.execute("{CALL SP_getCategoryDetails(?)}",(catid))
    return db_cursor.fetchall()

def getStatusDefinitionswithGrp(db_cursor,grp):
    db_cursor.execute("{CALL SP_getStatusDefinitionsWithGrp(?)}",(grp))
    return db_cursor.fetchall()