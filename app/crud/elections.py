
import io
from sqlalchemy.orm import Session
from app.database.database_crm import engine_crm

from fastapi import HTTPException

import pandas as pd


'''
    Always returned information by election
'''
dict_agregat = {
    'Municipales 2020': 'nuance',
    'Départementales 2015': 'nuance',
    'Législatives 2017': 'nuance',
    'Régionales 2015': 'nuance',
    'Régionales 2021': 'nuance',
    'Européennes 2014': 'nuance, nom, prenom',
    'Européennes 2019': 'nom_liste',
    'Présidentielles 2017': 'nuance, nom, prenom'
}


'''
    Detailled returned information by eelction
'''
dict_detail = {
    'Municipales 2020': 'nom, prenom',
    'Départementales 2015': 'num_dep_binome_candidat',
    'Législatives 2017': 'nom, prenom',
    'Régionales 2015': 'nom, prenom',
    'Régionales 2021': 'nom, prenom',
    'Européennes 2014': None,
    'Européennes 2019': None,
    'Présidentielles 2017': None
}


'''
    Hierarchical level of territorial division
'''
dict_maillage = {
    'bureau': 0,
    'commune': 1,
    'canton': 2,
    'circonscription': 3,
    'departement': 4,
    'region': 5,
    'national': 6 
    }


'''
    Election type with the level of division where we use detailled datas
'''
dict_election = {
    'Municipales': 1,
    'Départementales': 2,
    'Legislatives': 3,
    'Régionales': 4,
    'Européennes': 6,
    'Présidentielles': 6    
}


# 1er endpoint Participation
def get_participation(
    db: Session,
    scope: dict,
    election: str,
    tour: int,
    maillage: str,
    code_zone: str
):
    '''
        Retourne les informations de participations pour l'election et la zone selectionnee
    '''
    # pour le moment pas de scope, pas d'utilisation de db: Session (orm)
    query_participation = f'''
        select 
          election,
          tour,
          {maillage},
          cast(sum(inscrits) as integer) as inscrits,
          cast(sum(votants) as integer) as votants,
          cast(sum(exprimes) as integer) as exprimes 
        from (
          select distinct 
            election,
            tour,
            {maillage},
            inscrits,
            votants,
            exprimes 
          from elections
          where {maillage} = '{code_zone}'
            and election = '{election}'
            and tour = '{tour}'
        ) bureau_election
        where {maillage} = '{code_zone}'
          and election = '{election}'
          and tour = '{tour}'
        group by
          election,
          tour,
          {maillage}
        '''

    copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
        query=query_participation, head="HEADER")
    conn = engine_crm.raw_connection()
    cur = conn.cursor()
    store = io.StringIO()
    cur.copy_expert(copy_sql, store)
    store.seek(0)
    df = pd.read_csv(store, encoding='utf-8')

    return df


def ElectionAgregat(election: str, division: str):
    type_election = election.split()[0]
    if type_election not in dict_agregat.keys():
        raise HTTPException(status_code=400, detail=f'No data for election {election}')
    if division not in dict_maillage.keys():
        raise HTTPException(status_code=400, detail=f'The division {division} is not available yet')
    if dict_maillage[division] <= dict_election[type_election]:
        return dict_agregat[election] \
               + (', ' + dict_detail[election] if dict_detail[election] else '')
    return dict_agregat[election]


# 1er endpoint bis Results
def get_results(
    db: Session,
    scope: dict,
    election: str,
    tour: int,
    maillage: str,
    code_zone: str
):
    '''
        Retourne les resultats pour l'election et la zone selectionnee
    '''
    # pour le moment pas de scope, pas d'utilisation de db: Session (orm)
    agregat = ElectionAgregat(election, maillage)
    
    query_resultats = f'''
        select
          {agregat},
          cast(sum(voix) as integer) as voix
        from elections
        where {maillage} = '{code_zone}'
          and election = '{election}'
          and tour = '{tour}'
        group by
          {agregat}
        order by
          voix desc
        '''

    copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
        query=query_resultats, head="HEADER")
    conn = engine_crm.raw_connection()
    cur = conn.cursor()
    store = io.StringIO()
    cur.copy_expert(copy_sql, store)
    store.seek(0)
    df = pd.read_csv(store, encoding='utf-8')

    return df