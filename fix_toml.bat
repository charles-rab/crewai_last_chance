@echo off
echo [project] > pyproject.toml
echo name = "crewai_last_chance" >> pyproject.toml
echo version = "0.1.0" >> pyproject.toml
echo description = "Crewai_Last_Chance using crewAI" >> pyproject.toml
echo authors = [{ name = "Charles Rabico", email = "c.rabico@revivastudios.online" }] >> pyproject.toml
echo requires-python = ">=3.10,^<3.13" >> pyproject.toml
echo dependencies = [ >> pyproject.toml
echo     "crewai[tools]>=0.114.0,^<1.0.0" >> pyproject.toml
echo ] >> pyproject.toml
echo. >> pyproject.toml
echo [project.scripts] >> pyproject.toml
echo crewai_last_chance = "crewai_last_chance.main:run" >> pyproject.toml
echo run_crew = "crewai_last_chance.main:run" >> pyproject.toml
echo train = "crewai_last_chance.main:train" >> pyproject.toml
echo replay = "crewai_last_chance.main:replay" >> pyproject.toml
echo test = "crewai_last_chance.main:test" >> pyproject.toml
echo. >> pyproject.toml
echo [build-system] >> pyproject.toml
echo requires = ["hatchling"] >> pyproject.toml
echo build-backend = "hatchling.build" >> pyproject.toml
echo. >> pyproject.toml
echo [tool.crewai] >> pyproject.toml
echo type = "crew" >> pyproject.toml