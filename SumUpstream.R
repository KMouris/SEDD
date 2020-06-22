# Code sums up the cells of an input Raster (e.g. travel time per cell) in upstream direction
# Works for each eight-direction (D8) flow model, here the flow directions are defined according to Jenson & Domingue 1998 (ArcGIS)
# both rasters have to be in the same format (ArcGIS ASCII, same number of columns, rows and georeferencing)
inputr<-raster() # charge input raster
directr<-raster() # charge flow direction raster
inputr.matrix<-as.matrix(inputr)
rdir<-as.matrix(directr)
resultr.matrix<-inputr.matrix
# The code iterates through the flow direction grid to define the flow path and sums up the values from the inp.raster in the upstr. direction
for (i in 1:ncol(inputr.matrix)){
  for (j in 1:nrow(inputr.matrix)){
    x<-i
    y<-j
    value<-0
    while ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
      if (is.na(rdir[y,x])==TRUE){
        break
      }
      if (rdir[y,x]==1){
        value<-value+inputr.matrix[y,x]
        x<-x+1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==16){break}
        }
        next
      } 
      if (rdir[y,x]==2){
        value<-value+inputr.matrix[y,x]
        x<-x+1
        y<-y+1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==32){break}
        }
        next
      } 
      if (rdir[y,x]==4){
        value<-value+inputr.matrix[y,x]
        y<-y+1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==64){break}
        }
        next
      } 
      if (rdir[y,x]==8){
        value<-value+inputr.matrix[y,x]
        x<-x-1
        y<-y+1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==128){break}
        }
        next
      } 
      if (rdir[y,x]==16){
        value<-value+inputr.matrix[y,x]
        x<-x-1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==1){break}
        }
        next
      } 
      if (rdir[y,x]==32){
        value<-value+inputr.matrix[y,x]
        x<-x-1
        y<-y-1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==2){break}
        }
        next
      } 
      if (rdir[y,x]==64){
        value<-value+inputr.matrix[y,x]
        y<-y-1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==4){break}
        }
        next
      } 
      if (rdir[y,x]==128){
        value<-value+inputr.matrix[y,x]
        x<-x+1
        y<-y-1
        if ((x>=1) & (x<=ncol(inputr.matrix)) & (y>=1) & (y<=nrow(inputr.matrix))){
          if (is.na(rdir[y,x])==TRUE){
            break
          }
          if(rdir[y,x]==8){break}
        }
        next
      }
      
    }
    resultr.matrix[j,i]<-value
  }
}


resultr<-inputr
resultr[]<-resultr.matrix
writeRaster(resultr, filename="resultr.asc", format="ascii", overwrite=TRUE) # define name and format
