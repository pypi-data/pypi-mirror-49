##  @packege PyChart
#   Package per disegnare semplici grafici
#
#

from PIL import Image, ImageDraw
from mapper import Mapper

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
