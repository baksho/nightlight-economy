## nightlight_economy
There are several notable research papers that explore the use of nighttime lights as a proxy for economic activity. This approach is widely used due to the availability of satellite data that provides consistent and objective measures of light emissions, which correlate with human activities and economic development. This approach based on machine learning algorithms explores the correlation between night time luminosity with economic development of a country.

**This project is not final. Updates are in progress.**

#### Additional features included
1. **Correlate with GDP**: This function correlates night light intensity with GDP for a specific country. We use `rasterio` to mask the night light data to the country's geographic area and then calculate the correlation coefficient with GDP data.
2. **Time Series Analysis**: This function loads multiple monthly night light datasets and calculates average light intensity over time to observe changes. This feature helps identify trends in economic activity over the year.
3. **Handling Large Data with Dask**: We use `Dask` to efficiently process large datasets. Dask enables out-of-core computation by breaking data into manageable chunks and processing them in parallel.

#### Working with the script
- **Download Multiple Datasets**: We use multiple night light GeoTIFF files for time series analysis, named sequentially, such as `VIIRS_2023_01.tif`, `VIIRS_2023_02.tif` etc.
- **Country GDP Data**: The script uses the `naturalearth_lowres` dataset from GeoPandas, which includes basic GDP estimates. For more precise GDP data, consider integrating with other sources, such as World Bank datasets.

#### Additional Considerations
1. **Data Availability**: Night light data can be downloaded from [NOAA](https://www.noaa.gov/) and economic data from databases like the [World Bank](https://data.worldbank.org/).
2. **Modeling and Regression**: For more sophisticated analysis, consider using machine learning models to predict economic activity based on night light intensity and other variables.
3. **Parallel Computing**: Leverage Dask or other parallel computing frameworks for extensive datasets.

#### Additional Academic Papers
1. Henderson, J. V., Storeygard, A., Weil, D. N. (2009). Measuring Economic Growth from Outer Space. In National Bureau of Economic Research Working Paper Series, Working Paper 15199 [link](https://www.nber.org/system/files/working_papers/w15199/w15199.pdf)
2. Li, X., Zhou, Y., Zhao, X., Zhao, M. (2020). A harmonized global nighttime light dataset 1992–2018. In Nature.com Scientific Data Vol. 7, Article 168 [link](https://www.nature.com/articles/s41597-020-0510-y)
3. Chen, X. (2014). Making Visible the Invisible: Nighttime Lights Data and the Closing of the Human Rights Information Gap. In Case Western Reserve University, Societies Without Borders, Vol. 9, Issue 2, Article 6 [link](https://scholarlycommons.law.case.edu/swb/vol9/iss2/6/)
4. Nighttime Lights as a Proxy for Economic Performance of Regions (2022). DOI: 10.3390/books978-3-0365-3438-1, Publisher: MDPI [link](https://www.researchgate.net/publication/360145606_Nighttime_Lights_as_a_Proxy_for_Economic_Performance_of_Regions)
5. Prakash, A., Shukla, A. K., Bhowmick, C., Beyer, R. C. M. (2019). Night-time Luminosity: Does it Brighten Understanding of Economic Activity in India?. In Reserve Bank of India Occasional Papers Vol. 40, No. 1, 2019 [link](https://rbidocs.rbi.org.in/rdocs/Content/PDFs/01AR30072019EF4B60BF96E548F284D2C95EB59DD9A9.PDF)
