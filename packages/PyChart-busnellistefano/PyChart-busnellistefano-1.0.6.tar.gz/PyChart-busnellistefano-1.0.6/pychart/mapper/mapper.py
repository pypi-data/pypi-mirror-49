from linea import Linea

##  Classe Mapper
#   Classe che esegue la trasformazione lineare valori -> punti del grafico
#
#   I membri della classe sono i limiti inferiore e superiore nei due assi coordinati per quanto riguarda i valori da 
#   rappresentare ed il corrispettivo in termini di punti nell'immagine del grafico.
#   La variazione di un valore scatena il ricalcolo dei valori della trasformazione lineare.
#
class Mapper( object ):
    ##  Costruttore
    #   @param  self        Puntatore all' oggetto
    #   @param  box_values  Tupla con i margini dei valori da rappresentare ( x_min, y_min, x_max, y_max )
    #   @param  box_coord   Tupla con i margini dei punti del grafico ( x_min, y_min, x_max, y_max )
    def __init__( self, box_values = ( -1.0, 1.0, -1.0, 1.0 ), box_coord = ( 0.0, 0.0, 1.0, 1.0 ) ):
        self.b_init = True
      
        self.vx_min = box_values[ 0 ]
        self.vy_min = box_values[ 1 ]
        self.vx_max = box_values[ 2 ]
        self.vy_max = box_values[ 3 ]
        
        self.cx_min = box_coord[ 0 ]
        self.cy_min = box_coord[ 1 ]
        self.cx_max = box_coord[ 2 ]
        self.cy_max = box_coord[ 3 ]
      
        self.TX     = Linea( ( self.vx_min, self.cx_min ), ( self.vx_max, self.cx_max ) )
        #   Inverto cy_min e cy_max perche' nelle immagini la coordinata 0,0 e' in alto a sinistra invece che in basso a sinistra
        self.TY     = Linea( ( self.vy_min, self.cy_max ), ( self.vy_max, self.cy_min ) )
                
        self.b_init = False

        return None

    ##  Metodo __setattr__
    #   @param  self    Puntatore all' oggetto
    #   @param  name    Nome dell' attributo
    #   @param  value   Valore dell' attributo
    #
    #   Ricalcola i parametri m, q delle trasformazioni lineari p = m * v + q per passare da valore a punto sull' immagine del grafico
    def __setattr__( self, name, value ):
        super( Mapper, self ).__setattr__(name, value)

        if self.b_init or name == 'b_init':
            return None

        if name in [ 'cx_min', 'cx_max', 'vx_min', 'vx_max' ]:
            if hasattr(self, 'cx_min') and hasattr(self, 'cx_max') and hasattr(self, 'vx_min') and hasattr(self, 'vx_max'):
                self.TX.p0 = ( self.vx_min, self.cx_min )
                self.TX.p1 = ( self.vx_max, self.cx_max )
        if name in [ 'cy_min', 'cy_max', 'vy_min', 'vy_max' ]:
            if hasattr(self, 'cy_min') and hasattr(self, 'cy_max') and hasattr(self, 'vy_min') and hasattr(self, 'vy_max'):
                #   Inverto cy_min e cy_max perche' nelle immagini la coordinata 0,0 e' in alto a sinistra invece che in basso a sinistra
                self.TY.p0 = ( self.vy_min, self.cy_max )
                self.TY.p1 = ( self.vy_max, self.cy_min )
    
    ##  Metodo __str__
    #   @param  self    Puntatore all' oggetto
    def __str__( self ):
        s   = ""
        s  += "Value:\n"
        s  += "  Xmin: {0:6.2f} Ymin: {1:6.2f} Xmax: {2:6.2f} Ymax: {3:6.2f}\n".format( self.vx_min, self.vy_min, self.vx_max, self.vy_max )
        s  += "Coord:\n"
        s  += "  Xmin: {0:4d} Ymin: {1:4d} Xmax: {2:4d} Ymax: {3:4d}\n".format( self.cx_min, self.cy_min, self.cx_max, self.cy_max )
        s  += "cx = {0:6.2f} * vx + {1:6.2f}\ncy = {2:6.2f} * vy + {3:6.2f}\n".format( self.vx_m, self.vx_q, self.vy_m, self.vy_q )

        return s
    
    ##  Metodo map_v_c
    #   @param  self    Puntatore all' oggetto
    #   @param  v       Valore da trasformare
    #
    #   Mappa le coordinate del punto v tramite le due trasformazioni lineare px = x_m * vx + x_q, py = y_m * vy + y_q
    def map_v_c( self, v ):
        cx = self.TX.map_x_y( v[ 0 ] )
        cy = self.TY.map_x_y( v[ 1 ] )
        return ( cx, cy ) 
        

    ##  Metodo map_c_v
    #   @param  self    Puntatore all' oggetto
    #   @param  c       Valore da trasformare
    #
    #   Esegue la trasformazione inversa di map_v_c, da coordinate del grafico a valore
    def map_c_v( self, c ):
        vx = self.TX.map_y_x( c[ 0 ] )
        vy = self.TY.map_y_x( c[ 1 ] )
        return ( vx, vy ) 
