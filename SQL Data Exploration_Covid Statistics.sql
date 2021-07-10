SELECT *
FROM PortfolioProject..CovidDeaths
where continent is not null
order by 3,4

--SELECT *
--FROM PortfolioProject..CovidVaccinations
--order by 3,4

-- SELECT DATA that we are going to be using

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM PortfolioProject..CovidDeaths
where continent is not null
order by 1,2

-- Analyzing total cases vs total deaths
-- Shows the likelihood of dying if you contract COVID in India
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
FROM PortfolioProject..CovidDeaths
where location like '%India%'
order by 1,2

-- Analyzing total cases vs population
-- Shows what percentage of people got covid
-- On 13 April 2021, India hit the 1% mark (1% of the population contracted COVID)
SELECT location, date, population, total_cases, (total_cases/population)*100 as CasePercentage
FROM PortfolioProject..CovidDeaths
--where location like '%India%'
order by 1,2

-- Finding the country with the highest infection rate
SELECT location, population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as CasePercentage
FROM PortfolioProject..CovidDeaths
--where location like '%India%'
group by location, population
order by CasePercentage desc

--Showing countries with the highest death counts per population and mortality rate
SELECT location,  MAX(cast(total_deaths as int)) as HighestDeathCount, MAX((total_deaths/total_cases))*100 as DeathPercentage
FROM PortfolioProject..CovidDeaths
where continent is not null
group by location
order by HighestDeathCount desc

--Focusing by continent
--Showing continents with the highest death counts

SELECT continent,  MAX(cast(total_deaths as int)) as HighestDeathCount
FROM PortfolioProject..CovidDeaths
where continent is not null
group by continent
order by HighestDeathCount desc

--GLOBAL NUMBERS
--Till now 2% of the world who had covid have died
SELECT sum(new_cases) as TotalNewCases, sum(cast(new_deaths as int)) as TotalNewDeaths, sum(cast(new_deaths as int))/sum(new_cases)*100 as DeathPercentage
FROM PortfolioProject..CovidDeaths
--where location like '%India%'
where continent is not null
--group by date
order by 1,2


--Analyzing total population by vaccination and calculating rolling sum
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations
,sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location 
order by dea.location, dea.date) as RollingSum_Vaccinations
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 1,3

-- USE CTE FOR COMPLEX SUB QUERY (COMMON TABLE EXPRESSION)
--CTE isn't stored in memory; it is like a view (with differences of course)

with PopvsVac (location, continent, date, population, new_vaccinations, RollingSum_Vaccinations)
as 
(
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations
,sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location 
order by dea.location, dea.date) as RollingSum_Vaccinations
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 1,3
)
Select *, (RollingSum_Vaccinations/population)*100 as VaccinationPercent
from PopvsVac


--TEMP Table
drop table if exists #vaccinationpercent
create table #vaccinationpercent
(
continent nvarchar(255),
location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric)

insert into #vaccinationpercent
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations
,sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location 
order by dea.location, dea.date) as RollingSum_Vaccinations
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null

Select *, (RollingPeopleVaccinated/population)*100 as VaccinationPercent
from #vaccinationpercent

--creating view to store data for later visualizations
dROP VIEW IF EXISTS VaccinatedPeople
Create View VaccinatedPeople

AS 
Select dea.location, dea.continent, dea.date, dea.population, vac.new_vaccinations
,sum(convert(int, vac.new_vaccinations)) OVER (partition by dea.location 
order by dea.location, dea.date) as RollingSum_Vaccinations
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 1,3

select *
from VaccinatedPeople