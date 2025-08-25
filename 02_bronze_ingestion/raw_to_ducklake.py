import duckdb

duckdb.install_extension("ducklake")
duckdb.load_extension("ducklake")

con = duckdb.connect(":memory:")

con.execute("ATTACH 'ducklake:/Volumes/External/developyr/source/ducklake-demo/data/catalog.ducklake' as " \
"my_lake (DATA_PATH '/Volumes/External/developyr/source/ducklake-demo/data/catalog_data')")
con.execute("USE my_lake")

con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
con.execute("CREATE SCHEMA IF NOT EXISTS silver")
con.execute("CREATE SCHEMA IF NOT EXISTS gold")

con.execute("CREATE TABLE IF NOT EXISTS bronze.people AS" \
" SELECT * FROM '/Volumes/External/developyr/source/ducklake-demo/data/core_demographics/people.csv'")

con.execute("CREATE TABLE IF NOT EXISTS bronze.regions AS" \
" SELECT * FROM '/Volumes/External/developyr/source/ducklake-demo/data/political_geography/regions.csv'")

con.execute("CREATE TABLE IF NOT EXISTS bronze.region_biome AS" \
" SELECT * FROM '/Volumes/External/developyr/source/ducklake-demo/data/political_geography/region_biome.csv'")

con.execute("CREATE TABLE IF NOT EXISTS bronze.faction_distribution AS" \
" SELECT * FROM '/Volumes/External/developyr/source/ducklake-demo/data/political_geography/faction_distribution.csv'")

con.execute("CREATE TABLE IF NOT EXISTS bronze.households AS" \
" SELECT * FROM '/Volumes/External/developyr/source/ducklake-demo/data/core_demographics/households.csv'")

people = con.execute("SELECT * FROM bronze.people LIMIT 5").df()
regions = con.execute("SELECT * FROM bronze.regions LIMIT 5").df()
region_biome = con.execute("SELECT * FROM bronze.region_biome LIMIT 5").df()
faction_distribution = con.execute("SELECT * FROM bronze.faction_distribution LIMIT 5").df()

print(people.head())
print(regions.head())
print(region_biome.head())
print(faction_distribution.head())