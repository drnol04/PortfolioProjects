--Covid 19 Data Exploration 

SELECT *
FROM CovidDeaths
where continent is not null
ORDER BY 3,4

--SELECT *
--FROM CovidVaccinations
--ORDER BY 3,4

--Select Data that we are going to be using

--Select location, date, total_cases, new_cases, total_deaths, population
--from CovidDeaths
--order by 1,2


-- Look at Total Cases vs Total Deaths

--Select location, date, total_cases, total_deaths
--from CovidDeaths
--order by 1,2

--alter table CovidDeaths
--alter column total_cases float
--alter table CovidDeaths
--alter column total_deaths float


--Shows likelihood of dying if you contract covid in your country
Select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from CovidDeaths
--where location like '%MEXICO%'
where continent is not null
order by 1,2 


---Looking at Total Cases vs Population 
---Shows what percentage of population got COVID

Select location, date, Population, total_cases, (total_cases/population)*100 as PercentPopulationInfected
from CovidDeaths
--where location like '%MEXICO%'
order by 1,2 


--Looking at countries with Highest infection rate compared to Population 
Select location, Population, MAX(total_cases) as HighestInfectionCount, MAX((total_cases/population))*100 as PercentPopulationInfected
from CovidDeaths
--where location like '%Mexico%'
group by location, population
order by PercentPopulationInfected desc



--- Showing Countries with highest Death count per Population 
--Select location,  Max(cast(total_deaths)as int)) as TotalDeathCount
--from CovidDeaths
Select location, Max(total_deaths) as TotalDeathCount
from CovidDeaths
--where location like '%Mexico%'
where continent is  null
group by location
order by TotalDeathCount desc

--- LET´S BREAK THINGS DOWN BY CONTINENT
Select continent, Max(total_deaths) as TotalDeathCount
from CovidDeaths
--where location like '%Mexico%'
where continent is not null 
group by continent
order by TotalDeathCount desc



---Showing continents with the highest death count per population


--Global numbers


Select date, sum(new_cases) as total_cases, sum(new_deaths) as total_deaths, sum(new_deaths)/sum(new_cases)*100 as DeathPercentage
from CovidDeaths
--where location like '%Mexico%'
where continent is not null 
and new_cases <>0
and new_deaths <>0
group by date
order by 1,2 

Select sum(new_cases) as total_cases, sum(new_deaths) as total_deaths, sum(new_deaths)/sum(new_cases)*100 as DeathPercentage
from CovidDeaths
--where location like '%Mexico%'
where continent is not null 
and new_cases <>0
and new_deaths <>0
--group by date
order by 1,2 


--Select date, sum(new_cases) as total_cases1, sum(new_deaths) as total_deaths1--, sum(new_deaths)/sum(new_cases)*100 as DeathPercentage
--from CovidDeaths
----where location like '%Mexico%'
--where continent is not null 
----and new_cases <>0
----and new_deaths <>0
--group by date
--order by 1,2 



-- Looking at total population vs vaccinations 
select *
from CovidDeaths dea
JOIN CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date 

select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as float)) over (partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea
JOIN CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date 
where dea.continent is not null
order by 2,3


-- USE CTE

with PopvsVac (Continent, Location, Date, Population, new_vaccinations, RollingPeopleVaccinated)
as 
(
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as float)) over (partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea
JOIN CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date 
where dea.continent is not null
and new_vaccinations is not null
--order by 2,3
)

select * , (RollingPeopleVaccinated/Population)*100 AS PERCENTAGE
from PopvsVac



--Temp Table
DROP TABLE IF exists #PercentPopulationVaccinated
Create table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeoplevaccinated numeric
)


Insert into #PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as float)) over (partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea
JOIN CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date 
where dea.continent is not null
and new_vaccinations is not null
--order by 3,2

select * , (RollingPeopleVaccinated/Population)*100 AS PERCENTAGE
from #PercentPopulationVaccinated


--Creating View to store data for later visualizations

Create view PercentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(cast(vac.new_vaccinations as float)) over (partition by dea.location order by dea.date) as RollingPeopleVaccinated
from CovidDeaths dea
JOIN CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date 
where dea.continent is not null
and new_vaccinations is not null
--order by 3,2


select * 
from PercentPopulationVaccinated