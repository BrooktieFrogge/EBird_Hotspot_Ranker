from rapidfuzz import process, fuzz
import pandas as pd
import unicodedata
import re
import sqlite3

'''
API for dynamically searching eBird hotspot locations using rapidfuzz matching.

This feature works by loading three CSV datasets and a custom JSON file containing region and hotspot specific information, normalizing the names to remove accents and special characters to produce autocomplete/correction matching using Levenshtein Distance, and exposing two  API endpoints for searching by name or hotspot location id.
'''

#DATA LOADING=======================================================
countryInfo = pd.read_csv('server/data/countries-Table 1.csv')
sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv')
sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv')

'''
Normalize text by removing accents, converting to basic ASCII characters, lowercasing, and triming whitespace

Returns: Normalized string for rapidfuzz matching
'''
def normalize(text:str):
     if not text:
         return ''
     lower_c  = text.lower()
     no_accents  = unicodedata.normalize('NFKD', lower_c).encode('ascii','ignore').decode()
     no_punct = re.sub(r'[^\w\s]',' ',no_accents)
     return no_punct


'''SQLite database setup'''
def init_db():
    try:

        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
            cursor = sqlConn.cursor()

            sqlConn.create_function('norm',1, normalize)

            # query2 = "DROP TABLE norm_subregion1_names"
            # query3 = "DROP TABLE norm_subregion2_names"
            # query4 = "DROP TABLE norm_country_names"
            # query5 = "DROP TABLE norm_hotspot_names"

            # cursor.execute(query2)
            # cursor.execute(query3)
            # cursor.execute(query4)
            # cursor.execute(query5)

            query = '''CREATE TABLE IF NOT EXISTS hotspots( ID TEXT PRIMARY KEY, NAME TEXT, COUNTRY TEXT, SUBREGION1 TEXT,  SUBREGION2 TEXT, SPECIESCOUNT INTEGER )'''

            query2 = '''CREATE TABLE IF NOT EXISTS countries( country_code TEXT PRIMARY KEY, country_name TEXT )'''

            query3 = '''CREATE TABLE IF NOT EXISTS subregions1( subnational1_code TEXT PRIMARY KEY, subnational1_name TEXT,country_name TEXT)'''

            query4 = '''CREATE TABLE IF NOT EXISTS subregions2( subnational2_code TEXT PRIMARY KEY, subnational2_name TEXT,subnational1_name TEXT, country_name TEXT)'''


            query5 = '''CREATE TABLE IF NOT EXISTS norm_hotspot_names (ID TEXT PRIMARY KEY, NAME TEXT) '''

            subquery5 = '''INSERT INTO norm_hotspot_names(ID, NAME) SELECT ID, norm(NAME) AS NAME FROM 'hotspots'  '''

            query6 = '''CREATE TABLE IF NOT EXISTS norm_country_names (country_code TEXT PRIMARY KEY, country_name TEXT )'''

            subquery6 = '''INSERT INTO norm_country_names(country_code, country_name) SELECT country_code, norm(country_name) AS country_name FROM 'countries'  '''

            query7 = '''CREATE TABLE IF NOT EXISTS norm_subregion1_names (subnational1_code TEXT PRIMARY KEY, subnational1_name TEXT) '''

            subquery7 = '''INSERT INTO norm_subregion1_names (subnational1_code, subnational1_name) SELECT subnational1_code, norm(subnational1_name) AS subnational1_name FROM 'subregions1'  '''

            query8 = '''CREATE TABLE IF NOT EXISTS norm_subregion2_names (subnational2_code TEXT PRIMARY KEY, subnational2_name TEXT) '''

            subquery8 = '''INSERT INTO norm_subregion2_names (subnational2_code, subnational2_name) SELECT subnational2_code, norm(subnational2_name) AS subnational2_name FROM 'subregions2'  '''

            cursor.execute(query)
            cursor.execute(query2)
            cursor.execute(query3)
            cursor.execute(query4)
            cursor.execute(query5)
            cursor.execute(query6)
            cursor.execute(query7)
            cursor.execute(query8)

            cursor.execute(subquery5)
            cursor.execute(subquery6)
            cursor.execute(subquery7)
            cursor.execute(subquery8)
            
            # #ONLY DONE ONCE: loading loc specific info ===================================
            # countryInfo = pd.read_csv('server/data/countries-Table 1.csv', usecols=['country_code','country_name'])
            # sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv', usecols=[ 'subnational1_code','subnational1_name','country_name'])
            # sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv', usecols=['subnational2_code','subnational2_name','subnational1_name','country_name'])

            # countryInfo.to_sql('countries', sqlConn, if_exists='append',index=False)

            # sub1Info.to_sql('subregions1', sqlConn, if_exists='append',index=False)

            # sub2Info.to_sql('subregions2', sqlConn, if_exists='append',index=False)
            
            #===================================
            
            sqlConn.commit() 

            df = pd.read_sql_query('''SELECT * FROM 'hotspots' ''', sqlConn)

            df1 = pd.read_sql_query('''SELECT * FROM 'countries' ''', sqlConn)
            
            df2 = pd.read_sql_query('''SELECT * FROM 'subregions1' ''', sqlConn)
            
            df3 = pd.read_sql_query('''SELECT * FROM 'subregions2' ''', sqlConn)

            df4 = pd.read_sql_query('''SELECT * FROM 'norm_hotspot_names' ''', sqlConn)

            df5 = pd.read_sql_query('''SELECT * FROM 'norm_country_names' ''', sqlConn)

            df6 = pd.read_sql_query('''SELECT * FROM 'norm_subregion1_names' ''', sqlConn)

            df7 = pd.read_sql_query('''SELECT * FROM 'norm_subregion2_names' ''', sqlConn)

            print(f"Hotspot overview data loaded successfully. Length: {len(df)}, Head: \n {df.sample(20)}")

            print(f"Countries data loaded successfully. Length: {len(df1)}, Head: \n {df1.sample(20)}")
            
            print(f"Subregions1 data loaded successfully. Length: {len(df2)}, Head: \n {df2.sample(20)}")
            
            print(f"Subregions2 data loaded successfully. Length: {len(df3)}, Head: \n {df3.sample(20)}")

            print(f"norm_hotspots data loaded successfully. Length: {len(df4)}, Head: \n {df4.sample(20)}")

            print(f"norm_countries data loaded successfully. Length: {len(df5)}, Head: \n {df5.sample(20)}")
            
            print(f"norm_sub1 data loaded successfully. Length: {len(df6)}, Head: \n {df6.sample(20)}")

            print(f"norm_sub2 data loaded successfully. Length: {len(df7)}, Head: \n {df7.sample(20)}")

    except sqlite3.Error as e:
        print(f"Failed to execute hotspot table creation - {e}")

    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")

