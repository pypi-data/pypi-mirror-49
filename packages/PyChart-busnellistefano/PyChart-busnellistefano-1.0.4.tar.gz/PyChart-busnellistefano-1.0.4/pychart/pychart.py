##  @packege PyChart
#   Package per disegnare semplici grafici
#
#

from PIL import Image, ImageDraw

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
       
        self.vx_m   = None
        self.vx_q   = None
        self.vy_m   = None
        self.vy_q   = None

        self._calc_vx_m()
        self._calc_vx_q()
        self._calc_vy_m()
        self._calc_vy_q()
                
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
                self._calc_vx_m()
                self._calc_vx_q()
        if name in [ 'cy_min', 'cy_max', 'vy_min', 'vy_max' ]:
            if hasattr(self, 'cy_min') and hasattr(self, 'cy_max') and hasattr(self, 'vy_min') and hasattr(self, 'vy_max'):
                self._calc_vy_m()
                self._calc_vy_q()
    
    ##  Metodo __str__
    #   @param  self    Puntatore all' oggetto
    def __str__( self ):
        return "Value:\n  Xmin: {0:6.2f} Ymin: {1:6.2f} Xmax: {2:6.2f} Ymax: {3:6.2f}\nCoord:\n  Xmin: {4:4d} Ymin: {5:4d} Xmax: {6:4d} Ymax: {7:4d}\ncx = {8:6.2f} * vx + {9:6.2f}\ncy = {10:6.2f} * vy + {11:6.2f}\n".format( self.vx_min, self.vy_min, self.vx_max, self.vy_max, self.cx_min, self.cy_min, self.cx_max, self.cy_max, self.vx_m, self.vx_q, self.vy_m, self.vy_q )

    ##  Metodo _calc_vx_m
    #   @param  self    Puntatore all' oggetto
    #
    #   Calcola il parametro m della trasformazione lineare px = m * vx + q.
    #   In caso di denominatore nullo, setta il valore None
    def _calc_vx_m( self ):
        try:
            self.vx_m = 1.0 * ( self.cx_max - self.cx_min ) / ( self.vx_max - self.vx_min )
        except:
            self.vx_m = None
            
    ##  Metodo _calc_vx_q
    #   @param  self    Puntatore all' oggetto
    #
    #   Calcola il parametro q della trasformazione lineare px = m * vx + q.
    #   Se m vale None, setta il valore None
    def _calc_vx_q( self ):
        if self.vx_m is None:
            self.vx_q = None
        else:
            self.vx_q = self.cx_max - ( self.vx_m * self.vx_max )

    ##  Metodo _calc_vy_m
    #   @param  self    Puntatore all' oggetto
    #
    #   Calcola il parametro m della trasformazione lineare py = m * vy + q.
    #   In caso di denominatore nullo, setta il valore None
    def _calc_vy_m( self ):
        try:
            self.vy_m = 1.0 * ( self.cy_max - self.cy_min ) / ( self.vy_min - self.vy_max )
        except:
            self.vy_m = None

    ##  Metodo _calc_vy_q
    #   @param  self    Puntatore all' oggetto
    #
    #   Calcola il parametro q della trasformazione lineare py = m * vy + q.
    #   Se m vale None, setta il valore None
    def _calc_vy_q( self ):
        if self.vx_m is None:
            self.vy_q = None
        else:
            self.vy_q = self.cy_max - ( self.vy_m * self.vy_min )

    ##  Metodo map_v_c
    #   @param  self    Puntatore all' oggetto
    #   @param  v       Valore da trasformare
    #
    #   Mappa le coordinate del punto v tramite le due trasformazioni lineare px = x_m * vx + x_q, py = y_m * vy + y_q
    def map_v_c( self, v ):
        try:
            cx = self.vx_m * v[ 0 ] + self.vx_q
        except:
            cx = None
        try:
            cy = self.vy_m * v[ 1 ] + self.vy_q
        except:
            cy = None
        return ( cx, cy ) 
        

    ##  Metodo map_c_v
    #   @param  self    Puntatore all' oggetto
    #   @param  c       Valore da trasformare
    #
    #   Esegue la trasformazione inversa di map_v_c, da coordinate del grafico a valore
    def map_c_v( self, c ):
        try:
            vx = ( c[ 0 ] - self.vx_q ) / self.vx_m
        except:
            vx = self.vx_max
        try:
            vy = ( c[ 1 ] - self.vy_q ) / self.vy_m
        except:
            vy = self.vy_max
        return ( vx, vy ) 

