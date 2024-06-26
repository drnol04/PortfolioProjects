
-- Data Cleaning --
select *
from layoffs;

-- Remove duplicates
-- Standardize the data 
-- Null Values or blanck values
-- Remove any columns 

-- CREATE A DATA BASE 
create table layoffs_staging
like layoffs;

-- 


select *
from layoffs_staging;

insert layoffs_staging
select * 
from layoffs;

-- Remove duplicates

SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, 'date') as row_num
from layoffs_staging;

with duplicates_cte as
(
SELECT *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, 
'date', stage, country, funds_raised_millions) as row_num
from layoffs_staging
)

select * 
from duplicates_cte
where row_num > 1;

select *
from layoffs_staging
where company = 'Oda';


CREATE TABLE `layoffs_staging2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_num` int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


select *
from layoffs_staging2;

select *
from layoffs_staging2
where row_num = 2;

insert into layoffs_staging2
select *,
ROW_NUMBER() OVER(
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, 
'date', stage, country, funds_raised_millions) as row_num
from layoffs_staging;

delete
from layoffs_staging2
where row_num > 1;

select *
from layoffs_staging2;

-- Standardizzing data
select company, trim(company)
from layoffs_staging2;

update layoffs_staging2
set company = trim(company);

select *
from layoffs_staging2
where industry like 'Crypto%';

update layoffs_staging2
set industry = 'Crypto'
where industry like 'Crypto%';

select distinct company
from layoffs_staging2;


select *
from layoffs_staging2
where country = 'United States.';

update layoffs_staging2
set country = 'United States'
where country like 'United States.';
-- or using the function TRIM( TRAILING '.' FROM COUNTRY)
select *
from layoffs_staging2
where country = 'United States' ;

SELECT `date`
FROM layoffs_staging2; 

update layoffs_staging2
set `date` = str_to_date(`date`, '%m/%d/%Y');

SELECT `date`
FROM layoffs_staging2; 


alter table layoffs_staging2
modify column `date` Date; 

select *
from layoffs_staging2;

-- NULL BLANCK VALUES

SELECT *
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL; 

update  layoffs_staging2
set industry = null 
where industry = '';

SELECT *
from layoffs_staging2
where industry is null 
or industry = '';

select t1.industry, t2.industry
from layoffs_staging2 t1
join layoffs_staging2 t2
	on t1.company = t2.company
where (t1.industry is null or t1.industry = '')
and t2.industry is not null;

update layoffs_staging2 t1
join layoffs_staging2 t2
    on t1.company = t2.company
set t1.industry = t2.industry
where t1.industry is null
and t2.industry is not null;

select * 
from layoffs_staging2
where company like 'Bally%';

select *
from layoffs_staging2;
where company is  null or company = '';

SELECT *
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL; 

delete 
FROM layoffs_staging2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL; 

select *
from layoffs_staging2;

alter table layoffs_staging2	
drop column row_num;

-- FINAL -- 
select *
from layoffs_staging2;






