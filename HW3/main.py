import pandas as pd
import mysql.connector as sql
from tabulate import tabulate

db_connection = sql.connect(host='127.0.0.1', database='pyproject', user='root', password='Jordan1217!')
db_cursor = db_connection.cursor()
table_rows = db_cursor.fetchall()

db_cursor.execute('Delete from lifeexpectancy where population = 0')
db_connection.commit()


# Create new table and impute new averages into * Total_expenditure *
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_total_expenditure AS SELECT Country, AVG(Total_Expenditure) AS '
                  'avg_total_expenditure FROM LifeExpectancy WHERE Total_Expenditure IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_total_expenditure AS avg_total_data ON le1.Country = '
                  'avg_total_data.Country SET le1.Total_Expenditure = avg_total_data.avg_total_expenditure WHERE '
                  'le1.Total_Expenditure IS NULL;')

# Create new table and impute new averages into * alcohol *
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_alc AS SELECT Country, AVG(Alcohol) AS '
                  'avg_alc FROM LifeExpectancy WHERE alcohol IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_alc AS avg_alc_data ON le1.Country = '
                  'avg_alc_data.Country SET le1.Alcohol = avg_alc_data.avg_alc WHERE '
                  'le1.alcohol IS NULL;')
db_connection.commit()

# After filling in with new averages, we are left with Palau (one total instance) and South Sudan
# Deal with these issues
db_cursor.execute("select AVG(alcohol) as avgalc from lifeexpectancy where alcohol is not null;")
db_connection.commit()
# Use result in following step
db_cursor.execute("Update lifeexpectancy Set alcohol = 4.23 Where country = 'Palau'")
db_connection.commit()

# ------------------------------------------------------------------
# BMI
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_bmi AS SELECT Country, AVG(Bmi) AS '
                  'avg_bmi FROM LifeExpectancy WHERE Bmi IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_bmi AS avg_bmi_data ON le1.Country = '
                  'avg_bmi_data.Country SET le1.Bmi = avg_bmi_data.avg_bmi WHERE '
                  'le1.Bmi IS NULL;')
db_connection.commit()
# ------------------------------------------------------------------
# Fix other bmi values with average of bmi
db_cursor.execute('update lifeexpectancy set bmi = 40.7 where bmi is null')
db_connection.commit()
# -------------------------------------------------------------------
# population
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_pop AS SELECT Country, AVG(Population) AS '
                  'avg_pop FROM LifeExpectancy WHERE Population IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_pop AS avg_pop_data ON le1.Country = '
                  'avg_pop_data.Country SET le1.Population = avg_pop_data.avg_pop WHERE '
                  'le1.Population IS NULL;')
db_connection.commit()
# avg = 13290802.147151
db_cursor.execute('Update lifeexpectancy set population = 13290802.1 Where population is null')
db_connection.commit()

# -------------------------------------------------------------------
# Life_expectancy
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_le AS SELECT Country, AVG(life_expectancy) AS '
                  'avg_le FROM LifeExpectancy WHERE Life_expectancy IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_le AS avg_le_data ON le1.Country = '
                  'avg_le_data.Country SET le1.Life_expectancy = avg_le_data.avg_le WHERE '
                  'le1.Life_expectancy IS NULL;')
db_connection.commit()
# -------------------------------------------------------------------
# Adult_Mortality
# -------------------------------------------------------------------
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_Am AS SELECT Country, AVG(adult_mortality) AS '
                  'avg_Am FROM LifeExpectancy WHERE Adult_mortality IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_Am AS avg_Am_data ON le1.Country = '
                  'avg_Am_data.Country SET le1.Adult_mortality = avg_Am_data.avg_Am WHERE '
                  'le1.Adult_mortality IS NULL;')
db_connection.commit()
# -------------------------------------------------------------------
# le =  '71.00155'  Am = '152.9180'
# -------------------------------------------------------------------
db_cursor.execute('Update lifeexpectancy set life_expectancy = 71 Where life_expectancy is null')
db_connection.commit()
db_cursor.execute('Update lifeexpectancy set adult_mortality = 152.9 Where adult_mortality is null')
db_connection.commit()
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# GDP
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_gdp AS SELECT Country, AVG(GDP) AS '
                  'avg_gdp FROM LifeExpectancy WHERE GDP IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_gdp AS avg_gdp_data ON le1.Country = '
                  'avg_gdp_data.Country SET le1.GDP = avg_gdp_data.avg_gdp WHERE '
                  'le1.GDP IS NULL;')
db_connection.commit()
# -------------------------------------------------------------------
#Schooling
# -------------------------------------------------------------------
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_schooling AS SELECT Country, AVG(schooling) AS '
                  'avg_schooling FROM LifeExpectancy WHERE schooling IS NOT NULL GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_schooling AS avg_schooling_data ON le1.Country = '
                  'avg_schooling_data.Country SET le1.schooling = avg_schooling_data.avg_schooling WHERE '
                  'le1.schooling IS NULL;')
db_connection.commit()
# -------------------------------------------------------------------
db_cursor.execute('Update lifeexpectancy set GDP = 8706 Where GDP is null')
db_connection.commit()
db_cursor.execute('Update lifeexpectancy set Schooling = 12.7 Where Schooling is null')
db_connection.commit()
# -------------------------------------------------------------------
# -------------------------------------------------------------------
db_cursor.execute('CREATE TEMPORARY TABLE temp_avg_Pe AS SELECT Country, AVG(Percentage_Expenditure) AS '
                  'avg_Pe FROM LifeExpectancy WHERE Percentage_Expenditure != 0 GROUP BY Country;')
db_connection.commit()
db_cursor.execute('UPDATE LifeExpectancy AS le1 JOIN temp_avg_pe AS avg_pe_data ON le1.Country = '
                  'avg_pe_data.Country SET le1.Percentage_Expenditure = avg_pe_data.avg_pe WHERE '
                  'le1.Percentage_Expenditure = 0;')
db_connection.commit()
# avg PE = 1103.1365580115546
db_cursor.execute('Update lifeexpectancy set Percentage_Expenditure = 1103.1 Where Percentage_Expenditure = 0')
db_connection.commit()
# -------------------------------------------------------------------


db_cursor.execute('select * from temp_avg_alc')
table_rows2 = db_cursor.fetchall()
db_connection.commit()

lifeExDF = pd.DataFrame(table_rows)
lifeExDF2 = pd.DataFrame(table_rows2)
print(tabulate(lifeExDF, headers='keys', tablefmt='fancy_grid'))
print(tabulate(lifeExDF2, headers='keys', tablefmt='fancy_grid'))
print(lifeExDF.describe())
