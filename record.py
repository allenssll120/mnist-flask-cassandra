import logging

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

KEYSPACE = "newkeyspace5"

def createKeySpace():
   cluster = Cluster(contact_points=['0.0.0.0'],port=33)
   session = cluster.connect()
   log.info("Creating keyspace...")
   try:
       session.execute("""
           CREATE KEYSPACE %s
           WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
           """ % KEYSPACE)

       log.info("setting keyspace...")
       session.set_keyspace(KEYSPACE)

       log.info("creating table...")
       session.execute("""
           CREATE TABLE record_data (
               time timestamp,
               file text,
               result text,
               PRIMARY KEY (time)
           )
           """)
   except Exception as e:
       log.error("Unable to create keyspace.")
       log.error(e)

def recordData(time,file,result):
    cluster = Cluster(contact_points=['0.0.0.0'],port=33)
    session = cluster.connect(KEYSPACE)
    log.info("Recording data...")
    try:
        session.execute("""
            INSERT INTO record_data(time,file,result)
            VALUES(%s,%s,%s);
            """,(time,file,result))
    except Exception as e:
       log.error("Unable to record data.")
       log.error(e)
