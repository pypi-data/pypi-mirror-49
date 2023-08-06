from PIL import Image, ImageDraw

class Mapper( object ):
    def __init__( self, box_values = None, box_coord = None ):
        self.b_init = True
      
        if box_values != None:
            self.vx_min = box_values[ 0 ]
            self.vy_min = box_values[ 1 ]
            self.vx_max = box_values[ 2 ]
            self.vy_max = box_values[ 3 ]
        else:
            self.vx_min = -1.0 
            self.vy_min =  1.0
            self.vx_max = -1.0
            self.vy_max =  1.0
        if box_coord != None:
            self.cx_min = box_coord[ 0 ]
            self.cy_min = box_coord[ 1 ]
            self.cx_max = box_coord[ 2 ]
            self.cy_max = box_coord[ 3 ]
        else:
            self.cx_min = 0.0 
            self.cy_min = 0.0
            self.cx_max = 1.0
            self.cy_max = 1.0
       
        self.vx_m   = None
        self._calc_vx_m()
        self.vx_q   = None
        self._calc_vx_q()
        self.vy_m   = None
        self._calc_vy_m()
        self.vy_q   = None
        self._calc_vy_q()
                
        self.b_init = False

        return None

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
    
    def __str__( self ):
        return "Value:\n  Xmin: {0:6.2f} Ymin: {1:6.2f} Xmax: {2:6.2f} Ymax: {3:6.2f}\nCoord:\n  Xmin: {4:4d} Ymin: {5:4d} Xmax: {6:4d} Ymax: {7:4d}\ncx = {8:6.2f} * vx + {9:6.2f}\ncy = {10:6.2f} * vy + {11:6.2f}\n".format( self.vx_min, self.vy_min, self.vx_max, self.vy_max, self.cx_min, self.cy_min, self.cx_max, self.cy_max, self.vx_m, self.vx_q, self.vy_m, self.vy_q )

    def _calc_vx_m( self ):
        try:
            self.vx_m = 1.0 * ( self.cx_max - self.cx_min ) / ( self.vx_max - self.vx_min )
        except:
            self.vx_m = None
            
    def _calc_vx_q( self ):
        try:
            self.vx_q = self.cx_max - ( self.vx_m * self.vx_max )
        except:
            self.vx_q = None

    def _calc_vy_m( self ):
        try:
            self.vy_m = 1.0 * ( self.cy_max - self.cy_min ) / ( self.vy_min - self.vy_max )
        except:
            self.vy_m = None

    def _calc_vy_q( self ):
        try:
            self.vy_q = self.cy_max - ( self.vy_m * self.vy_min )
        except:
            self.vy_q = None

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

class Graph( object ):
    def __init__( self, values = [], cb_draw = None, v_min = None, v_max = None ):
        self.b_init = True

        self.values         = values
        self.cb_draw        = cb_draw
        self.width          = 0
        self.height         = 0
        self.padding        = 0
        self.v_min          = v_min
        self.v_max          = v_max
        self.alpha_color    = (   0, 255,   0, 0 )

        # Calcolo i limiti solo se sono sono stati specificati
        self._calc_val_limit()
        self.mapper = Mapper( ( -0.5, self.v_min, len( self.values ) - 0.5, self.v_max ), ( self.padding, self.padding, self.width - self.padding, self.height - self.padding ) )

        self.b_init = False

        return None

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

    def _calc_val_limit( self ):
        if len( self.values ) > 0:
            if self.v_max == None:
                self.v_max = self.values[ 0 ]
                for v in self.values:
                    if self.v_max < v:
                        self.v_max = v
            if self.v_min == None:
                self.v_min = self.values[ 0 ]
                for v in self.values:
                    if self.v_min > v:
                        self.v_min = v
        
    def render( self, width = 0, height = 0, padding = 0 ):
        if len( self.values ) == 0:
            return -1
        if width    != 0:
            self.width      = width
        if height   != 0:
            self.height     = height
        if padding  != 0:
            self.padding    = padding

        d_t = self.padding
        d_l = self.padding
        d_w = self.width  - ( 2 * self.padding )
        d_h = self.height - ( 2 * self.padding )

        img     = Image.new( 'RGBA', ( self.width, self.height ), self.alpha_color )
        d       = ImageDraw.Draw( img )

        #   Disegno valori
        for i in range( 0, len( self.values ) ):
            if self.cb_draw == None:
                v = self.values[ i ]
                ( x, y ) = self.mapper.map_v_c( ( i, v ) )
                d.arc( [ ( x - 2, y - 2 ), ( x + 2, y + 2 ) ], 0, 360, ( 0, 0, 0, 255 ) )
            else:
                self.cb_draw( d, self.mapper, i, self.values )
                
        #   Disegno asse y
        o  = self.mapper.map_v_c( ( 0.0, 0.0 ) )
        p0 = ( o[ 0 ], height - 2 )
        p1 = ( o[ 0 ],      0 + 2 )
        d.line( [ p0, p1 ], ( 0, 0, 0, 192 ), 3 )

        #   Disegno asse x
        if ( self.v_min <= 0 ) and ( self.v_max >= 0 ):
            p = self.mapper.map_v_c( ( 0, 0 ) )
            p0 = (          0 + 2, p[ 1 ] )
            p1 = ( self.width - 2, p[ 1 ] )
            d.line( [ p0, p1 ], ( 0, 0, 0, 192 ), 3 )
            for i in range( 0, len( self.values ) ):
                ( x, y ) = self.mapper.map_v_c( ( i, 0 ) )
                d.line( [ ( x, y + 2 ), ( x, y - 2 ) ], ( 0, 0, 0, 192 ), 3 )

        return img

class Panel( object ):
    def __init__( self, graphs = [] ):
        self.graphs         = graphs
        self.width          = 0
        self.height         = 0
        self.padding        = 0
        self.border_color   = ( 210, 210, 210, 255 )
        self.graph_color    = ( 255, 255, 255, 255 )
        return None

    def render( self, width = 0, height = 0, padding = 0 ):
        if len( self.graphs ) == 0:
            return -1
        if width    != 0:
            self.width      = width
        if height   != 0:
            self.height     = height
        if padding  != 0:
            self.padding    = padding

        g_t = self.padding
        g_l = self.padding
        g_w = self.width  - ( 2 * self.padding )
        g_h = self.height - ( 2 * self.padding )

        img     = Image.new( 'RGBA', ( self.width, self.height ), self.border_color )
        img_int = Image.new( 'RGBA', ( g_w, g_h ), self.graph_color )
        for g in self.graphs:
            g_img = g.render( g_w, g_h, self.padding )
            img_int.paste( g_img, (0, 0), g_img )
        img.paste( img_int, ( g_l, g_t ), img_int )

        return img

class Chart( object ):
    def __init__( self, panels = [] ):
        self.panels = panels
        self.width  = 0
        self.height = 0
        self.padding= 0
        self.bgcolor= ( 240, 240, 240, 255 )
        return None

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