##  Classe Graph
#   Oggetto che renderizza un grafico con una lista di valori
#
class Graph( object ):
    ##  Costruttore
    #   @param  self        Puntatore all' oggetto
    #   @param  values      Lista con i valori da rappresentare sul grafico
    #   @param  cb_draw     Funzione call back da eseguire per disegnare il grafico
    #   @param  value_color Colore con cui disegnare i valori del grafico
    def __init__( self, values = [], cb_draw = None, value_color = (   0,   0,   0, 255 ) ):
        self.b_init = True

        self.values         = values
        self.cb_draw        = cb_draw
        self.v_min          = 0.0
        self.v_max          = 0.0
        self.width          = 0
        self.height         = 0
        self.padding        = 0
        self.alpha_color    = (   0, 255,   0, 0   )
        self.axes_color     = (   0,   0,   0, 192 )
        self.value_color    = value_color

        # Calcolo i limiti solo se sono sono stati specificati
        self._calc_val_limit()

        # Inizializzo il mapper
        self.mapper = Mapper( ( -0.5, self.v_min, len( self.values ) - 0.5, self.v_max ), ( self.padding, self.padding, self.width - self.padding, self.height - self.padding ) )

        self.b_init = False

        return None

    ##  Metodo __setattr__
    #   @param  self    Puntatore all' oggetto
    #   @param  name    Nome dell' attributo
    #   @param  value   Valore dell' attributo
    #
    #   Ricalcola i limiti del grafico e l'oggetto mapper
    def __setattr__( self, name, value ):

        super( Graph, self ).__setattr__(name, value)

        if self.b_init or name == 'b_init':
            return None

        if name in [ 'values' ]:
            self._calc_val_limit()
            self.mapper.vx_min = - 0.5
            self.mapper.vx_max = len( self.values ) - 0.5

        if name in [ 'width', 'height', 'padding' ]:
            self.mapper.cx_min = self.padding
            self.mapper.cy_min = self.padding
            self.mapper.cx_max = self.width  - self.padding
            self.mapper.cy_max = self.height - self.padding
        
        if name in [ 'v_min' ]:
            self.mapper.vy_min = self.v_min

        if name in [ 'v_max' ]:
            self.mapper.vy_max = self.v_max

    ##  Metodo _calc_val_limit
    #   @param  self    Puntatore all' oggetto
    #
    #   Ricalcola i limiti v_min e v_max leggendo la lista values
    def _calc_val_limit( self ):
        if len( self.values ) > 0:
            self.v_max = self.values[ 0 ]
            for v in self.values:
                if self.v_max < v:
                    self.v_max = v

            self.v_min = self.values[ 0 ]
            for v in self.values:
                if self.v_min > v:
                        self.v_min = v
        
    ##  Metodo render
    #   @param  self    Puntatore all' oggetto
    #   @param  width   Larghezza in pixel dell' immagine
    #   @param  height  Altezza in pixel dell' immagine
    #   @param  padding Spazio in pixel della cornice e dei separatori
    #
    #   Disegna gli assi coordinati del grefico ed i valori presenti nella lista values richiamando per chiascuno la call back cb.draw
    #   Prototipo call back cb_draw:
    #   def cb_draw( ImageDraw.Draw(), Mapper(), Index, ListValues, value_color ):
    #       ....
    #       
    def render( self, width = 0, height = 0, padding = 0 ):
        if len( self.values ) == 0:
            return -1
        if width            != 0:
            self.width          = width
        if height           != 0:
            self.height         = height
        if padding          != 0:
            self.padding        = padding

        img     = Image.new( 'RGBA', ( self.width, self.height ), self.alpha_color )
        draw    = ImageDraw.Draw( img )

        #   Disegno valori
        for i in range( 0, len( self.values ) ):
            if self.cb_draw == None:
                v = self.values[ i ]
                ( x, y ) = self.mapper.map_v_c( ( i, v ) )
                draw.arc( [ ( x - 2, y - 2 ), ( x + 2, y + 2 ) ], 0, 360, self.value_color )
            else:
                self.cb_draw( draw, self.mapper, i, self.values, self.value_color )

        #   Calcolo coordinate origine
        o  = self.mapper.map_v_c( ( 0.0, 0.0 ) )
                
        #   Disegno asse y
        p0 = ( o[ 0 ], height - 2 )
        p1 = ( o[ 0 ],      0 + 2 )
        draw.line( [ p0, p1 ], self.axes_color, 3 )

        #   Disegno asse x
        if ( self.v_min <= 0 ) and ( self.v_max >= 0 ):
            p0 = (          0 + 2, o[ 1 ] )
            p1 = ( self.width - 2, o[ 1 ] )
            draw.line( [ p0, p1 ], self.axes_color, 3 )
            for i in range( 0, len( self.values ) ):
                ( x, y ) = self.mapper.map_v_c( ( i, 0 ) )
                draw.line( [ ( x, y + 2 ), ( x, y - 2 ) ], self.axes_color, 3 )

        return img

