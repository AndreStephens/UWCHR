require(gdata)

datesep <- function(datestring){
  # takes an ostensibly-date string
  # returns a list of parts as separated by hyphen, slash or period
  dlist <- unlist(strsplit(datestring, '-'))
  if (length(dlist)<3) dlist <- unlist(strsplit(datestring, '/'))
  if (length(dlist)<3) dlist <- unlist(strsplit(datestring, '.'))
  return(dlist)
}

check.date.quality <- function(datestring){
  # takes an ostensibly-date string
  # returns 1 if datesep(datestring) has three parts, 0 if not
  datelength <- length(datesep(datestring))
  return(ifelse(datelength==3,1,0))
}

get.date.part <- function(datecol, part.of.date){
  # takes a date column and a part of date ('year' or 'month' or 'day')
  # returns a column of the specified part
  # e.g. data$month <- get.date.order(data$date)
  datecol[is.na(datecol)] <- '0-0-0'                  # get rid of NAs
  datecheck <- sapply(datecol,check.date.quality)     # check for too-short dates
  if (0 %in% datecheck) {
    print(table(datecheck))
    print(datecol[datecheck==0]) 
    print('date(s) cannot be parsed! sapply check.date.quality and see what went wrong!')         
    stop                                          # stop if there are bad dates
  }
  datematrix <- sapply(datecol, datesep)
  d1 <- as.numeric(datematrix[1,])
  m1 <- max(d1)
  assign(as.character(m1),d1)
  d2 <- as.numeric(datematrix[2,])
  m2 <- max(d2)
  assign(as.character(m2),d2)
  d3 <- as.numeric(datematrix[3,])
  m3 <- max(d3)
  assign(as.character(m3),d3)
  stopifnot (m1!=m2 & m1!=m3 & m2!=m3)
  if (part.of.date=='month'){
    month <- as.character(min(c(m1,m2,m3)))
    return(as.numeric(get(month)))
  }
  else if (part.of.date=='year'){
    year <- as.character(max(c(m1,m2,m3)))
    return(as.numeric(get(year)))
  }
  else {
    month <- as.character(median(c(m1,m2,m3)))
    return(as.numeric(get(month)))
  }
}

##########################################

get.canonical.vocab <- function(keystring, vocablist, gen.or.specific){
  # takes string, list from which you're looking from vocab, and "general" or "specific"
  # "general" means perp categories for matching, e.g. "Salvadoran Army"
  # "specific" means canonical version of more specific perp label, e.g. "Second Brigade"
  new.vocab <- ''
  key <- unlist(strsplit(keystring, '-'))
  if (gen.or.specific=='specific') {
    for (k in key){
      if (k %in% vocablist$old){
        n <- setdiff(vocablist$new.specific[vocablist$old==k],NA)
      }
      else n <- 'Unknown'
      new.vocab <- paste(new.vocab,n,sep='-')
    }
  }
  else if (gen.or.specific=='general'){
    for (k in key){
      if (k %in% vocablist$old){
        n <- setdiff(vocablist$new[vocablist$old==k],NA)
      }
      else n <- 'Unknown'
      new.vocab <- paste(new.vocab,n,sep='-')
    }
  }
  else {
    print('cannot recognize general or specific command. only general or specific are accepted. did you misspell?')
    stop
  }
  new.vocab <- sub('-','',new.vocab)
  return(new.vocab)
}
##############################################

# function generators
# perp.vocab and viol.vocab are in individual/share/src,
# and can be linked to any individual/* project in SV
# they should always be called AS perp.vocab and viol.vocab, otherwise
# the code won't work, e.g.
# viol.vocab <- read.table('share/src/viols-vocab.csv', etc. etc.)

get.perp <- function(keystring){
  return(get.canonical.vocab(keystring,perp.vocab,'general'))
}

get.perp.specific <- function(keystring){
  return(get.canonical.vocab(keystring,perp.vocab,'specific'))
}

get.viol <- function(keystring){
  return(get.canonical.vocab(keystring,viol.vocab,'general'))
}

get.viol.specific <- function(keystring){
  return(get.canonical.vocab(keystring,viol.vocab,'specific'))
}

## general purpose string splitters

split.general <- function(splitter){
  # takes splitter
  # returns function to return vector of string parts
  return(
         function(stringlist){
           return(unlist(strsplit(stringlist,splitter,fixed=TRUE)))
         }
         )
}

comma.split <- split.general(',') # returns vector of string parts as split by commas
    

split.and.find <- function(stringlist,splitter,n){
  # takes string, splitter, and n
  # returns nth string part from string, as split by splitter
  new <- unlist(strsplit(stringlist,splitter))
  new.n <- new[n]
  return(new.n)
}

make.split.and.find <- function(splitter,n){
  # returns specific versions of split.and.find
  return(
         function(stringlist){
           return(split.and.find(stringlist,splitter,n))
         }
         )
}

