from rapidfuzz import process, fuzz
import pandas as pd
import unicodedata
import re
import sqlite3, traceback

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

        with sqlite3.connect('server/data/database/new.db') as sqlConn:
            cursor = sqlConn.cursor()

            sqlConn.create_function('norm',1, normalize)

            # query2 = "ALTER TABLE 'subregions1' RENAME COLUMN country TO  country_name"
            # query3 = "ALTER TABLE 'subregions2' RENAME COLUMN country TO country_name"
            # query4 = "ALTER TABLE 'subregions2' RENAME COLUMN subregion1 TO subnational1_name"

            # query5 = "ALTER TABLE 'hotspots' RENAME COLUMN subregion1 TO subnational1_name"
            # query6 = "ALTER TABLE 'hotspots' RENAME COLUMN subregion2 TO subnational2_name"
            # query7 = "ALTER TABLE 'hotspots' RENAME COLUMN country TO country_name"

            # # query7 = "ALTER TABLE 'hotspots' RENAME COLUMN SPECIESCOUNT TO species_count"
            # # query8 = "ALTER TABLE 'hotspots' RENAME COLUMN NORM_NAME TO norm_name"

            # cursor.execute("ALTER TABLE 'hotspots' RENAME COLUMN subnational1_name TO subnational1_code")

            # cursor.execute("ALTER TABLE 'hotspots' RENAME COLUMN subnational2_name TO subnational2_code")

            # cursor.execute( "ALTER TABLE 'hotspots' RENAME COLUMN country_name TO country_code")

            # query = '''CREATE TABLE IF NOT EXISTS hotspots( ID TEXT PRIMARY KEY, NAME TEXT, COUNTRY TEXT, SUBREGION1 TEXT,  SUBREGION2 TEXT, SPECIESCOUNT INTEGER )'''

            query2 = '''CREATE TABLE IF NOT EXISTS countries( country_code TEXT PRIMARY KEY, country_name TEXT )'''

            query3 = '''CREATE TABLE IF NOT EXISTS subregions1( subnational1_code TEXT PRIMARY KEY, subnational1_name TEXT,country_name TEXT)'''

            query4 = '''CREATE TABLE IF NOT EXISTS subregions2( subnational2_code TEXT PRIMARY KEY, subnational2_name TEXT,subnational1_name TEXT, country_name TEXT)'''


            # query5 = '''ALTER TABLE 'hotspots' ADD COLUMN NORM_NAME TEXT'''

            # subquery5 = '''UPDATE  'hotspots' SET NORM_NAME = norm(NAME)  '''

            # query6 = '''ALTER TABLE 'countries' ADD COLUMN norm_name TEXT'''

            subquery6 = '''UPDATE 'countries' SET norm_name = norm(country_name) '''

            # query7 ='''ALTER TABLE 'subregions1' ADD COLUMN norm_name TEXT'''

            subquery7 = '''UPDATE 'subregions1' SET norm_name = norm(subnational1_name) '''

            # query8 = '''ALTER TABLE 'subregions2' ADD COLUMN norm_name TEXT'''

            subquery8 = '''UPDATE 'subregions2' SET norm_name = norm(subnational2_name) '''

            # # cursor.execute(query)
            # cursor.execute(query2)
            # cursor.execute(query3)
            # cursor.execute(query4)
            # # cursor.execute(query5)
            # cursor.execute(query6)
            # cursor.execute(query7)
            # cursor.execute(query8)
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


            print(f"Hotspot overview data loaded successfully. Length: {len(df)}, Head: \n {df.head}")

            print(f"Countries data loaded successfully. Length: {len(df1)}, Head: \n {df1.head}")
            
            print(f"Subregions1 data loaded successfully. Length: {len(df2)}, Head: \n {df2.head}")
            
            print(f"Subregions2 data loaded successfully. Length: {len(df3)}, Head: \n {df3.head}")


    except sqlite3.Error as e:
        print(f"Failed to execute hotspot table creation - {e}")

    finally:
        if sqlConn:
            sqlConn.close()
            print("SQLite connection closed")

         
#TODO add doc!!!
            
def dynamic_search(hotspot='',country='',subregion1='',subregion2='',mode='hotspot', limit=60):
    print("HERE")

    #if mode provided 
    if mode == "country":
        return search_countries(normalize(country), limit)
    
    if mode == "subregion1":
        return search_sub1(normalize(subregion1),country,limit)
    
    if mode == "subregion2":
        return search_sub2(normalize(subregion2),country,subregion1,limit)
    
    if mode == "hotspot":
        return search_hotspots(normalize(hotspot),country,subregion1,subregion2,limit)
   
   