# init_db()
            
#TODO reduce repetitive logic 
#TODO add doc
def dynamic_search(hotspot='',country='',subregion1='',subregion2='',mode='hotspot', limit=60):

    #if mode provided 
    if mode == "country" and country:
        return search_countries(country, limit)
    
    if mode == "subregion1" and subregion1:
        return search_sub1(subregion1,country,limit)
    
    if mode == "subregion2" and subregion2:
        return search_sub2(subregion2,country,subregion1,limit)
    
    if mode == "hotspot":
        return search_hotspots(hotspot,country,subregion1,subregion2,limit)
   
   
def search(table,field,query,where_clause="",where_params=(),limit=50, hotspot:bool = False):
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                sqlConn.create_function('norm',1, normalize)

                cursor = sqlConn.cursor()

        #get options from db
        sql_q = f"SELECT {field} FROM {table}{where_clause} LIMIT 150"

        # print(sql_q, where_params) 
        
        rows = cursor.execute(sql_q,where_params).fetchall()

        names = [r[1] for r in rows]
        names_dict = {idx: val for idx, val in enumerate(names)}            

        #fuzzy matching
        ranked = process.extract(query,names_dict,scorer=fuzz.token_set_ratio,limit=limit)

        #structure results
        results = []
        if hotspot:
            for name,score,idx in ranked:
                r = rows[idx]
                results.append({
                    'id': r[0],
                    'name': get_orig_hotspot_name(r[0]),
                    'country': r[2],
                    'subregion1': r[3],
                    'subregion2': r[4],
                    'speciesCount': r[5]
                })
            return results

        
        for name,score,idx in ranked:
            r = rows[idx]
            results.append({
                'name': r[1]
            })
        return results
    
    except sqlite3.Error as e:
        print(f"Database retrieval failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")

def get_orig_hotspot_name(iD:str):
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                sqlConn.create_function('norm',1, normalize)

                cursor = sqlConn.cursor()

        #get options from db
        sql_q = f"SELECT NAME FROM 'hotspots' WHERE ID = '{iD}'"
        return cursor.execute(sql_q).fetchall()[0][0]

    except sqlite3.Error as e:
        print(f"Database original hotspot name retrieval failed: {e}")
        return(None)

    finally:
        if sqlConn:
            sqlConn.close()