get.last <- function(placestr){
  # specific to CDHES, for now
  # takes a place string and returns the final location
  # usually the department, in CDHES
  parts <- unlist(strsplit(placestr,','))
  last <- length(parts)
  candidate <- trim(parts[last])
  if (candidate %in% unique(geo$DEPT)) {
    return(candidate)
  }
  else {
    ok <- c()
    for (d in depts){
      if (length(grep(d,candidate))>0) ok <- c(ok,d)
      else next
      }
    if (length(ok)>1) return('TRAVELING')
    else if (length(ok)<1) return(NA)
    else return(trim(ok))
    }
  print(candidate)
  return(NA)
}

get.last.rescate <- function(namestr){
  namelist <- space.split(unlist(namestr))
  n <- length(namelist)
  if(n<2) return(NA)
  else return(namelist[n])
}

get.middle.names.rescate <- function(namestr){
  namelist <- space.split(namestr)
  n <- length(namelist)
  if(n<3) return (NA)
  else return(paste(namelist[2:(n-1)],collapse=' '))
}

get.nth <- function(character.vector,n){
  return(character.vector[n])
}

make.get.nth <- function(n){
  return(function(character.vector){
    return(get.nth(character.vector,n))
  }
         )
}

unlist.and.get.nth <- function(listitem,n){
  listitem <- unlist(listitem)
  return(get.nth(listitem,n))
}

make.get.fn <- function(n,listtype){
  if (listtype=='char'){
    return(function(character.vector){
      return(get.nth(character.vector,n))
    }
           )
  }
  else {
    return(function(listitem){
      return(unlist.and.get.nth(listitem,n))
    }
           )
  }
}

dot.split <- split.general('.')

fix.db.colnames <- function(dset){
  cols <- colnames(dset)
  cols2 <- lapply(cols,dot.split)
  cols3 <- unlist(lapply(cols2,make.get.nth(1)))
  colnames(dset) <- toupper(cols3)
  return(dset)
}

get.muni <- function(dept,mlist,placestring){
  # takes department name, list of munis in that dept, and lugar string
  # returns character string with munis from the list that appear in the given string
  munis <- c()
  for (m in mlist){
    if(length(grep(m,placestring))>0) {
      munis <- c(munis,m)
    }
  }
  munis <- paste(unique(munis),collapse=',')
  return(munis)
}

make.get.muni <- function(dept, mlist){
  # wrapper for get.muni, above
  # makes an (l-apply-able) function of a string specific to one dept.
  return(
         function(placestring){
           return(get.muni(dept,mlist,placestring))
         }
         )
}

fix.specific.error <- function(col, error, correction){
  #rows.with.error <- grep(error,col)
  #col[rows.with.error] <-
    ### still working on this one ###
}
    

#########################################
zfill <- function(number){
  while(nchar(number)<5) number <- paste("0", number, sep="")
  return(number)
}

zfill2 <- function(number){
  while(nchar(number)<2) number <- paste('0',number,sep='')
  return(number)
}

zfill4 <- function(number){
  while(nchar(number)<4) number <- paste('0',number,sep='')
  return(number)
}
###########################################

fix.colnames <- function(dataset){
  # rescate-specific
  cols <- colnames(dataset)
  cols.fixed <- c()
  for (c in cols){
    c.fixed <- toupper(unlist(strsplit(c,','))[1])
    cols.fixed <- c(cols.fixed,c.fixed)
  }
  colnames(dataset) <- cols.fixed
  return(dataset)
}

strsplit.dash <- function(string){
  new <- trim(unlist(strsplit(string,'-')))
  return(new)
}

# takes a list represented as a string with dashes as delimiters
# returns a sorted, unique list, also as a string

make.unique <- function(stringlist){
  new <- strsplit.dash(stringlist)
  new <- new[new!='' & is.na(new)==FALSE]
  if (length(new)==0) new <- 'Unknown'
  new <- sort(unique(new))
  new <- paste(new,collapse='-')
  return(new)
}

# takes a list represented as a string with slashes as delimiters
# returns UNSORTED, unique list, aslso as a string

make.unique.slash <- function(stringlist){
  new <- unlist(strsplit(stringlist,'/'))
  new <- unique(new)
  new <- paste(new,collapse='/')
  return(new)
}

######################################################

get.perp <- function(old.perp,spec){   
  row <- which(perp.vocab$old==old.perp)
  if (spec=='general') {
    new <- unique(perp.vocab$new[row])
    if (length(new)<1) return('Unknown')
    else return(new)
  }
  else {
    new <- unique(perp.vocab$new.specific[row])
    if (length(new)<1) return('Unknown')
    else return(new)
  }
}

get.perp.gen <- function(old.perp){
  return(get.perp(old.perp,'general'))
}

get.perp.spec <- function(old.perp){
  return(get.perp(old.perp,'specific'))
}

##########################################################
get.nth <- function(strlist,n){
  new <- strsplit.dash(strlist)
  return(new[n])
}

get.1st <- function(strlist){
  return(get.nth(strlist,1))
}
get.2nd <- function(strlist){
  return(get.nth(strlist,2))
}
get.3rd <- function(strlist){
  return(get.nth(strlist,3))
}
get.4th <- function(strlist){
  return(get.nth(strlist,4))
}


