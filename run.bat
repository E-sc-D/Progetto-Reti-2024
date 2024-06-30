start cmd /k scripts\server.py
for /l %%x in (1, 1, %1) do start cmd /k  scripts\client.py
rem this file starts the server and n clients specified by the first passed argument