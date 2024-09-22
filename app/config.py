from cassandra.cluster import Cluster

# Importation du module Cluster depuis la bibliothèque Cassandra
# Cassandra-driver est une bibliothèque Python qui permet d'interagir avec un cluster Apache Cassandra.
# Le module Cluster permet d'établir une connexion avec un cluster Cassandra, de gérer les nœuds du cluster et d'exécuter des requêtes.

from cassandra.cluster import Cluster

# Connexion au cluster Cassandra
# On initialise un objet Cluster en fournissant une liste des adresses IP des nœuds du cluster.
# Dans cet exemple, on se connecte au nœud local ('127.0.0.1'), qui est généralement utilisé pour une instance locale de Cassandra.
cluster = Cluster(['127.0.0.1'])  

# Connexion à un keyspace spécifique dans le cluster Cassandra
# Le keyspace dans Cassandra est un ensemble logique de tables, similaire à une base de données dans d'autres SGBD (Systèmes de Gestion de Base de Données).
# Ici, on se connecte au keyspace spécifié par 'my_keyspace'. Assurez-vous que ce keyspace a été créé dans Cassandra avant d'essayer de s'y connecter.
session = cluster.connect('my_keyspace')  