##  Classe Panel
#   Oggetto che dispone uno o piu' grafici in un pannello
#
class Panel( object ):
    ##  Costruttore
    #   @param  self        Puntatore all' oggetto
    #   @param  graphs      Lista di oggetti Graph
    def __init__( self, graphs = [] ):
        self.graphs         = graphs
        self.width          = 0
        self.height         = 0
        self.padding        = 0
        self.border_color   = ( 210, 210, 210, 255 )
        self.graph_color    = ( 255, 255, 255, 255 )
        return None

    ##  Metodo render
    #   @param  self    Puntatore all' oggetto
    #   @param  width   Larghezza in pixel dell' immagine
    #   @param  height  Altezza in pixel dell' immagine
    #   @param  padding Spazio in pixel della cornice e dei separatori
    #
    #   Dispone verticalmente in una immagine uno o piu' grafici richiamandone la funzione render
    def render( self, width = 0, height = 0, padding = 0 ):
        if len( self.graphs ) == 0:
            return -1
        if width    != 0:
            self.width      = width
        if height   != 0:
            self.height     = height
        if padding  != 0:
            self.padding    = padding

        #   Immagine del pannello contenente la cornice
        img     = Image.new( 'RGBA', ( self.width, self.height ), self.border_color )
        #   Sfondo del pannello contenente i grafici
        g_t = self.padding
        g_l = self.padding
        g_w = self.width  - ( 2 * self.padding )
        g_h = self.height - ( 2 * self.padding )
        # 
        img_int = Image.new( 'RGBA', ( g_w, g_h ), self.graph_color )
        #   Disegno i grafici
        g_tg= 0
        g_lg= 0
        g_hg= ( g_h - ( ( len( self.graphs ) - 1 ) * self.padding ) ) / len( self.graphs )
        for g in self.graphs:
            #   Immagine del grafico con trasparenza
            g_img = g.render( g_w, g_hg, self.padding )
            #   Aggiungo il grafico sullo sfondo
            img_int.paste( g_img, (g_lg, g_tg), g_img )
            g_tg += ( g_hg + self.padding )
        # Incollo il tutto sul pannello
        img.paste( img_int, ( g_l, g_t ), img_int )

        return img

##  Classe Chart
#   Oggetto che dispone uno o piu' pannelli in una immagine
#
class Chart( object ):
    ##  Costruttore
    #   @param  self        Puntatore all' oggetto
    #   @param  panels      Lista di oggetti Panel
    def __init__( self, panels = [] ):
        self.panels = panels
        self.width  = 0
        self.height = 0
        self.padding= 0
        self.bgcolor= ( 240, 240, 240, 255 )
        return None

    ##  Metodo render
    #   @param  self    Puntatore all' oggetto
    #   @param  width   Larghezza in pixel dell' immagine
    #   @param  height  Altezza in pixel dell' immagine
    #   @param  padding Spazio in pixel della cornice e dei separatori
    #
    #   Dispone verticalmente in una immagine uno o piu' pannelli richiamandone la funzione render
    def render( self, width, height, padding ):
        if len( self.panels ) == 0:
            return -1
        if width    != 0:
            self.width      = width
        if height   != 0:
            self.height     = height
        if padding  != 0:
            self.padding    = padding

        p_t = self.padding
        p_l = self.padding
        p_w = self.width  - ( 2 * self.padding )
        p_h = ( self.height - ( ( len( self.panels ) + 1 ) * self.padding ) ) / len( self.panels )

        img = Image.new( 'RGBA', ( self.width, self.height ), self.bgcolor )
        
        for p in self.panels:
            p_img = p.render( p_w, p_h, self.padding )
            img.paste( p_img, ( p_l, p_t ) )
            p_t += ( p_h + self.padding )

        return img