def search(table,field,query,where_clause="",where_params=(),limit=60, hotspot:bool = False):
    try:
        with sqlite3.connect('server/data/database/locations.db') as sqlConn:
             cursor = sqlConn.cursor()

        #get options from db
        sql_q = f"SELECT {field} FROM {table}{where_clause} LIMIT 150"
        
        rows = cursor.execute(sql_q, where_params).fetchall()

        print(sql_q, where_params)

        names = [r[-1] for r in rows]
        names_dict = {idx: val for idx, val in enumerate(names)}            

        #fuzzy matching
        ranked = process.extract(query,names_dict,scorer=fuzz.token_set_ratio,limit=limit)

        #structure results
        results = []
        if hotspot:
            for _,_,idx in ranked:
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

        
        for _,_,idx in ranked:
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


def tokenize(query:str):
    w_params = ()

    if query:
        tokens = [token.strip() for token in normalize(query).split() if token.strip()]

        prefix_q = query+'%' 
        w_params += (prefix_q,)  #prefix 

        for t in tokens:
            w_params += ("%" + t + '%',)
        
        return w_params,(len(tokens)+1),prefix_q
    return w_params, 0, ''


def get_where_clause(w_params:tuple,num_tokens:int,prefix_q:str,name:str, query:str = '', country:str = '', sub1:str = '', sub2:str = '', hotspot:bool = False):

    where = ' WHERE '
    where_clauses = []
    prepend = ()
    table_alias = ["","","",""]

    if hotspot:
        table_alias = ["h.","c.","s1.","s2."]

    if (query + country + sub1 + sub2) == '':
        where = ''
  
    if sub2:
        where_clauses.append(table_alias[3] + 'subnational2_name = ?')
        prepend += (sub2,)

    if sub1:
        where_clauses.append(table_alias[2] +'subnational1_name = ?')
        prepend += (sub1,)

    if country:
        where_clauses.append(table_alias[1] +'country_name = ?')
        prepend += (country,)
    
    w_params = prepend + w_params

    binders = 'OR '.join([(table_alias[0] + 'norm_name LIKE ? ')] * (num_tokens))
    if binders:
         where_clauses.append(f' ({binders}) ')

    where += ' AND '.join(where_clauses)
    
    if prefix_q:
        where += f"ORDER BY CASE WHEN {table_alias[0] + 'norm_name'} LIKE '{prefix_q}' THEN 0 ELSE 1 END, {table_alias[0] + name}"

    return where, w_params
    

def search_countries(query,limit):
    
    w_params,num_tokens,prefix_q = tokenize(query)

    where,w_params = get_where_clause(w_params=w_params,num_tokens=num_tokens,query=query,prefix_q=prefix_q,name='country_name')
    
    return search(
        table='countries',
        field='country_code, country_name, norm_name',
        where_clause=where,
        where_params=w_params,
        query=query,
        limit=limit
    )

def search_sub1(query, country,limit):

    w_params,num_tokens,prefix_q = tokenize(query)

    where,w_params = get_where_clause(w_params=w_params,num_tokens=num_tokens,query=query,prefix_q=prefix_q,name='subnational1_name', country=country)


    return search(
        table='subregions1',
        field='subnational1_code, subnational1_name, norm_name',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=limit
    )
    
def search_sub2(query,country,sub1,limit):

    w_params,num_tokens,prefix_q = tokenize(query)

    where,w_params = get_where_clause(w_params=w_params,num_tokens=num_tokens,query=query, prefix_q=prefix_q,name='subnational2_name', country=country, sub1=sub1)

    return search(
        table='subregions2',
        field='subnational2_code, subnational2_name, norm_name',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=limit
    )

def search_hotspots(query,country,sub1,sub2,limit):
    print("Q: ",query)

    w_params,num_tokens,prefix_q = tokenize(query)

    where,w_params = get_where_clause(w_params=w_params,num_tokens=num_tokens,query=query, prefix_q=prefix_q,name='name',country=country, sub1=sub1, sub2=sub2, hotspot=True)

    return search(
        table=""" 'hotspots' AS h LEFT JOIN 'countries' AS c ON h.country_code = c.country_code LEFT JOIN 'subregions1' AS s1 ON h.subnational1_code = s1.subnational1_code LEFT JOIN 'subregions2' AS s2 ON h.subnational2_code = s2.subnational2_code """,
        field='h.id, h.name, c.country_name, s1.subnational1_name, s2.subnational2_name, h.species_count, h.norm_name',
        query=query,
        where_clause=where,
        where_params=w_params,
        limit=limit,
        hotspot=True
    )