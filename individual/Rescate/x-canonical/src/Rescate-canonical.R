#!/usr/bin/env Rscript --vanilla

# Rescate/canonical/src/Rescate-canonical.R
# UPDATE 07/2014 Performs Rescate-specific canonicalization tasks
# UPDATE 07/2014 Other canonicalization tasks have moved to SV/clean/etc
# Authors:     AHG
# Maintainers: AHG, PB
# Copyright:   2014, HRDAG, GPL v2 or later
# =============================================

suppressPackageStartupMessages(library("argparse"))
parser <- ArgumentParser()
parser$add_argument("--functions", type='character')
parser$add_argument("--rescate", type='character')
parser$add_argument("--dept", type='character')
parser$add_argument("--vtypus",type='character')
parser$add_argument("--geocodes",type='character')
parser$add_argument("--output",type='character')
arguments <- parser$parse_args()

### READ IN DATA AND FUNCTIONS ###

options(scipen=999999)
source(arguments$functions)

rescate <- read.table(arguments$rescate,fill=TRUE,as.is=TRUE,header=TRUE,sep='|',quote="")
print(str(rescate))

vtyp <- read.table(arguments$vtypus,header=TRUE,fill=TRUE,as.is=TRUE,sep='|',fileEncoding='latin1',quote="")
vtyp <- fix.db.colnames(vtyp)
print(str(vtyp))

dept <- read.table(arguments$dept,header=TRUE,fill=TRUE,as.is=TRUE,sep='|',fileEncoding='latin1',quote="")
dept <- fix.db.colnames(dept)
print(str(dept))

geocodes <- read.table(arguments$geocodes,header=TRUE,fill=TRUE,as.is=TRUE,sep=',')
print(str(geocodes))

### FIX DATES ###

get.year <- function(datestr){
	return(unlist(strsplit(datestr,'-',fixed=TRUE))[1])
}
get.month <- function(datestr){
	return(unlist(strsplit(datestr,'-',fixed=TRUE))[2])
}
get.day <- function(datestr){
	return(unlist(strsplit(datestr,'-',fixed=TRUE))[3])
}

rescate$date <- rescate$VIOLATION_
rescate$year <- unlist(lapply(rescate$VIOLATION_,get.year))
rescate$month <- unlist(lapply(rescate$VIOLATION_,get.month))
rescate$day <- unlist(lapply(rescate$VIOLATION_,get.day))

head(table(rescate$date),n=50)


### FIX VIOLS ###

rescate$violation <- NA
rescate$newviol <- NA

colnames(vtyp) <- c('code','name','reportcode','reportname')

viols <- unique(rescate$VTYPCODE)
for (v in viols){
	desc <- setdiff(vtyp$name[vtyp$code==v],NA)
	rescate$violation[rescate$VTYPCODE==v] <- desc
	}

rescate$lethal <- NA

table(rescate$violation,useNA='always')
rescate$VTYPCODE <- NULL

### PERPS ###

uniqueperps <- function(perpstr){
  if(length(grep('-',perpstr,fixed=TRUE))>0) {
    perplist <- unique(unlist(strsplit(perpstr,'-')))
    perplist <- perplist[order(perplist)]
    return(paste(perplist,collapse='-'))
  }
  else {
    perplist <- unique(unlist(strsplit(perpstr,',')))
    perplist <- perplist[order(perplist)]
    return(paste(perplist,collapse='-'))
  }
}

rescate$perpstr <- paste(rescate$perp1,rescate$pdesc1,
                         rescate$perp2,rescate$pdesc2,
                         rescate$perp3,rescate$pdesc3,
                         rescate$perp4,rescate$pdesc4,
                         sep='-')

rescate$perpstr <- unlist(lapply(rescate$perpstr,uniqueperps))
table(rescate$perpstr)

rescate$state.or.FMLN <- NA

table(rescate$state.or.FMLN)

### FIX GEO ###

rescate$site <- trim(toupper(rescate$SITE))
rescate$site[rescate$site==''] <- 'UNKNOWN'
rescate$town <- trim(toupper(rescate$TOWN_CITY))
rescate$town[rescate$town==''] <- 'UNKNOWN'
rescate$juris <- trim(toupper(rescate$JURISDICTI))
rescate$juris[rescate$juris==''] <- 'UNKNOWN'

