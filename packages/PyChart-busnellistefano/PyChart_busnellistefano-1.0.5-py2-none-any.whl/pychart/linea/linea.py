##  Classe Linea
#   Esegue i calcoli per una trasformazione lineare
class Linea( object ):
    ##  Costruttore
    #   @param  self        Puntatore all' oggetto
    #   @param  p0          Tupla ( x0, y0 ) con le coordinate del punto 0
    #   @param  p1          Tupla ( x1, y1 ) con le coordinate del punto 1
    def __init__( self, p0 = ( 0.0, 0.0 ), p1 = ( 0.0, 0.0 ) ):
        self.mx = None
        self.qx = None
        self.my = None
        self.qy = None
        self.p0 = p0
        self.p1 = p1

    ##  Metodo __setattr__
    #   @param  self    Puntatore all' oggetto
    #   @param  name    Nome dell' attributo
    #   @param  value   Valore dell' attributo
    #
    #   Ricalcola i parametri mx, qx, my, qy
    def __setattr__( self, name, value ):
        super( Linea, self ).__setattr__(name, value)

        if name in [ 'p0', 'p1' ]:
            if hasattr(self, 'mx') and hasattr(self, 'qx') and hasattr(self, 'my') and hasattr(self, 'qy') and hasattr(self, 'p0') and hasattr(self, 'p1'):

                if self.p0[ 0 ] == self.p1[ 0 ] and self.p0[ 1 ] == self.p1[ 1 ]:
                    self.mx = 0.0
                    self.qx = self.p0[ 1 ]
                    self.my = 0.0
                    self.qy = self.p0[ 0 ]
                else: 
                    if self.p0[ 0 ] == self.p1[ 0 ]:
                        self.mx = None
                        self.qx = None
                        self.my = 0.0
                        self.qy = self.p0[ 0 ]
                    else:
                        self.mx = 1.0 * ( self.p1[ 1 ] - self.p0[ 1 ] ) / ( self.p1[ 0 ] - self.p0[ 0 ] )
                        self.qx = self.p1[ 1 ] - ( self.mx * self.p1[ 0 ] )
                        
                    if self.p0[ 1 ] == self.p1[ 1 ]:
                        self.my = None
                        self.qy = None
                        self.mx = 0.0
                        self.qx = self.p0[ 1 ]
                    else:
                        self.my = 1.0 * ( self.p1[ 0 ] - self.p0[ 0 ] ) / ( self.p1[ 1 ] - self.p0[ 1 ] )
                        self.qy = self.p1[ 0 ] - ( self.my * self.p1[ 1 ] )

    ##  Metodo __setattr__
    #   @param  self    Puntatore all' oggetto
    #
    #   Display contenuto dati
    def __str__( self ):
        s = "Parametri:\n"
        s+= "  p0( {0:>8.4f}, {1:>8.4f} )\n".format( self.p0[ 0 ], self.p0[ 1] )
        s+= "  p1( {0:>8.4f}, {1:>8.4f} )\n".format( self.p1[ 0 ], self.p1[ 1] )
        if ( self.mx != None ):
            sm = "{0:>8.4f}".format( self.mx )
        else:
            sm = "{0:>8s}".format( "Inf" )
        if ( self.qx != None ):
            sq = "{0:>8.4f}".format( self.qx )
        else:
            sq = "{0:>8s}".format( "Inf" )
        s+= "  Y = {0:>8s} * X + {1:>8s}\n".format( sm, sq )
        
        if ( self.my != None ):
            sm = "{0:>8.4f}".format( self.my )
        else:
            sm = "{0:>8s}".format( "Inf" )
        if ( self.qy != None ):
            sq = "{0:>8.4f}".format( self.qy )
        else:
            sq = "{0:>8s}".format( "Inf" )
        s+= "  X = {0:>8s} * Y + {1:>8s}\n".format( sm, sq )

        return s

    ##  Metodo map_x_y
    #   @param  self    Puntatore all' oggetto
    #   @param  x       Ascissa
    def map_x_y( self, x = 0 ):
        if self.mx == None:
            return self.qy
        else:
            return self.mx * x + self.qx

    ##  Metodo map_y_x
    #   @param  self    Puntatore all' oggetto
    #   @param  y       Ordinata
    def map_y_x( self, y = 0 ):
        if self.my == None:
            return self.qx
        else:
            return self.my * y + self.qy
        