def search_countries(q,limit):
    tokens = []
    where = ''
    w_params = ()

    query = normalize(q)
    
    tokens = [token.strip() for token in normalize(query).split() if token.strip()]

    prefix_q = query+'%' 
    w_params += (prefix_q,)  #prefix 

    for t in tokens:
        w_params += ("%" + t + '%',)

    where = (' WHERE N.country_name LIKE ?' + ' OR N.country_name LIKE ? '*(len(tokens))) + f"ORDER  BY CASE WHEN N.country_name LIKE '{prefix_q}' THEN 0 ELSE 1 END, C.country_name"
    
    return search(
        table='countries AS C JOIN norm_country_names AS N ON C.country_code = N.country_code',
        field='C.country_code, C.country_name',
        where_clause=where,
        where_params=w_params,
        query=q,
        limit=limit
    )

def search_sub1(q, country,limit):
    where = ' WHERE '
    w_params = ()
    where_clauses = []
    tokens = []

    query = normalize(q)
    
    if country:
        where_clauses.append('S.country_name = ?')
        w_params += (country,)

    tokens = [token.strip() for token in normalize(query).split() if token.strip()]

    prefix_q = query+'%'
    w_params += (prefix_q,)

    for t in tokens:
        w_params += ("%" + t + '%',) #substring for each token 

    where_clauses.append('N.subnational1_name LIKE ?' + ' OR N.subnational1_name LIKE ? '*(len(tokens)))

    where += ' AND '.join(where_clauses)  + f"ORDER  BY CASE WHEN N.subnational1_name LIKE '{prefix_q}' THEN 0 ELSE 1 END, S.subnational1_name"

    return search(
        table='subregions1 AS S JOIN norm_subregion1_names AS N ON S.subnational1_code = N.subnational1_code',
        field='S.subnational1_code, S.subnational1_name',
        query=q,
        where_clause=where,
        where_params=w_params,
        limit=limit
    )
    
def search_sub2(q,country,sub1,limit):
    tokens = []
    where = ' WHERE '
    w_params = ()
    where_clauses = []

    query = normalize(q)

    if country:
        where_clauses.append('S.country_name = ?')
        w_params += (country,)

    if sub1:
        where_clauses.append('S.subnational1_name = ?')
        w_params += (sub1,)


    tokens = [token.strip() for token in normalize(query).split() if token.strip()]

    prefix_q = query+'%'
    w_params += (prefix_q,)

    for t in tokens:
        w_params += ("%" + t + '%',) #prefix for each token 

    where_clauses.append('N.subnational2_name LIKE ?' + ' OR N.subnational2_name LIKE ? '*(len(tokens)))

    where += ' AND '.join(where_clauses) + f"ORDER  BY CASE WHEN N.subnational2_name LIKE '{prefix_q}' THEN 0 ELSE 1 END, S.subnational2_name"

    return search(
        table='subregions2 AS S JOIN norm_subregion2_names AS N ON S.subnational2_code = N.subnational2_code',
        field='S.subnational2_code, S.subnational2_name',
        query=q,
        where_clause=where,
        where_params=w_params,
        limit=limit
    )

def search_hotspots(q,country,sub1,sub2,limit):
    where = ' WHERE '
    where_clauses = []
    w_params = ()
    tokens = []

    query = normalize(q)

    if (query + country + sub1 + sub2) == '':
        where = ''
  
    if sub2:
        where_clauses.append('H.SUBREGION2 = ?')
        w_params += (sub2,)

    if sub1:
        where_clauses.append('H.SUBREGION1 = ?')
        w_params += (sub1,)

    if country:
        where_clauses.append('H.COUNTRY = ?')
        w_params += (country,)
    
    if query:
        tokens = [token.strip() for token in normalize(query).split() if token.strip()]

        prefix_q = query+'%'
        w_params += (prefix_q,)

        for t in tokens:
            w_params += ('%' + t + '%',)#prefix for each token 

        binders = ' OR '.join(['N.NAME LIKE ? '] * (len(tokens)+1))
        where_clauses.append(f'({binders})')

        #give the full query prefix precedence over query tokens
        where += ' AND '.join(where_clauses) + f"ORDER  BY CASE WHEN N.NAME LIKE '{prefix_q}' THEN 0 ELSE 1 END, H.NAME"
    else: 
         where += ' AND '.join(where_clauses)

    return search(
        table='hotspots AS H JOIN norm_hotspot_names AS N ON H.ID = N.ID',
        field='H.ID, N.NAME, H.COUNTRY, H.SUBREGION1, H.SUBREGION2, H.SPECIESCOUNT',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=limit,
        hotspot=True
    )