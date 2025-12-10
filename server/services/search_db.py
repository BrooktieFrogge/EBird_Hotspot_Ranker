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

            # query2 = "DROP TABLE countries"
            # query3 = "DROP TABLE subregions1"
            query4 = "DROP TABLE subregions2"
            # query5 = "DROP TABLE norm_hotspot_names"

            # cursor.execute(query2)
            # cursor.execute(query3)
            cursor.execute(query4)
            # cursor.execute(query5)

            query = '''CREATE TABLE IF NOT EXISTS hotspots( ID TEXT PRIMARY KEY, NAME TEXT, COUNTRY TEXT, SUBREGION1 TEXT,  SUBREGION2 TEXT, SPECIESCOUNT INTEGER )'''

            query2 = '''CREATE TABLE IF NOT EXISTS countries( country_code TEXT PRIMARY KEY, country_name TEXT )'''

            query3 = '''CREATE TABLE IF NOT EXISTS subregions1( subnational1_code TEXT PRIMARY KEY, subnational1_name TEXT,country_name TEXT)'''

            query4 = '''CREATE TABLE IF NOT EXISTS subregions2( subnational2_code TEXT PRIMARY KEY, subnational2_name TEXT,subnational1_name TEXT, country_name TEXT)'''

            query5 = '''CREATE TABLE IF NOT EXISTS norm_hotspot_names AS SELECT ID, norm(NAME) AS NAME FROM 'hotspots' '''

            query6 = '''CREATE TABLE IF NOT EXISTS norm_country_names AS SELECT country_code, norm(country_name) AS country_name FROM 'countries' '''

            query7 = '''CREATE TABLE IF NOT EXISTS norm_subregion1_names AS SELECT subnational1_code, norm(subnational1_name) AS subnational1_name FROM 'subregions1' '''

            query8 = '''CREATE TABLE IF NOT EXISTS norm_subregion2_names AS SELECT subnational2_code, norm(subnational2_name) AS subnational2_name FROM 'subregions2' '''

            cursor.execute(query)
            cursor.execute(query2)
            cursor.execute(query3)
            cursor.execute(query4)
            cursor.execute(query5)
            cursor.execute(query6)
            cursor.execute(query7)
            cursor.execute(query8)
            
            # #ONLY DONE ONCE: loading loc specific info ===================================
            # countryInfo = pd.read_csv('server/data/countries-Table 1.csv', usecols=['country_code','country_name'])
            # sub1Info = pd.read_csv('server/data/subnational1 regions-Table 1.csv', usecols=[ 'subnational1_code','subnational1_name','country_name'])
            sub2Info = pd.read_csv('server/data/subnational2 regions-Table 1.csv', usecols=['subnational2_code','subnational2_name','subnational1_name','country_name'])

            # countryInfo.to_sql('countries', sqlConn, if_exists='append',index=False)

            # sub1Info.to_sql('subregions1', sqlConn, if_exists='append',index=False)

            sub2Info.to_sql('subregions2', sqlConn, if_exists='append',index=False)
            
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

#init_db()
            
#TODO reduce repetitive logic 
#TODO add handling for accented names like Cañon
#TODO add doc
def dynamic_search(hotspot='',country='',subregion1='',subregion2='',mode=None):

    #if mode provided 
    if mode == "country" and country:
        return search_countries(normalize(country))
    
    if mode == "subregion1" and subregion1:
        return search_sub1(normalize(subregion1),country)
    
    if mode == "subregion2" and subregion2:
        return search_sub2(normalize(subregion2),country,subregion1)
    
    if mode == "hotspot":
        return search_hotspots(normalize(hotspot),country,subregion1,subregion2)
    else:
        return None
   
def search(table,field,query,where_clause="",where_params=(),limit=50, hotspot:bool = False):
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
                cursor = sqlConn.cursor()
        #get options from db
        sql_q = f"SELECT {field} FROM {table}{where_clause} LIMIT 250"

        print(sql_q, where_params) #TODO Remove

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
                    'name': r[1],
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


def search_countries(query):
    tokens = []
    where = ''
    w_params = ()

    tokens = [token.strip() for token in normalize(query).split() if token.strip()]

    w_params += (query+'%',)  #prefix for each token 

    for t in tokens:
        w_params += ("%" + t + '%',)

    where = (' WHERE N.country_name LIKE ?' + ' OR ? '*(len(tokens)))
    
    return search(
        table='countries AS C, norm_country_names AS N',
        field='C.country_code, C.country_name',
        where_clause=where,
        where_params=w_params,
        query=query,
        limit=50
    )

def search_sub1(query, country):
    where = ' WHERE '
    w_params = ()
    where_clauses = []
    tokens = []

    if country:
        where_clauses.append('country_name = ?')
        w_params += (country,)

    tokens = [token.strip() for token in normalize(query).split() if token.strip()]
    w_params += (query+'%',) 

    for t in tokens:
        w_params += ("%" + t + '%',) #substring for each token 

    where_clauses.append('N.subnational1_name LIKE ?' + ' OR ? '*(len(tokens)))

    where += ' AND '.join(where_clauses)

    return search(
        table='subregions1 AS S, norm_subregion1_names AS N',
        field='S.subnational1_code, S.subnational1_name',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=50
    )
    
def search_sub2(query,country,sub1):
    tokens = []
    where = ' WHERE '
    w_params = ()
    where_clauses = []

    if country:
        where_clauses.append('country_name = ?')
        w_params += (country,)

    if sub1:
        where_clauses.append('subnational1_name = ?')
        w_params += (sub1,)


    tokens = [token.strip() for token in normalize(query).split() if token.strip()]

    w_params += (query+'%',) 

    for t in tokens:
        w_params += ("%" + t + '%',) #prefix for each token 

    where_clauses.append('N.subnational2_name LIKE ?' + ' OR ? '*(len(tokens)))

    where += ' AND '.join(where_clauses)

    return search(
        table='subregions2 AS S, norm_subregion2_names AS N',
        field='S.subnational2_code, S.subnational2_name',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=50
    )

def search_hotspots(query,country,sub1,sub2):
    where = ' WHERE '
    where_clauses = []
    w_params = ()
    tokens = []

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

        w_params += (query+'%',) 
        for t in tokens:
            w_params += ("%" + t + '%',)#prefix for each token 

        where_clauses.append('N.NAME LIKE ?' + ' OR ? '*(len(tokens)))

    where += ' AND '.join(where_clauses) 

    return search(
        table='hotspots AS H, norm_hotspot_names AS N',
        field='H.ID, H.NAME, H.COUNTRY, H.SUBREGION1, H.SUBREGION2, H.SPECIESCOUNT',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=20,
        hotspot=True
    )