rescate$muni <- 'UNKNOWN'

# depts #

rescate$DEPTCODE <- toupper(rescate$DEPTCODE)
depts <- unique(rescate$DEPTCODE)
depts <- setdiff(depts,c('?',NA))

rescate$dept <- 'UNKNOWN'

for (d in depts){
  new.dept <- dept$NAME[dept$DEPTCODE==d]
  rescate$dept[rescate$DEPTCODE==d] <- new.dept
}

rescate$dept <- toupper(rescate$dept)
rescate$DEPTCODE <- NULL

table(rescate$dept)

# muni #

rescate$muni <- 'UNKNOWN'

# placestr
rescate$placestr <- paste(rescate$site, rescate$town, rescate$juris,rescate$dept,sep=', ')

# ditch old geo columns

rescate$site2 <- NULL
rescate$town2 <- NULL
rescate$juris2 <- NULL
rescate$site <- NULL
rescate$town <- NULL
rescate$juris <- NULL


### DEAL WITH NAMES ###

rescate$fullname <- toupper(rescate$VICTIM_NAM)
print(head(table(rescate$fullname),n=25))

rescate$fullname[rescate$fullname==''] <- NA
rescate$firstname <- NA
rescate$lastname <- NA

# temporarily stick some commonly used small words to their big partners
# also take care of double spaces

rescate$fullname <- gsub(' DE ',' DE-',rescate$fullname,fixed=TRUE)
rescate$fullname <- gsub(' DEL ',' DEL-',rescate$fullname,fixed=TRUE)
rescate$fullname <- gsub(' Y ',' Y-',rescate$fullname,fixed=TRUE)
rescate$fullname <- gsub(' DE-LA ',' DE-LA-',rescate$fullname,fixed=TRUE)
rescate$fullname <- gsub(' DE-LOS ',' DE-LOS-',rescate$fullname,fixed=TRUE)
rescate$fullname <- gsub('  ',' ',rescate$fullname)

# find number of tokens in fullname field
print('getting number of names')
ntokens <- function(string){
  return(length(unlist(strsplit(string,' ',fixed=TRUE))))
}
rescate$nametokens <- unlist(lapply(rescate$fullname,ntokens))
table(rescate$nametokens)

# split up fullname

find.space <- function(fullname){
  return(which(unlist(strsplit(fullname,character(0)))==' '))
}

split.at.nth <- function(fullname,n){
  return(c(substr(fullname,1,n-1),substr(fullname,n+1,nchar(fullname))))
}

for (i in 1:nrow(rescate)) {
  if (rescate$nametokens[i]==1 ){
    rescate$firstname[i] <- rescate$fullname[i]
    rescate$lastname[i] <- NA
  }
  else if (rescate$nametokens[i]==2){
    names <- unlist(strsplit(rescate$fullname[i],' '))
    rescate$firstname[i] <- names[1]
    rescate$lastname[i] <- names[2]
  }
  else if (rescate$nametokens[i]==3){
    spl <- find.space(rescate$fullname[i])[1]
    names <- split.at.nth(rescate$fullname[i],spl)
    rescate$firstname[i] <- names[1]
    rescate$lastname[i] <- names[2]
  }
  else {
    spl <- find.space(rescate$fullname[i])[2]
    names <- split.at.nth(rescate$fullname[i],spl)
    rescate$firstname[i] <- names[1]
    rescate$lastname[i] <- names[2]
  }
}

# now remove those added hyphens

rescate$fullname <- trim(gsub('-',' ',rescate$fullname,fixed=TRUE))
rescate$firstname <- trim(gsub('-',' ',rescate$firstname,fixed=TRUE))
rescate$lastname <- trim(gsub('-',' ',rescate$lastname,fixed=TRUE))

print(head(table(rescate$fullname)))
print(head(table(rescate$firstname)))
print(head(table(rescate$lastname)))

rescate$nametokens <- NULL

#### WRITE OUT ####
print(str(rescate))
write.table(rescate,file=arguments$output,row.names=FALSE,sep='|',quote=FALSE)
