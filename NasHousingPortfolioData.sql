/*

--Cleaning data in SQL Queries to make it more usable

*/
select *
from Portfolio.dbo.[Nashville Housing]


--select SaleDate, convert(date, saledate) as SaleDatev1
--from Portfolio.dbo.[Nashville Housing]

--update [Nashville Housing]
--SET SaleDate =  convert(date, saledate) 

alter table [Nashville Housing]
alter column SaleDate date

select *
from Portfolio.dbo.[Nashville Housing]
order by 2




--Populate Property Address DATA

 select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
 from [Nashville Housing] a
 Join [Nashville Housing] b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null 


update a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
 from [Nashville Housing] a
 Join [Nashville Housing] b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null 


SELECT *
FROM [Nashville Housing]



---Breaking out address into individual columns (Address, city, state)

select *
from [Nashville Housing]



select 
SUBSTRING(PropertyAddress, 1,CHARINDEX(',', PropertyAddress)-1 ) as Address, 
SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, len(PropertyAddress)) as Address
from [Nashville Housing]


alter table [Nashville Housing]
add PropertySplitAddress nvarchar(255);

update [Nashville Housing]
SET PropertySplitAddress =  SUBSTRING(PropertyAddress, 1,CHARINDEX(',', PropertyAddress)-1 )

alter table [Nashville Housing]
add PropertySplitCity nvarchar(255);
--AN ERROR, DELETE THE SECOND 'ADD PROPERTYSPLITADDRESS1'
--alter table [Nashville Housing]
--drop column PropertySplitAddress1

update [Nashville Housing]
SET PropertySplitCity =  SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) + 1, len(PropertyAddress))

select *
from [Nashville Housing]





select OwnerAddress
from [Nashville Housing]


SELECT
PARSENAME(replace(OwnerAddress, ',', '.'),3),
PARSENAME(replace(OwnerAddress, ',', '.'),2),
PARSENAME(replace(OwnerAddress, ',', '.'),1)
FROM [Nashville Housing]

alter table [Nashville Housing]
add OwnerSplitAddress nvarchar(255);

update [Nashville Housing]
SET OwnerSplitAddress =  PARSENAME(replace(OwnerAddress, ',', '.'),3)


alter table [Nashville Housing]
add OwnerSplitcity nvarchar(255);

update [Nashville Housing]
SET OwnerSplitCity =  PARSENAME(replace(OwnerAddress, ',', '.'),2)

alter table [Nashville Housing]
add OwnerSplitState nvarchar(255);


update [Nashville Housing]
SET OwnerSplitState =  PARSENAME(replace(OwnerAddress, ',', '.'),1)


select *
from Portfolio..[Nashville Housing]


---CHange Y and N to Yes and No in "Sold as Vacant" field

select Distinct(SoldAsVacant), count(SoldAsVacant)
from Portfolio..[Nashville Housing]
group by SoldAsVacant
order by 2


select(SoldAsVacant),
	 case when SoldAsVacant = 'Y' then 'Yes'
		  when SoldAsVacant = 'N' then 'No'
		  else SoldAsVacant
	 end 
	
from Portfolio..[Nashville Housing]


Update [Nashville Housing]
set SoldAsVacant =case when SoldAsVacant = 'Y' then 'Yes'
		  when SoldAsVacant = 'N' then 'No'
		  else SoldAsVacant
	 end 


select *
from [Nashville Housing]




---Remove Duplicants
--ALL OF THIS IS FOR TAKING THE DUPLICATES

--With ROWNumCTE AS (
--select *,
--	Row_number() over (
--	Partition by ParcelID,
--				 PropertyAddress,
--				 SaleDate,
--				 SalePrice,
--				 LegalReference
--				 Order by 
--					UniqueID
--					) row_num

--from [Nashville Housing]
----order by ParcelID
--)
--select *
--FROM RowNumCTE
--WHERE row_num > 1
--order by PropertyAddress

--AND NOW TO DELETE THEM

With ROWNumCTE AS (
select *,
	Row_number() over (
	Partition by ParcelID,
				 PropertyAddress,
				 SaleDate,
				 SalePrice,
				 LegalReference
				 Order by 
					UniqueID
					) row_num

from [Nashville Housing]
--order by ParcelID
)
DELETE
FROM RowNumCTE
WHERE row_num > 1
--order by PropertyAddress

---LET´S SEE
With ROWNumCTE AS (
select *,
	Row_number() over (
	Partition by ParcelID,
				 PropertyAddress,
				 SaleDate,
				 SalePrice,
				 LegalReference
				 Order by 
					UniqueID
					) row_num

from [Nashville Housing]
--order by ParcelID
)
--CHECK BEFORE
SELECT *
FROM RowNumCTE
WHERE row_num > 1


---SEE THE DATA WITHOUT DUPLICATES
select *
from [Nashville Housing]



---Delete Unused Columns


select*
from Portfolio..[Nashville Housing]

Alter table Portfolio..[Nashville Housing]
drop column OwnerAddress, TaxDistrict, PropertyAddress

Alter table Portfolio..[Nashville Housing]
drop column SaleDate


---END---