# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "63c78d9e-8b77-43ed-ba61-a34eb29a09a6",
# META       "default_lakehouse_name": "lakehouse1",
# META       "default_lakehouse_workspace_id": "d056be62-591c-4dbf-aba8-d17c5f5f4b16",
# META       "known_lakehouses": [
# META         {
# META           "id": "63c78d9e-8b77-43ed-ba61-a34eb29a09a6"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
print('hello analytics team in feature branch workspace')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM lakehouse1.health_data LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
