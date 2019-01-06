#Carreguem el dataset
PhotoDataset <- read.table("D:/Users/cagarcia/uoc/M2951/data/productData.csv", header=TRUE, sep=";", na.strings="NA", dec=".", strip.white=TRUE)

#Visualitzem les dades
fix(PhotoDataset)

#Resum de dades
summary(PhotoDataset)

#Comprovem que les columnes description i altImage són iguals
countDistinct <- length(which(PhotoDataset$description != PhotoDataset$altImage)) 
countDistinct

#Eliminem les columnes redundants
PhotoDataset <- subset( PhotoDataset, select = -c(price, stock, puntuation, stock, altImage, image) )

#Ens quedem amb el dia de la captura i eliminem dia i hora
PhotoDataset <- subset( PhotoDataset, select = -c(date, dateHour) )

#Estudiem la correlació entre variables numèriques
cor(PhotoDataset[,c("page","priceMax","priceValue","puntuationValue","stockValue")], use="complete")

#Eliminem duplicats, agafant la mínima pàgina
require(sqldf)
PhotoDataset <- sqldf("select	distinct searchConcept,code,imgName,description,priceValue,priceCurrency,priceMax,puntuationValue,stockValue,dateDay,min(page) as page from PhotoDataset group by searchConcept,code,imgName,description,priceValue,priceCurrency,priceMax,puntuationValue,stockValue,dateDay", drv = 'SQLite')

#Obtenim les dades
sqldf("select page, count(*) from PhotoDataset group by page order by page asc", drv = 'SQLite')

#Creem la columna que indica si hi ha stock limitat (1) o no (0)
PhotoDataset$stockIsLimited <- ifelse(is.na(PhotoDataset$stockValue), 0, 1)

#Validem que l'existència d'stock s'ha calculat ok
sqldf("select stockValue, stockIsLimited, count(*) from PhotoDataset group by stockValue, stockIsLimited", drv = 'SQLite')
sqldf("select stockIsLimited, count(*) from PhotoDataset group by stockIsLimited", drv = 'SQLite')


# Agrupem les pàgines
# Considerem que les pàgines 1-5 són més rellevants que les de 6-10, i aquestes més que les 11-15, ...
PhotoDataset$pageRelevance <- trunc((PhotoDataset$page-1) / 5)
sqldf("select page, count(*) from PhotoDataset group by page order by page asc", drv = 'SQLite')
sqldf("select pageRelevance, count(*) from PhotoDataset group by pageRelevance order by pageRelevance asc", drv = 'SQLite')
with(PhotoDataset, Hist(pageRelevance, scale="frequency", breaks="Sturges", col="darkgray"))


#Calculem els rangs de preus per a validar la dispersió
PhotoDataset$priceRang <- trunc(PhotoDataset$priceValue / 500)
sqldf("select priceRang, count(*) from PhotoDataset group by priceRang order by priceRang asc", drv = 'SQLite')

#Calculem la distribució dels preus
sd(PhotoDataset$priceValue, na.rm = FALSE)

#Assignem el valor de 3.000 als preus superiors
PhotoDataset$priceValue <- ifelse(PhotoDataset$priceValue > 3000, 3000, PhotoDataset$priceValue)

#Standaritzem el preu
PhotoDataset <- local({
  .Z <- scale(PhotoDataset[,c("priceValue")])
  within(PhotoDataset, {
    Z.priceValue <- .Z[,1] 
  })
})
with(PhotoDataset, Hist(Z.priceValue, scale="frequency", breaks="Sturges", col="darkgray"))

#Estudi de les puntuacions
summary(PhotoDataset$puntuationValue)
sd(PhotoDataset$puntuationValue, na.rm = TRUE)
#Assignam la mitja a les puntuacions NA
PhotoDataset$puntuationValue[is.na(PhotoDataset$puntuationValue)] <- mean(PhotoDataset$puntuationValue, na.rm = TRUE)

#Matriu de correlacions
cor(PhotoDataset[,c("page","priceMax","priceRang","priceValue","puntuationValue","stockValue","Z.priceValue", "pageRelevance", "stockIsLimited")], use="complete")
cor(PhotoDataset[,c("page","priceMax","priceRang","priceValue","puntuationValue","stockValue","Z.priceValue")], use="complete")

#Detall de les correlacions de preu
pageRelevance0 <- PhotoDataset[PhotoDataset$pageRelevance==0, ]
pageRelevance1 <- PhotoDataset[PhotoDataset$pageRelevance==1, ]
pageRelevance2 <- PhotoDataset[PhotoDataset$pageRelevance==2, ]
pageRelevance3 <- PhotoDataset[PhotoDataset$pageRelevance==3, ]
pageRelevance4 <- PhotoDataset[PhotoDataset$pageRelevance==4, ]



