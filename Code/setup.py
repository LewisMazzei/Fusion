#Lewis Mazzei - Fusion/Code/setup.py
#Note: If a comment is not on the same line then the corresponding comment to a line or chunk of code will be above it

#import relevant packages
import pygame, os

pygame.init() #initialise pygame

DISPLAY_WIDTH = 500 #width of window
DISPLAY_HEIGHT = 600 #width of height

os.environ['SDL_VIDEO_WINDOW_POS'] = '450' + "," + '50' #sets the position of the window

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT)) #set the size of the window

pygame.display.set_caption('Fusion') #set caption for the window

clock = pygame.time.Clock() #initialise pygame clock, used for 'ticking' through frames in the game loop

#initialise the rgb values for black and white
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#dictionary that matches each cell on the board to a coordinate of the centre of that cell, used for tile positioning
gridDictCoords = {(0, 0):(90, 190), (0, 1):(169, 190), (0, 2):(249, 190), (0, 3):(329, 190), (0, 4):(409, 190),
 				  (1, 0):(90, 269), (1, 1):(169, 269), (1, 2):(249, 269), (1, 3):(329, 269), (1, 4):(409, 269),
 				  (2, 0):(90, 349), (2, 1):(169, 349), (2, 2):(249, 349), (2, 3):(329, 349), (2, 4):(409, 349),
 				  (3, 0):(90, 429), (3, 1):(169, 429), (3, 2):(249, 429), (3, 3):(329, 429), (3, 4):(409, 429),
 				  (4, 0):(90, 509), (4, 1):(169, 509), (4, 2):(249, 509), (4, 3):(329, 509), (4, 4):(409, 509)}

#dictionary that matches each cell to a tuple value containing the width and height required for a tile occupying that cell, this differs between different cells due to the thickness of the grid lines that each cell touches (fixes the white gaps that used to be created)
gridDictDimensions = {(0, 0):(76, 76), (0, 1):(77, 76), (0, 2):(77, 76), (0, 3):(77, 76), (0, 4):(76, 76),
 				  	  (1, 0):(76, 77), (1, 1):(77, 77), (1, 2):(77, 77), (1, 3):(77, 77), (1, 4):(76, 77),
 				  	  (2, 0):(76, 77), (2, 1):(77, 77), (2, 2):(77, 77), (2, 3):(77, 77), (2, 4):(76, 77),
 				  	  (3, 0):(76, 77), (3, 1):(77, 77), (3, 2):(77, 77), (3, 3):(77, 77), (3, 4):(76, 77),
 				  	  (4, 0):(76, 75), (4, 1):(77, 75), (4, 2):(77, 75), (4, 3):(77, 75), (4, 4):(76, 75)}

#list of all elements from atomic number 1 through to 121, with the first letter in each capitalised
elementSymbols = [element.capitalize() for element in ('h,he,li,be,b,c,n,o,f,ne,na,mg,al,si,p,s,cl,k,ar,ca,sc,ti,v,cr,mn,fe,co,ni,cu,zn,ga,ge,as,se,br,kr,rb,sr,y,zr,nb,mo,tc,ru,rh,pd,ag,cd,in,sn,sb,te,i,xe,cs,ba,la,ce,pr,nd,pm,sm,eu,gd,tb,dy,ho,er,tm,yb,lu,hf,ta,w,re,os,ir,pt,au,hg,tl,pb,bi,po,at,rn,fr,ra,ac,pa,th,np,u,am,pu,cm,bk,cf,es,fm,md,no,lr,rf,db,sg,bh,hs,mt,ds,rg,cn,nh,fl,mc,lv,ts,og,uue,ubn,ubu').split(',')] #generates a new list with capitalised element abbreviations
